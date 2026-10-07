# Profile resolution, typing, and runtime checking — the three layers

**Read this first** if you are confused about "which profile is this code
talking about?" CIM-Builder has three separate mechanisms that all involve "the
CIM profile." They answer different questions, run at different times, and are
deliberately not merged. The other docs each cover one layer in depth; this one
is the map.

| # | Layer | Question it answers | Runs when | Mechanism | Deep-dive |
|---|---|---|---|---|---|
| 1 | **Edit-time typing** | "Am I touching a field outside this method's profile slice?" | In the editor only (Pylance). Never at runtime. | `TYPE_CHECKING` imports of sub-profile modules; `cim: EQ = self.network.cim` | `PROFILE_TYPING.md` |
| 2 | **Runtime checking** | "Is this the right attribute for this object, and is it a scalar or an association?" | Every `set_attr` / `set_assc` call | Name-keyed field lookup against a `part` module passed in | `GRAPH_WRITE_CONTRACT.md` §2 |
| 3 | **Profile selection** | "Which CIM version/module is this whole run using?" | Once, at parse/connection time | `Profile=` line → `CIMG_CIM_PROFILE` → `network.cim` | this doc |

The mistake to avoid: treating these as one thing. Layer 1 is advisory and
vanishes at runtime. Layer 2 is enforced but only as strong as the `part` you
hand it. Layer 3 decides what "the live class" even is.

---

## Layer 3 first: how a profile gets selected

Everything else hangs off this, so it comes first.

```
.cimtbl:   Profile = cimhub_2026          (or: caller sets the env var directly)
              │
              ▼
dsl/parser.py::parse_file
   os.environ['CIMG_CIM_PROFILE'] = 'cimhub_2026'     ← the ONLY writer in this repo
              │
              ▼
cimgraph.core.env_vars.get_cim_profile()              ← @cache'd, takes NO arguments,
   reads CIMG_CIM_PROFILE, imports the module            reads the env var and nothing else
              │
              ▼
GraphModel / ConnectionInterface __init__             ← resolves the profile ONCE
   self.cim = <that module>      →  network.cim
              │
      ┌───────┴────────────────────────────┐
      ▼                                    ▼
builders / binder / connectivity        dsl/validate.py
   cim = self.network.cim                  reflects on the same profile's classes
   (the live classes objects are           to decide which columns a row may carry
    constructed from)
```

Rules that follow from this chain:

- **`Profile=` in a `.cimtbl` is the user-facing selector.** It is parsed before
  any record is built and written into `CIMG_CIM_PROFILE`. With no `Profile=`
  line the environment's existing `CIMG_CIM_PROFILE` is used; with neither,
  validation fails fast (`no CIM profile selected`). See `CIMTBL_DESIGN.md` §3.9.
- **Builders and the binder read `network.cim`, never `get_cim_profile()`.** The
  profile is resolved once at the connection. Re-deriving it in a leaf can yield
  a different class object under a merged profile and miss every graph key
  (`BASELINE.md` §5a, `BUILDER_TEST_CREATION.md`).
- **`get_cim_profile()` takes no arguments and is `@cache`'d.** The env var must
  be set before the first call (before the model/connection is created).
  Changing it afterwards does nothing until the cache is cleared. This is why
  `parse_file` must run before the `GraphModel` is constructed.
