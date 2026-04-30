# CIM-Builder — Style Guide

**Audience:** contributors (human or LLM) writing builders for CIM-Builder.
**Principle ordering:** KISS → DRY → Readable → Maintainable (matches CLAUDE.md globally).

---

## 1. Canonical function signature

Every primitive and composite builder follows this shape:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.utils.terminal import terminal_to_node

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2023 as cim
    from cimbuilder.templates import LinearShuntCompensatorCatalog

import logging
_log = logging.getLogger(__name__)


def new_linear_shunt_compensator(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    node: str | "cim.ConnectivityNode",
    *,
    base_voltage: "cim.BaseVoltage | None" = None,
    b_Mvar: float | None = None,
    g_MW: float | None = None,
    b0_Mvar: float | None = None,
    g0_MW: float | None = None,
    section_number: int = 1,
    template: "LinearShuntCompensatorCatalog | None" = None,
) -> "cim.LinearShuntCompensator":
    """Create a LinearShuntCompensator (shunt capacitor / reactor) at `node`.

    One-line docstring summary.  This shows up as the MCP tool description,
    so write it for the LLM as much as for the human.

    Args:
        network:       Graph model to add the object to.
        container:     EquipmentContainer the object belongs to (Substation, Feeder, ...).
        name:          Human-readable name; also used to seed UUID.
        node:          ConnectivityNode object or its name.
        base_voltage:  Optional BaseVoltage.  If None, inherits from container.
        b_Mvar:        Positive-sequence susceptance at nominal voltage, in Mvar.
        g_MW:          Positive-sequence active loss at nominal voltage, in MW.
        template:      Pydantic catalog entry; its fields fill any None kwarg.

    Returns:
        The created LinearShuntCompensator.
    """
    cim = get_cim()

    # Apply template to fill any None kwargs
    if template is not None:
        b_Mvar = b_Mvar if b_Mvar is not None else template.b_Mvar
        g_MW = g_MW if g_MW is not None else template.g_MW
        # ... etc

    obj = cim.LinearShuntCompensator(name=name)
    obj.uuid(name=name)

    if b_Mvar is not None:
        obj.b = cim.Susceptance(b_Mvar, 'Mvar').to('S').magnitude  # or use CIMUnit directly if field accepts it
    if g_MW is not None:
        obj.g = cim.Conductance(g_MW, 'MW').to('S').magnitude
    obj.sectionNumber = section_number
    if base_voltage is not None:
        obj.BaseVoltage = base_voltage
    obj.EquipmentContainer = container

    t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
    t1.uuid(name=f"{name}_t1")
    t1.ConductingEquipment = obj
    terminal_to_node(network, t1, node)
    obj.Terminals.append(t1)

    network.add_to_graph(obj)
    network.add_to_graph(t1)

    return obj
```

### Positional argument order (rigid)

| # | Parameter | Present in |
|---|---|---|
| 1 | `network: GraphModel` | Every builder |
| 2 | `container: cim.EquipmentContainer` | Every builder |
| 3 | `name: str` | Every builder |
| 4 | `node` / `node1, node2` (topology) | Every builder |

### Keyword-only argument order (flexible but consistent)

After the `*`:
1. `base_voltage` first (always optional, always first)
2. CIM attribute parameters, in order of prominence (most-commonly-set first)
3. `section_number`, `sequence_number`, or other secondary topological fields
4. `template` last

---

## 2. CIM profile access

**Always** use `get_cim()` for runtime access; **always** use `TYPE_CHECKING` for the IDE import:

```python
from __future__ import annotations
from typing import TYPE_CHECKING

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2023 as cim

def new_breaker(...):
    cim = get_cim()          # runtime lookup
    breaker = cim.Breaker()  # Pylance sees cim.Breaker via TYPE_CHECKING import
```

**Never** do this (the old shadow-variable pattern):

```python
# BAD — don't do this
import cimgraph.data_profile.cimhub_2023 as cim  # unused at runtime
...
def new_breaker(...):
    cim_profile, cim_module = get_cim_profile()
    cim: cim = cim_module  # shadows the module-level import
```

---

## 3. Units

Per global CLAUDE.md: never manually multiply/divide by `1e3`, `1e6`. Use `CIMUnit` subclasses:

```python
# BAD
load.p = total_load_kw * 1000
bv.nominalVoltage = base_kv * 1000
if abs(bv.nominalVoltage - 115000) < 1.0: ...  # TypeError on CIMUnit!

