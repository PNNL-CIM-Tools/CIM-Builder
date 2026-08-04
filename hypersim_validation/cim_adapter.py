"""CIM XML to GLM-style model adapter.

Produces the same module-level surface as ``glmanip`` so ``Interpreter.py``
can consume CIM input through the existing ``g.model[type][name][param]``
access pattern.
"""

import csv
import math
import os
import inspect

model = {}
clock = {}
modules = {}
classes = {}
schedules = {}
directives = []
coordinates_csv = None

_network = None
_cim = None


def reset():
    global model, clock, modules, classes, schedules, directives, _network, _cim, coordinates_csv
    model = {}
    clock = {}
    modules = {}
    classes = {}
    schedules = {}
    directives = []
    _network = None
    _cim = None
    coordinates_csv = None


def ingest(fn, basedir='.'):
    """Load a CIM XML file and populate ``model`` in GLM dict shape."""
    print('...Reading ' + fn)

    os.environ.setdefault('CIMG_CIM_PROFILE', 'cim17v40')
    import cimgraph.data_profile.cim17v40 as cim
    from cimgraph.databases import XMLFile
    from cimgraph.models import FeederModel

    global _network, _cim
    _cim = cim
    _network = FeederModel(container=cim.Feeder(), connection=XMLFile(filename=fn))

    _add_nodes(cim)
    _add_loads(cim)
    _add_lines(cim)
    _add_capacitors(cim)
    _add_transformers(cim)
    _add_regulators(cim)
    _add_switches(cim)
    _generate_coordinates_csv(cim, fn)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _name(obj):
    """Stable identifier: prefer name, fall back to mRID."""
    nm = getattr(obj, 'name', None)
    if nm:
        return nm
    return getattr(obj, 'mRID', None) or repr(obj)


def _cn_names(obj):
    """Yield ConnectivityNode names reachable from an equipment object's terminals."""
    for attr in ('Terminals', 'Terminal'):
        terminals = getattr(obj, attr, None)
        if terminals is None:
            continue
        if not isinstance(terminals, list):
            terminals = [terminals]
        for t in terminals:
            cn = getattr(t, 'ConnectivityNode', None)
            if cn is not None:
                nm = _name(cn)
                if nm:
                    yield nm
        return


def _sorted_terminals(obj):
    terminals = list(getattr(obj, 'Terminals', []) or [])
    try:
        terminals.sort(key=lambda t: int(t.sequenceNumber))
    except (TypeError, AttributeError):
        pass
    return terminals


def _get_phases(equipment):
    # Neither ACLineSegment nor Switch (the only callers) carries a 'phases'
    # field.  Phase membership lives in per-phase records — ACLineSegmentPhase
    # for lines, SwitchPhase for switches — populated on the parent equipment
    # after get_all_edges is called.  Equipment with no such records (e.g. a
    # 3-phase switch) falls through to the ABCN default.
    seg_phases = (getattr(equipment, 'ACLineSegmentPhases', None)
                  or getattr(equipment, 'SwitchPhase', None) or [])
    # ACLineSegmentPhase exposes the phase as 'phase'; SwitchPhase as 'phaseSide1'.
    letters = sorted({
        ph_letter
        for ph in seg_phases
        for ph_letter in [str(getattr(ph, 'phase', None)
                              or getattr(ph, 'phaseSide1', '') or '').split('.')[-1].upper()]
        if ph_letter in ('A', 'B', 'C')
    })
    if letters:
        return '"' + ''.join(letters) + 'N"'
    return '"ABCN"'


def _phase_tokens(raw):
    """Parse a CIM PhaseCode/phases value into ({'A','B','C'...}, has_split).

    Accepts the enum string in any form ('PhaseCode.AN', 'AN', 'A.N', 's1N'),
    returning the set of present A/B/C letters and whether a split-phase
    (triplex s1/s2) winding is indicated.
    """
    if raw is None:
        return set(), False
    upper = str(raw).split('.')[-1].strip().upper()
    letters = {p for p in ('A', 'B', 'C') if p in upper}
    has_split = 'S1' in upper or 'S2' in upper
    return letters, has_split


def _glm_phases(letters, has_split):
    """Build a quoted GLM phase string from parsed phase tokens, or None.

    Returns None when no usable phase information was found so callers can
    fall back to their 3-phase default rather than emitting an empty phase.
    """
    if has_split:
        return '"' + ''.join(sorted(letters)) + 'S"'
    if letters:
        return '"' + ''.join(sorted(letters)) + 'N"'
    return None


def _end_phase_tokens(end):
    """Phase tokens for a transformer/regulator end.

    TransformerTankEnd carries 'phases' directly; PowerTransformerEnd exposes
    its phasing only through its Terminal.  Prefer the end's own value and
    fall back to the Terminal's.
    """
    letters, has_split = _phase_tokens(getattr(end, 'phases', None))
    if not letters and not has_split:
        term = getattr(end, 'Terminal', None)
        if term is not None:
            letters, has_split = _phase_tokens(getattr(term, 'phases', None))
    return letters, has_split


# ---------------------------------------------------------------------------
# Node Loading
# ---------------------------------------------------------------------------

def _build_cn_phases_map(cim):
    """Return a dict mapping ConnectivityNode name -> set of phase letters ('A','B','C').

    Terminal objects have no 'phases' field in CIM XML.  Phase membership is
    encoded in ACLineSegmentPhase and EnergyConsumerPhase records, each of
    which carries a back-reference to its parent equipment and thereby to the
    ConnectivityNodes on either side of that equipment.
    """
    cn_phases = {}

    aclsp_cls = getattr(cim, 'ACLineSegmentPhase', None)
    if aclsp_cls is not None:
        try:
            for seg_ph in (_network.list_by_class(aclsp_cls) or []):
                ph = str(getattr(seg_ph, 'phase', '') or '').split('.')[-1].upper()
                if ph not in ('A', 'B', 'C'):
                    continue
                line = getattr(seg_ph, 'ACLineSegment', None)
                if line is None:
                    continue
                for cn_name in _cn_names(line):
                    cn_phases.setdefault(cn_name, set()).add(ph)
        except Exception:
            pass

    ecp_cls = getattr(cim, 'EnergyConsumerPhase', None)
    if ecp_cls is not None:
        try:
            for ecp in (_network.list_by_class(ecp_cls) or []):
                ph = str(getattr(ecp, 'phase', '') or '').split('.')[-1].upper()
                if ph not in ('A', 'B', 'C'):
                    continue
                ec = getattr(ecp, 'EnergyConsumer', None)
                if ec is None:
                    continue
                for cn_name in _cn_names(ec):
                    cn_phases.setdefault(cn_name, set()).add(ph)
        except Exception:
            pass

    return cn_phases


