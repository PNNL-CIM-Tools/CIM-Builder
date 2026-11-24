# User guide

CIM-Builder builds CIM power system models from scratch. This guide covers installing it, building
node-breaker substations with feeders inserted into them, and building any piece of equipment one object at
a time. To change CIM-Builder itself, see the [developer docs](../developer/index.md).

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

-   __Object builders__

    ---

    [The builder pattern](../03_object_builder/3_1_object_builders.ipynb) and
    [a feeder from scratch](../03_object_builder/3_2_feeder_from_scratch.ipynb), then one notebook per kind
    of equipment, from [lines](../03_object_builder/3_4_lines.ipynb) and
    [transformers](../03_object_builder/3_6_transformers_and_regulators.ipynb) to
    [measurements and limits](../03_object_builder/3_10_measurements_and_limits.ipynb).

</div>

## The idea in four lines

- One builder class per CIM class, or per substation layout: `BreakerBuilder`, `RingBusSubstationBuilder`.
- `create()` makes the object; each `add_*` method fills in one more part of it, or adds what it contains.
- Objects refer to each other by mRID string: `BaseVoltage="bv_115kV"`, `node="line_1"`.
- Values carry their units, `Qty(115, "kV")`, and are stored in CIM's SI units.
