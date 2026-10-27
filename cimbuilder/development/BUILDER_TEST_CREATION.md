# Creating Atom Tests for CIM-Builder Builders

**Status:** revised. Every code snippet below originally showed the pre-
implementation fluent/chainable API (`cgmes_3_0_0`, `add_electrical_bal`,
`.create().add_connectivity(...)` chaining); the shipped `EnergyConsumerBuilder`
is stateless and the calling convention differs throughout. See the revision
note. The methodology (atom factories, test tiers, checklist shape) is
unchanged and still the right approach.

> **Revision note.** `tests/builders/test_consumer.py` is the real, working
> test suite for the shipped `EnergyConsumerBuilder` and is the ground truth
> this doc is rewritten against. Key differences from the original sketch:
> builder methods take the object as an explicit first parameter and return
> `None` (no chaining); the real profile is `cimprofiles.cim18.cimhub_2026` (or
> `cim18v17` for the part-scoped modules), not `cgmes_3_0_0`; a `BusBranchModel`
> built with a real `XMLFile` connection (even with no file on disk) is used
> instead of a bare `GraphModel()` with a hand-set `.graph = {}`, because
> `network.name_index` (used by `graph_write.resolve`) needs a real model to
> exist on; and there is no `add_electrical_bal`/`add_short_circuit` method —
> the method set is whatever profile parts the equipment type actually has
> (`add_connectivity`/`add_electrical`/`add_ssh` for `EnergyConsumer`).

Step-by-step instructions for building a unit test for any **builder** —
`ObjectBuilder` subclass (`EnergyConsumerBuilder`, …) or a substation assembly
class (`SingleBusSubstation`, …). Designed for both human developers and AI
coding agents.

This is the builder-side counterpart to CIMHub's
[`ATOM_TEST_CREATION.md`](../../../CIMHub_2_0/cimhub_core/src/cimhub_core/development/ATOM_TEST_CREATION.md).
The structure is the same; the **direction is inverted**:

| | Converter (CIMHub) | Builder (CIM-Builder) |
|---|---|---|
| Input | a CIM subgraph (exporter) or a format object (importer) | a minimal **container atom** (network + container + nodes) |
| Act | run the builder: `create()`, then each `add_<profile>(obj, ...)` | the read crossed profiles correctly |
| Output asserted | a format string / a few new CIM objects | the CIM object(s) the builder added to the graph |
| What you check | the read crossed profiles correctly | each `add_<profile>` method wrote *its* profile's fields |

A converter *reads* an existing graph; a builder *grows* one. So the atom for a
builder is not "the objects the converter looks up" — it is "the container and
nodes the builder needs to attach to."

---

## What is a Builder Atom Test?

An atom test verifies a **single builder** (or a single `add_<profile>` method)
against a minimal CIM container subgraph — the "atom." The atom holds only what
the builder must attach to: a `GraphModel`, an `EquipmentContainer`
(Substation / Feeder / VoltageLevel), a `BaseVoltage`, and one or two
`ConnectivityNode`s. Typically 3–6 CIM objects.

Builder atom tests are:
- **Fast** — pure Python, no DB, no file I/O, no Blazegraph.
- **Isolated** — one builder (or one profile method) per test; a failure
  pinpoints which profile part is wrong.
- **Profile-scoped** — they mirror the method-per-part contract: a test for
  `add_electrical` asserts only the electrical fields it touches, never a
  field another `add_<profile>` method owns.
- **Self-documenting** — the atom factory shows exactly what container the
  builder expects.

---

## ⚠️ Connection API: do NOT use `ConnectionParameters`

`ConnectionParameters` doesn't exist in any currently-supported cim-graph
version (`ImportError`). Build the connection with **direct kwargs**; the
profile comes from the `CIMG_CIM_PROFILE` env var, set *before* importing any
`cimgraph.data_profile`/`cimprofiles` module (profile resolution happens at
import time):

```python
import os
os.environ['CIMG_CIM_PROFILE'] = 'cimhub_2026'   # set before importing a profile module

import cimprofiles.cim18.cimhub_2026 as cim
from cimgraph.databases import XMLFile
from cimgraph.models import BusBranchModel
import tempfile

connection = XMLFile(filename=tempfile.mktemp(suffix='.xml'))   # no file needs to exist on disk
container = cim.Feeder(name='test_feeder')
network = BusBranchModel(connection=connection, container=container, distributed=False)
network.name_index = NameIndex()   # cimtables.name_index.NameIndex — see below
```

