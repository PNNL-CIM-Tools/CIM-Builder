# CIM-Builder Development Docs

Planning and contributor documentation for the **uniform builder-API refactor** —
the effort to replace CIM-Builder's fragmented mix of standalone object-builder
functions, class-based substation builders, and a documented-but-absent
`*_functions.py` API with a single, uniform builder-class API where every
equipment type is built **one CIM profile-part at a time** (EQ → electrical →
short-circuit → dynamics → measurement → asset).

This directory is the CIM-Builder counterpart to CIMHub's
`cimhub_core/.../development/` doc set. It is the spec the phased work executes
against.

---

## Start here

1. **The phase roadmap** — the day-by-day execution plan (phases 0–11, one per
   working day) lives in
   `/home/ande188/.claude/plans/take-a-look-at-buzzing-crane.md`. It holds the
   context (why this refactor exists), the locked decisions, and the ordered
   phases. Read it first; the docs below are the detailed specs each phase
   implements against.

2. **`ARCHITECTURE.md`** — the target architecture: the `ObjectBuilder` contract,
   the `builder_base` shared mixin, the profile-part build flow, the
   `network.cim` profile-source rule (cim-graph 0.5 §2/§5), and the separate
   substation assembly layer. `LineBuilder` is the reference implementation.

3. **`BUILDER_API.md`** — the public, user-facing API contract: the
   `create() → add_<profile>() → build()` chain, method naming, node-argument
   conventions, `from_catalog`, and convenience facades. What a user actually
   types.

4. **`PROFILE_TYPING.md`** — the §5a edit-time typing model: per-method
   single-sub-profile annotations (`cim: CN`, `cim: EQ`, `cim: SC`) via
   `TYPE_CHECKING` imports, narrowing writes to one profile while the runtime
   value stays the full `network.cim` module. Includes the today-vs-0.5 gap.

5. **`UNITS.md`** — how `add_electrical_bal` sets physical quantities via
   `CIMUnit` (no manual scaling), CIMUnit on first pass, and the per-unit
   (`z_base`) engine deferred to Phase 11.

6. **`BUILDER_TEST_CREATION.md`** — the test strategy: atom factories, the
   chained-build "act", per-profile assertions, the `network.cim` identity
   guardrail, and the three test tiers (atom / composition / integration).
   Includes the `ConnectionParameters` → direct-kwarg migration that the broken
   `docs/03_substation_builder/deliverable.ipynb` tests need.

---

## The locked decisions (quick reference)

| Decision | Choice |
|---|---|
| API shape | Builder classes; `add_<profile>` methods built in sequence, chainable |
| Profile source | `cim = self.network.cim` (never `get_cim_profile()` in a builder) |
| Substations | Separate assembly layer that orchestrates object builders |
| Units | CIMUnit now; full per-unit (`z_base`) deferred to Phase 11 |
| Profile dependency | Targets cim-graph 0.5.0a1 — `network.cim` is live and the `cgmes_3_0_0` merged profile ships real sub-profile parts (`core_equipment`, `short_circuit`, `topology`, …). Gap closed at source; only the dependency pin bump remains (Phase 1) |
| Electrical split | `add_electrical_bal` (balanced, implemented) vs. `add_electrical_unbal` (per-phase, stubbed until CIM18 unbalanced parts ship) |
| Typing | §5a per-method single-sub-profile via `TYPE_CHECKING`; no `.pyi` for builders |

---

## Reading order by task

- **Writing a new builder** → `ARCHITECTURE.md` → `BUILDER_API.md` →
  `PROFILE_TYPING.md` → `UNITS.md`, then `BUILDER_TEST_CREATION.md` for the test.
- **Migrating an existing `new_*` function** → `ARCHITECTURE.md`
  ("`builder_base` mixin" + "Profile-source rule"), then `BUILDER_API.md`
  ("convenience facades") to keep the old call working.
- **Working on substations** → `ARCHITECTURE.md` ("Substation assembly layer").
- **Touching units / impedance** → `UNITS.md`.
- **Adding tests** → `BUILDER_TEST_CREATION.md`.

---

## External references

- cim-graph 0.5 profile-identity contract (the basis for `network.cim` and the
  §5a/§5c typing split):
  `/home/ande188/CIM-Graph/docs/development/PROFILE_IDENTITY_0_5_PLAN.md`.
- CIMHub converter-side docs (the structural model these mirror):
  `/home/ande188/CIMHub_2_0/cimhub_core/src/cimhub_core/development/`.
- Global coding-style and CIMUnit guidance: `~/.claude/CLAUDE.md`.