def _build_node_maps(cim):
    voltmap = {}
    swing = {}

    base = getattr(cim, 'ConductingEquipment', None)
    if base is not None:
        for name, cls in inspect.getmembers(cim, inspect.isclass):
            if not issubclass(cls, base):
                continue
            try:
                items = _network.list_by_class(cls) or []
            except Exception:
                continue

            is_source = name == 'EnergySource'
            
            for eq in items:
                bv = getattr(eq, 'BaseVoltage', None)
                nv = getattr(bv, 'nominalVoltage', None) if bv else None

                for cn_name in _cn_names(eq):
                    if nv is not None and cn_name not in voltmap:
                        voltmap[cn_name] = str(nv)
                    if is_source:
                        swing[cn_name] = eq

    # PowerTransformerEnd carries BaseVoltage but isn't ConductingEquipment
    pte = getattr(cim, 'PowerTransformerEnd', None)
    if pte is not None:
        try:
            for end in (_network.list_by_class(pte) or []):
                bv = getattr(end, 'BaseVoltage', None)
                nv = getattr(bv, 'nominalVoltage', None) if bv else None
                if nv is None:
                    continue
                for cn_name in _cn_names(end):
                    if cn_name not in voltmap:
                        voltmap[cn_name] = str(nv)
        except Exception:
            pass

    return voltmap, swing


def _add_nodes(cim):
    try:
        cns = _network.list_by_class(cim.ConnectivityNode)
    except Exception as e:
        print('WARNING: No ConnectivityNode List Available: ' + str(e))
        cns = []

    voltmap, swing = _build_node_maps(cim)
    cn_phases_map = _build_cn_phases_map(cim)
    model.setdefault('node', {})
    unresolved = []

    for cn in cns or []:
        nm = _name(cn)

        # --- Phases from ACLineSegmentPhase / EnergyConsumerPhase records ---
        # Terminal objects carry no 'phases' field; use the pre-built map instead.
        phase_letters = cn_phases_map.get(nm, set())
        phase_str = '"' + ''.join(sorted(phase_letters)) + 'N"' if phase_letters else '"ABCN"'

        # --- Nominal voltage from BaseVoltage ---
        # CIM BaseVoltage.nominalVoltage is line-to-line, but GLM 'nominal_voltage'
        # (the convention glmanip yields and Interpreter.py consumes) is
        # line-to-neutral: Interpreter multiplies a 3-phase node's voltage by
        # sqrt(3) to recover the L-L base, so store the L-N magnitude here.
        v_ll = voltmap.get(nm, '')
        if not v_ll:
            unresolved.append(nm)
            voltage = '0'
        else:
            voltage = str(_float(v_ll) / math.sqrt(3))

        params = {
            'phases': phase_str,
            'nominal_voltage': voltage,
        }

        # --- Swing bus: source voltage from EnergySource ---
        # EnergySource.voltageMagnitude is also line-to-line; convert to L-N to
        # match the nominal_voltage convention above.
        if nm in swing:
            es = swing[nm]
            src_ll = getattr(es, 'voltageMagnitude', None)
            src_v = str(_float(src_ll) / math.sqrt(3)) if src_ll else voltage
            params['bustype'] = 'SWING'
            params['voltage_A'] = src_v
            params['voltage_B'] = src_v
            params['voltage_C'] = src_v

        model['node'][nm] = params

    if unresolved:
        print('WARNING: No BaseVoltage Found For ' + str(len(unresolved))
              + ' ConnectivityNode(s); Defaulted to 0. First Few: '
              + ', '.join(unresolved[:5]))

    if model['node']:
        print('...Mapped ' + str(len(model['node'])) + ' ConnectivityNode(s) to Node Entries')


# ---------------------------------------------------------------------------
# Load Loading
# ---------------------------------------------------------------------------

