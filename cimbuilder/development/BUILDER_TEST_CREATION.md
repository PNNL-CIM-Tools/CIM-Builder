# Creating Atom Tests for CIM-Builder Builders

Step-by-step instructions for building a unit test for any **builder** —
`ObjectBuilder` subclass (`LineBuilder`, `BreakerBuilder`, …) or a substation
assembly class (`SingleBusSubstation`, …). Designed for both human developers and
AI coding agents.

This is the builder-side counterpart to CIMHub's
[`ATOM_TEST_CREATION.md`](../../../CIMHub_2_0/cimhub_core/src/cimhub_core/development/ATOM_TEST_CREATION.md).
The structure is the same; the **direction is inverted**:

| | Converter (CIMHub) | Builder (CIM-Builder) |
|---|---|---|
| Input | a CIM subgraph (exporter) or a format object (importer) | a minimal **container atom** (network + container + nodes) |
| Act | run the converter | call `create()` → `add_connectivity()` → `add_electrical_bal()` … |
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
- **Profile-scoped** — they mirror the §5a contract: a test for
  `add_electrical_bal` asserts the balanced electrical fields and *only* those.
- **Self-documenting** — the atom factory shows exactly what container the
  builder expects.

---

## ⚠️ Connection API: do NOT use `ConnectionParameters`

The original integration tests came from
[`docs/03_substation_builder/deliverable.ipynb`](../../docs/03_substation_builder/deliverable.ipynb),
which built connections the **pre-0.3 way**:

```python
# BROKEN since cim-graph 0.3 — ConnectionParameters was removed
from cimgraph.databases import ConnectionParameters, RDFlibConnection
params = ConnectionParameters(filename=None, cim_profile=cim_profile, iec61970_301=8)
connection = RDFlibConnection(params)
```

`ConnectionParameters` no longer exists (`ImportError`), which broke every test
and demo derived from that notebook. The current API takes **direct kwargs** and
gets the profile from the `CIMG_CIM_PROFILE` env var via `get_cim_profile()`:

```python
# CORRECT — cim-graph 0.3+
import os
os.environ['CIMG_CIM_PROFILE'] = 'cgmes_3_0_0'   # the 0.5.0a1 merged profile
from cimgraph.databases import XMLFile
connection = XMLFile(filename=str(output_xml))     # filename=None for build-from-scratch
```

`XMLFile.__init__(self, filename=None, namespaces=None, metadata=None)` — no
`cim_profile`, no `iec61970_301`. **For unit atom tests you usually need no
connection at all** — see Step 2; you construct a `GraphModel` directly.

> The live-database round-trip from `deliverable.ipynb` (Blazegraph + CIM-Loader
> upload, re-query) is an **integration tier**, not a unit test. Keep it out of
> the atom suite; gate it behind a marker (`@pytest.mark.integration`) and a
> running database. Atom tests must run with `pytest` and nothing else.

---

## The CIM Object Model (Quick Reference)

> Snippets import `cgmes_3_0_0` — the cim-graph 0.5.0a1 merged profile this first
> pass targets. Builders read `cim = self.network.cim`, and the per-method type
> annotations narrow to the `cgmes_3_0_0` sub-profiles (`EQ` = `core_equipment`,
> `SC` = `short_circuit`, …) per §5a of `PROFILE_IDENTITY_0_5_PLAN.md`. Tests
> assert against `network.cim.X` so they stay correct under a merged profile.
> (Under CIM17 the connectivity classes live in the EQ part; the CIM18 CN split
> and the unbalanced `add_electrical_unbal` path are a later round.)

```python
import cimgraph.data_profile.cgmes_3_0_0 as cim

line = cim.ACLineSegment(name='test_line')   # UUID auto-seeded from class+name
line.r = cim.Resistance(0.01, 'ohm')          # CIMUnit: quantity + unit
line.EquipmentContainer = feeder              # association
line.Terminals.append(terminal)               # list association
network.add_to_graph(line)                    # keyed by (type, identifier)
```

Key `GraphModel` / `NodeBreakerModel` methods used in assertions:

| Method | What it does |
|--------|-------------|
| `network.add_to_graph(obj)` | Add to `network.graph[type(obj)][obj.identifier]` |
| `network.graph[cim.X]` | dict of `{identifier: obj}` for type X — the identity-keyed store |
| `network.list_by_class(cim.X)` | All objects of type X, sorted by URI |
| `network.find_by_attribute(cim.X, 'name', value)` | Linear search by attribute |
| `network.get_all_edges(cim.X)` | Hydrate associations (needed before deep traversal on a DB-backed model) |