`XMLFile.__init__(self, filename=None, namespaces=None, metadata=None)` — no
`cim_profile`, no `iec61970_301`. A real `BusBranchModel` (not a bare
`GraphModel()`) is needed even for a pure unit test: `graph_write.resolve` (used
by `add_connectivity`/`add_electrical`'s by-name FK resolution) reads
`network.name_index`, which only a real model construction sets up correctly —
set `network.name_index = NameIndex()` explicitly in the atom fixture, exactly
as `tests/builders/test_consumer.py`'s `network` fixture does.

> A live-database round-trip (Blazegraph + CIM-Loader upload, re-query) is an
> **integration tier**, not a unit test. Keep it out of the atom suite; gate it
> behind a marker (`@pytest.mark.integration`) and a running database. Atom
> tests must run with `pytest` and nothing else.

---

## The CIM Object Model (Quick Reference)

> Snippets import `cimprofiles.cim18.cimhub_2026` — the merged profile
> `tests/builders/test_consumer.py` actually uses. Builders read `self.cim`
> (`= network.cim`, set once in `__init__`) for construction/FK resolution,
> and import real part modules (`cimprofiles.cim18.cim18v17.electrical_unbalanced
> as EL`, …) for the `graph_write.set_attr`/`set_assc` calls their
> `add_<profile>` methods make. Tests assert against `cim.X` (the same merged
> module) so they stay correct whether the profile is flat or merged.

```python
import cimprofiles.cim18.cimhub_2026 as cim
from cimtables import graph_write

consumer = cim.EnergyConsumer(name='test_load')   # bare construction, no UUID seeding needed
consumer.EquipmentContainer = feeder              # association (or via graph_write.set_assc)
graph_write.add_to_graph(network, consumer)       # adds to network.graph AND network.name_index
```

Key `GraphModel` methods and `cimtables.graph_write` functions used in
assertions:

| Call | What it does |
|------|-------------|
| `graph_write.add_to_graph(network, obj)` | adds to `network.graph` and `network.name_index` together — always use this, not a bare `network.add_to_graph(obj)`, so the two never drift |
| `network.graph[cim.X]` | dict of `{identifier: obj}` for type X — the identity-keyed store |
| `graph_write.resolve(network, cim.X, name)` | O(1) name → object lookup via `network.name_index`; `None` if not found |
| `network.find_by_attribute(cim.X, 'name', value)` | linear search by attribute — use only where `name_index` isn't populated (rare in a builder test) |
| `network.get_all_edges(cim.X)` | hydrate associations (needed before deep traversal on a DB-backed model) |

---

## Step 1: Identify the Builder's Prerequisites

Read the builder and list **what it attaches to** (the container side) and
**what it produces** (the equipment side). Unlike a converter, a builder does
not `find_by_attribute` for inputs — its prerequisites are its constructor /
`add_<profile>` arguments.

Example — the real `EnergyConsumerBuilder` (`builders/load/consumer.py`):

```python
class EnergyConsumerBuilder(ObjectBuilder):
    cim_class_name = 'EnergyConsumer'
    # no create() override — base.py's bare cim_cls(name=name) is enough

    def add_connectivity(self, load, *, node: str, container=None,
                          phaseConnection=None, grounded=None,
                          customerCount=None, BaseVoltage=None) -> None:
        ...   # PREREQ: a node name (auto-vivified if absent); BaseVoltage, if given, must already be in the graph by that name

    def add_electrical(self, load, *, pfixed=None, qfixed=None,
                        pfixedPct=None, qfixedPct=None, LoadResponse=None) -> None:
        ...   # PREREQ: LoadResponse, if given, must already be in the graph by that name

    def add_ssh(self, load, *, p=None, q=None) -> None:
        ...   # no prerequisites beyond the object itself
```

Prerequisites for the atom:
- a `BusBranchModel` (built with a real `XMLFile` connection, no file needed on
  disk) with `network.name_index` set;
- a `container` (a `Feeder`) — either passed explicitly to the builder, or left
  to fall back to `network.container`;
- any by-name FK target (`BaseVoltage`, `LoadResponse`) the test wants to
  resolve, already added via `graph_write.add_to_graph` *before* calling the
  `add_<profile>` method that resolves it — `add_connectivity`/`add_electrical`
  auto-vivify a `ConnectivityNode` by name but never auto-vivify a `BaseVoltage`
  or `LoadResponseCharacteristic`.

This maps to the `make_network_atom()` factory below.

For a **substation** assembly class (e.g. `SingleBusSubstation`), the
prerequisites are inverted — it *creates* its own container and buses, and its
`new_feeder(...)` needs a feeder `GraphModel` with a source bus. Those tests use
a `make_feeder_atom()` (a tiny feeder with a `sourcebus` `ConnectivityNode` +
`EnergySource`) — exactly the minimal feeder the existing
`test_single_bus_integration.py` fixture builds inline.

---

## Step 2: Choose or Build the Atom Factory

Put a shared `network` fixture in the test module (or a shared `conftest.py`),
mirroring `tests/builders/test_consumer.py`'s own `network` fixture — build it
with a real (file-less) `XMLFile` connection, not a bare `GraphModel()`:

```python
# conftest.py (or inline, as tests/builders/test_consumer.py does today)
import os
import tempfile

import pytest

os.environ['CIMG_CIM_PROFILE'] = 'cimhub_2026'

import cimprofiles.cim18.cimhub_2026 as cim
from cimgraph.databases import XMLFile
from cimgraph.models import BusBranchModel
from cimtables.name_index import NameIndex


@pytest.fixture
def network():
    conn = XMLFile(filename=tempfile.mktemp(suffix='.xml'))
    container = cim.Feeder(name='test_feeder')
    net = BusBranchModel(connection=conn, container=container, distributed=False)
    net.name_index = NameIndex()
    return net
```

### Referent atoms (whatever the builder resolves by name)

A builder's `add_<profile>` methods resolve by-name FKs with
`graph_write.resolve` — add exactly the referents a given test needs, by name,
*before* calling the method that resolves them:

```python
def test_add_connectivity_resolves_base_voltage_by_name(network):
    base_voltage = cim.BaseVoltage(name='base_4160')
    graph_write.add_to_graph(network, base_voltage)

    builder = EnergyConsumerBuilder(network)
    load = builder.create(name='load_671')
    builder.add_connectivity(load, node='671', BaseVoltage='base_4160')
    consumer = builder.add(load)

    assert consumer.BaseVoltage is base_voltage
```

A `ConnectivityNode` named by `node=` is auto-vivified by
`connectivity.add_connectivity` if it doesn't already exist — unlike
`BaseVoltage`/`LoadResponse`, it is never a prerequisite you need to add
yourself unless the test specifically wants to connect to a node already used
by other equipment.

### Feeder atom (substation `new_feeder` tests)

```python
def make_feeder_atom(mrid='TEST-FEEDER-001'):
    """Minimal feeder GraphModel with a 'sourcebus' CN + EnergySource."""
    feeder = cim.Feeder(mRID=mrid)
    conn = XMLFile(filename=tempfile.mktemp(suffix='.xml'))
    network = BusBranchModel(connection=conn, container=feeder, distributed=False)
    network.name_index = NameIndex()
    src_node = cim.ConnectivityNode(name='sourcebus', ConnectivityNodeContainer=feeder)
    source = cim.EnergySource(name='source', EquipmentContainer=feeder)
    t = cim.Terminal(name='source_t1', sequenceNumber=1,
                     ConnectivityNode=src_node, ConductingEquipment=source)
    source.Terminals.append(t)
    feeder.NormalHeadTerminal = t
    for o in (feeder, src_node, source, t):
        graph_write.add_to_graph(network, o)
    return network, feeder, src_node
```

**Reuse, don't reinvent.** `make_feeder_atom` is the inline fixture in
`tests/test_single_bus_integration.py` extracted into a factory. If a builder
needs a `BaseVoltage` lookup, reuse `cimbuilder.utils.get_base_voltage`; if it
needs source-bus discovery, reuse `cimbuilder.utils.get_source_bus`.

---

## Step 3: Run the Builder Through Its Profile Methods

A builder test's "act" is: construct the builder, call `create()`, then call
each `add_<profile>` the test cares about, always passing the object back in.
Each method is a separate testable unit, so you can stop after the method
under test and skip calling `add()` (adding to the graph) entirely if the
assertion doesn't need it:

```python
builder = EnergyConsumerBuilder(network, container=feeder)
load = builder.create(name='test_load')                  # bare object, not yet in the graph
builder.add_connectivity(load, node='671')                # terminals + node wiring
builder.add_electrical(load, pfixed=10_000, qfixed=3_000)  # electrical fields on load
consumer = builder.add(load)                               # add_to_graph, returns the object
```

To unit-test just `add_electrical`, do the minimal setup (`create` +
`add_connectivity`, since `add_electrical` assumes the object already has
terminals/container) then call only `add_electrical` and assert only its
fields.

---

## Step 4: Write the Test

```python
# tests/builders/test_consumer.py (the real, shipped example)
import os
import tempfile

import pytest

os.environ['CIMG_CIM_PROFILE'] = 'cimhub_2026'

import cimprofiles.cim18.cimhub_2026 as cim
from cimgraph.databases import XMLFile
from cimgraph.models import BusBranchModel

from cimbuilder.builders.load.consumer import EnergyConsumerBuilder
from cimtables import graph_write
from cimtables.name_index import NameIndex
from cimtables.units import Qty


@pytest.fixture
def network():
    conn = XMLFile(filename=tempfile.mktemp(suffix='.xml'))
    container = cim.Feeder(name='test_feeder')
    net = BusBranchModel(connection=conn, container=container, distributed=False)
    net.name_index = NameIndex()
    return net


def test_create_add_connectivity_add_ssh_add(network):
    builder = EnergyConsumerBuilder(network)
    load = builder.create(name='load_671')
    builder.add_connectivity(load, node='671')
    builder.add_ssh(load, p=Qty(1155.0, 'kW'), q=Qty(660.0, 'kVAr'))
    consumer = builder.add(load)

    assert consumer.name == 'load_671'
    assert consumer.p.to('kW') == pytest.approx(1155.0)
    assert consumer.q.to('kVAr') == pytest.approx(660.0)
    assert len(consumer.Terminals) == 1
    node = graph_write.resolve(network, cim.ConnectivityNode, '671')
    assert node is not None
    assert consumer.Terminals[0].ConnectivityNode is node


def test_add_connectivity_resolves_base_voltage_by_name(network):
    base_voltage = cim.BaseVoltage(name='base_4160')
    graph_write.add_to_graph(network, base_voltage)

    builder = EnergyConsumerBuilder(network)
    load = builder.create(name='load_671')
    builder.add_connectivity(load, node='671', BaseVoltage='base_4160')
    consumer = builder.add(load)

    assert consumer.BaseVoltage is base_voltage
    assert consumer in base_voltage.ConductingEquipment
```

Each assertion reads straight off the live object (`consumer.p`,
`consumer.BaseVoltage`, `len(consumer.Terminals)`) or through
`graph_write.resolve` — there is no separate `assert_added_to_graph`/
`assert_terminal_connected` helper module in the real test suite; the fixture
and the objects' own attributes are enough, since every write already went
through `graph_write.set_attr`/`set_assc`/`add_to_graph`.

---

## Step 5: Profile-Identity Assertion

Because `create()`/builder methods read `self.cim` (`= network.cim`, set once
in `__init__`), every object lands under the graph's own class identity. Add
one assertion that would catch a stray `get_cim_profile()` re-derivation:

```python
def test_objects_use_network_profile_identity(network):
    builder = EnergyConsumerBuilder(network)
    load = builder.create(name='test_load')
    builder.add_connectivity(load, node='671')
    consumer = builder.add(load)

    # The graph key and isinstance must agree on ONE EnergyConsumer class object.
    assert network.cim.EnergyConsumer in network.graph
    assert isinstance(consumer, network.cim.EnergyConsumer)
```

If a builder used `get_cim_profile()` instead of `self.cim` under a merged
profile, this key lookup would miss and the test would fail loudly — which is
the point.

---

## Step 6: Run It

```bash
uv run pytest tests/builders/load/test_<equipment>.py -v
```

Mirror the source tree under `tests/`: `tests/builders/<category>/test_<name>.py`,
matching `cimbuilder/builders/<category>/<name>.py` — see
`tests/builders/test_consumer.py` for `builders/load/consumer.py`'s layout.

---

## Saving an Atom as XML (Optional)

For a debugging reference or an integration fixture, serialize any atom — using
the real connection API (no `ConnectionParameters`):

```python
from cimgraph.utils import write_xml

builder = EnergyConsumerBuilder(network)
load = builder.create(name='test_load')
builder.add_connectivity(load, node='671')
consumer = builder.add(load)

write_xml(network, 'tests/test_models/load_atom.xml')
```

This produces valid CIM XML with correct UUID cross-references because cimgraph
manages `Identity.identifier → obj.uri()` internally. Do **not** hand-edit XML or
rely on external exporters for fixtures — mismatched UUIDs break round-trips.

---

## Test Tiers (what runs where)

| Tier | Scope | Deps | Where |
|---|---|---|---|
| **Atom (unit)** | one builder / one `add_<profile>` method | pytest only | `tests/builders/**` |
| **Composition** | a builder sequence + substation assembly (e.g. single-bus + feeder) | pytest, in-memory graph | `tests/composite_builder/**` (currently missing `.py` source — see `OBJECT_BUILDER_MIGRATION.md`), `tests/test_single_bus_integration.py` |
| **Integration** | XML round-trip / Blazegraph upload + re-query | running DB + CIM-Loader | `@pytest.mark.integration`, opt-in |

The atom and composition tiers must be green on every commit. The integration
tier is opt-in (it needs a database).

---

## Checklist for a Complete Builder Atom Test

- [ ] Read the builder — list what each `add_<profile>` method writes and
      which by-name FKs it resolves
- [ ] Build the `network` fixture with a real (file-less) `XMLFile`
      connection + `NameIndex`, not a bare `GraphModel()`
- [ ] Add any by-name FK referent (`BaseVoltage`, `LoadResponse`, …) via
      `graph_write.add_to_graph` before the method that resolves it
- [ ] Run only up to the method under test (`create` → `add_connectivity` → …,
      calling `add()` only if the assertion needs the object in the graph)
- [ ] Assert creation: the object's own attributes, or `graph_write.resolve`
      for by-name lookups
- [ ] Assert wiring: terminals connected to the right nodes and equipment
- [ ] Assert per-profile values: `add_electrical` checks only electrical
      fields, `add_ssh` checks only SSH fields — a field from a part the
      method under test never touched should still be `None`
- [ ] Assert containment: equipment assigned to the right container (explicit
      override, or `network.container` fallback)
- [ ] Assert profile identity: objects live under `network.cim.X`
- [ ] A relative (`pu`/`%`) impedance value: assert the converted ohm value
      (`float(obj.r) == pytest.approx(r_pct / 100 * z_base)`), not a
      `NotImplementedError` — the conversion already exists (see `UNITS.md`)

---

## Common Patterns

### Testing a profile method in isolation

```python
def test_add_electrical_only_touches_electrical_fields(network):
    builder = EnergyConsumerBuilder(network)
    load = builder.create(name='test_load')
    builder.add_connectivity(load, node='671')
    builder.add_electrical(load, pfixed=10_000, qfixed=3_000)

    assert load.pfixed.to('W') == pytest.approx(10_000)
    assert load.qfixed.to('VAr') == pytest.approx(3_000)
    assert load.p is None   # add_ssh was never called — SSH fields untouched
```

### Testing a resolved-by-name FK that's missing

```python
def test_add_connectivity_unresolved_base_voltage_name_links_none(network):
    builder = EnergyConsumerBuilder(network)
    load = builder.create(name='load_671')
    builder.add_connectivity(load, node='671', BaseVoltage='does_not_exist')
    consumer = builder.add(load)
    assert consumer.BaseVoltage is None
```

This is deliberate: an unresolved by-name FK leaves the field `None` rather
than raising, for a field that's optional in the first place (`BaseVoltage=`
defaults to `None`). Contrast `from_table`'s `EquipmentContainer` handling
(`tests/builders/test_consumer.py::test_from_table_missing_equipment_container_raises`),
which does raise — because a `.cimtbl` row's `EquipmentContainer` column, when
present, is never optional; see `CIMTBL_DESIGN.md` §12.3 for why the two cases
differ.

### Testing substation assembly (feeder insertion)

```python
def test_single_bus_new_feeder(self):
    network, feeder, src = make_feeder_atom()
    sub = SingleBusSubstation(connection=None, name='sb', base_voltage=115000)
    sub.new_feeder(breaker_number=1, feeder=feeder, feeder_network=network)

    assert feeder.NormalEnergizingSubstation is sub.substation
    assert feeder in sub.substation.NormalEnergizedFeeder
    assert_added_to_graph(sub.network, cim.Breaker, expected_count=1)
    assert_added_to_graph(sub.network, cim.Disconnector, expected_count=2)
```