def _add_loads(cim):
    ec_cls = getattr(cim, 'EnergyConsumer', None)
    ecp_cls = getattr(cim, 'EnergyConsumerPhase', None)
    if ec_cls is None or ecp_cls is None:
        return

    try:
        consumers = _network.list_by_class(ec_cls) or []
    except Exception as e:
        print('WARNING: No EnergyConsumer List Available: ' + str(e))
        consumers = []

    # Build a lookup from EnergyConsumer -> list of EnergyConsumerPhase
    try:
        all_phases = _network.list_by_class(ecp_cls) or []
    except Exception as e:
        print('WARNING: No EnergyConsumerPhase List Available: ' + str(e))
        all_phases = []

    phase_map = {}  # EnergyConsumer mRID -> [EnergyConsumerPhase, ...]
    for ecp in all_phases:
        parent_ec = getattr(ecp, 'EnergyConsumer', None)
        if parent_ec is None:
            continue
        ec_id = getattr(parent_ec, 'mRID', None) or id(parent_ec)
        phase_map.setdefault(ec_id, []).append(ecp)

    model.setdefault('load', {})
    skipped = []

    for ec in consumers:
        nm = _name(ec)
        ec_id = getattr(ec, 'mRID', None) or id(ec)

        # --- Determine parent node (first connected ConnectivityNode) ---
        parent = None
        for cn_name in _cn_names(ec):
            parent = cn_name
            break

        # --- Per-phase power from EnergyConsumerPhase ---
        ec_phases = phase_map.get(ec_id, [])

        phase_letters = set()
        power_by_phase = {}  # e.g. {'A': (p, q), 'B': (p, q)}

        if ec_phases:
            for ecp in ec_phases:
                ph = getattr(ecp, 'phase', None)
                if ph is None:
                    continue
                ph_str = str(ph).strip().upper()
                # Extract the letter — handle values like 'SinglePhaseKind.A'
                if '.' in ph_str:
                    ph_str = ph_str.split('.')[-1]
                if ph_str not in ('A', 'B', 'C'):
                    continue

                p = getattr(ecp, 'p', None) or 0.0
                q = getattr(ecp, 'q', None) or 0.0
                try:
                    p, q = float(p), float(q)
                except (TypeError, ValueError):
                    p, q = 0.0, 0.0

                phase_letters.add(ph_str)
                power_by_phase[ph_str] = (p, q)

            # All phase records resolved to something other than A/B/C — i.e. a
            # split-phase/triplex load (SinglePhaseKind.s1/s2).  Skip it rather
            # than fabricating a powerless 'ABCN' entry that drops the load's
            # power and misrepresents its connectivity.
            if not power_by_phase:
                skipped.append(nm)
                continue
        else:
            # No EnergyConsumerPhase records: the power lives on the
            # EnergyConsumer itself (e.g. IEEE13's balanced 3-phase load '671',
            # phaseConnection=D).  Spread the total evenly across A/B/C.
            p_tot, q_tot = _float(getattr(ec, 'p', None)), _float(getattr(ec, 'q', None))
            if p_tot == 0.0 and q_tot == 0.0:
                skipped.append(nm)
                continue
            for ph in ('A', 'B', 'C'):
                phase_letters.add(ph)
                power_by_phase[ph] = (p_tot / 3.0, q_tot / 3.0)

        # Delta (phase-to-phase) vs wye connection.  GLM marks delta loads with
        # 'D' in the phase string (vs 'N' for a wye neutral), and a delta load
        # sees the line-to-line voltage rather than the L-N magnitude.
        conn = str(getattr(ec, 'phaseConnection', '') or '').split('.')[-1].upper()
        is_delta = conn == 'D'
        suffix = 'D' if is_delta else 'N'
        phase_str = '"' + ''.join(sorted(phase_letters)) + suffix + '"' if phase_letters else '"ABC' + suffix + '"'

        # The parent node's nominal_voltage is line-to-neutral (see _add_nodes).
        # A wye load's per-phase voltage IS that L-N magnitude; a delta load sees
        # the line-to-line magnitude (L-N * sqrt(3)).
        nom_v_ln = (model.get('node', {}).get(parent, {}).get('nominal_voltage', '0')
                    if parent else '0')
        v_ln = _float(nom_v_ln)
        phase_volt = v_ln * math.sqrt(3) if is_delta else v_ln

        params = {
            'phases': phase_str,
            'nominal_voltage': nom_v_ln,
        }

        if parent:
            params['parent'] = parent

        # GLM per-phase voltage and constant-power fields
        for ph, (p, q) in power_by_phase.items():
            params['voltage_' + ph] = str(phase_volt)
            params['constant_power_' + ph] = '{}{:+}j'.format(p, q)

        # Suffix with '_ld' to avoid colliding with a ConnectivityNode of the
        # same name (e.g. EnergyConsumer '671' vs ConnectivityNode '671').
        # A collision causes add_load() in Interpreter.py to overwrite the
        # node's voltage attr and create a self-loop edge, which breaks the
        # baseVolt lookup in the line-processing loop.
        model['load'][nm + '_ld'] = params

    _consolidate_loads()

    if skipped:
        print('WARNING: No Usable Per-Phase (A/B/C) Power For ' + str(len(skipped))
              + ' EnergyConsumer(s); Skipped. First Few: '
              + ', '.join(skipped[:5]))

    if model['load']:
        print('...Mapped ' + str(len(model['load'])) + ' EnergyConsumer(s) to Load Entries')


def _consolidate_loads():
    """Merge single-phase load entries sharing the same parent ConnectivityNode
    into multi-phase entries so Interpreter.py emits a single customLoad3
    instead of per-phase breakouts with muxes.  Sums power when multiple
    entries contribute to the same phase."""
    loads = model.get('load', {})
    if not loads:
        return

    # Group single-phase load keys by (parent, is_delta).
    groups = {}
    for key, params in list(loads.items()):
        parent = params.get('parent')
        if parent is None:
            continue
        phase_str = params.get('phases', '')
        letters = {c for c in phase_str if c in 'ABC'}
        if len(letters) != 1:
            continue
        is_delta = phase_str.rstrip('"').endswith('D')
        groups.setdefault((parent, is_delta), []).append((key, letters.pop()))

    merged_count = 0
    for (parent, is_delta), members in groups.items():
        if len(members) < 2:
            continue

        # Accumulate per-phase power, summing if multiple entries share a phase.
        power = {}   # phase letter -> (p, q)
        nom_v_ln = '0'
        for key, ph in members:
            params = loads[key]
            nom_v_ln = params.get('nominal_voltage', nom_v_ln)
            cp = params.get('constant_power_' + ph)
            if cp is None:
                continue
            c = complex(cp)
            if ph in power:
                power[ph] = (power[ph][0] + c.real, power[ph][1] + c.imag)
            else:
                power[ph] = (c.real, c.imag)

        if len(power) < 2:
            continue

        v_ln = _float(nom_v_ln)
        phase_volt = v_ln * math.sqrt(3) if is_delta else v_ln
        phase_letters = sorted(power.keys())
        suffix = 'D' if is_delta else 'N'

        merged = {
            'phases': '"' + ''.join(phase_letters) + suffix + '"',
            'nominal_voltage': nom_v_ln,
            'parent': parent,
        }
        for ph in phase_letters:
            p, q = power[ph]
            merged['voltage_' + ph] = str(phase_volt)
            merged['constant_power_' + ph] = '{}{:+}j'.format(p, q)

        for key, _ph in members:
            del loads[key]
        loads[parent + '_ld'] = merged
        merged_count += len(members) - 1

    if merged_count:
        print('...Consolidated ' + str(merged_count)
              + ' Single-Phase Load(s) Into Multi-Phase Entries')


# ---------------------------------------------------------------------------
# Capacitor Loading
# ---------------------------------------------------------------------------

