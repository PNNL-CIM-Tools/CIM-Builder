# mRID migration: what changed upstream, and what to clean up here

Upstream (cimprofiles, cim-graph, cimtables) moved from **name-keyed** to **mRID-keyed**
objects. CIM-Builder still uses the old API in places and is currently broken against it.
This note describes the new API shape and lists the call sites to fix.

## The rule

- **mRID is the key.** CIM 18 makes the mRID a freeform string unique within the whole
  model, across all classes (not per class). Every reference (`.cimtbl` FK cells, builder
  `resolve` calls) is by mRID.
- **`name` is plain data**: optional and non-unique. Never look anything up by name.
- **Identity-only classes** (CIM 18 classes that are not `IdentifiedObject`s, e.g. cim18v17
  `PhaseImpedanceData`) have no `mRID` or `name` field at all. Check with
  `'mRID' in cls.__dataclass_fields__`; there is no hand-kept list any more
  (cim-graph's old `known_problem_classes.py` is gone).
- **Target profile: `cim18v17`** (and comma specs of its sub-profiles). cimhub_2026 and
  gmdm are out of scope.

## cimprofiles: `Identity` UUID seeding (`identity.py`)

A built object's UUID is `uuid5(authority namespace, model+Class+mRID+name+seed)`. There
are now two separate routes, and only one of mRID or name is ever used:

| Built with | UUID seeded from | Rename (`name`) changes UUID? |
|---|---|---|
| `cls(mRID='xf_sub3', name='sub3')` | class + mRID (+ seed) | **no** |
| `cls(name='sub3')` (no mRID) | class + name (+ seed) | yes |
| nothing | random `uuid4` | n/a |
| Identity-only class: `obj = cls(); obj.uuid(mRID='lc_mtx601_21')` | class + key; nothing is stored, since there is no mRID field | n/a |

`cls(mRID=...)` raises `TypeError` on an Identity-only class. Use the `uuid(mRID=...)`
route instead.

## cim-graph: mRID index on `GraphModel`

- `network.find_by_mRID(mRID) -> obj | None` is an O(1) lookup in the local graph. It
  never queries the database (unlike `get_object`).
- `network.mrid_index() -> dict[str, obj]` is kept current by `add_to_graph`. Objects
  that readers or queries put into `network.graph` directly are picked up too: the index
  rebuilds when the object count changes. Don't reassign an object's mRID after it is
  in the graph.
- `network.list_identities()` returns `[{identifier, mRID, name, class}, ...]`
  (CIM-Graph #150).
- `network.add_to_graph(obj)` **raises `ValueError`** if another object, of any class,
  already has that mRID.
- **`network.name_index` no longer exists.** It was never part of cim-graph's API, and
  that is what the Pylance warning was about. Don't recreate it.

## cimtables: changed API

| Old | New |
|---|---|
| `from cimtables.name_index import NameIndex` | **removed**; there is no name index anywhere |
| `net.name_index = NameIndex()` in fixtures | delete the line |
| `graph_write.resolve(network, cls, name)` | `graph_write.resolve(network, cls, mRID)`: `cls` may be an abstract base (any subclass matches). It returns `None` if not found and **raises** if the mRID belongs to an object of another class |
| `graph_write.resolve_any_subclass(network, base, name)` | **removed**; use `resolve` (it already matches subclasses) |
| `graph_write.add_to_graph(network, obj)` | unchanged; it now just calls `network.add_to_graph` (mRID uniqueness enforced there) |
| `row.name` as the row key | `row.mRID` (`None` for Identity-only classes, which have `row.identifier` instead). `row.name` is now ordinary data and may be `None` |
| `bind_row` built `cls(name=row.name)` | `bind_row` builds `cls(mRID=row.mRID)`, or for Identity-only classes `cls()` + `uuid(mRID=row.identifier)`, then sets `name` with `set_attr` |
| generated `Terminal(name=f'{obj.name}_T{i}')` | `Terminal(mRID=f'{obj.mRID}_T{i}')`; phase children `mRID=f'{obj.mRID}_{phase}'`; TransformerEnd terminal `f'{transformer.mRID}_T{endNumber}'` |
| `set_assc(..., network=)` / string targets / `resolve_name` | never landed upstream; resolve first, then pass the object |

`.cimtbl` files: the first column is `mRID` (required on `IdentifiedObject` rows) or
`identifier` (optional, Identity-only rows). See `CIM-Tables/CLAUDE.md`, and
CIMTBL-Models' `.claude/skills/cimtbl-translate/SKILL.md` for the prefix convention
(`ld_671`, `xf_reg1`, `sw_brkr1`, ...).

## Call sites to fix in CIM-Builder

Found by `grep -rn "resolve_any_subclass\|graph_write.resolve\|name_index\|(name=" cimbuilder`:

- **`builders/base.py`**
  - `create(*, name, mRID=None, identifier=None)` should key on `mRID`, with `name`
    optional.
  - `from_table` calls `self.create(name=row.name)`. That is wrong now: it seeds the
    UUID from the name and drops the mRID. Either call `bind_row(network, row,
    container=...)` with no `obj` (bind_row builds it correctly), or have `create` mirror
    `binder._new_object` (mRID, else identifier, else nothing).
- **`resolve_any_subclass` → `resolve`:**
  - `builders/line/ac_line_segment.py:121`
  - `builders/line/wire_configuration.py:22`
  - `builders/switch/switch_phase.py:42`
- **`resolve(..., name)` → `resolve(..., mRID)`:** parameters and docstrings should say
  mRID.
  - `builders/line/ac_line_segment.py:95,135`
  - `builders/switch/switch.py:56`
  - `builders/load/consumer.py:21,32`
  - `builders/transformer/power_transformer.py:103-104`
  - `builders/transformer/by_template.py:82,87`
- **Objects built with `name=` as their identity** should take an mRID (child mRIDs
  extend the parent's, e.g. `<xf>_tank`, `<xf>_<endNumber>`):
  - `builders/line/conductor_distance_spacing.py:21`
  - `builders/transformer/power_transformer.py:126`
  - `builders/transformer/by_template.py:60,79`
  - `object_builder/line/line_builder.py:34`
  - `object_builder/base/new_base_voltage.py:42`
- **`object_builder/shunt/new_breaker.py:20`**: `breaker.uuid(name=name, seed=...)` still
  works (name route), but an mRID-keyed breaker should use `uuid(mRID=...)`.
- **Identity-only classes** (e.g. `PhaseImpedanceData` in `per_length_impedance.py`):
  don't pass `name`/`mRID`; seed with `obj.uuid(mRID=key)` if a stable UUID is needed.
- **Tests and fixtures** (`tests/builders/*`, `development/*.cimtbl`):
  - drop `name_index` setup;
  - switch `name` keys to `mRID` and keep them unique across classes (a load and its bus
    can't share `671`);
  - move to `cim18v17`.
- **Docs that describe NameIndex / name lookup** need updating: `CIMTBL_DESIGN.md` §5.5,
  `GRAPH_WRITE_CONTRACT.md`, `BUILDER_API.md`, `ARCHITECTURE.md`.

Reference implementation for every pattern above: CIM-Tables' `cimtables/binder.py`
(`_new_object`), `cimtables/connectivity.py`, `cimtables/graph_write.py`, and its tests.
