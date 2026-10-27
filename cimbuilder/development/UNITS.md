# Units in CIM-Builder

**Status:** revised. The code sketches below (`add_electrical_bal`, a deferred
Phase 11 per-unit engine) described a method name and a feature that were
superseded before either shipped — see the revision note. The physics/CIMUnit
guidance elsewhere in this doc is unaffected.

> **Revision note.** The shipped reference implementation
> (`cimbuilder/builders/load/consumer.py`) has no `add_electrical_bal` method —
> the real split is `add_electrical`/`add_ssh`, named after the object's actual
> profile parts, not a balanced/unbalanced electrical split. More importantly,
> the "Phase 11" per-unit (`pu`/`%`) conversion engine this doc deferred has
> already shipped — in `cimtables.binder.bind_row` (the `cimtables` package,
> split out of this repo; see `CIMTBL_DESIGN.md` §8.1 and
> `PERCENT_IMPEDANCE_BASE.md`), not as a `cimbuilder/units/` module. A relative
> (`pu`/`%`) `Qty` on an impedance field is converted to ohms against a
> `z_base` resolved from the object's own rating or its `From*` reference's
> rating — see `bind_row`'s module docstring for the exact rule. A hand-written
> builder method that needs the same conversion calls
> `graph_write.set_attr(obj, part, attr, qty, z_base=...)` directly rather than
> raising `NotImplementedError`.

How builders put physical quantities onto CIM objects. This is the builder-side
application of the cim-graph `CIMUnit` system; for the full unit-class reference
(base SI units, `.to()`, `float()`, the complete `CIMUnit` table) see the
canonical
[`UNITS.md`](../../../CIMHub_2_0/cimhub_core/src/cimhub_core/development/UNITS.md)
and the global units guide in `~/.claude/CLAUDE.md`. This doc covers only what a
builder author needs to get right.

---

## The one rule

**Never manually scale.** No `* 1e3`, `* 1e6`, `/ 1e6`. Every physical field is
set through a `CIMUnit` constructor that takes the source unit; cimgraph stores
SI internally and handles conversion.

```python
# BAD — manual scaling, the exact anti-pattern this refactor removes
self.line.r = value * 1.0
bv.nominalVoltage = base_kv * 1000

# GOOD — CIMUnit with the input unit
cim = self.network.cim
self.line.r = cim.Resistance(value, r_unit or 'ohm')
bv.nominalVoltage = cim.Voltage(base_kv, 'kV')
```

---

## Where units live: `add_electrical` (and friends)