def _add_capacitors(cim):
    lsc_cls = getattr(cim, 'LinearShuntCompensator', None)
    lscp_cls = getattr(cim, 'LinearShuntCompensatorPhase', None)
    if lsc_cls is None:
        return

    try:
        compensators = _network.list_by_class(lsc_cls) or []
        _network.get_all_edges(lsc_cls)
    except Exception as e:
        print('WARNING: No LinearShuntCompensator List Available: ' + str(e))
        compensators = []

    phase_map = {}  # compensator mRID -> [LinearShuntCompensatorPhase, ...]
    if lscp_cls is not None:
        try:
            all_phases = _network.list_by_class(lscp_cls) or []
            _network.get_all_edges(lscp_cls)
        except Exception:
            all_phases = []
        for lscp in all_phases:
            parent_lsc = getattr(lscp, 'ShuntCompensator', None)
            if parent_lsc is None:
                continue
            lsc_id = getattr(parent_lsc, 'mRID', None) or id(parent_lsc)
            phase_map.setdefault(lsc_id, []).append(lscp)

    model.setdefault('capacitor', {})
    skipped = []

    for lsc in compensators:
        nm = _name(lsc)
        lsc_id = getattr(lsc, 'mRID', None) or id(lsc)

        parent = None
        for cn_name in _cn_names(lsc):
            parent = cn_name
            break

        if not parent:
            skipped.append(nm)
            continue

        nom_u = _float(getattr(lsc, 'nomU', None))
        b_per_section = _float(getattr(lsc, 'bPerSection', None))
        sections = _float(getattr(lsc, 'sections', None) or getattr(lsc, 'normalSections', None))
        if sections == 0.0:
            sections = 1.0

        conn = str(getattr(lsc, 'phaseConnection', '') or '').split('.')[-1].upper()
        is_delta = conn == 'D'

        lsc_phases = phase_map.get(lsc_id, [])

        params = {'parent': parent}

        if lsc_phases:
            phase_letters = set()
            for lscp in lsc_phases:
                ph = getattr(lscp, 'phase', None)
                if ph is None:
                    continue
                ph_str = str(ph).split('.')[-1].upper()
                if ph_str not in ('A', 'B', 'C'):
                    continue
                phase_letters.add(ph_str)

                ph_b = _float(getattr(lscp, 'bPerSection', None))
                ph_sections = _float(
                    getattr(lscp, 'sections', None)
                    or getattr(lscp, 'normalSections', None))
                if ph_sections == 0.0:
                    ph_sections = sections

                ph_var = nom_u * nom_u * ph_b * ph_sections
                params['capacitor_' + ph_str] = str(ph_var / 1e6)

            if not phase_letters:
                skipped.append(nm)
                continue

            suffix = 'D' if is_delta else 'N'
            params['phases'] = '"' + ''.join(sorted(phase_letters)) + suffix + '"'
            params['nominal_voltage'] = str(nom_u / 1000)
        else:
            total_var = nom_u * nom_u * b_per_section * sections
            per_phase_var = total_var / 3.0
            for ph in ('A', 'B', 'C'):
                params['capacitor_' + ph] = str(per_phase_var / 1e6)

            suffix = 'D' if is_delta else 'N'
            params['phases'] = '"ABC' + suffix + '"'
            if is_delta:
                params['nominal_voltage'] = str(nom_u / 1000)
            else:
                params['nominal_voltage'] = str(nom_u / math.sqrt(3) / 1000)

        model['capacitor'][nm] = params

    if skipped:
        print('WARNING: Skipped ' + str(len(skipped))
              + ' LinearShuntCompensator(s) Due to Missing Connectivity/Phases. First Few: '
              + ', '.join(skipped[:5]))

    if model['capacitor']:
        print('...Mapped ' + str(len(model['capacitor']))
              + ' LinearShuntCompensator(s) to Capacitor Entries')


# ---------------------------------------------------------------------------
# Line Loading
# ---------------------------------------------------------------------------

def _add_lines(cim):
    seg_cls = getattr(cim, 'ACLineSegment', None)
    if seg_cls is None:
        return

    try:
        segments = _network.list_by_class(seg_cls) or []
        _network.get_all_edges(seg_cls)
    except Exception as e:
        print('WARNING: No ACLineSegment List Available: ' + str(e))
        segments = []

    model.setdefault('overhead_line', {})
    model.setdefault('underground_line', {})
    skipped = []

    for line in segments:
        nm = _name(line)
        terminals = _sorted_terminals(line)
        if len(terminals) < 2:
            skipped.append(nm)
            continue

        from_cn = getattr(terminals[0], 'ConnectivityNode', None)
        to_cn = getattr(terminals[1], 'ConnectivityNode', None)
        from_node = _name(from_cn) if from_cn else None
        to_node = _name(to_cn) if to_cn else None
        if not from_node or not to_node:
            skipped.append(nm)
            continue

        length = line.length if line.length is not None else 0.0
        entry = {
            'from': from_node,
            'to': to_node,
            'phases': _get_phases(line),
            'length': str(length),
        }
        entry.update(_get_line_impedance(line, float(length)))

        if _is_overhead(line, cim):
            model['overhead_line'][nm] = entry
        else:
            model['underground_line'][nm] = entry

    if skipped:
        print('WARNING: Skipped ' + str(len(skipped))
              + ' ACLineSegment(s) Due to Missing Terminals/Nodes. First Few: '
              + ', '.join(skipped[:5]))
    total = len(model['overhead_line']) + len(model['underground_line'])
    if total:
        print('...Mapped ' + str(len(model['overhead_line'])) + ' Overhead and '
              + str(len(model['underground_line'])) + ' Underground Line(s)')


def _phase_index_map(line):
    """Map a line's 1-based PhaseImpedanceData conductor index to a global
    matrix position (A=0, B=1, C=2).

    CIM stores reduced impedance matrices whose rows/columns follow the
    ACLineSegmentPhase.sequenceNumber order, not global ABC order.  A 2-phase
    B/C line, for instance, lists C as conductor 1 and B as conductor 2, so its
    (1,1) entry is the C-C self impedance and belongs at global z[2][2].  Falls
    back to identity (1->A, 2->B, 3->C) when no phase records exist.
    """
    mapping = {}
    for ph in getattr(line, 'ACLineSegmentPhases', None) or []:
        seq = getattr(ph, 'sequenceNumber', None)
        letter = str(getattr(ph, 'phase', '') or '').split('.')[-1].upper()
        gi = {'A': 0, 'B': 1, 'C': 2}.get(letter)
        if seq is None or gi is None:
            continue
        try:
            mapping[int(seq)] = gi
        except (TypeError, ValueError):
            continue
    return mapping or {1: 0, 2: 1, 3: 2}