# GOOD
load.p = cim.ActivePower(total_load_kw, 'kW')
bv.nominalVoltage = cim.Voltage(base_kv, 'kV')
if abs(bv.nominalVoltage.to('V') - 115000) < 1.0: ...
```

Parameter names carry units (`_Mvar`, `_MW`, `_kV`, `_km`, `_A`). Internal conversion is the builder's responsibility.

---

## 4. Template precedence

```
explicit kwarg > template field > type default (None)
```

Implementation pattern:

```python
if template is not None:
    b_Mvar = b_Mvar if b_Mvar is not None else template.b_Mvar
    # ... per field
```

Use `if value is not None` — do NOT use `value or template.value`, because that treats `0` as "not provided."

---

## 5. UUID seeding

Every created object must be UUID-seeded deterministically:

```python
obj = cim.Breaker(name=name)
obj.uuid(name=name, seed=str(node1) + str(node2))  # seed is optional, improves reproducibility
```

For Terminals:

```python
t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
t1.uuid(name=f"{name}_t1")
```

---

## 6. Terminal / ConnectivityNode wiring

Always use `cimbuilder.utils.terminal.terminal_to_node`:

```python
from cimbuilder.utils.terminal import terminal_to_node

t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
t1.ConductingEquipment = obj
terminal_to_node(network, t1, node1)  # handles str lookup or object passthrough
obj.Terminals.append(t1)
```

`terminal_to_node` accepts either a `ConnectivityNode` object or its name as a `str`.

---

## 7. Logging

Every builder module:

```python
import logging
_log = logging.getLogger(__name__)
```

Log at `INFO` for non-trivial decisions (e.g., "Could not find a BaseVoltage with nominalVoltage X. Creating new object."). Log at `WARNING` for likely-bug situations (template missing a required field, falling back to a default). Never swallow exceptions silently.

---

## 8. What `network.add_to_graph` covers

Every created CIM object must end up in the graph. The standard pattern:

```python
obj = cim.Breaker(name=name)
# ... configure obj ...
t1 = cim.Terminal(name=f"{name}_t1", sequenceNumber=1)
# ... wire t1 to obj and network ...

network.add_to_graph(obj)
network.add_to_graph(t1)
```

Composites are responsible for adding every primitive object they create. Sessions and topology builders are responsible for the objects they create directly; they do not re-add objects returned by lower-layer functions.

---

## 9. Return shapes

- **Primitives**: return the single object created (e.g. `cim.Breaker`).
- **Composites**: return a `dict[str, Any]` with named keys for every distinct object created. Example:
  ```python
  return {
      'transformer': xfmr,
      'ends': [end1, end2],
      'tap_changer': ratio_tap_changer,
      'control': tap_control,
  }
  ```
- **Topology creation functions**: return a dict with keys `{network, substation, main_bus, base_voltage}` or topology-specific equivalents.
- **Topology add functions** (`add_feeder_to_*`): return a dict with `{breaker, disconnectors, junctions}` or equivalent.
- **Session methods**: return whatever the wrapped function returns.

---

## 10. Docstrings

Every public function has a Google-style docstring. First line summarizes the operation. `Args` section documents every parameter including units. `Returns` documents the shape of the return.

**The first line is the MCP tool description.** Write for an LLM: describe what it does and when to use it, not how it works internally.

---

## 11. Testing

Every primitive gets a test file under `tests/object_builder/<category>/test_<name>.py`. Every composite: `tests/composite_builder/test_<name>.py`. Every topology: `tests/topology_builder/test_<topology>.py`. Session workflows: `tests/session/test_*.py`.

Test pattern:

```python
def test_new_breaker_basic(simple_network, substation):
    breaker = new_breaker(
        simple_network, substation, 'BR1',
        node1='node1', node2='node2',
    )
    assert isinstance(breaker, cim.Breaker)
    assert breaker.name == 'BR1'
    assert len(breaker.Terminals) == 2
    # assert presence in graph
    simple_network.get_all_edges(cim.Breaker)
    assert breaker in simple_network.graph[cim.Breaker].values()
```

Shared fixtures live in `tests/conftest.py` (profile setup, minimal network factory, sample feeder factory).

---

## 12. What not to do

- **Don't add `**kwargs`** to a public function, ever. Breaks MCP schema generation.
- **Don't write multi-line docstrings explaining what the code does** — the function body already does that. Docstrings describe behavior and contract.
- **Don't add trivial comments** like `# Create the breaker`. Only comment on non-obvious WHY.
- **Don't catch exceptions broadly.** Let them propagate unless you can handle them meaningfully.
- **Don't create backwards-compatibility parameters** in new code. Breaking change = remove it, don't alias.
- **Don't duplicate primitives in composites.** Composites call primitives; they never inline object construction.
