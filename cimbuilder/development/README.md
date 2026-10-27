# CIM-Builder Development Docs

Planning and contributor documentation for the **uniform builder-API refactor** —
the effort to replace CIM-Builder's fragmented mix of standalone object-builder
functions (`cimbuilder/object_builder/`), class-based substation builders, and
a documented-but-absent `*_functions.py` API with a single, uniform
builder-class API where every equipment type is built **one CIM profile-part
at a time** (connectivity → electrical → SSH → short-circuit → asset), and
each `add_<profile>` method is stateless, taking the object as an explicit
first parameter.

`cimbuilder/builders/load/consumer.py` (`EnergyConsumerBuilder`) is the real,
shipped reference implementation this whole doc set is reconciled against —
not a forward sketch. This directory is the CIM-Builder counterpart to
CIMHub's `cimhub_core/.../development/` doc set.

---

## Start here

1. **`PROFILE_RESOLUTION.md`** — the map of the three "profile" mechanisms that are
   easy to conflate: edit-time Pylance typing, runtime `set_attr`/`set_assc` checking,
   and user-selected profile (`Profile=` → `CIMG_CIM_PROFILE` → `network.cim`).
   Read before touching any of them.

2. **`ARCHITECTURE.md`** — the real architecture: the `ObjectBuilder` contract
   (`builders/base.py`), where the mechanics actually live (`cimtables`, not a
   `cimbuilder`-local mixin), the profile-source rule (`self.cim`), and the
   separate substation assembly layer. `EnergyConsumerBuilder` is the
   reference implementation.

3. **`BUILDER_API.md`** — the public, user-facing API contract: construct the
   builder, `create()`, then each `add_<profile>(obj, ...)` the equipment type
   actually has — stateless, no chaining, no `build()`. What a user actually
   types.

4. **`PROFILE_TYPING.md`** — the edit-time typing model: real, always-imported
   part modules (`cimprofiles.cim18.cim18v17.<part>`) aliased per part (`CN`,
   `EL`, `SSH`, …), the same module object `graph_write`'s runtime check uses.

5. **`UNITS.md`** — how an `add_<profile>` method sets physical quantities via
   `graph_write.set_attr` (no manual `CIMUnit` construction, no manual
   scaling), and the relative (`pu`/`%`) impedance → ohm conversion (already
   shipped, in `cimtables.binder.bind_row` / `graph_write.set_attr`'s
   `z_base` parameter).

6. **`BUILDER_TEST_CREATION.md`** — the test strategy: the `network` fixture
   (a real file-less `XMLFile` connection + `NameIndex`, not a bare
   `GraphModel()`), per-profile assertions, the profile-identity guardrail,
   and the test tiers (atom / composition / integration).

7. **`OBJECT_BUILDER_MIGRATION.md`** — the phased plan porting the rest of
   `cimbuilder/object_builder/`'s old `new_*` functions onto this API,
   prioritized by real duplicated construction logic found in CIMHub_2_0's
   importer scripts (Transformer → Load → Line → Switch → Capacitor →
   Generator/Inverter; Measurement deprioritized — no real caller found).

8. **`GRAPH_WRITE_CONTRACT.md`** / **`CIMTBL_DESIGN.md`** — the `cimtables`
   package's own contract (`set_attr`/`set_assc`, `bind_row`, the `.cimtbl`
   DSL) that every builder method is built on. `cimtables` is a separate
   package now (`/home/ande188/CIM-Tables`) — see `CIMTBL_DESIGN.md` §8.1.

---

## The locked decisions (quick reference)

| Decision | Choice |
|---|---|
| API shape | Builder classes; stateless `add_<profile>(obj, ...)` methods, no chaining |
| Profile source | `self.cim` (`= network.cim`, set once in `__init__`); never `get_cim_profile()` in a builder method |
| Substations | Separate assembly layer that orchestrates object builders |
| Units | `graph_write.set_attr`/`set_assc` construct and convert `CIMUnit`s; relative (`pu`/`%`) impedance → ohm conversion already shipped |
| Profile dependency | `cimprofiles.cim18.cim18v17.*` for part-scoped modules; `network.cim` (merged) for construction/FK resolution |
| Associations | Owned by whichever `add_<profile>` method owns that field (e.g. `BaseVoltage` in `add_connectivity`, `LoadResponse` in `add_electrical`) — no separate `add_references`/`add_assc` method |
| Typing | A method imports its own real part module and passes it to `graph_write`'s `part` argument; no `TYPE_CHECKING` gating needed |
| Profile selection | `.cimtbl` `Profile=` sets `CIMG_CIM_PROFILE`; resolved once to `network.cim`; `.cimtbl` validation reflects on that profile (no LinkML) — `PROFILE_RESOLUTION.md` |
| DSL/core layering | The `.cimtbl` parser/validator/binder/graph_write live in the separate `cimtables` package, not in `cimbuilder` |

---

## Reading order by task

- **Writing a new builder** → `PROFILE_RESOLUTION.md` → `ARCHITECTURE.md` →
  `BUILDER_API.md` → `PROFILE_TYPING.md` → `UNITS.md`, then
  `BUILDER_TEST_CREATION.md` for the test. `OBJECT_BUILDER_MIGRATION.md` has a
  worked example per equipment category.
- **Porting an existing `new_*` function from `object_builder/`** →
  `OBJECT_BUILDER_MIGRATION.md` directly — it has the phase-by-phase plan and
  per-category notes.
- **Working on substations** → `ARCHITECTURE.md` ("Substation assembly layer").
- **Touching units / impedance** → `UNITS.md`, `GRAPH_WRITE_CONTRACT.md`.
- **Adding tests** → `BUILDER_TEST_CREATION.md`.
- **Touching the `.cimtbl` DSL itself** (parser/validator/binder) → that code
  now lives in `/home/ande188/CIM-Tables`; see `CIMTBL_DESIGN.md` §8.1.

---

## External references

- CIMHub converter-side docs (the structural model these mirror):
  `/home/ande188/CIMHub_2_0/cimhub_core/src/cimhub_core/development/`.
- CIMHub_2_0's importer scripts (`cimhub_<format>/importer/`) are the real
  downstream consumer `OBJECT_BUILDER_MIGRATION.md`'s priority order is based
  on — not `substation_builder/`.
- Global coding-style and CIMUnit guidance: `~/.claude/CLAUDE.md`.