def _nominal_frequency() -> float:
    """Read BaseFrequency.frequency from the network; default 60 Hz."""
    bf_cls = getattr(_cim, 'BaseFrequency', None) if _cim else None
    if bf_cls is None or _network is None:
        return 60.0
    try:
        for bf in _network.list_by_class(bf_cls) or []:
            f = getattr(bf, 'frequency', None)
            if f:
                return float(f)
    except Exception:
        pass
    return 60.0


def _get_line_impedance(line, length: float) -> dict:
    pli = getattr(line, 'PerLengthImpedance', None)
    if pli is None:
        return {'R': '', 'L': '', 'C': ''}

    twopif = 2 * math.pi * _nominal_frequency()

    def _fmt(grid, fn):
        return '[' + ' '.join(str(fn(grid[r][c])) for r in range(3) for c in range(3)) + ']'

    if _cim and isinstance(pli, getattr(_cim, 'PerLengthPhaseImpedance', type(None))):
        z = [[complex(0, 0)] * 3 for _ in range(3)]
        b = [[0.0] * 3 for _ in range(3)]
        idx = _phase_index_map(line)
        for elem in getattr(pli, 'PhaseImpedanceData', []) or []:
            row = idx.get(getattr(elem, 'row', 1) or 1)
            col = idx.get(getattr(elem, 'column', 1) or 1)
            if row is not None and col is not None:
                r_val = (getattr(elem, 'r', 0.0) or 0.0) * length
                x_val = (getattr(elem, 'x', 0.0) or 0.0) * length
                b_val = (getattr(elem, 'b', 0.0) or 0.0) * length
                z[row][col] = complex(r_val, x_val)
                b[row][col] = b_val
                if row != col:
                    z[col][row] = complex(r_val, x_val)
                    b[col][row] = b_val

        active = sorted(set(idx.values()))  # global indices (0=A,1=B,2=C) of active conductors
        if len(active) != 1:
            # 3-phase: full matrix. 2-phase: Interpreter.py promotes the 5-char phase
            # string (e.g. '"BCN"') to '"ABCN"' and uses type=line with R_matrix, so
            # we still return the 3×3 matrix (zeros fill the absent-phase row/col).
            return {
                'R': _fmt(z, lambda v: v.real),
                'L': _fmt(z, lambda v: v.imag / twopif),
                'C': _fmt(b, lambda v: v / twopif),
            }
        # 1-phase: 4-char phase string (e.g. '"CN"') is NOT promoted by Interpreter.py,
        # so it goes to type=customPI which expects scalar R and L.
        gi = active[0]
        return {
            'R': str(z[gi][gi].real),
            'L': str(z[gi][gi].imag / twopif),
            'C': str(b[gi][gi] / twopif),
        }

    if _cim and isinstance(pli, getattr(_cim, 'PerLengthSequenceImpedance', type(None))):
        r1 = _float(getattr(pli, 'r', None)) * length
        x1 = _float(getattr(pli, 'x', None)) * length
        r0 = _float(getattr(pli, 'r0', None)) * length
        x0 = _float(getattr(pli, 'x0', None)) * length
        b1 = _float(getattr(pli, 'bch', None)) * length
        b0 = _float(getattr(pli, 'b0ch', None)) * length
        z1 = complex(r1, x1)
        z0 = complex(r0, x0)
        z_self = (z0 + 2 * z1) / 3.0
        z_mut  = (z0 - z1) / 3.0
        b_self = (b0 + 2 * b1) / 3.0
        b_mut  = (b0 - b1) / 3.0
        z = [[z_self, z_mut, z_mut],
             [z_mut, z_self, z_mut],
             [z_mut, z_mut, z_self]]
        b = [[b_self, b_mut, b_mut],
             [b_mut, b_self, b_mut],
             [b_mut, b_mut, b_self]]
        return {
            'R': _fmt(z, lambda v: v.real),
            'L': _fmt(z, lambda v: v.imag / twopif),
            'C': _fmt(b, lambda v: v / twopif),
        }

    return {'R': '', 'L': '', 'C': ''}


def _is_overhead(line, cim) -> bool:
    # CIM17 XML from this source does not populate WireInfo on ACLineSegmentPhase
    # or AssetDatasheet on ACLineSegment, so wire-type classification is not
    # available.  Default to overhead (True) for all segments.
    return True


# ---------------------------------------------------------------------------
# Transformer Loading
# ---------------------------------------------------------------------------

def _end_cn(end):
    """First ConnectivityNode name reachable from a transformer end's terminal."""
    for nm in _cn_names(end):
        return nm
    return None


def _float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return 0.0


def _per_unit(ohm, z_base):
    """Convert an ohmic value to per-unit on z_base; '' if either is unknown."""
    if ohm is None or not z_base:
        return ''
    return str(round(_float(ohm) / z_base, 6))


def _winding(kind):
    """Reduce a CIM WindingConnection enum to 'D' (delta) or 'Y' (wye)."""
    s = str(kind or '').split('.')[-1].upper()
    if s.startswith('D'):
        return 'D'
    if s.startswith('Y') or s.startswith('Z'):
        return 'Y'
    return ''


def _connect_type(prim_kind, sec_kind):
    """Map a primary/secondary WindingConnection pair to a GLM connect_type."""
    p, s = _winding(prim_kind), _winding(sec_kind)
    if p == 'D' and s == 'D':
        return 'DELTA_DELTA'
    if p == 'D' and s == 'Y':
        return 'DELTA_GWYE'
    if p == 'Y' and s == 'Y':
        return 'WYE_WYE'
    return ''


