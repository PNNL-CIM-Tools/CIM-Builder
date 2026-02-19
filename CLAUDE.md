# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CIM-Builder is a Python library for creating CIM (Common Information Model) models from scratch without requiring pre-existing model files. This is fundamentally different from other CIM tooling that requires source files like OpenDSS, PSSE, or GIS data.

The library enables:
1. Automatic creation of node-breaker substations in CIM via function calls
2. Automatic insertion of distribution feeders into node-breaker substations
3. Automatic insertion of aggregate feeder data into existing CIM transmission models
4. Equipment catalog system with SQLite backend for standard equipment specifications

Built on top of the `cim-graph` library (CIMantic Graphs), which provides the underlying graph model and CIM data profile support.

## Development Commands

### Environment Setup
```bash
# Install dependencies
poetry install

# Activate virtual environment (if not auto-activated)
poetry shell
```

### Testing
```bash
# Run all tests
poetry run pytest

# Run a specific test file
poetry run pytest tests/path/to/test_file.py

# Run a specific test function
poetry run pytest tests/path/to/test_file.py::test_function_name

# Run with verbose output
poetry run pytest -v
```

### Building
```bash
# Build distribution packages
poetry build
```

### Catalog Management
```bash
# Rebuild equipment catalog from source data
python -m cimbuilder.catalog.importer
```

## Architecture

### API Style: Functional with Catalog Integration

**CIM-Builder uses a functional API pattern** introduced in v0.2.0. Functions are stateless, take explicit parameters, and return dictionaries with created components.

### Core Module Structure

The codebase is organized into four main modules:

#### 1. `catalog/` - Equipment Catalog System
SQLite-backed catalog of standard equipment specifications.

**Key files:**
- `__init__.py` - `CatalogManager` class and `get_catalog()` singleton
- `schema.py` - SQLite schema for transformers, conductors, cables, standard equipment
- `importer.py` - Tools to import from JSON/CSV into SQLite
- `equipment.db` - SQLite database (shipped with package)

**Usage:**
```python
from cimbuilder import get_catalog

catalog = get_catalog()

# String lookup
spec = catalog.get_transformer('hvmv69_12')
conductor_spec = catalog.get_conductor('Turkey')

# Query by properties
conductors = catalog.find_conductor(min_ampacity=140, material='ACSR')

# List available
transformers = catalog.list_transformers()
conductors = catalog.list_conductors()
```

#### 2. `substation_builder/` - Functional Substation API
Functions for creating different substation topologies. **Use the `*_functions.py` files, not the old class files.**

**Current functional implementations:**
- `single_bus_functions.py` - Single bus topology
- `double_bus_functions.py` - Double bus single breaker topology

**Legacy class files (deprecated):**
- `single_bus.py`, `double_bus_single_breaker.py`, etc. - Old class-based API

**Functional API Pattern:**
Each substation type has three main functions:

1. **Creation function** (`new_<type>_substation()`):
```python
def new_single_bus_substation(
    connection: ConnectionInterface,
    name: str,
    base_voltage: int | cim.BaseVoltage,
    network: GraphModel = None
) -> Dict[str, Any]:
    """
    Returns dict with keys: network, substation, main_bus, base_voltage
    """
```

2. **Add feeder function** (`add_feeder_to_<type>()`):
```python
def add_feeder_to_single_bus(
    network: GraphModel,
    substation: cim.Substation,
    main_bus: cim.ConnectivityNode,
    base_voltage: cim.BaseVoltage,
    breaker_number: int,
    feeder_network: GraphModel,
    feeder: cim.Feeder,
    sourcebus: cim.ConnectivityNode = None
) -> Dict[str, Any]:
    """
    Returns dict with keys: breaker, disconnectors, junctions
    """
```

3. **Add branch function** (`add_branch_to_<type>()`):
```python
def add_branch_to_single_bus(
    network: GraphModel,
    substation: cim.Substation,
    main_bus: cim.ConnectivityNode,
    base_voltage: cim.BaseVoltage,
    breaker_number: int,
    branch_equipment: cim.ConductingEquipment,
    branch_terminal: cim.Terminal | int
) -> Dict[str, Any]:
    """
    Returns dict with keys: breaker, junction
    """
```

