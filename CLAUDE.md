# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CIM-Builder is a Python library for creating CIM (Common Information Model) models from scratch without requiring pre-existing model files. This is fundamentally different from other CIM tooling that requires source files like OpenDSS, PSSE, or GIS data.

The library enables:
1. Automatic creation of node-breaker substations in CIM via function calls
2. Automatic insertion of distribution feeders into node-breaker substations
3. Automatic insertion of aggregate feeder data into existing CIM transmission models

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

## Architecture

### Core Module Structure

The codebase is organized into four main modules:

#### 1. `substation_builder/`
Contains functions for creating different substation topologies and adding equipment to them. Each substation type has three main functions:
- `new_<type>_substation()`: Creates the base substation structure and returns a dict with network, substation, buses, and base_voltage
- `add_feeder_to_<type>()`: Adds a distribution feeder to the substation with switching equipment
- `add_branch_to_<type>()`: Adds transmission branches, transformers, and shunt equipment to the substation

**Supported substation types:**
- Single Bus (`new_single_bus_substation`)
- Main and Transfer (`new_main_and_transfer_substation`)
- Ring Bus (`new_ring_bus_substation`)
- Double Bus Single Breaker (`new_double_bus_single_breaker_substation`)
- Breaker and a Half (`new_breaker_and_a_half_substation`)
- Sectionalized Bus (`new_sectionalized_bus_substation`)

**Functional API Pattern:**
```python
# Create a substation
result = new_single_bus_substation(connection, name='MySub', base_voltage=115000)
network = result['network']
substation = result['substation']
main_bus = result['main_bus']
base_voltage = result['base_voltage']

# Add a feeder to it
add_feeder_to_single_bus(network, substation, main_bus, base_voltage,
                         breaker_number=1, feeder_network=feeder_net,
                         feeder=my_feeder)

# Add a branch to it
add_branch_to_single_bus(network, substation, main_bus, base_voltage,
                         breaker_number=2, branch_equipment=transformer,
                         branch_terminal=transformer.Terminals[0])
```

**Key Design Principles:**
- Functions are stateless - all required parameters are explicit
- Creation functions return dicts with all components needed for subsequent operations
- No inheritance hierarchy or class-based abstraction
- Each topology has its own set of functions tailored to its specific requirements
- Private helper functions (prefixed with `_`) handle internal bus tie creation

#### 2. `object_builder/`
Factory functions for creating individual CIM equipment objects. Organized by equipment category:
- `base/`: Base voltage objects
- `shunt/`: Breakers, capacitors, and shunt equipment
- `switch/`: Disconnectors and switching devices
- `topology/`: Bus bar sections and connectivity nodes
- `transformer/`: Power transformers and tap changers
- `line/`: Transmission lines and conductors
- `load/`: Energy consumers
- `generator/`: Synchronous generators
- `inverter/`: Power electronics connections (PEC), battery units (BU), EVSE
- `measurement/`: Analog and discrete measurements
- `protection/`: Protection function blocks
- `generic/`: `new_one_terminal_object()` and `new_two_terminal_object()` for flexible object creation

**Key Pattern**: All builder functions take a `GraphModel` as the first argument and automatically add created objects to the graph. They handle Terminal creation, ConnectivityNode associations, and UUID generation.

#### 3. `feeder_builder/`
Functions for creating and managing distribution feeders:
- `aggregate_feeder.py`: Creates aggregate feeder representations with load and generation totals
- `insert_measurements.py`: Adds measurements to feeder equipment
- `cim_measurement_manager.py`: Manages measurement configurations

#### 4. `utils/`
Helper utilities:
- `get_base_voltage.py`: Retrieves or creates BaseVoltage objects
- `get_source_bus.py`: Locates feeder source buses (used by all substation add_feeder functions)
- `catalog_parser.py`: Parses JSON equipment catalogs from `data_catalog/`
- `utils.py`: Common utilities including `terminal_to_node()` for terminal-node connections

### Data Catalog

The `data_catalog/` directory contains JSON files with equipment specifications:
- `transformers/`: Power transformer specifications
- `conductors/`: Conductor type specifications
- `houses/`: Housing/load profile data

These are parsed by `catalog_parser.py` using recursive item parsing to create CIM objects from nested JSON structures.

### CIM Profile Integration

The library uses dynamic CIM profile loading via `cimgraph.databases.get_cim_profile()`. This returns:
1. Profile name string (e.g., "cimhub_2023")
2. CIM module for type annotations and object creation

**Critical Pattern**: Most modules import a specific CIM profile for type hints:
```python
import cimgraph.data_profile.cimhub_2023 as cim
```
But then call `get_cim_profile()` at runtime to get the actual module to use:
```python
cim_profile, cim_module = get_cim_profile()
cim_mod = cim_module  # Use this for object creation
```

### Graph Model Operations

All CIM objects must be added to a `GraphModel` instance (from cim-graph):
- `network.add_to_graph(obj)`: Adds object to graph
- `network.get_all_edges(cim_class)`: Loads all edges for a CIM class type
- `network.pprint(cim_class)`: Pretty prints all instances of a class
- `network.upload()`: Uploads to database (requires ConnectionInterface)

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
