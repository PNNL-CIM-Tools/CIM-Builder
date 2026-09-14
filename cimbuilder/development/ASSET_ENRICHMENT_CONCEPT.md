# Asset Enrichment Concept — CIMHub + CIM-Asset-Manager + CIM-Builder

**Date:** 2026-07-02
**Status:** Concept (pre-implementation)
**Author:** aandersn

---

## Problem

CIMHub importers (DSS, SXST, UN GDB) convert simulator files into CIM graphs.
These source formats carry only what the simulator needs: impedance numbers,
geometry, and ratings. They do **not** carry manufacturer identity, cable layer
construction, standard references, or catalog cross-references — the data that
fills IEC 61968 `ProductAssetModel`, `CatalogAssetType`, `Manufacturer`, and the
detailed sub-layer fields on `ConcentricNeutralCableInfo`
(`shieldMaterial`, `insulationMaterial`, `outerJacketKind`, etc.).

The result is a CIM graph that is electrically correct but asset-incomplete.
Downstream consumers — CYME, PSCAD, a utility GIS, a compliance tool — need the
full asset record, not just the impedance tuple.

Concrete example: the IEEE 9500 DSS model imports 112 cable segments whose
`ConcentricNeutralCableInfo` has `radius`, `gmr`, `rAC25`, `neutralStrandCount`,
and `diameterOverScreen`. The CYME SXST exporter writes a `CableDB` entry that
CYME displays with `Conductor Material: (blank)`, `Construction Type: (blank)`,
`Insulation Material: (blank)`. CYME can still run a power flow using the
geometry, but the asset record is incomplete and fails catalog validation.

The same gap exists for:
- `OverheadWireInfo` — no `material`, `strandCount`, `ratedStrength`
- `PowerTransformerInfo` — no `Manufacturer`, `catalogNumber`, `weightTotal`
- `WireSpacingInfo` / `WireAssemblyInfo` — no construction standard reference

---

## Proposed Solution: Three-Layer Enrichment

Three repos divide the work cleanly:

```
CIM-Asset-Manager               (owns: native format catalogs + CIM asset objects)
        │  publishes: cim_asset_manager (PyPI)
        │  provides: match_cable(), match_wire(), match_transformer()
        ▼
CIM-Builder                     (owns: enrichment insertion into a live CIM graph)
        │  publishes: cimbuilder (PyPI)
        │  provides: AssetEnricher (wraps Asset-Manager match + ObjectBuilder write)
        ▼
CIMHub importers                (consume enrichment as an optional post-import pass)
        │  dss_to_cim(), sxst_to_cim(), un_to_cim() call enrich() if installed
```

The direction of dependency is **one-way downward**. CIM-Asset-Manager knows
nothing about CIMHub. CIM-Builder knows nothing about DSS or SXST. CIMHub
importers gain full enrichment by `pip install cim_asset_manager cimbuilder` with
zero changes to the core importer logic.

---

## CIM-Asset-Manager's Role

CIM-Asset-Manager (repo: `/home/ande188/CIM-Asset-Manager/`) is already scoped to
produce `cimhub_2026` AssetInfo objects from vendor datasheets (see its
`ARCHITECTURE.md`). This concept extends its scope slightly:

### 1. Native catalog ingestion (already planned)

Vendor Excel/CSV → `OverheadWireInfo`, `ConcentricNeutralCableInfo`,
`PowerTransformerInfo`, stored as Parquet. Phases 0–6 of the existing roadmap.

### 2. CYME `.cymcfg` ingestion (new)

CYME exports its equipment library as `.cymcfg` — an XML format structurally
identical to the `CableDB` / `ConductorDB` / `TransformerDB` sub-trees inside
`.sxst`, wrapped in `<ExportedEquipmentDBConfig>` with a `<Category>` field
(`Type|Manufacturer|VoltageKV|Standard|Material`). A single Southwire/Okonite
export contains 1,066+ fully-specified cable entries with all construction layers
populated.

These map directly to CIM:

| `.cymcfg` field | CIM target |
|---|---|
| `CableConductorDBData/MaterialID` | `WireMaterialKind` on `CableInfo.material` |
| `CableConductorDBData/ConstructionType` | `CableConstructionKind` on `CableInfo.constructionKind` |
| `CableInsulationDBData/MaterialID` | `WireInsulationKind` on `CableInfo.insulationMaterial` |
| `CableSheathDBData/MaterialID` | `CableShieldMaterialKind` on `CableInfo.shieldMaterial` |
| `CableSheathDBData/SheathType` | `CableOuterJacketKind` on `CableInfo.outerJacketKind` |
| `Category` field: `Manufacturer` segment | `Manufacturer.name` → `ProductAssetModel` |
| `Category` field: `Standard` segment | `CatalogAssetType.standard` |
| `Level` (kV L-N) | `CableInfo.ratedVoltage` (kV L-L via × √3) |
| `NominalRating` (A) | `CableInfo.ratedCurrent` |

Adding a `cymcfg` reader to CIM-Asset-Manager is a natural extension of its
existing ingestion pipeline — same `ConverterRegistry` pattern, new reader that
parses the XML rather than Excel.

### 3. Physical-parameter matching API (new)

Given a CIM `ConcentricNeutralCableInfo` with only electrical geometry
(`radius`, `gmr`, `rAC25`, `neutralStrandCount`, `diameterOverScreen`), find the
closest catalog entry:

```python
from cim_asset_manager import CableMatchRequest, match_cable

req = CableMatchRequest(
    radius_m=cable.radius,         # CIMUnit Length
    r_ac25=cable.rAC25,            # CIMUnit ResistancePerLength
    neutral_strand_count=cable.neutralStrandCount,
    diameter_over_screen_m=cable.diameterOverScreen,
    voltage_kv_ll=12.47,           # from BaseVoltage
)
match = match_cable(req, catalog="southwire_mv105")
# returns: CableMatchResult(score=0.97, asset_info=ConcentricNeutralCableInfo(...fully populated))
```

Matching logic: normalize parameters to SI, score by weighted Euclidean distance
on `(radius, rAC25, neutralStrandCount, diameterOverScreen)`, threshold at a
configurable tolerance (default 2%). Return `None` if no match within tolerance
rather than returning a wrong answer.

The catalog to search against is configurable — different utilities stock
different cable families.

---

## CIM-Builder's Role

CIM-Builder (repo: `/home/ande188/CIM-Builder/`) already has the `from_catalog`
stub on `ObjectBuilder`. This concept gives it a concrete implementation:

### AssetEnricher (new class in `cimbuilder/enrichment/`)

```python
class AssetEnricher:
    """Post-import pass: match CIM asset objects against a catalog and fill gaps."""

    def __init__(self, network: GraphModel, catalog: str = "default"):
        self.network = network
        self.catalog = catalog

    def enrich_cables(self, *, overwrite: bool = False) -> int:
        """Match all ConcentricNeutralCableInfo objects and fill asset fields."""
        ...

    def enrich_wires(self, *, overwrite: bool = False) -> int:
        """Match all OverheadWireInfo objects and fill asset fields."""
        ...

    def enrich_transformers(self, *, overwrite: bool = False) -> int:
        """Match all PowerTransformerInfo objects and fill asset fields."""
        ...

    def enrich_all(self, *, overwrite: bool = False) -> dict[str, int]:
        return {
            "cables": self.enrich_cables(overwrite=overwrite),
            "wires": self.enrich_wires(overwrite=overwrite),
            "transformers": self.enrich_transformers(overwrite=overwrite),
        }
```

`AssetEnricher` calls `cim_asset_manager.match_*()` for each unresolved asset
object, then uses the existing `ObjectBuilder` mechanics (`_add`, CIMUnit
constructors) to write the matched fields back into the live graph. It does **not**
create new CIM objects — it only fills `None` fields on existing ones (or all
fields if `overwrite=True`).

The `overwrite=False` default means enrichment is safe to run on a graph that
already has partial asset data (e.g. an SXST import that already carried
`insulationMaterial`).

---

## CIMHub Integration

CIMHub importers gain enrichment via an optional post-import call. The pattern
mirrors the existing `propagate_base_voltages` integration:

```python
# dss_to_cim.py (after BFS base-voltage pass)

try:
    from cimbuilder.enrichment import AssetEnricher
    enriched = AssetEnricher(feeder, catalog=catalog).enrich_all()
    _log.info("Asset enrichment: %s", enriched)
except ImportError:
    _log.debug("cimbuilder not installed — skipping asset enrichment")
```

The `try/except ImportError` guard is intentional: `cimbuilder` and
`cim_asset_manager` are optional dependencies. A bare CIMHub install without them
produces the same electrically-correct but asset-incomplete graph it always has.
Installing them silently upgrades every importer's output.