def _add_transformers(cim):
    ptx_cls = getattr(cim, 'PowerTransformer', None)
    pte_cls = getattr(cim, 'PowerTransformerEnd', None)
    if ptx_cls is None or pte_cls is None:
        return

    try:
        transformers = _network.list_by_class(ptx_cls) or []
        _network.get_all_edges(ptx_cls)
    except Exception as e:
        print('WARNING: No PowerTransformer List Available: ' + str(e))
        transformers = []

    try:
        ends = _network.list_by_class(pte_cls) or []
        _network.get_all_edges(pte_cls)
    except Exception:
        ends = []

    # Group PowerTransformerEnds by their parent PowerTransformer.
    ends_by_ptx = {}
    for end in ends:
        parent = getattr(end, 'PowerTransformer', None)
        if parent is None:
            continue
        ptx_id = getattr(parent, 'mRID', None) or id(parent)
        ends_by_ptx.setdefault(ptx_id, []).append(end)

    # Per-winding-pair leakage impedance from TransformerMeshImpedance, keyed
    # on the unordered pair of end mRIDs.  PowerTransformerEnd carries r but
    # not x; the reactance lives here.  The impedance is in ohms referred to
    # the FromTransformerEnd, so that end's mRID is retained to pick the base.
    mesh_map = {}  # frozenset({from,to}) -> (r_ohm, x_ohm, from_mrid)
    mesh_cls = getattr(cim, 'TransformerMeshImpedance', None)
    if mesh_cls is not None:
        try:
            _network.get_all_edges(mesh_cls)
            for mi in (_network.list_by_class(mesh_cls) or []):
                fe = getattr(mi, 'FromTransformerEnd', None)
                te = getattr(mi, 'ToTransformerEnd', None)
                if fe is None or te is None:
                    continue
                fmr = getattr(fe, 'mRID', None) or id(fe)
                # ToTransformerEnd has CIM multiplicity 1..* and is exposed as a
                # list; pair the FromTransformerEnd with each ToTransformerEnd.
                to_ends = te if isinstance(te, list) else [te]
                for t in to_ends:
                    if t is None:
                        continue
                    tmr = getattr(t, 'mRID', None) or id(t)
                    mesh_map[frozenset({fmr, tmr})] = (
                        getattr(mi, 'r', None), getattr(mi, 'x', None), fmr)
        except Exception:
            pass

    model.setdefault('transformer', {})
    model.setdefault('transformer_configuration', {})
    skipped = []

    for ptx in transformers:
        nm = _name(ptx)
        ptx_id = getattr(ptx, 'mRID', None) or id(ptx)

        ptx_ends = ends_by_ptx.get(ptx_id, [])
        # Tank-based transformers (regulators, center-tapped) carry their
        # windings on TransformerTankEnd with catalog-derived ratings rather
        # than on PowerTransformerEnd; skip them instead of fabricating data.
        if len(ptx_ends) < 2:
            skipped.append(nm)
            continue

        ptx_ends = sorted(ptx_ends, key=lambda e: int(getattr(e, 'endNumber', 0) or 0))
        if len(ptx_ends) > 2:
            print('WARNING: ' + nm + ' has ' + str(len(ptx_ends))
                  + ' windings; only primary/secondary modeled, tertiary dropped.')
        prim, sec = ptx_ends[0], ptx_ends[1]

        from_node = _end_cn(prim)
        to_node = _end_cn(sec)
        if not from_node or not to_node:
            skipped.append(nm)
            continue

        prim_id = getattr(prim, 'mRID', None) or id(prim)
        sec_id = getattr(sec, 'mRID', None) or id(sec)
        mesh = mesh_map.get(frozenset({prim_id, sec_id}))
        if mesh is not None:
            r_ohm, x_ohm, from_mrid = mesh
            # The mesh impedance is referred to its FromTransformerEnd; use that
            # winding's voltage/power for the per-unit base.
            base_end = sec if from_mrid == sec_id else prim
        else:
            # No mesh record: fall back to per-winding r and x on the primary end.
            r_ohm = getattr(prim, 'r', None)
            x_ohm = getattr(prim, 'x', None)
            base_end = prim

        # GLM transformer_configuration resistance/reactance are per-unit:
        # Z_pu = Z_ohm / Z_base, Z_base = V_rated^2 / S_rated on the referred end.
        base_u = _float(getattr(base_end, 'ratedU', None))
        base_s = _float(getattr(base_end, 'ratedS', None))
        z_base = (base_u ** 2 / base_s) if (base_u and base_s) else 0.0

        config_name = nm + '_cfg'
        conn_type = _connect_type(getattr(prim, 'connectionKind', None),
                                  getattr(sec, 'connectionKind', None))
        prim_voltage = _float(getattr(prim, 'ratedU', None))

        # Convert DELTA_GWYE to an equivalent WYE_WYE by dividing the
        # delta-side (primary) voltage by sqrt(3).
        if conn_type == 'DELTA_GWYE':
            conn_type = 'WYE_WYE'
            if prim_voltage:
                prim_voltage = prim_voltage / math.sqrt(3)

        model['transformer_configuration'][config_name] = {
            'connect_type': conn_type,
            'primary_voltage': str(prim_voltage) if prim_voltage else '',
            'secondary_voltage': str(getattr(sec, 'ratedU', '') or ''),
            'power_rating': str(getattr(prim, 'ratedS', '') or ''),
            'resistance': _per_unit(r_ohm, z_base),
            'reactance': _per_unit(x_ohm, z_base),
        }

        # Phases come from the windings' Terminals (PowerTransformerEnd has no
        # 'phases' field of its own); a genuinely single-phase transformer is
        # labeled per its phase rather than the 3-phase ABCN default.
        letters, has_split = _end_phase_tokens(prim)
        if not letters and not has_split:
            letters, has_split = _end_phase_tokens(sec)
        phases = _glm_phases(letters, has_split) or '"ABCN"'

        model['transformer'][nm] = {
            'from': from_node,
            'to': to_node,
            'phases': phases,
            'configuration': config_name,
        }

    if skipped:
        print('WARNING: Skipped ' + str(len(skipped))
              + ' PowerTransformer(s) Without PowerTransformerEnd Windings'
              + ' (e.g. Tank-Based Regulators/Center-Tapped). First Few: '
              + ', '.join(skipped[:5]))

    if model['transformer']:
        print('...Mapped ' + str(len(model['transformer']))
              + ' PowerTransformer(s) to Transformer Entries')


# ---------------------------------------------------------------------------
# Regulator Loading
# ---------------------------------------------------------------------------