Per the profile partition (`ARCHITECTURE.md`), physical quantities are set in
the profile method that owns them — e.g. `add_electrical` for impedance/power
fields, `add_ssh` for steady-state hypothesis values (`p`, `q`), a future
`add_short_circuit` for zero-sequence. `create` and `add_connectivity` set no
physical quantities (beyond `add_connectivity`'s own by-name FK resolution,
which isn't a physical quantity).

A builder's `add_<profile>` method takes a **plain value or a `cimtables.units.
Qty`** per quantity and writes it with `graph_write.set_attr`, which does the
`CIMUnit` construction:

```python
def add_electrical(self, load, *, pfixed=None, qfixed=None,
                    pfixedPct=None, qfixedPct=None, LoadResponse=None) -> None:
    graph_write.set_attr(load, EL, 'pfixed', pfixed)
    graph_write.set_attr(load, EL, 'qfixed', qfixed)
    graph_write.set_attr(load, EL, 'pfixedPct', pfixedPct)
    graph_write.set_attr(load, EL, 'qfixedPct', qfixedPct)
    if LoadResponse is not None:
        target = graph_write.resolve(self.network, self.cim.LoadResponseCharacteristic, LoadResponse)
        graph_write.set_assc(load, EL, 'LoadResponse', target)
```

`graph_write.set_attr` (in `cimtables`) is the one place that actually
constructs the `CIMUnit`: a plain `float`/`int`/`bool`/`str` is set as-is (for
non-quantity fields); a `Qty(value, unit)` is converted via the attribute's own
`CIMUnit` subclass (resolved by reflecting on the object's type hints) and, if
it's a relative (`pu`/`%`) quantity on an ohm-typed field, converted to ohms
against a `z_base` the caller supplies (or that `bind_row` resolves
automatically for `.cimtbl`-driven construction — see the revision note
above). A hand-written builder method never constructs a `CIMUnit` itself.

Common builder quantities and their CIMUnit class + base unit:

| Quantity | CIMUnit class | Base SI | Typical input units |
|----------|---------------|---------|---------------------|
| resistance / reactance | `Resistance` / `Reactance` | ohm | `'ohm'` |
| susceptance / conductance | `Susceptance` / `Conductance` | S | `'S'` |
| voltage | `Voltage` | V | `'V'`, `'kV'` |
| active power | `ActivePower` | W | `'W'`, `'kW'`, `'MW'` |
| reactive power | `ReactivePower` | VAr | `'VAr'`, `'kVAr'`, `'MVAr'` |
| apparent power / rating | `ApparentPower` | VA | `'VA'`, `'kVA'`, `'MVA'` |
| length | `Length` | m | `'m'`, `'km'` |

---

## The per-unit (pu/%) engine

CIMUnit handling for physical units (ohm, S, V, MVA, …) and relative (`pu`/`%`)
impedance conversion both already exist, in `cimtables` rather than a
`cimbuilder`-local module:

```
z_base = ratedU**2 / ratedS          # ohms (or baseU/baseS on a TransformerWinding)
r_ohm  = r_pct / 100 * z_base
```

`cimtables.binder.bind_row` resolves `z_base` automatically for `.cimtbl`-driven
construction (from the object's own rating, or its `From*` reference's rating —
see `bind_row`'s docstring and `PERCENT_IMPEDANCE_BASE.md` for the full rule and
the open IEC WG clarification it stands in for). A hand-written builder method
that needs the same conversion resolves `z_base` itself and passes it to
`graph_write.set_attr(obj, part, attr, qty, z_base=z_base)` — `set_attr` raises
if a relative `Qty` reaches an ohm-typed field with no `z_base` given, so there
is no silent wrong-units write (Fail Fast).

---

## Comparisons

Never compare a CIMUnit directly to a raw number — it raises `TypeError`. Convert
first:

```python
# BAD
if bv.nominalVoltage == base_voltage * 1000:   # TypeError under CIMUnit

# GOOD
if abs(bv.nominalVoltage.to('V') - target_volts) < 1.0:
```

Note: `utils.get_base_voltage` currently compares `bv.nominalVoltage ==
base_voltage` against a raw int. That works only while `nominalVoltage` is a
plain number; once it is a `Voltage` CIMUnit it must use `.to('V')`. Flag this
when a `GeneratorBuilder`/`InverterBuilder` ports this helper
(`OBJECT_BUILDER_MIGRATION.md`).

---

## Generator sign convention

CIM Terminal convention: positive `p` = power flowing **into** the equipment.
Generators produce power, so a generator's terminal `p` is **negative**.
Builders for `SynchronousMachine` / `PowerElectronicsConnection` must negate
when taking a "generation MW" input — see the Generator/Inverter phase in
`OBJECT_BUILDER_MIGRATION.md`.

---

## Checklist

- [ ] every physical field set via `graph_write.set_attr`/`set_assc`, never a
      bare `setattr` or manual `CIMUnit` construction
- [ ] no `* 1e3` / `* 1e6` / `/ 1e6` anywhere in a builder
- [ ] a relative (`pu`/`%`) `Qty` on an impedance field passes `z_base` to
      `graph_write.set_attr` — never silently dropped or treated as absolute
- [ ] CIMUnit-vs-number comparisons go through `.to(...)` / `float(...)`
- [ ] generator terminal `p` negated for generation inputs

---

## Related documents

- `BUILDER_API.md` — `add_<profile>` signatures and calling convention.
- `ARCHITECTURE.md` — why physical quantities live in the `add_<profile>`
  method that owns that profile part.
- `GRAPH_WRITE_CONTRACT.md` — the full `set_attr`/`set_assc` contract,
  including the relative-`Qty`/`z_base` conversion rule.
- `PERCENT_IMPEDANCE_BASE.md` — the full `z_base` resolution rule `bind_row`
  uses for `.cimtbl`-driven construction.
- `OBJECT_BUILDER_MIGRATION.md` — the phased plan porting `object_builder/`,
  including the generator sign-convention and per-unit-base ports.
- Canonical unit reference: cim-graph / CIMHub `UNITS.md`; global guide in
  `~/.claude/CLAUDE.md`.