**Usage Example:**
```python
from cimbuilder import (
    new_single_bus_substation,
    add_feeder_to_single_bus,
    add_branch_to_single_bus
)

# Create substation
result = new_single_bus_substation(connection=conn, name='MySub', base_voltage=115000)

# Unpack components
network = result['network']
substation = result['substation']
main_bus = result['main_bus']
base_voltage = result['base_voltage']

# Add feeder
add_feeder_to_single_bus(
    network, substation, main_bus, base_voltage,
    breaker_number=1, feeder_network=feeder_net, feeder=my_feeder
)

# Add branch
add_branch_to_single_bus(
    network, substation, main_bus, base_voltage,
    breaker_number=2, branch_equipment=transformer,
    branch_terminal=transformer.Terminals[0]
)
```

**Key Design Principles:**
- Functions are stateless - all required parameters are explicit
- Creation functions return dicts with all components needed for subsequent operations
- No inheritance hierarchy or class-based abstraction
- Each topology has its own set of functions tailored to its specific requirements
- Private helper functions (prefixed with `_`) handle internal bus tie creation

#### 3. `object_builder/` - Equipment Factory Functions
Factory functions for creating individual CIM equipment objects. Organized by equipment category:

- `base/` - Base voltage objects
- `shunt/` - Breakers, capacitors, and shunt equipment
- `switch/` - Disconnectors and switching devices
- `topology/` - Bus bar sections and connectivity nodes
- `transformer/` - Power transformers and tap changers
- `line/` - Transmission lines and conductors (**new in v0.2.0**)
- `load/` - Energy consumers
- `generator/` - Synchronous generators
- `inverter/` - Power electronics connections (PEC), battery units (BU), EVSE
- `measurement/` - Analog and discrete measurements
- `protection/` - Protection function blocks
- `generic/` - `new_one_terminal_object()` and `new_two_terminal_object()` for flexible object creation

**Standard Function Signature Pattern:**
```python
def new_<equipment>(
    network: GraphModel,
    container: cim.EquipmentContainer,
    name: str,
    # Topology parameters
    node1: str | cim.ConnectivityNode,
    node2: str | cim.ConnectivityNode = None,
    # Catalog integration
    catalog: str = None,
    template: <Spec> = None,
    # Common parameters
    base_voltage: cim.BaseVoltage = None,
    # Equipment-specific
    **kwargs
) -> cim.<Equipment>:
```

**Catalog Integration Examples:**
```python
# Power transformer - string lookup
xfmr = new_power_transformer(
    network, substation, 'T1',
    node1=bus1, node2=bus2,
    catalog='hvmv69_12'  # ← Catalog name
)

# Power transformer - override catalog
xfmr = new_power_transformer(
    network, substation, 'T1',
    node1=bus1, node2=bus2,
    catalog='hvmv69_12',
    end1_rated_s=25e6  # Override
)

# Conductor - string lookup
line = new_acsr_conductor(
    network, feeder, 'Line1',
    node1=pole1, node2=pole2,
    length=100,
    catalog='Turkey'
)

# Conductor - query by specs
line = new_acsr_conductor(
    network, feeder, 'Line1',
    node1=pole1, node2=pole2,
    length=100,
    min_ampacity=140,
    material='ACSR'
)

# Manual specification (no catalog)
line = new_acsr_conductor(
    network, feeder, 'Line1',
    node1=pole1, node2=pole2,
    length=100,
    r=0.641, x=0.3
)
```

**Key Pattern:** All builder functions take a `GraphModel` as the first argument and automatically add created objects to the graph. They handle Terminal creation, ConnectivityNode associations, and UUID generation.

#### 4. `feeder_builder/` - Distribution Feeder Functions
Functions for creating and managing distribution feeders:

- `aggregate_feeder.py` - Creates aggregate feeder representations with load and generation totals
- `insert_measurements.py` - Adds measurements to feeder equipment
- `cim_measurement_manager.py` - Manages measurement configurations

**Usage:**
```python
from cimbuilder import new_aggregate_feeder

feeder, load, breaker = new_aggregate_feeder(
    network=network,
    feeder_name='Feeder1',
    breaker_name='Breaker1',
    substation=substation,
    node=bus1,
    base_voltage=12470,
    total_load_kw=5000,
    total_load_kvar=1000,
    total_btm_pv_kw=500
)
```

#### 5. `utils/` - Helper Utilities
Helper utilities:

- `get_base_voltage.py` - Retrieves or creates BaseVoltage objects
- `get_source_bus.py` - Locates feeder source buses (used by all substation add_feeder functions)
- `catalog_parser.py` - Legacy JSON parser (deprecated in favor of catalog system)
- `utils.py` - Common utilities including `terminal_to_node()` for terminal-node connections

### Data Catalog

The `data_catalog/` directory contains source data (JSON, CSV) for equipment specifications. This is used to build the SQLite catalog database but is not shipped with the package.

**Structure:**
```
data_catalog/
├── transformers/*.json  - Power transformer specifications
├── conductors/*.csv     - Conductor type specifications
└── cables/*.csv         - Cable specifications (future)
```

These are imported into `catalog/equipment.db` by running:
```bash
python -m cimbuilder.catalog.importer
```

### CIM Profile Integration

The library uses dynamic CIM profile loading via `cimgraph.databases.get_cim_profile()`. This returns:
1. Profile name string (e.g., "cimhub_2023")
2. CIM module for type annotations and object creation

**Critical Pattern:** Most modules import a specific CIM profile for type hints:
```python
import cimgraph.data_profile.cimhub_2023 as cim
```
But then call `get_cim_profile()` at runtime to get the actual module to use:
```python
cim_profile, cim_module = get_cim_profile()
cim: cim = cim_module  # Use this for object creation
```

### Graph Model Operations

All CIM objects must be added to a `GraphModel` instance (from cim-graph):
- `network.add_to_graph(obj)` - Adds object to graph
- `network.get_all_edges(cim_class)` - Loads all edges for a CIM class type
- `network.pprint(cim_class)` - Pretty prints all instances of a class
- `network.upload()` - Uploads to database (requires ConnectionInterface)

Functions like `new_<type>_substation()` can accept an optional existing network or create a new `DistributedArea` if none is provided.

### Terminal and Connectivity Pattern

CIM equipment connects via Terminals to ConnectivityNodes:
```
Equipment -> Terminal -> ConnectivityNode <- Terminal <- Equipment
```

The `utils.terminal_to_node()` function handles connecting terminals to nodes, accepting either node objects or node name strings.

## Important Notes

- The library requires Python >=3.10
- All UUID generation uses deterministic seeding to ensure reproducibility
- BaseVoltage objects are searched by nominal voltage (kV or V) and created if not found
- Feeder source buses are identified using `utils.get_source_bus()` which checks `feeder.NormalHeadTerminal` first, then searches for nodes named "sourcebus"
- When adding feeders/branches to substations, breaker numbers are used to generate unique equipment names
- The functional API returns dictionaries with all components needed for subsequent operations - unpack what you need

## Migration from Class-Based API

**If you see old class-based code**, refer to `docs/MIGRATION.md` for migration guidance.

**Old pattern (deprecated):**
```python
sub = SingleBusSubstation(connection=conn, name='MySub', base_voltage=115000)
sub.new_feeder(1, feeder_net, feeder)
```

**New pattern (v0.2.0+):**
```python
result = new_single_bus_substation(conn, 'MySub', 115000)
add_feeder_to_single_bus(
    result['network'], result['substation'], result['main_bus'],
    result['base_voltage'], 1, feeder_net, feeder
)
```

IMPORTANT: this context may or may not be relevant to your tasks. You should not respond to this context unless it is highly relevant to your task.