def _reg_connect_type(ptx):
    """GLM connect_type from a PowerTransformer's vectorGroup (e.g. 'Yy')."""
    vg = str(getattr(ptx, 'vectorGroup', '') or '').upper()
    if vg.startswith('DD'):
        return 'DELTA_DELTA'
    if vg.startswith('DY'):
        return 'DELTA_GWYE'
    if vg.startswith('Y'):
        return 'WYE_WYE'
    return ''


def _regulator_config(ptx, tap_changers):
    """Build a GLM regulator_configuration from the tank's RatioTapChanger(s).

    The per-phase tap changers of one regulator share highStep/lowStep/
    stepVoltageIncrement, so the first is representative for the band fields.
    Per-phase tap positions (RatioTapChanger.step) are not emitted: the
    OrderedPhaseCodeKind on each TransformerTankEnd that would map a tank to
    A/B/C is absent from the cim17v40 profile, so the phase->step assignment
    cannot be made without guessing.
    """
    tc = tap_changers[0]
    high = getattr(tc, 'highStep', None)
    low = getattr(tc, 'lowStep', None)
    incr = _float(getattr(tc, 'stepVoltageIncrement', None))

    # GLM raise/lower_taps count steps relative to the neutral position, but CIM
    # highStep/lowStep are absolute indices into the tap range.  They coincide
    # only when neutralStep == 0 (IEEE13); for a range like low=0/neutral=16/
    # high=32 the GLM counts are both 16, so subtract the neutral offset.
    neutral = getattr(tc, 'neutralStep', None)
    n = 0
    try:
        n = int(neutral) if neutral is not None else 0
    except (TypeError, ValueError):
        n = 0

    cfg = {
        'connect_type': _reg_connect_type(ptx),
        'dwell_time': str(_float(getattr(tc, 'initialDelay', None))),
    }
    raise_count = None
    if high is not None:
        raise_count = int(high) - n
        cfg['raise_taps'] = str(raise_count)
    if low is not None:
        cfg['lower_taps'] = str(n - int(low))
    # GLM 'regulation' is the total raise band as a fraction of nominal: a
    # per-step increment of stepVoltageIncrement percent across the raise steps.
    if incr and raise_count is not None:
        cfg['regulation'] = str(round(incr / 100.0 * raise_count, 6))
    return cfg


def _add_regulators(cim):
    rtc_cls = getattr(cim, 'RatioTapChanger', None)
    tte_cls = getattr(cim, 'TransformerTankEnd', None)
    if rtc_cls is None or tte_cls is None:
        return

    try:
        tap_changers = _network.list_by_class(rtc_cls) or []
        _network.get_all_edges(rtc_cls)
    except Exception as e:
        print('WARNING: No RatioTapChanger List Available: ' + str(e))
        return
    if not tap_changers:
        return

    try:
        tank_ends = _network.list_by_class(tte_cls) or []
        _network.get_all_edges(tte_cls)
    except Exception:
        tank_ends = []

    ptx_cls = getattr(cim, 'PowerTransformer', None)
    if ptx_cls is not None:
        try:
            _network.get_all_edges(ptx_cls)
        except Exception:
            pass

    # A regulator's windings live on TransformerTankEnd (one tank per phase),
    # so the per-phase RatioTapChangers all roll up to a single PowerTransformer.
    # Group every tank end and tap changer by that parent transformer; the ones
    # with a tap changer are regulators (vs. plain tank-based/center-tapped
    # transformers, which _add_transformers skips).
    ends_by_ptx = {}   # ptx_id -> [TransformerTankEnd, ...]
    ptx_by_id = {}
    for end in tank_ends:
        tank = getattr(end, 'TransformerTank', None)
        ptx = getattr(tank, 'PowerTransformer', None) if tank else None
        if ptx is None:
            continue
        ptx_id = getattr(ptx, 'mRID', None) or id(ptx)
        ptx_by_id[ptx_id] = ptx
        ends_by_ptx.setdefault(ptx_id, []).append(end)

    tc_by_ptx = {}     # ptx_id -> [RatioTapChanger, ...]
    for tc in tap_changers:
        end = getattr(tc, 'TransformerEnd', None)
        tank = getattr(end, 'TransformerTank', None) if end else None
        ptx = getattr(tank, 'PowerTransformer', None) if tank else None
        if ptx is None:
            continue
        ptx_id = getattr(ptx, 'mRID', None) or id(ptx)
        tc_by_ptx.setdefault(ptx_id, []).append(tc)

    model.setdefault('regulator', {})
    model.setdefault('regulator_configuration', {})
    skipped = []

    for ptx_id, tcs in tc_by_ptx.items():
        ptx = ptx_by_id.get(ptx_id)
        nm = _name(ptx)

        ends = sorted(ends_by_ptx.get(ptx_id, []),
                      key=lambda e: int(getattr(e, 'endNumber', 0) or 0))
        if len(ends) < 2:
            skipped.append(nm)
            continue

        # Every tank shares the same node pair; the lowest endNumber feeds the
        # regulator (from) and the highest is the regulated side (to).
        from_node = _end_cn(ends[0])
        to_node = _end_cn(ends[-1])
        if not from_node or not to_node:
            skipped.append(nm)
            continue

        config_name = nm + '_rcfg'
        model['regulator_configuration'][config_name] = _regulator_config(ptx, tcs)

        # A regulator's windings live on one TransformerTankEnd per phase, so
        # the regulator's phasing is the union across all its tank ends.  A
        # single-phase regulator (one tank) is labeled per its phase rather
        # than the 3-phase ABCN default; add_regulator() in Interpreter.py only
        # splits a regulator per phase when A, B, and C are all present.
        letters, has_split = set(), False
        for e in ends:
            l, s = _end_phase_tokens(e)
            letters |= l
            has_split = has_split or s
        phases = _glm_phases(letters, has_split) or '"ABCN"'

        model['regulator'][nm] = {
            'from': from_node,
            'to': to_node,
            'phases': phases,
            'configuration': config_name,
        }

    if skipped:
        print('WARNING: Skipped ' + str(len(skipped))
              + ' Regulator(s) Due to Missing Tank Ends/Nodes. First Few: '
              + ', '.join(skipped[:5]))

    if model['regulator']:
        print('...Mapped ' + str(len(model['regulator']))
              + ' Regulator(s) to Regulator Entries')


