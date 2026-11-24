# User guide

CIM-Builder builds CIM power system models from scratch. This guide covers installing it and building
node-breaker substations, with feeders inserted into them. To change CIM-Builder itself, see the
[developer docs](../developer/index.md).

<div class="grid cards" markdown>

-   __Getting started__

    ---

    An [overview](../01_overview/1_1_overview.ipynb) of what CIM-Builder does and where it fits, and
    [installation](../01_overview/1_2_installation.ipynb).

-   __Substation builder__

    ---

    [Layouts and call order](../02_substation_builder/2_1_substation_builder.ipynb), shared by every layout,
    then one notebook per layout, from [single bus](../02_substation_builder/2_2_single_bus.ipynb) to
    [breaker and a half](../02_substation_builder/2_7_breaker_and_half.ipynb), and
    [all layouts](../02_substation_builder/2_8_all_layouts.ipynb) in one notebook.

</div>

## The idea in four lines

- One builder class per CIM class, or per substation layout: `BreakerBuilder`, `RingBusSubstationBuilder`.
- `create()` makes the object; each `add_*` method fills in one more part of it, or adds what it contains.
- Objects refer to each other by mRID string: `BaseVoltage="bv_115kV"`, `node="line_1"`.
- Values carry their units, `Qty(115, "kV")`, and are stored in CIM's SI units.