---

## Step 1: Identify the Builder's Prerequisites

Read the builder and list **what it attaches to** (the container side) and
**what it produces** (the equipment side). Unlike a converter, a builder does
not `find_by_attribute` for inputs — its prerequisites are its constructor /
`create()` arguments.

Example — the target `LineBuilder` (Phase 3):

```python
class LineBuilder(ObjectBuilder):
    network: GraphModel
    container: "EQ.EquipmentContainer"        # PREREQ: a container (Feeder/Line/VL)

    def create(self, name): ...               # makes the ACLineSegment
    def add_connectivity(self, node1, node2): # PREREQ: two ConnectivityNodes
        cim = self.network.cim
        ...                                   # builds 2 terminals, wires to nodes
    def add_electrical_bal(self, r, x, bch, ...): # writes balanced EQ fields on self.line
    def add_short_circuit(self, r0, x0, ...): # writes SC fields on self.line
```

Prerequisites for the atom:
- a `GraphModel` (no connection needed for a pure unit test);
- an `EquipmentContainer` to pass as `container`;
- two `ConnectivityNode`s in the graph named `node1` / `node2`.

This maps to the `make_2node_atom()` factory below.

For a **substation** assembly class (e.g. `SingleBusSubstation`), the
prerequisites are inverted — it *creates* its own container and buses, and its
`new_feeder(...)` needs a feeder `GraphModel` with a source bus. Those tests use
a `make_feeder_atom()` (a tiny feeder with a `sourcebus` `ConnectivityNode` +
`EnergySource`) — exactly the minimal feeder the existing
`test_single_bus_integration.py` fixture builds inline.

---

## Step 2: Choose or Build the Atom Factory

Put shared factories in `tests/atoms.py` and shared assertions in
`tests/assertions.py` (mirroring CIMHub's `cimhub_core/tests/atoms.py` /
`assertions.py`). Build the network **directly**, no connection:

```python
# tests/atoms.py
import cimgraph.data_profile.cgmes_3_0_0 as cim
from cimgraph.models import GraphModel

def _empty_network() -> GraphModel:
    # No connection, no DB. A GraphModel with an empty graph is enough to build into.
    network = GraphModel()
    network.graph = {}
    return network
```

### Container-only atom (most object builders)

```python
def make_2node_atom(base_kv: float = 115000):
    """Substation container + BaseVoltage + 2 ConnectivityNodes('node1','node2')."""
    network = _empty_network()
    bv = cim.BaseVoltage(name=f'BaseV_{base_kv}', nominalVoltage=base_kv)
    sub = cim.Substation(name='test_sub')
    n1 = cim.ConnectivityNode(name='node1', ConnectivityNodeContainer=sub)
    n2 = cim.ConnectivityNode(name='node2', ConnectivityNodeContainer=sub)
    for o in (bv, sub, n1, n2):
        network.add_to_graph(o)
    return network, sub, bv, n1, n2
```

### Single-node atom (one-terminal devices: loads, shunts, sources)

```python
def make_1node_atom(base_kv: float = 12470):
    network = _empty_network()
    bv = cim.BaseVoltage(name=f'BaseV_{base_kv}', nominalVoltage=base_kv)
    sub = cim.Substation(name='test_sub')
    n1 = cim.ConnectivityNode(name='node1', ConnectivityNodeContainer=sub)
    for o in (bv, sub, n1):
        network.add_to_graph(o)
    return network, sub, bv, n1
```

### Feeder atom (substation `new_feeder` tests)

```python
def make_feeder_atom(mrid='TEST-FEEDER-001'):
    """Minimal feeder GraphModel with a 'sourcebus' CN + EnergySource."""
    network = _empty_network()
    feeder = cim.Feeder(mRID=mrid)
    src_node = cim.ConnectivityNode(name='sourcebus', ConnectivityNodeContainer=feeder)
    source = cim.EnergySource(name='source', EquipmentContainer=feeder)
    t = cim.Terminal(name='source_t1', sequenceNumber=1,
                     ConnectivityNode=src_node, ConductingEquipment=source)
    source.Terminals.append(t)
    feeder.NormalHeadTerminal = t
    for o in (feeder, src_node, source, t):
        network.add_to_graph(o)
    return network, feeder, src_node
```

**Reuse, don't reinvent.** `make_feeder_atom` is the inline fixture in
`tests/test_single_bus_integration.py` extracted into a factory. If a builder
needs a `BaseVoltage` lookup, reuse `cimbuilder.utils.get_base_voltage`; if it
needs source-bus discovery, reuse `cimbuilder.utils.get_source_bus`.

