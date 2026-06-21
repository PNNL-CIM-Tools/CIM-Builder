# Units in CIM-Builder

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

Per the profile partition (`ARCHITECTURE.md`), physical quantities are set in the
profile method that owns them — almost always `add_electrical`, plus
`add_short_circuit` for zero-sequence. `create` and `add_connectivity` set no
physical quantities.

A builder's `add_electrical` signature takes a **value + a unit string** per
quantity, defaulting the unit to the CIM base SI unit:

```python
def add_electrical(self, r, x, bch,
                   r_unit=None, x_unit=None, bch_unit=None) -> "LineBuilder":
    cim = self.network.cim
    self.line.r   = cim.Resistance(r,   r_unit   or 'ohm')
    self.line.x   = cim.Reactance(x,    x_unit   or 'ohm')
    self.line.bch = cim.Susceptance(bch, bch_unit or 'S')
    return self
```

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

## CIMUnit on first pass; per-unit deferred to Phase 11

**This refactor wires real CIMUnit handling for physical units (ohm, S, V, MVA,
…) now.** It does **not** build the per-unit conversion engine now — that is
Phase 11.

The `line_builder.py` sketch referenced a `convert_to_ohm(...)` helper that does
not exist. Until Phase 11, the per-unit path is an explicit stub, not a silent
pass-through:

```python
def add_electrical(self, r, x, bch, r_unit=None, x_unit=None, bch_unit=None):
    cim = self.network.cim
    if (r_unit or '').lower() in ('pu', 'perunit', 'per_unit'):
        raise NotImplementedError(
            'per-unit impedance conversion lands in Phase 11; pass ohms for now'
        )
    self.line.r = cim.Resistance(r, r_unit or 'ohm')
    ...
```

Fail Fast: a `pu` value before Phase 11 raises, so nobody gets a wrong-units
write that looks fine. (A logged warning + skip is acceptable only if a caller
genuinely needs partial builds; default to raising.)

---

## Phase 11: the per-unit engine

When Phase 11 lands `cimbuilder/units/`, the pu branch converts instead of
raising, using the standard base-impedance relation:

```
z_base = base_kv**2 / base_mva          # ohms
r_ohm  = r_pu * z_base
b_base = 1 / z_base                       # siemens
b_S    = b_pu * b_base
```

The builder reads `base_kv` from the object's `BaseVoltage` (via
`utils.get_base_voltage`) and `base_mva` from the system/MVA base, then sets
`cim.Resistance(r_pu * z_base, 'ohm')`. No manual scaling — the conversion is the
documented physics, and the result still goes through the CIMUnit constructor.

The test for this (see `BUILDER_TEST_CREATION.md` → "Testing the deferred
per-unit path") flips from asserting `NotImplementedError` to asserting
`float(line.r) ≈ r_pu * z_base`.

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
when porting (Phase 10 units audit).

---

## Generator sign convention

CIM Terminal convention: positive `p` = power flowing **into** the equipment.
Generators produce power, so a generator's terminal `p` is **negative**. Builders
for `SynchronousGenerator` / `PowerElectronicsConnection` must negate when taking
a "generation MW" input. Handled in the generator builders (Phase 6) and revisited
in Phase 11 alongside the pu engine.

---

## Checklist

- [ ] every physical field set via a `CIMUnit` constructor with an input unit
- [ ] no `* 1e3` / `* 1e6` / `/ 1e6` anywhere in a builder
- [ ] unit strings default to the CIM base SI unit (`'ohm'`, `'S'`, `'V'`, …)
- [ ] `pu` input raises `NotImplementedError` until Phase 11, then converts via
      `z_base`
- [ ] CIMUnit-vs-number comparisons go through `.to(...)` / `float(...)`
- [ ] generator terminal `p` negated for generation inputs

---

## Related documents

- `BUILDER_API.md` — `add_electrical` signatures (value + unit string).
- `ARCHITECTURE.md` — why physical quantities live in `add_electrical`.
- `BUILDER_TEST_CREATION.md` — unit-value assertions and the pu-path test.
- Canonical unit reference: cim-graph / CIMHub `UNITS.md`; global guide in
  `~/.claude/CLAUDE.md`.
