# Developer docs

How CIM-Builder is built: one object builder per CIM class, each writing one CIM profile part per method
through `cimtables`, and the substation layout builders composed from them. To contribute a change, see
[Contributing](../01_overview/1_3_contributing.ipynb).

## Object builders

Every builder in `cimbuilder/object_builder/<category>/` (`line`, `switch`, `shunt`, `transformer`, `load`,
`topology`, `container`, ...) subclasses `ObjectBuilder` from `cimbuilder/object_builder/object_builder.py`:

```python
class ObjectBuilder(ABC):
    cim_class_name: str  # e.g. "LinearShuntCompensator", resolved on network.cim at runtime

    def __init__(self, network: GraphModel, container: CN.EquipmentContainer): ...

    def create(self, *, mRID=None, name=None, identifier=None, description=None) -> object:
        """Instantiates cim_class_name and adds it to network.graph"""

    def from_table(self, row: object) -> object:
        """Binds a validated cimtables <Class>Row with cimtables.binder.bind_row"""
```

On top of `create()`, each builder has one `add_*` method per CIM profile part it writes:

| Method | Profile part | Writes |
|---|---|---|
| `add_connectivity` | `connectivity_unbalanced` | Terminals, `EquipmentContainer`, `BaseVoltage`, per-phase children |
| `add_electrical` | `electrical_balanced` / `electrical_unbalanced` | steady-state electrical parameters |
| `add_short_circuit` | `short_circuit` | zero-sequence and fault parameters |
| `add_ssh` | `steady_state_hypothesis` | operating state such as `sections` and `inService` |

Other builders also write `topology`, `operational_limit`, `construction`, `asset_deployment`,
`asset_info` and `regulating_control`. Each method takes the created object plus keyword-only arguments,
writes through `cimtables.graph_write.set_attr` (scalars, with unit handling) and `set_assc_from_mrid`
(associations by mRID), and returns the object, plus any Terminals or phase objects it created.
`LinearShuntCompensatorBuilder` in `cimbuilder/object_builder/shunt/linear_shunt_compensator.py` is a good
reference for a new builder: keep one `add_*` method per profile part.

## Substation builders

`cimbuilder/substation_builder/substation_builder.py` holds `SubstationBuilder`, a subclass of the container
`SubstationBuilder`, with `add_voltage_level` and `add_bay`, plus the layout pieces every layout shares:

| Helper | Builds |
|---|---|
| `_bus_node(voltage_level, label)` | the mRID `<vl>_bus_<label>` of a bus node |
| `_node(voltage_level, node)` | the `ConnectivityNode` with that mRID, created in the VoltageLevel if missing |
| `_require_node(node)` | the node unchanged, raising if `add_buses()` has not built it |
| `_add_busbar(voltage_level, node)` | a bus node with a `BusbarSection` `<node>_bbs` on it |
| `_add_switch(builder_class, voltage_level, ...)` | one switch between two nodes, with `normalOpen` and `open` set together |
| `_add_breaker_bay(voltage_level, prefix=...)` | `<p>_d1` - `<p>_j1` - `<p>_brk` - `<p>_j2` - `<p>_d2` between two nodes |

Each layout is one subclass in its own module with two methods, `add_buses(voltage_level, ...)` and
`add_branch(voltage_level, *, ..., node)`, built only from these helpers. A new layout follows the same
shape: add the module, export the class from `cimbuilder/substation_builder/__init__.py`, add tests under
`tests/substation_builder/`, and add a notebook to these docs.

A new object builder goes in the [object builder](../03_object_builder/3_1_object_builders.ipynb) page for
its kind of equipment, with a short example that runs.

## Working on it

```bash
uv sync                          # the package, its dependencies and the dev group
uv run pytest                    # the suite
uv run pytest tests/substation_builder/test_substation_builder.py -q
```

## Building these docs

The site is MkDocs with the Material theme, configured in `mkdocs.yml`; the pages are in `docs/`.

```bash
uv sync --group docs
uv run mkdocs serve              # http://127.0.0.1:8000, reloads on save
uv run mkdocs build --strict     # what CI runs
```

The notebooks are stored with their outputs, and the build does not run them. After changing a notebook,
or the behaviour it shows, re-run it in place:

```bash
(cd docs/02_substation_builder && uv run jupyter nbconvert --to notebook --execute --inplace 2_*.ipynb)
(cd docs/03_object_builder && uv run jupyter nbconvert --to notebook --execute --inplace 3_*.ipynb)
```

In a notebook's Markdown cells, mkdocs-jupyter escapes a mermaid arrow (`-->`) twice, which breaks the
diagram, so connect nodes with `---` there. Arrows work as usual in the `.md` pages.

The theme lives in `docs/stylesheets/extra.css` and uses only Material's CSS variables. It is the same file
as the [CIM-Tables](https://pnnl-cim-tools.github.io/CIM-Tables/) and
[CIM-Graph](https://pnnl-cim-tools.github.io/CIM-Graph/) docs; keep the copies in step.

The site is deployed to GitHub Pages by `.github/workflows/docs.yml` on every push to `develop` that touches
the docs, and built (but not deployed) on pull requests.