The `catalog` parameter propagates from `dss_to_cim(path, catalog="southwire_mv105")`
so utilities can point at their stocked catalog without code changes.

---

## Round-Trip Benefit for SXST

With enrichment in place, the DSS → CIM → SXST round-trip gains:

| Field | Before enrichment | After enrichment |
|---|---|---|
| `CableDB/CableConductorDBData/MaterialID` | `ALUMINUM` (hardcoded) | `COPPER` or `ALUMINUM` from matched catalog entry |
| `CableDB/CableConductorDBData/ConstructionType` | `StrandedConcentric` (hardcoded) | Matched value (`Solid`, `StrandedConcentric`, …) |
| `CableDB/CableInsulationDBData/MaterialID` | `PPP-PPL` (hardcoded) | Matched value (`XLPE`, `PVC`, `PPP-PPL`, …) |
| `CableDB/CableSheathDBData/*` | absent | Populated from matched `shieldMaterial` |
| `EquipmentID` | DSS name (`1/0_Al_15kV_1/3`) | Manufacturer catalog name if match score ≥ threshold |
| CYME dialog `Conductor Material` | `(blank)` | Populated dropdown |
| CYME dialog `Construction Type` | `(blank)` | Populated dropdown |

The SXST exporter (`cable_info.py`) needs no changes — it already reads
`CableInfo.material`, `constructionKind`, `insulationMaterial`, `shieldMaterial`
from the CIM object. Enrichment simply populates them before the exporter runs.

---

## Dependency and Publication Plan

```
Phase 0 (now):     Concept doc only. No code.

Phase 1:           CIM-Asset-Manager adds cymcfg reader + match_cable() API.
                   Ships as cim_asset_manager 0.1 (internal / TestPyPI).

Phase 2:           CIM-Builder adds AssetEnricher using cim_asset_manager.
                   Ships as cimbuilder 0.X (internal / TestPyPI).

Phase 3:           CIMHub adds optional import guard + catalog= param to
                   dss_to_cim(), sxst_to_cim(), un_to_cim().
                   Validated against IEEE 9500: all CableDB material fields
                   populated, CYME dialog dropdowns show values.

Phase 4:           Public PyPI release. CIMHub optional dep block in
                   pyproject.toml:
                   [project.optional-dependencies]
                   asset = ["cim_asset_manager>=0.1", "cimbuilder>=0.X"]
```

---

## Open Questions

1. **Matching tolerance**: 2% on `rAC25` + `radius` catches manufacturing
   variation but may over-match in dense catalogs. Should tolerance be per-field
   or a single scalar? Empirical tuning against the 1,066-entry cymcfg needed.

2. **No-match policy**: Log a warning and leave fields `None`, or fall back to
   a "Typical/IEEE" default entry? The current hardcoded strings (`ALUMINUM`,
   `PPP-PPL`) are effectively that fallback — the question is whether to keep it
   explicit.

3. **CIM profile gaps**: `CableInfo.shieldMaterial` maps to `CableShieldMaterialKind`
   but CYME has a richer sheath model (`SheathType`, armor layers, jacket). These
   extra layers have no CIM equivalent today. Log in `CIM_EXTENSIONS.md` and
   omit from enrichment until the profile is extended.

4. **Assembly vs. asset boundary**: This concept covers `CableInfo` / `WireInfo`
   (asset-level). `WireSpacingInfo` + `WireAssemblyInfo` (assembly-level, from
   RUS/utility construction standards) are a separate CIM-Asset-Manager scope item
   per the existing `ASSEMBLY_CATALOG_SCOPE.md`. Do not conflate.

---

## Related Documents

- `CIM-Asset-Manager/.development/ARCHITECTURE.md` — AssetInfo catalog pipeline
- `CIM-Asset-Manager/.development/ASSEMBLY_CATALOG_SCOPE.md` — assembly vs. asset boundary
- `CIM-Builder/cimbuilder/development/ARCHITECTURE.md` — ObjectBuilder + from_catalog stub
- `CIMHub_2_0/CLAUDE.md` — converter anti-patterns
- `CIMHub_2_0/cimhub_cyme/src/cimhub_cyme/exporter/lines/cable_info.py` — current hardcoded fields
- `CIMHub_2_0/debug/Equipments.cymcfg` — 1,066-entry CYME cable catalog export (source data)