# ---------------------------------------------------------------------------
# Switch Loading
# ---------------------------------------------------------------------------

def _switch_status(sw):
    """Map a CIM switch's open state to a GLM status string ('OPEN'/'CLOSED').

    Prefer the runtime ``open`` flag; fall back to the planning-model
    ``normalOpen`` flag, and default to closed when neither is present.  A
    bare ``False`` for ``open`` (a closed switch) must not trip the fallback,
    so the ``is None`` check distinguishes 'absent' from 'present and false'.
    """
    is_open = getattr(sw, 'open', None)
    if is_open is None:
        is_open = getattr(sw, 'normalOpen', None)
    return 'OPEN' if is_open else 'CLOSED'


def _add_switches(cim):
    base = getattr(cim, 'Switch', None)
    if base is None:
        return

    # Every switching device (Breaker, LoadBreakSwitch, Recloser, Fuse,
    # Sectionaliser, Disconnector, ...) subclasses Switch and is consumed by
    # add_switch() in Interpreter.py through model['switch'].
    switch_classes = [
        cls for _, cls in inspect.getmembers(cim, inspect.isclass)
        if issubclass(cls, base)
    ]

    # Load SwitchPhase edges so single-phase switches expose their phase via
    # _get_phases; absent these, every switch would default to ABCN.
    sp_cls = getattr(cim, 'SwitchPhase', None)
    if sp_cls is not None:
        try:
            _network.get_all_edges(sp_cls)
        except Exception:
            pass

    # The class list includes base classes (Switch, ProtectedSwitch) alongside
    # leaf types, so a single object may surface under more than one
    # list_by_class() call; de-duplicate on mRID.
    switches = []
    seen = set()
    for cls in switch_classes:
        try:
            items = _network.list_by_class(cls) or []
            _network.get_all_edges(cls)
        except Exception:
            continue
        for sw in items:
            sw_id = getattr(sw, 'mRID', None) or id(sw)
            if sw_id in seen:
                continue
            seen.add(sw_id)
            switches.append(sw)

    model.setdefault('switch', {})
    skipped = []

    for sw in switches:
        nm = _name(sw)
        terminals = _sorted_terminals(sw)
        if len(terminals) < 2:
            skipped.append(nm)
            continue

        from_cn = getattr(terminals[0], 'ConnectivityNode', None)
        to_cn = getattr(terminals[1], 'ConnectivityNode', None)
        from_node = _name(from_cn) if from_cn else None
        to_node = _name(to_cn) if to_cn else None
        if not from_node or not to_node:
            skipped.append(nm)
            continue

        model['switch'][nm] = {
            'from': from_node,
            'to': to_node,
            'phases': _get_phases(sw),
            'status': _switch_status(sw),
        }

    if skipped:
        print('WARNING: Skipped ' + str(len(skipped))
              + ' Switch(es) Due to Missing Terminals/Nodes. First Few: '
              + ', '.join(skipped[:5]))

    if model['switch']:
        print('...Mapped ' + str(len(model['switch'])) + ' Switch(es) to Switch Entries')


# ---------------------------------------------------------------------------
# Coordinate CSV Generation
# ---------------------------------------------------------------------------

def _generate_coordinates_csv(cim, source_path):
    """Extract x/y coordinates from CIM Location/PositionPoint data and write
    a Bus,X,Y CSV file that Interpreter.py can consume for node placement.

    Equipment objects (ACLineSegment, Switch, EnergyConsumer, etc.) carry a
    Location reference whose PositionPoints hold the spatial coordinates.
    Terminal sequenceNumber aligns with PositionPoint sequenceNumber, so
    position point 1 maps to the first terminal's ConnectivityNode and
    position point 2 maps to the second terminal's ConnectivityNode.
    """
    global coordinates_csv

    try:
        _network.get_all_edges(cim.Location)
    except Exception:
        pass
    try:
        _network.get_all_edges(cim.PositionPoint)
    except Exception:
        pass

    bus_coords = {}

    base = getattr(cim, 'ConductingEquipment', None)
    if base is None:
        return

    for _, cls in inspect.getmembers(cim, inspect.isclass):
        if not issubclass(cls, base):
            continue
        try:
            items = _network.list_by_class(cls) or []
            _network.get_all_edges(cls)
        except Exception:
            continue

        for eq in items:
            loc = getattr(eq, 'Location', None)
            if loc is None:
                continue
            pts = sorted(
                getattr(loc, 'PositionPoints', None) or [],
                key=lambda p: int(getattr(p, 'sequenceNumber', 0) or 0))
            if not pts:
                continue

            terminals = _sorted_terminals(eq)

            if len(terminals) >= 2 and len(pts) >= 2:
                for idx, term in enumerate(terminals):
                    cn = getattr(term, 'ConnectivityNode', None)
                    if cn is None:
                        continue
                    nm = _name(cn)
                    if nm in bus_coords:
                        continue
                    # The last terminal sits at the end of the polyline, which
                    # may have more vertices than the equipment has terminals.
                    if idx == len(terminals) - 1:
                        pt = pts[-1]
                    else:
                        pt = pts[min(idx, len(pts) - 1)]
                    x = getattr(pt, 'xPosition', None)
                    y = getattr(pt, 'yPosition', None)
                    if x is not None and y is not None:
                        bus_coords[nm] = (x, y)
            else:
                pt = pts[0]
                x = getattr(pt, 'xPosition', None)
                y = getattr(pt, 'yPosition', None)
                if x is None or y is None:
                    continue
                for cn_name in _cn_names(eq):
                    if cn_name not in bus_coords:
                        bus_coords[cn_name] = (x, y)

    if not bus_coords:
        print('WARNING: No coordinate data found in CIM model')
        return

    csv_path = os.path.splitext(source_path)[0] + '_buscoords.csv'
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Bus', 'X', 'Y'])
        for bus in sorted(bus_coords):
            x, y = bus_coords[bus]
            writer.writerow([bus, x, y])

    coordinates_csv = csv_path
    print('...Wrote ' + str(len(bus_coords)) + ' bus coordinate(s) to ' + csv_path)