- **`dsl/validate.py` follows the same selection.** It reflects directly on the
  selected profile's dataclasses (no parallel schema). `validate(record,
  profile=...)` may name a module explicitly (`cim17v40`, `cimhub_2026`, ...);
  omitted, it uses `CIMG_CIM_PROFILE`. Its row-class cache is keyed by
  `(profile, class_name)`, because the same class name has different fields
  under different profiles.
- **Comma-spec (runtime-merged) profiles work.** `CIMG_CIM_PROFILE=a.connectivity,a.electrical`
  is resolved through `get_cim_profile()` like everywhere else. Merged classes' annotations
  can't be resolved from their own module, so `validate.py` falls back to resolving them
  against the selected profile module (`_real_fields`).
- **Any class in the selected profile is automatically a legal `.cimtbl` class.**
  There is no curated allowlist or per-version schema file. The only columns a
  profile can never explain are the DSL's own shorthand, fixed in
  `dsl/synthetic.py`: `node`, `node1`, `node2`, `bus1`, `bus2`, `phases`,
  `Template`.

### Known limitations (as of this writing)

- **The profile module is trusted as-is.** If an installed profile lacks a field
  a sample `.cimtbl` uses (e.g. `TransformerTank.noLoadLoss`,
  `LinearShuntCompensator.nomQ` are not on the installed `cimhub_2026`),
  validation rejects it with a closest-match message. See
  `_KNOWN_SCHEMA_GAPS` in `tests/dsl/test_parser.py`.

---

## Layer 1: edit-time typing (Pylance)

**Purpose:** catch "wrong profile slice" mistakes while you type, for
hand-written builder code.

- At runtime `self.network.cim` is the *full* (possibly merged) module — one
  object carrying every profile's fields. Pylance sees it as `ModuleType`/`Any`.
- Each `add_<profile>` method annotates its local as **one** sub-profile:
  `cim: EQ = self.network.cim`, with `EQ`/`SC`/... imported under
  `if TYPE_CHECKING:`. The annotation *narrows the editor's view*; the runtime
  value is unchanged.
- It is erased at runtime. It does **nothing** for data that arrives at runtime
  — in particular `.cimtbl` rows, which are bound reflectively
  (`core/binder.py`) with no statically typed call site for Pylance to inspect.

So: layer 1 protects *code you write*; it cannot protect *data you load*.
Full model and checklist: `PROFILE_TYPING.md`.

## Layer 2: runtime checking (`set_attr` / `set_assc`)

**Purpose:** a check that actually fires when the code runs, including for
`.cimtbl` data.

`graph_write.set_attr(obj, part, attr, value)` and `set_assc(obj, part, assc,
target)` look up `getattr(part, type(obj).__name__)` and check `attr` against
that class's dataclass fields **by name** — never by `isinstance`. They raise
`ValueError` when:

- `attr` is not a field of that `part` class (wrong profile slice, or a typo);
- `attr` is an association but you called `set_attr`, or a scalar but you called
  `set_assc` (decided by `field.metadata['inverse']`).

`set_attr` also does the Qty → `CIMUnit` conversion; `set_assc` writes both
sides of an association.

**How strong the check is depends on the `part` argument:**

| Call site | `part` passed | Effect of the "is this attr in this slice?" check |
|---|---|---|
| A builder's `add_<part>` method (target design) | a genuinely part-scoped reference module (`CN`, `EL`, ...) | Real: rejects out-of-slice attributes |
| `core/binder.py` / `core/connectivity.py` (reflective, class unknown until runtime) | `network.cim` | No-op for slice membership — a merged module has every field. The scalar-vs-association (`inverse`) check still applies. |

For the `.cimtbl` path the slice question is answered **earlier**, by layer 3's
validation (Phase 2), which rejects any column that is not a field of the class
in the selected profile. The binder's `network.cim` call is therefore not a gap;
it is the second line of defense, not the first.

Details, API contract, and the history of why this replaced a Pylance-only
design: `GRAPH_WRITE_CONTRACT.md` §2.

---

## Where each check sits on the `.cimtbl` path

```
file text
  │  Profile= → CIMG_CIM_PROFILE                         (layer 3: select)
  ▼
parse → RawRecord            grammar knows no CIM names
  ▼
validate → <Class>Row        reflects on the selected profile:   (layer 3: legal columns,
                              unknown class/column fails fast,    types, Qty vs FK vs scalar)
                              with a closest-match suggestion
  ▼
bind_row → live objects      set_attr/set_assc, part=network.cim (layer 2: scalar/assoc,
                              builds on network.cim classes        units, reverse side)
```

Layer 1 does not appear on this path. It only applies to the Python builder API.

## Quick answers

- *"Why does my editor not flag a bad attribute in a `.cimtbl` flow?"* — Layer 1
  is static and doesn't see data. Validation (layer 3) reports it at parse time.
- *"Why didn't `set_attr` complain about a field outside this profile part?"* —
  The caller passed `network.cim` (merged), which has every field. Pass a real
  part module to get slice enforcement.
- *"Which profile will `validate()` use?"* — `profile=` if given, else
  `CIMG_CIM_PROFILE`, which `Profile=` in the `.cimtbl` sets.
- *"I changed `CIMG_CIM_PROFILE` mid-process and nothing changed."* —
  `get_cim_profile()` is `@cache`'d; set the variable before the model is
  created.
