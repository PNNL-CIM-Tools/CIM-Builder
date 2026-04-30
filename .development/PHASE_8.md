# Phase 8+ — Deferred Scope

**Status:** Gated. All items below are post-rewrite work that depends on external factors.

---

## Phase 8 — Dynamics Builders

**Gated on:** `cimgraph.data_profile.cim17v40.dynamics` (or equivalent) being stable in cim-graph.

Scope:
- `new_synchronous_machine_dynamics` (link existing SynchronousMachine to dynamics params)
- `new_genrou`, `new_gencls`, `new_gentpj`, `new_gensal`
- `new_exciter_esst1a`, `new_exciter_iee_ac1a`, ... (common excitation system models)
- `new_governor_hygov`, `new_governor_tgov1`, ... (common governor models)
- `new_stabilizer_pss1a`, `new_stabilizer_pss2b`, ...
- Composites: `new_dynamic_generator` = SynchronousMachine + GENROU + ESST1A + HYGOV + PSS1A

Use pattern: `TYPE_CHECKING` import of the dynamics sub-profile at the top of each file, `get_cim()` with a `profile='cim17v40'` or equivalent override in the session.

---

## Phase 9 — Split-Profile Distribution

**Gated on:** `cimgraph.data_profile.merge.merge_profiles` + `generate_type_stubs` being verified end-to-end.

Scope:
- `new_distribution_transformer_tank` (composite: TransformerTank + N×TransformerTankEnd + ...)
- `new_concentric_cable_line_segment` (AC line segment specifically for cable, with concentric neutral info)
- `new_tape_shield_cable_line_segment`
- GridLAB-D / CIMHub distribution use cases

Use pattern: generate merged profile stub via `generate_type_stubs(connectivity, electrical, output_path=...)`, commit the stub, `TYPE_CHECKING` import it.

---

## Phase 10 — Protection Builders

**Gated on:** downstream demand (CIMantic Studio, specific utility use cases).

Scope beyond the existing `new_under_frequency_protection_function_block`:
- `new_distance_relay`
- `new_differential_relay`
- `new_overcurrent_relay`
- `new_recloser` (composite with Breaker + ProtectionEquipment + timing curves)
- Protection coordination helpers (common settings profiles)

---

## Phase 11 — MCP Server (separate repo: `cim-builder-mcp`)

Scope (owned by a separate repo, not CIM-Builder):
- Import `cimbuilder.__all__`
- Auto-generate MCP tool schemas via `inspect.signature()` + docstring parsing
- Expose every `new_*` function + `SubstationSession` classmethods as tools
- Network state persistence between tool calls (resource handles)

---

## Phase 12 — GUI Binding (separate repo: `CIMantic-Studio`)

Scope (owned by CIMantic Studio's Phase 5-6 roadmap, not CIM-Builder):
- "Add capacitor" button → `SubstationSession.add_capacitor(...)` via Flask endpoint
- Form introspection from `inspect.signature()` output
- Template selection UI pulling from `cim-asset-manager` catalog