---

## Step 3: Run the Builder Through Its Profile Methods

A builder test's "act" is the chained build. Each method is a separate testable
unit, so you can stop after the method under test:

```python
builder = LineBuilder(network=network, container=feeder)
builder.create('test_line')                       # EQ object exists
builder.add_connectivity(node1='node1', node2='node2')   # terminals wired
builder.add_electrical_bal(r=0.01, x=0.1, bch=0.0, r_unit='ohm', x_unit='ohm', bch_unit='S')
```

To unit-test just `add_electrical_bal`, do the minimal setup (`create` +
`add_connectivity`) then call only `add_electrical_bal` and assert only its
fields.

---

## Step 4: Write the Test

```python
# tests/object_builder/line/test_line_builder.py
import cimgraph.data_profile.cgmes_3_0_0 as cim
from cimbuilder.object_builder.line.line_builder import LineBuilder
from tests.atoms import make_2node_atom
from tests.assertions import (
    assert_added_to_graph,
    assert_terminal_connected,
    assert_in_container,
)


class TestLineBuilder:

    def test_create_adds_segment(self):
        network, sub, bv, n1, n2 = make_2node_atom()
        LineBuilder(network=network, container=sub).create('test_line')

        assert_added_to_graph(network, cim.ACLineSegment, expected_count=1)
        line = network.find_by_attribute(cim.ACLineSegment, 'name', 'test_line')[0]
        assert_in_container(line, cim.Substation)

    def test_add_connectivity_wires_two_terminals(self):
        network, sub, bv, n1, n2 = make_2node_atom()
        b = LineBuilder(network=network, container=sub)
        b.create('test_line').add_connectivity(node1='node1', node2='node2')

        line = network.find_by_attribute(cim.ACLineSegment, 'name', 'test_line')[0]
        assert_added_to_graph(network, cim.Terminal, expected_count=2)
        assert len(line.Terminals) == 2
        assert_terminal_connected(line.Terminals[0], 'node1', 'test_line')
        assert_terminal_connected(line.Terminals[1], 'node2', 'test_line')

    def test_add_electrical_bal_sets_impedance(self):
        network, sub, bv, n1, n2 = make_2node_atom()
        b = LineBuilder(network=network, container=sub)
        b.create('test_line').add_connectivity('node1', 'node2')
        b.add_electrical_bal(r=0.01, x=0.1, bch=0.0,
                             r_unit='ohm', x_unit='ohm', bch_unit='S')

        line = network.find_by_attribute(cim.ACLineSegment, 'name', 'test_line')[0]
        assert abs(float(line.r) - 0.01) < 1e-9       # CIMUnit stores SI ohms
        assert abs(float(line.x) - 0.1) < 1e-9
```

Shared assertions (`tests/assertions.py`), builder-flavored:

```python
def assert_added_to_graph(network, cim_class, expected_count=None):
    """The class is a graph key and (optionally) has the expected count."""
    assert cim_class in network.graph, f'{cim_class.__name__} not in graph'
    objs = network.graph[cim_class]
    if expected_count is not None:
        assert len(objs) == expected_count, \
            f'expected {expected_count} {cim_class.__name__}, got {len(objs)}'

def assert_terminal_connected(terminal, node_name, equipment_name):
    assert terminal.ConnectivityNode is not None
    assert terminal.ConnectivityNode.name == node_name
    assert terminal.ConductingEquipment.name == equipment_name
    assert terminal in terminal.ConnectivityNode.Terminals

def assert_in_container(obj, container_class):
    c = obj.EquipmentContainer
    assert c is not None and isinstance(c, container_class)
```

---

## Step 5: Profile-Identity Assertion (the 0.5 guardrail)

Because builders read `cim = self.network.cim`, every object lands under the
graph's own class identity. Add one assertion that would catch a stray
`get_cim_profile()` re-derivation (0.5 Failure 1):

```python
def test_objects_use_network_profile_identity(self):
    network, sub, bv, n1, n2 = make_2node_atom()
    LineBuilder(network=network, container=sub).create('test_line').add_connectivity('node1', 'node2')

    # The graph key and isinstance must agree on ONE ACLineSegment class object.
    assert network.cim.ACLineSegment in network.graph
    line = network.graph[network.cim.ACLineSegment].popitem()[1]
    assert isinstance(line, network.cim.ACLineSegment)
```

If a builder used `get_cim_profile()` instead of `network.cim` under a merged
profile, this key lookup would miss and the test would fail loudly — which is the
point.

---

## Step 6: Run It

```bash
uv run pytest tests/object_builder/line/test_line_builder.py -v
```

Mirror the source tree under `tests/` (the `__pycache__` remnants show the
intended layout): `tests/object_builder/<category>/test_<eq>_builder.py`,
`tests/topology_builder/test_<topology>.py`, `tests/composite_builder/…`.

---

## Saving an Atom as XML (Optional)

For a debugging reference or an integration fixture, serialize any atom — using
the **current** API (no `ConnectionParameters`):

```python
from cimgraph.utils import write_xml
network, sub, bv, n1, n2 = make_2node_atom()
LineBuilder(network=network, container=sub).create('test_line').add_connectivity('node1', 'node2')

write_xml(network, 'tests/test_models/line_atom.xml')
```

This produces valid CIM XML with correct UUID cross-references because cimgraph
manages `Identity.identifier → obj.uri()` internally. Do **not** hand-edit XML or
rely on external exporters for fixtures — mismatched UUIDs break round-trips.

---

## Test Tiers (what runs where)

| Tier | Scope | Deps | Where |
|---|---|---|---|
| **Atom (unit)** | one builder / one `add_<profile>` method | pytest only | `tests/object_builder/**`, `tests/topology_builder/**` |
| **Composition** | a builder chain + substation assembly (e.g. single-bus + feeder) | pytest, in-memory graph | `tests/composite_builder/**`, `tests/test_single_bus_integration.py` |
| **Integration** | XML round-trip / Blazegraph upload + re-query (the old `deliverable.ipynb` flow) | running DB + CIM-Loader | `@pytest.mark.integration`, opt-in |

The atom and composition tiers must be green on every commit. The integration
tier is opt-in (it needs a database) and is the modern, `XMLFile`/`get_cim_profile`
replacement for the `ConnectionParameters` round-trip that broke in 0.3.

---

## Checklist for a Complete Builder Atom Test

- [ ] Read the builder — list its constructor/`create` prerequisites
      (container) and what each `add_<profile>` method writes
- [ ] Choose the atom factory (1-node, 2-node, 2-voltage-level, feeder)
- [ ] Build the network **directly** — no `ConnectionParameters`, no DB, no file
- [ ] Run only up to the method under test (`create` → `add_connectivity` → …)
- [ ] Assert creation: correct count of each CIM class in `network.graph`
- [ ] Assert wiring: terminals connected to the right nodes and equipment
- [ ] Assert per-profile values: `add_electrical_bal` checks balanced EQ fields
      only, `add_short_circuit` checks SC fields only (mirrors the §5a write-scoping)
- [ ] Assert containment: equipment assigned to the right container
- [ ] Assert profile identity: objects live under `network.cim.X` (0.5 guardrail)
- [ ] (Per-unit, Phase 11) assert pu→SI conversion once the units engine exists;
      until then assert the pu path raises `NotImplementedError` / warns

---

## Common Patterns

### Testing a profile method in isolation

```python
def test_short_circuit_only_touches_zero_sequence(self):
    network, sub, bv, n1, n2 = make_2node_atom()
    b = LineBuilder(network=network, container=sub)
    b.create('test_line').add_connectivity('node1', 'node2')
    b.add_short_circuit(r0=0.03, x0=0.3, b0ch=0.0)

    line = network.find_by_attribute(cim.ACLineSegment, 'name', 'test_line')[0]
    assert abs(float(line.r0) - 0.03) < 1e-9
    assert abs(float(line.x0) - 0.3) < 1e-9
    assert line.r is None   # add_electrical_bal was never called — EQ untouched
```

### Testing the deferred per-unit path (until Phase 11)

```python
import pytest

def test_per_unit_not_yet_supported(self):
    network, sub, bv, n1, n2 = make_2node_atom()
    b = LineBuilder(network=network, container=sub)
    b.create('test_line').add_connectivity('node1', 'node2')
    with pytest.raises(NotImplementedError):
        b.add_electrical_bal(r=0.01, x=0.1, bch=0.0, r_unit='pu', x_unit='pu', bch_unit='pu')
```

When Phase 11 lands the `z_base = base_kv**2 / base_mva` engine, replace this
with the conversion assertion (compare `float(line.r)` to `r_pu * z_base`),
exactly as CIMHub's `ATOM_TEST_CREATION.md` "per-unit to SI conversion" pattern.

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
