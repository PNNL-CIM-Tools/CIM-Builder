import tempfile, shutil, os
import networkx as nx
import xmltodict
import math
import copy
import matplotlib.pyplot as plt
import csv
import pandas as pd
import collections


def Model_edges(g,link_objects):
    model_link_objects=[]
    components=list(g.model.keys())
    for i in range(len(link_objects)):
        if link_objects[i] in components:
            model_link_objects.append(link_objects[i])
    del components, i
    return model_link_objects

def Model_nodes(g,node_objects):
    model_node_objects=[]
    nodes=list(g.model.keys())
    for i in range(len(node_objects)):
        if node_objects[i] in nodes:
            model_node_objects.append(node_objects[i])
    del nodes, i
    return model_node_objects

def add_node(G,g):
    node_names=list(g.model['node'].keys())
    for i in range(len(node_names)):
        nodeinfo={'components':'node','phases':g.model['node'][node_names[i]]['phases'],'voltage':g.model['node'][node_names[i]]['nominal_voltage'],'issource':False}
        if ('bustype' in g.model['node'][node_names[i]]):
            if (g.model['node'][node_names[i]]['bustype']=='SWING'):
                nodeinfo = {'components': 'node', 'phases': g.model['node'][node_names[i]]['phases'],
                            'voltage': g.model['node'][node_names[i]]['voltage_A'],'issource':True}
        G.add_node(node_names[i])
        G.nodes[node_names[i]]['attr']=nodeinfo
    return G

def add_load(G,g):
    load_names=list(g.model['load'].keys())
    for i in range(len(load_names)):
        if 'parent' in list(g.model['load'][load_names[i]].keys()):
            G.add_node(load_names[i])
            parent=g.model['load'][load_names[i]]['parent']
            linkinfo={'phases':g.model['load'][load_names[i]]['phases']}
            #G.add_edge(load_names[i],parent,attr=linkinfo)
            G.add_edge(load_names[i],parent,attr='parent_child')
            loadinfo = {'components':'load','phases': g.model['load'][load_names[i]]['phases'],'parent':parent, 'config': g.model['load'][load_names[i]]}
            G.nodes[load_names[i]]['attr'] = loadinfo
        else:
            # Only pq load considered for now
            G.add_node(load_names[i])
            loadinfo={'components':'load','phases':g.model['load'][load_names[i]]['phases'],'config':g.model['load'][load_names[i]]}
            G.nodes[load_names[i]]['attr']=loadinfo
    return G

def add_capacitor(G,g):
    cap_names=list(g.model['capacitor'].keys())
    for i in range(len(cap_names)):
        if 'parent' in list(g.model['capacitor'][cap_names[i]].keys()):
            G.add_node(cap_names[i])
            parent=g.model['capacitor'][cap_names[i]]['parent']
            G.add_edge(cap_names[i], parent,attr='parent_child')
            capinfo={'components':'capacitor','phases':g.model['capacitor'][cap_names[i]]['phases'],'parent':parent,'config':g.model['capacitor'][cap_names[i]]}
            G.nodes[cap_names[i]]['attr']=capinfo
        else:
            print('Capacitor '+cap_names[i]+' connectivity not found')
    return G

def add_dieseldg(G,g):
    dgnames=list(g.model['diesel_dg'].keys())
    for i in range(len(dgnames)):
        if 'parent' in list(g.model['diesel_dg'][dgnames[i]].keys()):
            G.add_node(dgnames[i])
            # Explicit logic for 9500
            met=g.model['diesel_dg'][dgnames[i]]['parent']
            pnode=g.model['meter'][met]['parent']
            G.add_edge(dgnames[i],pnode,attr='parent_child')
            ph=''
            if 'power_out_A' in g.model['diesel_dg'][dgnames[i]].keys():
                ph=ph+'A'
            if 'power_out_B' in g.model['diesel_dg'][dgnames[i]].keys():
                ph=ph+'B'
            if 'power_out_C' in g.model['diesel_dg'][dgnames[i]].keys():
                ph=ph+'C'
            dginfo={'components':'diesel_dg', 'phases':ph,'parent':pnode,'config':g.model['diesel_dg'][dgnames[i]]}
            G.nodes[dgnames[i]]['attr']=dginfo
    return G

def add_inverter(G,g):
    inv_names=list(g.model['inverter'].keys())
    for i in range(len(inv_names)):
        if 'parent' in list(g.model['inverter'][inv_names[i]].keys()):
            G.add_node(inv_names[i])
            G.add_edge(inv_names[i],g.model['inverter'][inv_names[i]]['parent'],attr='parent_child')
            invinfo={'components':'inverter','phases':g.model['inverter'][inv_names[i]]['phases'],'parent':g.model['inverter'][inv_names[i]]['parent'],'config':g.model['inverter'][inv_names[i]]}
            G.nodes[inv_names[i]]['attr']=invinfo
    return G

def add_overhead_line(G,g,Impedance_dict):
    overhead_line_names=list(g.model['overhead_line'].keys())
    for i in range(len(overhead_line_names)):
        u=g.model['overhead_line'][overhead_line_names[i]]['from']
        v=g.model['overhead_line'][overhead_line_names[i]]['to']
        #lineinfo={'name':overhead_line_names[i],'component':'overhead_line','phases':g.model['overhead_line'][overhead_line_names[i]]['phases'],'length':str(float(g.model['overhead_line'][overhead_line_names[i]]['length'])*0.0003048),'R':'','L':'','C':''}
        line_entry=g.model['overhead_line'][overhead_line_names[i]]  
        lineinfo = {'name': overhead_line_names[i], 'component': 'overhead_line',
                    # 'phases': g.model['overhead_line'][overhead_line_names[i]]['phases'],
                    'phases': line_entry['phases'],
                    'length': '1',
                    # 'R': '', 'L': '', 'C': ''}
                    'R': line_entry.get('R', ''), 'L': line_entry.get('L', ''), 'C': line_entry.get('C', '')}
        if(len(lineinfo['phases'])<6 and len(lineinfo['phases'])>4):
            G.nodes[u]['attr']['phases']='"ABCN"'
            G.nodes[v]['attr']['phases'] = '"ABCN"'
            lineinfo['phases']='"ABCN"'

        
        if Impedance_dict is not None:
            lineinfo=update_line_parameters(lineinfo,Impedance_dict)
        G.add_edge(u,v,attr=lineinfo)
    return G

def add_underground_line(G,g,Impedance_dict):
    underground_line_names=list(g.model['underground_line'].keys())
    for i in range(len(underground_line_names)):
        u=g.model['underground_line'][underground_line_names[i]]['from']
        v=g.model['underground_line'][underground_line_names[i]]['to']
        #lineinfo={'name':underground_line_names[i],'component':'underground_line','phases':g.model['underground_line'][underground_line_names[i]]['phases'],'length':str(float(g.model['underground_line'][underground_line_names[i]]['length'])*0.0003048),'R':'','L':'','C':''}
        line_entry=g.model['underground_line'][underground_line_names[i]]
        lineinfo = {'name': underground_line_names[i], 'component': 'underground_line',
                    # 'phases': g.model['underground_line'][underground_line_names[i]]['phases'],
                    'phases': line_entry['phases'],
                    'length': '1',
                    # 'R': '', 'L': '', 'C': ''}
                    'R': line_entry.get('R', ''), 'L': line_entry.get('L', ''), 'C': line_entry.get('C', '')}
        if (len(lineinfo['phases']) < 6 and len(lineinfo['phases']) > 4):
            G.nodes[u]['attr']['phases'] = '"ABCN"'
            G.nodes[v]['attr']['phases'] = '"ABCN"'
            lineinfo['phases'] = '"ABCN"'
            
        if Impedance_dict is not None:
            lineinfo = update_ugline_parameters(lineinfo, Impedance_dict)
        G.add_edge(u,v,attr=lineinfo)
    return G

def add_regulator(G,g):
    regulator_names=list(g.model['regulator'].keys())
    for i in range(len(regulator_names)):
        u=g.model['regulator'][regulator_names[i]]['from']
        v=g.model['regulator'][regulator_names[i]]['to']
        config_name=g.model['regulator'][regulator_names[i]]['configuration']
        config=g.model['regulator_configuration'][config_name]
        reginfo={'name':regulator_names[i],'component':'regulator','phases':g.model['regulator'][regulator_names[i]]['phases'],'config':config,'Vbase_prim':G.nodes[u]['attr']['voltage'],'Vbase_sec':G.nodes[v]['attr']['voltage'],}

        G.add_edge(u,v,attr=reginfo)
    return G

def add_switch(G,g):
    switch_names=list(g.model['switch'].keys())
    for i in range(len(switch_names)):
        u=g.model['switch'][switch_names[i]]['from']
        v = g.model['switch'][switch_names[i]]['to']
        switchinfo={'name':switch_names[i],'component':'switch','phases':g.model['switch'][switch_names[i]]['phases'],'status':g.model['switch'][switch_names[i]]['status']}
        G.add_edge(u,v,attr=switchinfo)
    return G

def add_transformer(G,g):
    transformer_names=list(g.model['transformer'].keys())
    for i in range(len(transformer_names)):
        u = g.model['transformer'][transformer_names[i]]['from']
        v = g.model['transformer'][transformer_names[i]]['to']
        config_name=g.model['transformer'][transformer_names[i]]['configuration']
        config=g.model['transformer_configuration'][config_name]
        transformerinfo={'name':transformer_names[i],'component':'transformer','phases':g.model['transformer'][transformer_names[i]]['phases'],'config':config}
        G.add_edge(u,v,attr=transformerinfo)
    return G

def update_line_parameters(lineinfo,Impedance_dict):
    if '"' in lineinfo['name']:
        nn=lineinfo['name'].replace('"','')
    else:
        nn=lineinfo['name']
    for i in Impedance_dict['gridlabd']['overhead_line']:
        if nn==i['name']:

            twopif=2*math.pi*60.0
            z11 = complex(i['b_matrix']['b11'])
            z12 = complex(i['b_matrix']['b12'])
            z13 = complex(i['b_matrix']['b13'])
            z21 = complex(i['b_matrix']['b21'])
            z22 = complex(i['b_matrix']['b22'])
            z23 = complex(i['b_matrix']['b23'])
            z31 = complex(i['b_matrix']['b31'])
            z32 = complex(i['b_matrix']['b32'])
            z33 = complex(i['b_matrix']['b33'])

            if(z11.real==0 and z11.imag==0):
                z11 = complex(100000,100000)
                z12 = complex(100000, 100000)
                z13 = complex(100000, 100000)
                z21 = complex(100000, 100000)
                z31 = complex(100000, 100000)
            if (z22.real == 0 and z22.imag == 0):
                z21 = complex(100000, 100000)
                z22 = complex(100000, 100000)
                z23 = complex(100000, 100000)
                z12 = complex(100000, 100000)
                z32 = complex(100000, 100000)
            if (z33.real == 0 and z33.imag == 0):
                z31 = complex(100000, 100000)
                z32 = complex(100000, 100000)
                z33 = complex(100000, 100000)
                z13 = complex(100000, 100000)
                z23 = complex(100000, 100000)

            if(lineinfo['phases']=='"ABCN"' or lineinfo['phases']=='ABCN'):

                R11 = '['+str(z11.real)+' '
                R12 = str(z12.real)+' '
                R13 = str(z13.real)+' '
                R21 = str(z21.real)+' '
                R22 = str(z22.real)+' '
                R23 = str(z23.real)+' '
                R31 = str(z31.real)+' '
                R32 = str(z32.real)+' '
                R33 = str(z33.real)+']'

                R=''.join([R11,R12,R13,R21,R22,R23,R31,R32,R33])

                lineinfo['R']=R

                L11 = '[' + str(z11.imag/twopif) + ' '
                L12 = str(z12.imag/twopif) + ' '
                L13 = str(z13.imag/twopif) + ' '
                L21 = str(z21.imag/twopif) + ' '
                L22 = str(z22.imag/twopif) + ' '
                L23 = str(z23.imag/twopif) + ' '
                L31 = str(z31.imag/twopif) + ' '
                L32 = str(z32.imag/twopif) + ' '
                L33 = str(z33.imag/twopif) + ']'

                L = ''.join([L11, L12, L13, L21, L22, L23, L31, L32, L33])

                lineinfo['L'] = L

                lineinfo['C']='[1.0383e-08 -3.2895e-09 -2.07596e-09 -3.28956e-09 9.82303e-09 -1.2225e-09 -2.0759e-09 -1.2225e-09 9.2937e-09]'
            else:
                if('A' in lineinfo['phases']):
                    lineinfo['R']=str(z11.real)
                    lineinfo['L']=str(z11.imag/twopif)
                    lineinfo['C']='0.77e-8'
                if ('B' in lineinfo['phases']):
                    lineinfo['R'] = str(z22.real)
                    lineinfo['L'] = str(z22.imag / twopif)
                    lineinfo['C'] = '0.77e-8'
                if ('C' in lineinfo['phases']):
                    lineinfo['R'] = str(z33.real)
                    lineinfo['L'] = str(z33.imag / twopif)
                    lineinfo['C'] = '0.77e-8'
    return lineinfo


def update_ugline_parameters(lineinfo,Impedance_dict):
    if '"' in lineinfo['name']:
        nn=lineinfo['name'].replace('"','')
    else:
        nn=lineinfo['name']
    for i in Impedance_dict['gridlabd']['underground_line']:
        if nn==i['name']:

            twopif=2*math.pi*60.0
            z11 = complex(i['b_matrix']['b11'])
            z12 = complex(i['b_matrix']['b12'])
            z13 = complex(i['b_matrix']['b13'])
            z21 = complex(i['b_matrix']['b21'])
            z22 = complex(i['b_matrix']['b22'])
            z23 = complex(i['b_matrix']['b23'])
            z31 = complex(i['b_matrix']['b31'])
            z32 = complex(i['b_matrix']['b32'])
            z33 = complex(i['b_matrix']['b33'])

            if(z11.real==0 and z11.imag==0):
                z11 = complex(100000,100000)
                z12 = complex(100000, 100000)
                z13 = complex(100000, 100000)
                z21 = complex(100000, 100000)
                z31 = complex(100000, 100000)
            if (z22.real == 0 and z22.imag == 0):
                z21 = complex(100000, 100000)
                z22 = complex(100000, 100000)
                z23 = complex(100000, 100000)
                z12 = complex(100000, 100000)
                z32 = complex(100000, 100000)
            if (z33.real == 0 and z33.imag == 0):
                z31 = complex(100000, 100000)
                z32 = complex(100000, 100000)
                z33 = complex(100000, 100000)
                z13 = complex(100000, 100000)
                z23 = complex(100000, 100000)

            if(lineinfo['phases']=='"ABCN"' or lineinfo['phases']=='ABCN'):

                R11 = '['+str(z11.real)+' '
                R12 = str(z12.real)+' '
                R13 = str(z13.real)+' '
                R21 = str(z21.real)+' '
                R22 = str(z22.real)+' '
                R23 = str(z23.real)+' '
                R31 = str(z31.real)+' '
                R32 = str(z32.real)+' '
                R33 = str(z33.real)+']'

                R=''.join([R11,R12,R13,R21,R22,R23,R31,R32,R33])

                lineinfo['R']=R

                L11 = '[' + str(z11.imag/twopif) + ' '
                L12 = str(z12.imag/twopif) + ' '
                L13 = str(z13.imag/twopif) + ' '
                L21 = str(z21.imag/twopif) + ' '
                L22 = str(z22.imag/twopif) + ' '
                L23 = str(z23.imag/twopif) + ' '
                L31 = str(z31.imag/twopif) + ' '
                L32 = str(z32.imag/twopif) + ' '
                L33 = str(z33.imag/twopif) + ']'

                L = ''.join([L11, L12, L13, L21, L22, L23, L31, L32, L33])

                lineinfo['L'] = L

                lineinfo['C']='[1.0383e-08 -3.2895e-09 -2.07596e-09 -3.28956e-09 9.82303e-09 -1.2225e-09 -2.0759e-09 -1.2225e-09 9.2937e-09]'
            else:
                if('A' in lineinfo['phases']):
                    lineinfo['R']=str(z11.real)
                    lineinfo['L']=str(z11.imag/twopif)
                    lineinfo['C']='0.77e-8'
                if ('B' in lineinfo['phases']):
                    lineinfo['R'] = str(z22.real)
                    lineinfo['L'] = str(z22.imag / twopif)
                    lineinfo['C'] = '0.77e-8'
                if ('C' in lineinfo['phases']):
                    lineinfo['R'] = str(z33.real)
                    lineinfo['L'] = str(z33.imag / twopif)
                    lineinfo['C'] = '0.77e-8'
    return lineinfo



def delta_basevolt_ll(config):
    """Line-to-line voltage base in volts for a delta load.  nominal_voltage is
    line-to-neutral in both GLM and CIM, so L-L base = nominal * sqrt(3).
    Returns None if nominal_voltage is missing or zero."""
    if ('nominal_voltage' not in config):
        return None
    vll = abs(complex(config['nominal_voltage'])) * 1.73205080757
    if (vll == 0):
        return None
    return round(vll, 6)


def delta_config_to_phase_powers(config, vll):
    """Map a delta-connected load's legs onto per-phase powers in MW/Mvar.
    Each leg keeps its power on its primary phase (AB on A, BC on B, CA on C)
    and phases without a leg get the 1e-9 MW placeholder.  Constant impedance
    legs convert to PQ using the line-to-line voltage, and constant current legs
    convert at the nominal leg voltage phasor (flat-start approximation)."""
    leg_angle = {'A': math.radians(30.0), 'B': math.radians(-90.0), 'C': math.radians(150.0)}
    P = {}
    Q = {}
    for ph in 'ABC':
        S = complex(0)
        if ('constant_power_' + ph in config):
            S = S + complex(config['constant_power_' + ph])
        if ('constant_impedance_' + ph in config):
            Z = complex(config['constant_impedance_' + ph])
            S = S + vll * vll / Z.conjugate()
        if ('constant_current_' + ph in config):
            I = complex(config['constant_current_' + ph])
            V = vll * complex(math.cos(leg_angle[ph]), math.sin(leg_angle[ph]))
            S = S + V * I.conjugate()
        if (S == 0):
            P[ph] = 1e-9
            Q[ph] = 0.0
        else:
            P[ph] = S.real / 1000000
            Q[ph] = S.imag / 1000000
    return P, Q


def delta_load_entry(G, i, busname):
    """Build a wye-equivalent customLoad3 netlist entry for a 3-leg delta load."""
    config = G.nodes[i]['attr']['config']
    vll = delta_basevolt_ll(config)
    if (vll is None):
        return None
    converted = False
    for ph in 'ABC':
        if ('constant_power_' + ph in config or 'constant_impedance_' + ph in config or 'constant_current_' + ph in config):
            converted = True
    if (not converted):
        return None
    Pd, Qd = delta_config_to_phase_powers(config, vll)
    if ('constant_impedance_A' in config or 'constant_impedance_B' in config or 'constant_impedance_C' in config):
        print('Impedance Load ' + i + ' converter to PQ')
    if ('constant_current_A' in config or 'constant_current_B' in config or 'constant_current_C' in config):
        print('Current Load ' + i + ' converted to PQ at nominal voltage')
    print('Delta load ' + i + ' stored as wye-equivalent customLoad3')
    n = i.replace('"', '')
    n = n.replace('-', '_')
    Entry = 'type=customLoad3, name=' + n + '_DtoY, bus=' + busname + ', Pa=' + str(Pd['A']) + ', Qa=' + str(Qd['A']) + ', Pb=' + str(Pd['B']) + ', Qb=' + str(Qd['B'])
    Entry = Entry + ', Pc=' + str(Pd['C']) + ', Qc=' + str(Qd['C']) + ', freq=60, Vbase=' + str(vll / 1000) + ', hypersim_type=PQ_threeph_wye, hypersim_lib=PNNL Loads.clf, x='
    Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 30))
    return Entry


def delta_load2_entries(G, i, busname, count):
    """Build netlist entries for partial delta load legs as customLoad2 components.
    Each leg gets individual 1-phase MUXes and a phase-to-phase customLoad2.
    Returns (entries, new_count) or (None, count) if conversion fails."""
    config = G.nodes[i]['attr']['config']
    vll = delta_basevolt_ll(config)
    if (vll is None):
        return None, count
    legs = ''
    for ph in 'ABC':
        if ('constant_power_' + ph in config or 'constant_impedance_' + ph in config or 'constant_current_' + ph in config):
            legs = legs + ph
    if (not legs):
        return None, count
    Pd, Qd = delta_config_to_phase_powers(config, vll)
    vln = round(vll / 1.73205080757, 6)
    n = i.replace('"', '')
    n = n.replace('-', '_')
    x = round(float(G.nodes[i]['attr']['x']))
    y = round(float(G.nodes[i]['attr']['y']))
    legpairs = {'A': ('A', 'B'), 'B': ('B', 'C'), 'C': ('C', 'A')}
    legbuses = {}
    entries = []
    for lp in legs:
        if ('constant_impedance_' + lp in config):
            print('Impedance Load ' + i + ' converter to PQ')
        if ('constant_current_' + lp in config):
            print('Current Load ' + i + ' converted to PQ at nominal voltage')
        for legph in legpairs[lp]:
            if (legph in legbuses):
                continue
            conn = n + 'bo' + legph
            legbuses[legph] = conn
            xo = x + 30 * len(legbuses)
            Entry = 'type=bus, name=' + conn + ', baseVolt=' + str(vln) + ', nb_phases=1, lf_type=PV, '
            Entry = Entry + 'x=' + str(xo) + ', y=' + str(y - 30)
            entries.append(Entry)
            Entry = 'type=customMUX' + legph.lower() + ', name=MUX' + legph.lower() + str(count) + ', bus=' + busname
            Entry = Entry + ', ph' + legph + '=' + conn + ', Vbase=' + str(vll / 1000)
            Entry = Entry + ', hypersim_type=bus2' + legph.lower() + ', hypersim_lib=PNNL Loads.clf, x=' + str(xo) + ', y=' + str(y - 50)
            count = count + 1
            entries.append(Entry)
        ph1, ph2 = legpairs[lp]
        print('Delta load ' + i + ' stored as customLoad2 across phases ' + ph1 + ph2)
        Entry = 'type=customLoad2, name=' + n + '_2ph_' + ph1 + ph2 + ', net_T1=' + legbuses[ph1] + ', net_T3=' + legbuses[ph2]
        Entry = Entry + ', P=' + str(Pd[lp]) + ', Q=' + str(Qd[lp])
        Entry = Entry + ', Vbase=' + str(vln / 1000) + ', Frequency=60, hypersim_type=PQsinglephase2p_solved, hypersim_lib=PNNL Loads.clf, x='
        Entry = Entry + str(x) + ', y=' + str(y - 70)
        entries.append(Entry)
    return entries, count


def _select_adapter(input_path):
    """Pick the parser module based on the input file extension."""
    ext = os.path.splitext(input_path)[1].lower()
    if ext == '.glm':
        import glmanip as adapter
        return adapter, 'glm'
    if ext in ('.xml', '.cim'):
        import cim_adapter as adapter
        return adapter, 'cim'
    raise ValueError(
        "Unsupported input file type '" + ext + "' (expected .glm, .xml, or .cim)"
    )


def _discover_input(input_path=None):
    """Resolve an input file. If none is given, scan ./input/ for the first
    supported source file."""
    if input_path:
        return input_path
    input_dir = os.path.join(os.getcwd(), 'input')
    if not os.path.exists(input_dir):
        raise FileNotFoundError('Input files not found: ./input directory missing')
    for fn in sorted(os.listdir(input_dir)):
        if fn.lower().endswith(('.glm', '.xml', '.cim')):
            return os.path.join(input_dir, fn)
    raise FileNotFoundError('No .glm/.xml/.cim file found in ./input')


def _load_impedance_dict(source_path):
    """Load Impedance.xml sitting alongside the GLM source. GLM path only."""
    impedance_path = os.path.join(os.path.dirname(source_path), 'Impedance.xml')
    with open(impedance_path, 'r', encoding='utf-8') as fh:
        return xmltodict.parse(fh.read())


def _find_buscoords_csv(source_path):
    """Search for a Bus,X,Y coordinates CSV in the input directory."""
    input_dir = os.path.dirname(source_path) or '.'
    for fn in sorted(os.listdir(input_dir)):
        if not fn.lower().endswith('.csv') or fn.lower().endswith('_buscoords.csv'):
            continue
        path = os.path.join(input_dir, fn)
        try:
            with open(path, 'r') as fh:
                header = fh.readline().strip()
            if header == 'Bus,X,Y':
                print('...Found bus coordinates file: ' + path)
                return path
        except OSError:
            continue
    return None


def main(input_path=None):
    source = _discover_input(input_path)
    g, kind = _select_adapter(source)
    if hasattr(g, 'reset'):
        g.reset()
    print('Interpreting input file ' + os.path.basename(source))
    g.ingest(source)

    if kind == 'glm':
        Impedance_dict = _load_impedance_dict(source)
        Buscoordsfile = _find_buscoords_csv(source)
    else:
        Impedance_dict = None
        Buscoordsfile = getattr(g, 'coordinates_csv', None)


    ## Start interpreting all model parameters

    library_objects=['emissions','line_configuration','line_spacing','overhead_line_conductor','power_metrics','regulator_configuration','restoration','transformer_configuration','triplex_line_configuration','underground_line_conductor','billdump','currdump','voltdump']

    link_objects=['fuse','overhead_line','triplex_line','underground_line','regulator','relay','series_reactor','switch','recloser','sectionalizer','transformer']

    node_objects=['node','capacitor','load','pqload','meter','substation','triplex_node','triplex_meter','diesel_dg','inverter'] # need to handle inverters

    a=0

    # Parse link objects to check 3-ph and unbalanced connections

    model_link_objects=Model_edges(g,link_objects)
    model_node_objects=Model_nodes(g,node_objects)

    G=nx.Graph()


    # Add node attributes to Graph

    for i in model_node_objects:
        node_class=i
        if node_class=='node':
            add_node(G,g)
        elif node_class=='load':
            add_load(G,g)
        elif node_class=='capacitor':
            add_capacitor(G,g)
        elif node_class=='diesel_dg':
            add_dieseldg(G,g)
        elif node_class=='inverter':
            add_inverter(G,g)
        else:
            if (node_class!='triplex_meter' or node_class!='meter'):
                print('Component '+node_class+': Not currently supported by converter. Please contact Rohit Jinsiwale - rohit.jinsiwale@pnnl.gov for assistance')

    # Add connectivity based on
    for i in model_link_objects:
        # Select link class and parse connectivity
        component_class=i
        if component_class=='overhead_line':
            add_overhead_line(G,g,Impedance_dict)
        elif component_class=='underground_line':
            add_underground_line(G,g,Impedance_dict)
        elif component_class=='regulator':
            add_regulator(G,g)
        elif component_class=='switch':
            add_switch(G,g)
        elif component_class=='transformer':
            add_transformer(G,g)
        #elif component_class
        else:
            print('Component '+component_class+': Not currently supported by converter. Please contact Rohit Jinsiwale - rohit.jinsiwale@pnnl.gov for assistance')


    # Identify phase changes in graph to identify need for muxes for specific segments

    GraphNodeList=list(G.nodes())
    Mux_debug=[]
    for i in GraphNodeList:
        connected_edges=list(G.edges(i))
        nodephase=G.nodes[i]['attr']['phases']
        nodephase=nodephase.replace('N','')
        nodephase = nodephase.replace('D', '')
        nodephase = nodephase.replace('"', '')
        nodephase=''.join(sorted(nodephase))

        mux_edge_dict=[]
        breakout_number=1
        for j in range(len(connected_edges)):
            u = connected_edges[j][0]
            v = connected_edges[j][1]
            if (G[u][v]['attr']!='parent_child'):
                ph=G[u][v]['attr']['phases']

                ph = ph.replace('N', '')
                ph = ph.replace('"','')
                ph = ''.join(sorted(ph))

                if(ph!=nodephase):

                    mux_edge_dict.append({'node1':u,'node2':v,'nodephase':nodephase,'edgephase':ph})
                    Mux_debug.append(mux_edge_dict)
                    umod=u+'_'+ph+'_'+str(breakout_number)
                    breakout_number=breakout_number+1
                    att=G[u][v]['attr']

                    nodeatt=copy.deepcopy(G.nodes[u]['attr'])
                    nodeatt['phases']=G[u][v]['attr']['phases']
                    G.add_node(umod)
                    G.nodes[umod]['attr'] = nodeatt
                    G.add_edge(u, umod, attr='mux_'+nodephase+'_to_'+ph)
                    G.remove_edge(u,v)
                    G.add_edge(umod,v,attr=att)





        #print(mux_edge_dict)

    # Handle the regulators
    Edges=list(G.edges(data=True))
    Edgelist=copy.deepcopy(Edges)
    for i in Edgelist:
        if('component' in list(i[2]['attr'])):
            if(i[2]['attr']['component']=='regulator'):
                ph=i[2]['attr']['phases']
                if('A' in ph and 'B' in ph and 'C' in ph):
                    # 3-phase regulator
                    u=i[0]
                    v=i[1]
                    att=copy.deepcopy(G[u][v]['attr'])
                    att_a = copy.deepcopy(att)
                    att_a['phases']='"AN"'
                    att_b = copy.deepcopy(att)
                    att_b['phases'] = '"BN"'
                    att_c = copy.deepcopy(att)
                    att_c['phases'] = '"CN"'

                    nodeattu = G.nodes[u]['attr']
                    nodeattv = G.nodes[v]['attr']
                    nodeattu_a = copy.deepcopy(nodeattu)
                    nodeattu_b = copy.deepcopy(nodeattu)
                    nodeattu_c = copy.deepcopy(nodeattu)
                    nodeattu_a['phases'] = '"AN"'
                    nodeattu_b['phases'] = '"BN"'
                    nodeattu_c['phases'] = '"CN"'

                    nodeattv_a = copy.deepcopy(nodeattv)
                    nodeattv_b = copy.deepcopy(nodeattv)
                    nodeattv_c = copy.deepcopy(nodeattv)
                    nodeattv_a['phases'] = '"AN"'
                    nodeattv_b['phases'] = '"BN"'
                    nodeattv_c['phases'] = '"CN"'

                    umod1=u+'_phase_a_reg'
                    umod2 = u + '_phase_b_reg'
                    umod3 = u + '_phase_c_reg'

                    vmod1 = v + '_phase_a_reg'
                    vmod2 = v + '_phase_b_reg'
                    vmod3 = v + '_phase_c_reg'

                    G.add_node(umod1)
                    G.nodes[umod1]['attr'] = nodeattu_a
                    G.add_node(umod2)
                    G.nodes[umod2]['attr'] = nodeattu_b
                    G.add_node(umod3)
                    G.nodes[umod3]['attr'] = nodeattu_c

                    G.add_node(vmod1)
                    G.nodes[vmod1]['attr'] = nodeattv_a
                    G.add_node(vmod2)
                    G.nodes[vmod2]['attr'] = nodeattv_b
                    G.add_node(vmod3)
                    G.nodes[vmod3]['attr'] = nodeattv_c

                    G.add_edge(umod1,vmod1,attr =att_a)
                    G.add_edge(umod2, vmod2, attr=att_b)
                    G.add_edge(umod3, vmod3, attr=att_c)

                    G.remove_edge(u, v)
                    G.add_edge(u, umod1, attr='mux_"ABC"_to_"A"')
                    G.add_edge(u, umod2, attr='mux_"ABC"_to_"B"')
                    G.add_edge(u, umod3, attr='mux_"ABC"_to_"C"')

                    G.add_edge(v, vmod1, attr='mux_"ABC"_to_"A"')
                    G.add_edge(v, vmod2, attr='mux_"ABC"_to_"B"')
                    G.add_edge(v, vmod3, attr='mux_"ABC"_to_"C"')

    #nx.draw(G, with_labels = False) # turn to true for small networks
    #plt.show()

    # Assign missing coordinates for nodes/edges

    if Buscoordsfile and os.path.isfile(Buscoordsfile):
        Coords=pd.read_csv(Buscoordsfile).to_dict('records')
        Allnodes=dict(G.nodes())
        Coordnotfound=[]
        AssignedXY=[]
        Coordfound=[]
        Coordfoundx=[]
        Coordfoundy=[]

        for i in Allnodes:
            name=i
            if('"' in name):
                name=name.replace('"','')
            found=0
            for j in range(len(Coords)):
                if name.lower()==Coords[j]['Bus'].lower():
                    found=1
                    G.nodes[i]['attr']['x'] = Coords[j]['X']
                    G.nodes[i]['attr']['y'] = Coords[j]['Y']
                    AssignedXY.append((Coords[j]['X'],Coords[j]['Y']))
            if(found==0):
                Coordnotfound.append(i)

        # Extrapolate coordinates for missing nodes based on connectivity

        # If the orphan node is connected to just one node use the adjacent one's x+60,y+60
        Corrected=[]
        for i in range(len(Coordnotfound)):
            # Check if the node got updated in this process
            if ('x' in G.nodes[Coordnotfound[i]]['attr']):
                pass
            else:

                neighbors=list(G.adj[Coordnotfound[i]])
                if(len(neighbors)==1 and 'x' in G.nodes[neighbors[0]]['attr']):
                    x = float(G.nodes[neighbors[0]]['attr']['x'])
                    y = float(G.nodes[neighbors[0]]['attr']['y']) + 60

                    if ((x,y) in AssignedXY):
                        set=0
                        for k in range(4):
                            if(set<1):
                                x=x+60
                                if((x,y) in AssignedXY):
                                    a=0
                                else:
                                    set=1
                        if(set==0):
                            print('Please manually enter coordinates for '+Coordnotfound[i])
                        else:
                            G.nodes[Coordnotfound[i]]['attr']['x'] = str(x)
                            G.nodes[Coordnotfound[i]]['attr']['y'] = str(y)
                            Corrected.append(Coordnotfound[i])
                            AssignedXY.append((x,y))
                    else:
                        G.nodes[Coordnotfound[i]]['attr']['x'] = str(x)
                        G.nodes[Coordnotfound[i]]['attr']['y'] = str(y)
                        Corrected.append(Coordnotfound[i])
                        AssignedXY.append((x,y))

                if(len(neighbors)>1):
                    count=0
                    iter=0
                    candidates=[]
                    while (count<2 and iter<len(neighbors)):

                        if('x' in G.nodes[neighbors[iter]]['attr']):
                            candidates.append(neighbors[iter])
                            count=count+1
                        iter=iter+1
                    if(count==2):
                        x1=float(G.nodes[candidates[0]]['attr']['x'])
                        x2 = float(G.nodes[candidates[1]]['attr']['x'])
                        y1 = float(G.nodes[candidates[0]]['attr']['y'])
                        y2 = float(G.nodes[candidates[1]]['attr']['y'])

                        x = 0.5 * abs(x1 - x2) + min(x1, x2)
                        y = 0.5 * abs(y1 - y2) + min(y1, y2)

                        if ((x, y) in AssignedXY):
                            print('Please manually enter coordinates for ' + Coordnotfound[i])
                        else:


                            G.nodes[Coordnotfound[i]]['attr']['x'] = str(x)
                            G.nodes[Coordnotfound[i]]['attr']['y'] = str(y)
                            Corrected.append(Coordnotfound[i])
                            AssignedXY.append((x,y))
                    if(count==1):
                        # If the orphan node is connected to one node with xy but no other connected node has xy start charting a path to the
                        # node with xy and memorize path
                        # then divide the line length by factions and assign the xy
                        Path=[]
                        Path.append(Coordnotfound[i])
                        # Find next node without xy
                        startnode=Coordnotfound[i]
                        found=0
                        step=0
                        x1 = float(G.nodes[candidates[0]]['attr']['x'])
                        y1 = float(G.nodes[candidates[0]]['attr']['y'])
                        while found < 1:
                            if ('x' in G.nodes[neighbors[step]]['attr']):


                                pass
                            else:
                                found = 1
                                nextnode = neighbors[step]
                            step = step + 1
                        Path.append(nextnode)
                        foundall=0
                        while foundall<1:
                            found=0
                            step=0
                            neighborsCurr=list(G.adj[nextnode])
                            while found<1 and step<len(neighborsCurr):
                                if ('x' in G.nodes[neighborsCurr[step]]['attr']):
                                    foundall=1
                                    found=1
                                    endnode=neighborsCurr[step]
                                    x2 = float(G.nodes[endnode]['attr']['x'])
                                    y2 = float(G.nodes[endnode]['attr']['y'])

                                step=step+1
                            if found==0:
                            # No neightbors with xy found
                            # choose one not in the path currently
                                possiblenextnode=0
                                step=0
                                while possiblenextnode<1:
                                    if neighborsCurr[step] in Path:
                                        pass
                                    else:
                                        nextnode=neighborsCurr[step]
                                        possiblenextnode=1
                                    step=step+1

                                Path.append(nextnode)



                        # Use the path with final xy coordinates to chart coordinates for all path nodes
                        split=len(Path)+1

                        diffx=(x2-x1)/split
                        diffy=(y2-y1)/split
                        for k in range(len(Path)):
                            x=x1+(k+1)*diffx
                            y=y1+(k+1)*diffy
                            if ((x, y) in AssignedXY):
                                y=y+25
                                G.nodes[Path[k]]['attr']['x'] = str(x)
                                G.nodes[Path[k]]['attr']['y'] = str(y)
                                Corrected.append(Path[k])
                                AssignedXY.append((x, y))
                            else:
                                G.nodes[Path[k]]['attr']['x'] = str(x)
                                G.nodes[Path[k]]['attr']['y'] = str(y)
                                Corrected.append(Path[k])
                                AssignedXY.append((x, y))


        for i in Corrected:
            Coordnotfound.remove(i)
        if (len(Coordnotfound)>0):
            print('Please enter coordinates for ')
            print(Coordnotfound)

    for node in G.nodes():
        G.nodes[node]['attr'].setdefault('x', 0)
        G.nodes[node]['attr'].setdefault('y', 0)

    # Check for spacing between nodes and if there are overlaps
    '''
    Allnodes=list(G.nodes(data=True))
    liststore=[]
    liststorexy=[]
    for i in range(len(Allnodes)):
        liststore.append({Allnodes[i][0], Allnodes[i][1]['attr']['x'], Allnodes[i][1]['attr']['y']})
        liststorexy.append((Allnodes[i][1]['attr']['x'],Allnodes[i][1]['attr']['y']))

    # First checking for overlap

    frequency_xy=collections.Counter(liststorexy)
    for i in frequency_xy:
        if frequency_xy[i] >1:
            # Find instances and try incrementing y by 60 until unique value is found
            for j in range(len(liststorexy)):
                if (float(liststorexy[j][0]),float(liststorexy[j][1]))==(float(i[0]),float(i[1])):
                    tup=(float(liststorexy[j][0]),float(liststorexy[j][1])+60)
                    check=0
                    while (check<1 and frequency_xy[i]>1):
                        if tup in liststorexy:
                            tup=(tup[0],tup[1]+60)
                        else:
                            liststorexy[j]=tup
                            frequency_xy[i]=frequency_xy[i]-1
                            check=1

    # Now get the deltax and deltay
    dx=100
    dy=100
    for i in range(len(liststorexy)):
        x=liststorexy[i][0]
        y=liststorexy[i][1]
        for j in range(len(liststorexy)):
            deltax=abs(float(x)-float(liststorexy[j][0]))
            deltay=abs(float(y)-float(liststorexy[j][1]))
            if(deltax>0 and deltax<dx):
                dx=deltax
            if (deltay > 0 and deltay < dy):
                dy = deltay
    '''
    # Now take the smaller of the 2 and scale all distances by the scaling factor
    # Still need to finish the spacing logic

    # We need to account for parent child shunt elements here
    # Graph modification is required to just modify the load to be at the main node
    # St



    # Populate netlist with nodes first

    Netlist=[]
    count=0
    Nodes_added=0
    Loads_added=0
    Capacitors_added=0
    Inverters_added=0
    DG_Added=0

    Load_addedlist=[]
    Load_list=[]
    for i in G.nodes:
        if (G.nodes[i]['attr']['components']=='node'):
            voltage=G.nodes[i]['attr']['voltage']
            phases=G.nodes[i]['attr']['phases']
            ph=0
            if('A' in phases or 'B' in phases or 'C' in phases):
                ph=1
            if ('A' in phases and 'B' in phases or 'A' in phases and 'C' in phases or 'C' in phases and 'B' in phases):
                ph=2
            if ('A' in phases and 'B' in phases and 'C' in phases):
                ph=3
            if(ph==0):
                print('Incomplete phase information provided in glm')

            if('j' in voltage):
                basevolt=abs(complex(voltage))
            else:
                basevolt=float(voltage)


            if(ph==3):
                basevolt=basevolt*1.73205080757

            if(G.nodes[i]['attr']['issource'] and 'reg' not in i):
                lf='SLACK'
            else:
                lf='PV'

            n=i.replace('"','')
            n=n.replace('-','_')
            Entry='type=bus, name='+n+', baseVolt='+str(basevolt)+', nb_phases='+str(ph)+', lf_type='+lf+', '
            Entry=Entry+'x='+str(round(float(G.nodes[i]['attr']['x'])))+', y='+str(round(float(G.nodes[i]['attr']['y'])))
            Netlist.append(Entry)
            Nodes_added=Nodes_added+1

            if lf=='SLACK':
                Entry='type=customSource, name=source, net_1='+n+', module=['+str(basevolt)+' '+str(basevolt)+' '+str(basevolt)+'], '
                Entry=Entry+'angle=[0 -120 120] , R=[1e-5 1e-5 1e-5], L=[0 0 0], C=[0 0 0], hypersim_type=AC V source, hypersim_lib=Network Sources.clf, '
                Entry=Entry+'x='+str(G.nodes[i]['attr']['x']-60)+', y='+str(G.nodes[i]['attr']['y'])
                Netlist.append(Entry)


        if (G.nodes[i]['attr']['components'] == 'load'):
            Load_list.append(i)
            if('parent' in G.nodes[i]['attr'].keys()):
                #a=0
                parent=G.nodes[i]['attr']['parent']
                phases = G.nodes[parent]['attr']['phases']

                phases = phases.replace('N', '')
                phases = phases.replace('D', '')
                phases = phases.replace('"', '')

                ph = len(phases)

                configlist = ''.join(list(G.nodes[i]['attr']['config'].keys()))
                loadph = ''
                if ('power_A' in configlist or 'impedance_A' in configlist or 'current_A' in configlist):
                    loadph = loadph + 'A'
                if ('power_B' in configlist or 'impedance_B' in configlist or 'current_B' in configlist):
                    loadph = loadph + 'B'
                if ('power_C' in configlist or 'impedance_C' in configlist or 'current_C' in configlist):
                    loadph = loadph + 'C'

                if(ph==len(loadph)):
                    if ('D' in G.nodes[i]['attr']['config']['phases']):
                        isDelta = True
                    else:
                        isDelta = False
                    if (isDelta):
                        Entry = None
                        if (ph == 3):
                            pp = parent.replace('"', '')
                            pp = pp.replace('-', '_')
                            Entry = delta_load_entry(G, i, pp)
                        if (Entry is not None):
                            Netlist.append(Entry)
                            Loads_added = Loads_added + 1
                            Load_addedlist.append(i)
                        else:
                            print('Please populate Delta load ' + i + ' manually ')
                            #Netlist.append('Placeholder for Load ' + i)
                            print('Placeholder for Load ' + i)
                    else:
                        voltage = G.nodes[i]['attr']['config']['voltage_' + phases[0]]
                        if ('j' in voltage):
                            basevolt = abs(complex(voltage))
                        else:
                            basevolt = float(voltage)

                        if (ph == 3):
                            basevolt = basevolt * 1.73205080757


                        if (len(loadph)==3):

                            if ('power_A' in configlist):
                                Sa = complex(G.nodes[i]['attr']['config']['constant_power_A'])
                                Sb = complex(G.nodes[i]['attr']['config']['constant_power_B'])
                                Sc = complex(G.nodes[i]['attr']['config']['constant_power_C'])
                                Pa=Sa.real/1000000
                                Qa=Sa.imag/1000000
                                Pb=Sb.real/1000000
                                Qb=Sb.imag/1000000
                                Pc=Sc.real/1000000
                                Qc=Sc.imag/1000000
                                #Entry = 'type=bus, name=' + i + '_bus' + ', baseVolt=' + str(basevolt) + ', nb_phases=' + str(ph) + ', lf_type=' + 'PV' + ', '
                                #Entry = Entry + 'x=' + str(G.nodes[i]['attr']['x']) + ', y=' + str(G.nodes[i]['attr']['y'])
                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                pp=parent.replace('"', '')
                                pp=pp.replace('-', '_')

                                Entry = 'type=customLoad3, name=' + n + ', bus=' +pp+', Pa=' + str(Pa) + ', Qa=' + str(Qa) + ', Pb=' + str(Pb) + ', Qb=' + str(Qb)
                                Entry = Entry + ', Pc=' + str(Pc) + ', Qc=' + str(Qc) + ', freq=60, Vbase=' + str(basevolt / 1000) + ', hypersim_type=PQ_threeph_wye, hypersim_lib=PNNL Loads.clf, x='
                                Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 30))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                            if ('impedance_A' in configlist):
                                print('Impedance Load ' + i + ' converter to PQ')
                                Za = complex(G.nodes[i]['attr']['config']['constant_impedance_A'])
                                Zb = complex(G.nodes[i]['attr']['config']['constant_impedance_B'])
                                Zc = complex(G.nodes[i]['attr']['config']['constant_impedance_C'])
                                Va = complex(G.nodes[i]['attr']['config']['voltage_A'])
                                Vb = complex(G.nodes[i]['attr']['config']['voltage_B'])
                                Vc = complex(G.nodes[i]['attr']['config']['voltage_C'])
                                Ia_star = (Va / Za).conjugate()
                                Ib_star = (Vb / Zb).conjugate()
                                Ic_star = (Vc / Zc).conjugate()
                                Sa = Va * Ia_star
                                Sb = Vb * Ib_star
                                Sc = Vc * Ic_star

                                Pa = Sa.real / 1000000
                                Qa = Sa.imag / 1000000
                                Pb = Sb.real / 1000000
                                Qb = Sb.imag / 1000000
                                Pc = Sc.real / 1000000
                                Qc = Sc.imag / 1000000

                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                pp = parent.replace('"', '')
                                pp = pp.replace('-', '_')
                                Entry = 'type=customLoad3, name=' + n + '_ZtoPQ, bus=' + pp+', Pa=' + str(Pa) + ', Qa=' + str(Qa) + ', Pb=' + str(Pb) + ', Qb=' + str(Qb)
                                Entry = Entry + ', Pc=' + str(Pc) + ', Qc=' + str(Qc) + ', freq=60, Vbase=' + str(basevolt / 1000) + ', hypersim_type=PQ_threeph_wye, hypersim_lib=PNNL Loads.clf, x='
                                Entry = Entry + str(round(float(G.nodes[i]['attr']['x']) - 20)) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 30))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                            if ('current_A' in configlist):
                                print('Current Load ' + i + ' converted to PQ')
                                Ia = complex(G.nodes[i]['attr']['config']['constant_current_A'])
                                Ib = complex(G.nodes[i]['attr']['config']['constant_current_B'])
                                Ic = complex(G.nodes[i]['attr']['config']['constant_current_C'])
                                Va = complex(G.nodes[i]['attr']['config']['voltage_A'])
                                Vb = complex(G.nodes[i]['attr']['config']['voltage_B'])
                                Vc = complex(G.nodes[i]['attr']['config']['voltage_C'])
                                Sa = Va * Ia.conjugate()
                                Sb = Vb * Ib.conjugate()
                                Sc = Vc * Ic.conjugate()

                                Pa = Sa.real / 1000000
                                Qa = Sa.imag / 1000000
                                Pb = Sb.real / 1000000
                                Qb = Sb.imag / 1000000
                                Pc = Sc.real / 1000000
                                Qc = Sc.imag / 1000000

                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                pp = parent.replace('"', '')
                                pp = pp.replace('-', '_')
                                Entry = 'type=customLoad3, name=' + n + '_ItoPQ, bus=' + pp + ', Pa=' + str(Pa) + ', Qa=' + str(Qa) + ', Pb=' + str(Pb) + ', Qb=' + str(Qb)
                                Entry = Entry + ', Pc=' + str(Pc) + ', Qc=' + str(Qc) + ', freq=60, Vbase=' + str(basevolt / 1000) + ', hypersim_type=PQ_threeph_wye, hypersim_lib=PNNL Loads.clf, x='
                                Entry = Entry + str(round(float(G.nodes[i]['attr']['x']) - 40)) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 30))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                        if (len(loadph) == 1):
                            if ('constant_power_' in configlist):
                                S = complex(G.nodes[i]['attr']['config']['constant_power_' + loadph])
                                Pa = S.real / 1000000
                                Qa = S.imag / 1000000
                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                pp = parent.replace('"', '')
                                pp = pp.replace('-', '_')
                                # Voltage changed
                                Entry = 'type=customLoad, name=' + n + '_1ph_' + loadph + ', net_T1=' + pp + ', P=' + str(
                                    Pa) + ', Q=' + str(Qa) + ', Vbase=' + str(
                                    basevolt / 1000.0) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                                Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 30))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                            if ('constant_impedance_' in configlist):
                                print('Impedance Load ' + i + ' converted to PQ')
                                Za = complex(G.nodes[i]['attr']['config']['constant_impedance_' + loadph])
                                Va = complex(G.nodes[i]['attr']['config']['voltage_' + loadph])
                                Ia_star = (Va / Za).conjugate()
                                Sa = Va * Ia_star
                                Pa = Sa.real / 1000000
                                Qa = Sa.imag / 1000000
                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                pp = parent.replace('"', '')
                                pp = pp.replace('-', '_')

                                Entry = 'type=customLoad, name=' + n + '_1ph_' + loadph + ', net_T1=' + pp + ', P=' + str(
                                    Pa) + ', Q=' + str(Qa) + ', Vbase=' + str(
                                    basevolt / 1000.0) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                                Entry = Entry + str(round(G.nodes[i]['attr']['x'])) + ', y=' + str(round(
                                    float(G.nodes[i]['attr']['y']) - 50))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                            if ('current_' in configlist):
                                print('Current Load ' + i + ' converted to PQ')
                                Ia = complex(G.nodes[i]['attr']['config']['constant_current_' + loadph])
                                Va = complex(G.nodes[i]['attr']['config']['voltage_' + loadph])
                                Sa = Va * Ia.conjugate()
                                Pa = Sa.real / 1000000
                                Qa = Sa.imag / 1000000
                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                pp = parent.replace('"', '')
                                pp = pp.replace('-', '_')

                                Entry = 'type=customLoad, name=' + n + '_1ph_' + loadph + ', net_T1=' + pp + ', P=' + str(
                                    Pa) + ', Q=' + str(Qa) + ', Vbase=' + str(
                                    basevolt / 1000.0) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                                Entry = Entry + str(round(G.nodes[i]['attr']['x'])) + ', y=' + str(round(
                                    float(G.nodes[i]['attr']['y']) - 70))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                        # 2 phase loads should not enter here since all 2 phase nodes are assumed to be 3phase nodes



            else:

                # Add a bus for the load
                #print(i,G.nodes[i]['attr'])
                phases = G.nodes[i]['attr']['phases']

                phases=phases.replace('N', '')
                phases=phases.replace('D', '')
                phases=phases.replace('"', '')

                ph=len(phases)
                voltage=G.nodes[i]['attr']['config']['voltage_'+phases[0]]
                if ('j' in voltage):
                    basevolt = abs(complex(voltage))
                else:
                    basevolt = float(voltage)

                if (ph == 3):
                    if ('D' in G.nodes[i]['attr']['config']['phases'] and delta_basevolt_ll(G.nodes[i]['attr']['config']) is not None):
                        basevolt = delta_basevolt_ll(G.nodes[i]['attr']['config'])
                    else:
                        basevolt = basevolt * 1.73205080757

                n = i.replace('"', '')
                n = n.replace('-', '_')
                Entry = 'type=bus, name=' + n+'_bus' + ', baseVolt=' + str(basevolt) + ', nb_phases=' + str(ph) + ', lf_type=' + 'PV' + ', '
                Entry = Entry + 'x=' + str(round(G.nodes[i]['attr']['x'])) + ', y=' + str(round(G.nodes[i]['attr']['y']))
                Netlist.append(Entry)
                # Add the load and if necessary a mux

                configlist=''.join(list(G.nodes[i]['attr']['config'].keys()))
                loadph=''
                if('power_A' in configlist or 'impedance_A' in configlist or 'current_A' in configlist):
                    loadph=loadph+'A'
                if ('power_B' in configlist or 'impedance_B' in configlist or 'current_B' in configlist):
                    loadph = loadph + 'B'
                if ('power_C' in configlist or 'impedance_C' in configlist or 'current_C' in configlist):
                    loadph = loadph + 'C'

                if(ph==len(loadph)):
                    if('D' in G.nodes[i]['attr']['config']['phases']):
                        isDelta=True
                    else:
                        isDelta=False
                    if(isDelta):
                        Entry = None
                        if (ph == 3):
                            n = i.replace('"', '')
                            n = n.replace('-', '_')
                            Entry = delta_load_entry(G, i, n + '_bus')
                        if (Entry is not None):
                            Netlist.append(Entry)
                            Loads_added = Loads_added + 1
                            Load_addedlist.append(i)
                        else:
                            print('Please populate Delta load ' +i+' manually ')
                            #Netlist.append('Placeholder for Load '+i)
                            print('Placeholder for Load '+i)
                    else:
                        if (len(loadph)==3):
                            if ('power_A' in configlist):
                                Sa = complex(G.nodes[i]['attr']['config']['constant_power_A'])
                                Sb = complex(G.nodes[i]['attr']['config']['constant_power_B'])
                                Sc = complex(G.nodes[i]['attr']['config']['constant_power_C'])
                                Pa=Sa.real/1000000
                                Qa=Sa.imag/1000000
                                Pb=Sb.real/1000000
                                Qb=Sb.imag/1000000
                                Pc=Sc.real/1000000
                                Qc=Sc.imag/1000000
                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                Entry='type=customLoad3, name='+n+', bus='+i+'_bus, Pa='+str(Pa)+', Qa='+str(Qa)+', Pb='+str(Pb)+', Qb='+str(Qb)
                                Entry=Entry+', Pc='+str(Pc)+', Qc='+str(Qc)+', freq=60, Vbase='+str(basevolt/1000)+', hypersim_type=PQ_threeph_wye, hypersim_lib=PNNL Loads.clf, x='
                                Entry=Entry+str(round(G.nodes[i]['attr']['x']))+', y='+str(round(float(G.nodes[i]['attr']['y'])-30))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                            if('impedance_A' in configlist):
                                print('Impedance Load '+i+' converter to PQ')
                                Za = complex(G.nodes[i]['attr']['config']['constant_impedance_A'])
                                Zb = complex(G.nodes[i]['attr']['config']['constant_impedance_B'])
                                Zc = complex(G.nodes[i]['attr']['config']['constant_impedance_C'])
                                Va = complex(G.nodes[i]['attr']['config']['voltage_A'])
                                Vb = complex(G.nodes[i]['attr']['config']['voltage_B'])
                                Vc = complex(G.nodes[i]['attr']['config']['voltage_C'])
                                Ia_star = (Va/Za).conjugate()
                                Ib_star = (Vb / Zb).conjugate()
                                Ic_star = (Vc / Zc).conjugate()
                                Sa=Va*Ia_star
                                Sb=Vb*Ib_star
                                Sc=Vc*Ic_star

                                Pa = Sa.real / 1000000
                                Qa = Sa.imag / 1000000
                                Pb = Sb.real / 1000000
                                Qb = Sb.imag / 1000000
                                Pc = Sc.real / 1000000
                                Qc = Sc.imag / 1000000
                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                Entry = 'type=customLoad3, name=' + n + '_ZtoPQ, bus=' + i + '_bus, Pa=' + str(Pa) + ', Qa=' + str(Qa) + ', Pb=' + str(Pb) + ', Qb=' + str(Qb)
                                Entry = Entry + ', Pc=' + str(Pc) + ', Qc=' + str(Qc) + ', freq=60, Vbase=' + str(basevolt / 1000) + ', hypersim_type=PQ_threeph_wye, hypersim_lib=PNNL Loads.clf, x='
                                Entry = Entry + str(round(float(G.nodes[i]['attr']['x'])-20)) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 30))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                            if('current_A' in configlist):
                                print('Current Load ' + i + ' converted to PQ')
                                Ia = complex(G.nodes[i]['attr']['config']['constant_current_A'])
                                Ib = complex(G.nodes[i]['attr']['config']['constant_current_B'])
                                Ic = complex(G.nodes[i]['attr']['config']['constant_current_C'])
                                Va = complex(G.nodes[i]['attr']['config']['voltage_A'])
                                Vb = complex(G.nodes[i]['attr']['config']['voltage_B'])
                                Vc = complex(G.nodes[i]['attr']['config']['voltage_C'])
                                Sa = Va * Ia.conjugate()
                                Sb = Vb * Ib.conjugate()
                                Sc = Vc * Ic.conjugate()

                                Pa = Sa.real / 1000000
                                Qa = Sa.imag / 1000000
                                Pb = Sb.real / 1000000
                                Qb = Sb.imag / 1000000
                                Pc = Sc.real / 1000000
                                Qc = Sc.imag / 1000000
                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                Entry = 'type=customLoad3, name=' + n + '_ItoPQ, bus=' + i + '_bus, Pa=' + str(Pa) + ', Qa=' + str(Qa) + ', Pb=' + str(Pb) + ', Qb=' + str(Qb)
                                Entry = Entry + ', Pc=' + str(Pc) + ', Qc=' + str(Qc) + ', freq=60, Vbase=' + str(basevolt / 1000) + ', hypersim_type=PQ_threeph_wye, hypersim_lib=PNNL Loads.clf, x='
                                Entry = Entry + str(round(float(G.nodes[i]['attr']['x'])-40)) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 30))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                        if(len(loadph)==1):
                            if('constant_power_' in configlist):
                                S = complex(G.nodes[i]['attr']['config']['constant_power_'+loadph])
                                Pa = S.real / 1000000
                                Qa = S.imag / 1000000
                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                Entry='type=customLoad, name='+n+'_1ph_'+loadph+', net_T1='+i+'_bus, P='+str(Pa)+', Q='+str(Qa)+', Vbase='+str(basevolt/1000.0)+', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                                Entry=Entry+str(round(float(G.nodes[i]['attr']['x'])))+', y='+str(round(float(G.nodes[i]['attr']['y'])-30))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                            if('constant_impedance_' in configlist):
                                print('Impedance Load ' + i + ' converted to PQ')
                                Za = complex(G.nodes[i]['attr']['config']['constant_impedance_'+loadph])
                                Va = complex(G.nodes[i]['attr']['config']['voltage_'+loadph])
                                Ia_star = (Va / Za).conjugate()
                                Sa = Va * Ia_star
                                Pa = Sa.real / 1000000
                                Qa = Sa.imag / 1000000
                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                Entry = 'type=customLoad, name=' + n + '_1ph_' + loadph + ', net_T1=' + i + '_bus, P=' + str(Pa) + ', Q=' + str(Qa) + ', Vbase=' + str(basevolt / 1000.0) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                                Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 50))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                            if('current_' in configlist):
                                print('Current Load ' + i + ' converted to PQ')
                                Ia = complex(G.nodes[i]['attr']['config']['constant_current_' + loadph])
                                Va = complex(G.nodes[i]['attr']['config']['voltage_' + loadph])
                                Sa = Va * Ia.conjugate()
                                Pa = Sa.real / 1000000
                                Qa = Sa.imag / 1000000
                                n = i.replace('"', '')
                                n = n.replace('-', '_')
                                Entry = 'type=customLoad, name=' + n + '_1ph_' + loadph + ', net_T1=' + i + '_bus, P=' + str(Pa) + ', Q=' + str(Qa) + ', Vbase=' + str(basevolt / 1000.0) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                                Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 70))
                                Netlist.append(Entry)
                                Loads_added = Loads_added + 1
                                Load_addedlist.append(i)
                        # 2 phase loads should not enter here since all 2 phase nodes are assumed to be 3phase nodes
                else:
                    if ('D' in G.nodes[i]['attr']['config']['phases'] and not ((ph == 3 and len(loadph) in (1, 2)) or (ph == 2 and len(loadph) == 1))):
                        isDelta = True
                    else:
                        isDelta = False
                    if (isDelta):
                        print('Please populate Delta load ' + i + ' manually ')
                        #Netlist.append('Placeholder for Load ' + i)
                        print('Placeholder for Load ' + i)
                    else:
                        pass
                        # Populate 3ph to 1ph loads (wye and delta) after muxes

        if (G.nodes[i]['attr']['components'] == 'capacitor'):
            if ('parent' in G.nodes[i]['attr'].keys()):
                parent=G.nodes[i]['attr']['parent']
                phases = G.nodes[parent]['attr']['phases']

                phases = phases.replace('N', '')
                phases = phases.replace('D', '')
                phases = phases.replace('"', '')
                ph=len(phases)
                configlist = ''.join(list(G.nodes[i]['attr']['config'].keys()))
                capph = ''
                if ('capacitor_A' in configlist):
                    capph = capph + 'A'
                if ('capacitor_B' in configlist):
                    capph = capph + 'B'
                if ('capacitor_C' in configlist):
                    capph = capph + 'C'


                if(ph==len(capph)):
                    if(ph==3):
                        # Populate the cap value with A phase as the reference
                        Var=float(G.nodes[i]['attr']['config']['capacitor_A'])
                        Nom_Volt=float(G.nodes[i]['attr']['config']['nominal_voltage'])
                        Capacitance=Var/(2*math.pi*60*Nom_Volt*Nom_Volt)
                        n = i.replace('"', '')
                        n = n.replace('-', '_')
                        Entry='type=capacitor, name='+n+', p1='+parent+', nb_phases=3, C='+str(Capacitance)+', vbase='
                        Entry=Entry+str(Nom_Volt)+', fbase=60, sbase='+str(Var/1000000)+', x='+str(round(float(G.nodes[i]['attr']['x'])))
                        Entry=Entry+', y='+str(round(float(G.nodes[i]['attr']['y'])))
                        Netlist.append(Entry)

                        Capacitors_added=Capacitors_added+1
                    if(ph==1):
                        Var = float(G.nodes[i]['attr']['config']['capacitor_'+capph])
                        Nom_Volt = float(G.nodes[i]['attr']['config']['nominal_voltage'])
                        Capacitance = Var / (2 * math.pi * 60 * Nom_Volt * Nom_Volt)
                        n = i.replace('"', '')
                        n = n.replace('-', '_')
                        Entry='type=capacitor, name='+n+', p1='+parent+', nb_phases=1, C='+str(Capacitance)+', vbase='
                        Entry=Entry+str(Nom_Volt)+', fbase=60, sbase='+str(Var/1000000)+', x='+str(round(float(G.nodes[i]['attr']['x'])))
                        Entry=Entry+', y='+str(round(float(G.nodes[i]['attr']['y'])))
                        Netlist.append(Entry)
                        Capacitors_added = Capacitors_added + 1

                else:
                    # Accounting for 3 phase to 1 phase transition from parent to capacitor
                    # Need to insert Mux and create independent bus for capacitor
                    Var = float(G.nodes[i]['attr']['config']['capacitor_' + capph])
                    Nom_Volt = float(G.nodes[i]['attr']['config']['nominal_voltage'])
                    Capacitance = Var / (2 * math.pi * 60 * Nom_Volt * Nom_Volt)

                    n = i.replace('"', '')
                    n = n.replace('-', '_')

                    u=parent.replace('"', '')
                    u=u.replace('-', '_')
                    v=n+'_bus'
                    v=v.replace('"', '')
                    v=v.replace('-', '_')
                    if ph == 3 and len(capph) == 1:
                        if ('A' in capph):
                            Entry = 'type=bus, name=' + v + ', baseVolt=' + str(Nom_Volt) + ', nb_phases=' + str(len(capph)) + ', lf_type=' + lf + ', '
                            Entry = Entry + 'x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            Netlist.append(Entry)

                            Entry = 'type=customMUXa, name=MUXa' + str(
                                count) + ', bus=' + u + ', phA=' + v + ', Vbase=' + str(Nom_Volt)
                            Entry = Entry + ', hypersim_type=bus2a, hypersim_lib=PNNL Loads.clf, x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            #count = count + 1
                            Netlist.append(Entry)


                            Entry = 'type=capacitor, name=' + n + ', p1=' + v + ', nb_phases=1, C=' + str(
                                Capacitance) + ', vbase='
                            Entry = Entry + str(Nom_Volt) + ', fbase=60, sbase=' + str(Var / 1000000) + ', x=' +str(round(float(G.nodes[i]['attr']['x'])))
                            Entry = Entry + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            count = count + 1
                            Netlist.append(Entry)
                            Capacitors_added = Capacitors_added + 1
                        elif ('B' in capph):
                            Entry = 'type=bus, name=' + v + ', baseVolt=' + str(Nom_Volt) + ', nb_phases=' + str(len(capph)) + ', lf_type=' + lf + ', '
                            Entry = Entry + 'x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            Netlist.append(Entry)

                            Entry = 'type=customMUXb, name=MUXb' + str(
                                count) + ', bus=' + u + ', phB=' + v + ', Vbase=' + str(Nom_Volt)
                            Entry = Entry + ', hypersim_type=bus2b, hypersim_lib=PNNL Loads.clf, x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            Netlist.append(Entry)

                            Entry = 'type=capacitor, name=' + n + ', p1=' + v + ', nb_phases=1, C=' + str(
                                Capacitance) + ', vbase='
                            Entry = Entry + str(Nom_Volt) + ', fbase=60, sbase=' + str(Var / 1000000) + ', x=' + str(round(float(G.nodes[i]['attr']['x'])))
                            Entry = Entry + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))

                            count = count + 1
                            Netlist.append(Entry)
                            Capacitors_added = Capacitors_added + 1
                        elif ('C' in capph):

                            Entry = 'type=bus, name=' + v + ', baseVolt=' + str(Nom_Volt) + ', nb_phases=' + str(len(capph)) + ', lf_type=' + lf + ', '
                            Entry = Entry + 'x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            Netlist.append(Entry)

                            Entry = 'type=customMUXc, name=MUXc' + str(
                                count) + ', bus=' + u + ', phC=' + v + ', Vbase=' + str(Nom_Volt)
                            Entry = Entry + ', hypersim_type=bus2c, hypersim_lib=PNNL Loads.clf, x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            Netlist.append(Entry)

                            Entry = 'type=capacitor, name=' + n + ', p1=' + v + ', nb_phases=1, C=' + str(
                                Capacitance) + ', vbase='
                            Entry = Entry + str(Nom_Volt) + ', fbase=60, sbase=' + str(Var / 1000000) + ', x=' +str(round(float(G.nodes[i]['attr']['x'])))
                            Entry = Entry + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))

                            count = count + 1
                            Netlist.append(Entry)
                            Capacitors_added = Capacitors_added + 1



            else:
                print('Capacitor '+i+' must be defined with a parent')

        if (G.nodes[i]['attr']['components'] == 'inverter'):

            if ('parent' in G.nodes[i]['attr'].keys()):
                #print(i)
                parent = G.nodes[i]['attr']['parent']
                phases = G.nodes[parent]['attr']['phases']

                phases = phases.replace('N', '')
                phases = phases.replace('D', '')
                phases = phases.replace('"', '')

                ph = len(phases)

                invph=G.nodes[i]['attr']['phases']

                invph=invph.replace('N', '')
                invph = invph.replace('S', '')
                invph = invph.replace('"', '')

                Nom_Volt=float(G.nodes[parent]['attr']['voltage'])
                lf = 'PV'


                if (len(phases)==len(invph)):

                    if(len(invph)>2):
                        # Populate 3 phase
                        n = i.replace('"', '')
                        n = n.replace('-', '_')
                        pp = parent.replace('"', '')
                        pp = pp.replace('-', '_')
                        Entry='type=customInv3ph, name='+n+', Bus='+pp
                        Entry=Entry+', hypersim_type=SOLAR_GFL_3ph, hypersim_lib=PNNL Loads.clf, x='+str(round(float(G.nodes[i]['attr']['x'])))
                        Entry=Entry+', y='+str(round(float(G.nodes[i]['attr']['y'])))
                        Netlist.append(Entry)
                        Inverters_added = Inverters_added + 1

                    if(len(invph)==1):
                        n = i.replace('"', '')
                        n = n.replace('-', '_')
                        pp = parent.replace('"', '')
                        pp = pp.replace('-', '_')
                        Entry='type=customInv1ph, name='+n+', Bus='+pp
                        Entry=Entry+', hypersim_type=SOLAR_GFL_1ph, hypersim_lib=PNNL Loads.clf, x='
                        Entry=Entry+str(round(float(G.nodes[i]['attr']['x'])))+', y='+str(round(float(G.nodes[i]['attr']['y'])))

                        #print('Need to populate netlist entry for 1 phase')

                        Inverters_added = Inverters_added + 1

                else:

                    if(len(phases)==3 and len(invph)==1):
                        pp = parent.replace('"', '')
                        pp = pp.replace('-', '_')
                        u=pp
                        v = i + '_bus'
                        v = v.replace('"', '')
                        v = v.replace('-', '_')
                        n = i.replace('"', '')
                        n = n.replace('-', '_')

                        if('A' in invph):
                            Entry = 'type=bus, name=' + v + ', baseVolt=' + str(Nom_Volt / 1000) + ', nb_phases=' + str(len(invph)) + ', lf_type=' + lf + ', '
                            Entry = Entry + 'x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            Netlist.append(Entry)

                            Entry = 'type=customMUXa, name=MUXa' + str(
                                count) + ', bus=' + u + ', phA=' + v + ', Vbase=' + str(Nom_Volt / 1000)
                            Entry = Entry + ', hypersim_type=bus2a, hypersim_lib=PNNL Loads.clf, x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            count = count + 1
                            Netlist.append(Entry)

                            Entry = 'type=customInv1ph, name='+n+', Bus=' + v
                            Entry = Entry + ', hypersim_type=SOLAR_GFL_1ph, hypersim_lib=PNNL Loads.clf, x='
                            Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            Netlist.append(Entry)

                            Inverters_added = Inverters_added + 1

                            ## Put 1 phase inverter definition here
                        if ('B' in invph):
                            Entry = 'type=bus, name=' + v + ', baseVolt=' + str(Nom_Volt / 1000) + ', nb_phases=' + str(len(invph)) + ', lf_type=' + lf + ', '
                            Entry = Entry + 'x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            Netlist.append(Entry)

                            Entry = 'type=customMUXb, name=MUXb' + str(
                                count) + ', bus=' + u + ', phB=' + v + ', Vbase=' + str(Nom_Volt / 1000)
                            Entry = Entry + ', hypersim_type=bus2b, hypersim_lib=PNNL Loads.clf, x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            count = count + 1
                            Netlist.append(Entry)

                            Entry = 'type=customInv1ph, name='+n+', Bus=' + v
                            Entry = Entry + ', hypersim_type=SOLAR_GFL_1ph, hypersim_lib=PNNL Loads.clf, x='
                            Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            Netlist.append(Entry)

                            Inverters_added = Inverters_added + 1
                            ## Put 1 phase inverter definition here
                        if ('C' in invph):
                            Entry = 'type=bus, name=' + v + ', baseVolt=' + str(Nom_Volt / 1000) + ', nb_phases=' + str(len(invph)) + ', lf_type=' + lf + ', '
                            Entry = Entry + 'x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            Netlist.append(Entry)

                            Entry = 'type=customMUXc, name=MUXc' + str(
                                count) + ', bus=' + u + ', phC=' + v + ', Vbase=' + str(Nom_Volt / 1000)
                            Entry = Entry + ', hypersim_type=bus2c, hypersim_lib=PNNL Loads.clf, x=' + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            count = count + 1
                            Netlist.append(Entry)

                            Entry = 'type=customInv1ph, name='+n+', Bus=' + v
                            Entry = Entry + ', hypersim_type=SOLAR_GFL_1ph, hypersim_lib=PNNL Loads.clf, x='
                            Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y'])))
                            Netlist.append(Entry)

                            Inverters_added = Inverters_added + 1
                            ## Put 1 phase inverter definition here




        if (G.nodes[i]['attr']['components'] == 'diesel_dg'):

            if('parent' in G.nodes[i]['attr'].keys()):
                # DG currently only populated as 3-phase
                parent=G.nodes[i]['attr']['parent']
                if('ABC' in G.nodes[parent]['attr']['phases'] and 'ABC' in G.nodes[i]['attr']['phases']):
                    n = i.replace('"', '')
                    n = n.replace('-', '_')
                    pp = parent.replace('"', '')
                    pp = pp.replace('-', '_')

                    Entry='type=customDG, name='+n+', DG_N1='+pp+', Base_P='+str(float(G.nodes[i]['attr']['config']['Rated_VA'])/1000000)
                    Entry=Entry+', Base_V='+str(float(G.nodes[parent]['attr']['voltage'])/1000)
                    Entry=Entry+', hypersim_type=DG, hypersim_lib=PNNL Loads.clf, x='+str(round(float(G.nodes[i]['attr']['x'])))
                    Entry=Entry+', y='+str(round(float(G.nodes[i]['attr']['y'])))
                    Netlist.append(Entry)
                    DG_Added=DG_Added+1




    Mux_added=0


    Edges=list(G.edges(data=True))
    Edgelist=copy.deepcopy(Edges)

    for i in range(len(Edgelist)):
        u = Edgelist[i][0]
        v = Edgelist[i][1]


        att=Edgelist[i][2]

        if('mux' in att['attr']):
            mux_info=att['attr'].split('_')
            phasefrom=mux_info[1]
            phaseto=mux_info[3]
            phasefrom=phasefrom.replace('"', '')
            phaseto = phaseto.replace('"', '')
            # basevolt=abs(complex(G.nodes[u]['attr']['voltage']))* 1.73205080757
            xdiff=round(float(G.nodes[v]['attr']['x'])-float(G.nodes[u]['attr']['x']))
            ydiff = round(float(G.nodes[v]['attr']['y']) - float(G.nodes[u]['attr']['y']))
            x=round(float(G.nodes[u]['attr']['x'])+(xdiff/3))
            y = round(float(G.nodes[u]['attr']['y']) + (ydiff / 3))

            if phasefrom=='ABC' and len(phaseto)==1:
                volt = (G.nodes[u]['attr'].get('voltage')
                        or G.nodes[u]['attr'].get('config', {}).get('nominal_voltage', '0'))
                basevolt=abs(complex(volt))* 1.73205080757
                if('A' in phaseto):
                    u = u.replace('"', '')
                    u = u.replace('-', '_')
                    v = v.replace('"', '')
                    v = v.replace('-', '_')
                    Entry='type=customMUXa, name=MUXa'+str(count)+', bus='+u+', phA='+v+', Vbase='+str(basevolt/1000)
                    Entry=Entry+', hypersim_type=bus2a, hypersim_lib=PNNL Loads.clf, x='+str(x)+', y='+str(y)
                    count=count+1
                    Netlist.append(Entry)
                    Mux_added=Mux_added+1
                elif ('B' in phaseto):
                    u = u.replace('"', '')
                    u = u.replace('-', '_')
                    v = v.replace('"', '')
                    v = v.replace('-', '_')
                    Entry = 'type=customMUXb, name=MUXb'+str(count)+', bus=' + u + ', phB=' + v + ', Vbase=' + str(basevolt / 1000)
                    Entry = Entry + ', hypersim_type=bus2b, hypersim_lib=PNNL Loads.clf, x=' + str(x) + ', y=' + str(y)
                    count=count+1
                    Netlist.append(Entry)
                    Mux_added = Mux_added + 1
                elif ('C' in phaseto):
                    u = u.replace('"', '')
                    u = u.replace('-', '_')
                    v = v.replace('"', '')
                    v = v.replace('-', '_')
                    Entry = 'type=customMUXc, name=MUXc'+str(count)+', bus=' + u + ', phC=' + v + ', Vbase=' + str(basevolt / 1000)
                    Entry = Entry + ', hypersim_type=bus2c, hypersim_lib=PNNL Loads.clf, x=' + str(x) + ', y=' + str(y)
                    count=count+1
                    Netlist.append(Entry)
                    Mux_added = Mux_added + 1
            else:
                print('Please populate a Mux for edge' + str(Edgelist[i]))
                
                #print(Edgelist[i])

    # Now populate the 3ph bus to 1ph loads
    for i in G.nodes:
        if (G.nodes[i]['attr']['components'] == 'load'):

            # Add a bus for the load
            #print(i,G.nodes[i]['attr'])
            pflag=0
            if('parent' in G.nodes[i]['attr'].keys()):
                parent= G.nodes[i]['attr']['parent']
                phases=G.nodes[parent]['attr']['phases']
                pflag=1
            else:
                phases = G.nodes[i]['attr']['phases']

            phases=phases.replace('N', '')
            phases=phases.replace('D', '')
            phases=phases.replace('"', '')

            ph=len(phases)

            configlist = ''.join(list(G.nodes[i]['attr']['config'].keys()))

            basevolt=abs(complex(G.nodes[i]['attr']['config']['nominal_voltage']))
            x=round(float(G.nodes[i]['attr']['x']))
            y = round(float(G.nodes[i]['attr']['y']))

            #configlist = ''.join(list(G.nodes[i]['attr']['config'].keys()))
            loadph = ''
            if ('power_A' in configlist or 'impedance_A' in configlist or 'current_A' in configlist):
                loadph = loadph + 'A'
            if ('power_B' in configlist or 'impedance_B' in configlist or 'current_B' in configlist):
                loadph = loadph + 'B'
            if ('power_C' in configlist or 'impedance_C' in configlist or 'current_C' in configlist):
                loadph = loadph + 'C'
            if (ph==3 and len(loadph) in (1, 2)) or (ph==2 and len(loadph)==1 and 'D' in G.nodes[i]['attr']['config']['phases']):
                # Find the relevant loadbus
                #print(i)
                if ('D' in G.nodes[i]['attr']['config']['phases']):
                    isDelta = True
                else:
                    isDelta = False
                if (isDelta):
                    if (pflag == 1):
                        busname = parent.replace('"', '')
                        busname = busname.replace('-', '_')
                    else:
                        busname = i.replace('"', '')
                        busname = busname.replace('-', '_') + '_bus'
                    entries, count = delta_load2_entries(G, i, busname, count)
                    if (entries is not None):
                        for Entry in entries:
                            Netlist.append(Entry)
                        Loads_added = Loads_added + 1
                        Load_addedlist.append(i)
                    else:
                        print('Please populate Delta load ' + i + ' manually ')
                        #Netlist.append('Placeholder for Load ' + i)
                        print('Placeholder for Load ' + i)
                elif (len(loadph) == 1):
                    if('parent' in G.nodes[i]['attr'].keys()):
                        if ('A' in loadph):
                            n = i.replace('"', '')
                            n = n.replace('-', '_')
                            conn = i + 'boA'
                            conn = conn.replace('"', '')
                            conn = conn.replace('-', '_')
                            pp = parent.replace('"', '')
                            pp = pp.replace('-', '_')
                            Entry = 'type=bus, name=' + conn + ', baseVolt=' + str(basevolt) + ', nb_phases=' + str(1) + ', lf_type=' + 'PV' + ', '
                            Entry = Entry + 'x=' + str(x) + ', y=' + str(y-30)
                            Netlist.append(Entry)
                            Entry = 'type=customMUXa, name=MUXa' + str(count) + ', bus=' + pp + ', phA=' + n +'boA' +', Vbase=' + str(
                                basevolt*1.73205080757 / 1000)
                            Entry = Entry + ', hypersim_type=bus2a, hypersim_lib=PNNL Loads.clf, x=' + str(x) + ', y=' + str(y-50)
                            count=count+1

                            Netlist.append(Entry)
                            Loads_added = Loads_added + 1
                            Load_addedlist.append(i)

                        elif ('B' in loadph):

                            n = i.replace('"', '')
                            n = n.replace('-', '_')
                            conn = i + 'boB'
                            conn = conn.replace('"', '')
                            conn = conn.replace('-', '_')
                            pp = parent.replace('"', '')
                            pp = pp.replace('-', '_')
                            Entry = 'type=bus, name=' + conn + ', baseVolt=' + str(basevolt) + ', nb_phases=' + str(1) + ', lf_type=' + 'PV' + ', '
                            Entry = Entry + 'x=' + str(x) + ', y=' + str(y - 30)
                            Netlist.append(Entry)
                            Entry = 'type=customMUXb, name=MUXb' + str(count) + ', bus=' + pp + ', phB=' + n + 'boB, Vbase=' + str(
                                basevolt*1.73205080757 / 1000)
                            Entry = Entry + ', hypersim_type=bus2b, hypersim_lib=PNNL Loads.clf, x=' + str(x) + ', y=' + str(y-70)
                            count = count + 1

                            Netlist.append(Entry)

                            Loads_added = Loads_added + 1
                            Load_addedlist.append(i)
                        elif ('C' in loadph):
                            n = i.replace('"', '')
                            n = n.replace('-', '_')
                            conn = i + 'boC'
                            conn = conn.replace('"', '')
                            conn = conn.replace('-', '_')
                            pp = parent.replace('"', '')
                            pp = pp.replace('-', '_')
                            Entry = 'type=bus, name=' + conn + ', baseVolt=' + str(basevolt) + ', nb_phases=' + str(1) + ', lf_type=' + 'PV' + ', '
                            Entry = Entry + 'x=' + str(x) + ', y=' + str(y - 30)
                            Netlist.append(Entry)
                            Entry = 'type=customMUXc, name=MUXc' + str(count) + ', bus=' + pp + ', phC=' + n + 'boC, Vbase=' + str(
                                basevolt*1.73205080757 / 1000)
                            Entry = Entry + ', hypersim_type=bus2c, hypersim_lib=PNNL Loads.clf, x=' + str(x) + ', y=' + str(y-90)
                            count = count + 1

                            Netlist.append(Entry)

                            Loads_added = Loads_added + 1
                            Load_addedlist.append(i)

                        if ('constant_power_' in configlist):
                            S = complex(G.nodes[i]['attr']['config']['constant_power_' + loadph])
                            Pa = S.real / 1000000
                            Qa = S.imag / 1000000
                            n = i.replace('"', '')
                            n = n.replace('-', '_')
                            Entry = 'type=customLoad, name=' + n + '_1ph_' + loadph + ', net_T1=' + conn + ', P=' + str(
                                Pa) + ', Q=' + str(Qa) + ', Vbase=' + str(
                                basevolt/1000) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                            Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 60))
                            Netlist.append(Entry)
                        if ('constant_impedance_' in configlist):
                            print('Impedance Load ' + i + ' converter to PQ')
                            Za = complex(G.nodes[i]['attr']['config']['constant_impedance_' + loadph])
                            Va = complex(G.nodes[i]['attr']['config']['voltage_' + loadph])
                            Ia_star = (Va / Za).conjugate()
                            Sa = Va * Ia_star
                            Pa = Sa.real / 1000000
                            Qa = Sa.imag / 1000000
                            n = i.replace('"', '')
                            n = n.replace('-', '_')
                            Entry = 'type=customLoad, name=' + n + '_1ph_' + loadph + ', net_T1=' + conn + ', P=' + str(
                                Pa) + ', Q=' + str(Qa) + ', Vbase=' + str(
                                basevolt/1000) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                            Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 70))
                            Netlist.append(Entry)
                        if ('current_' in configlist):
                            print('Current Load ' + i + ' converted to PQ')
                            Ia = complex(G.nodes[i]['attr']['config']['constant_current_' + loadph])
                            Va = complex(G.nodes[i]['attr']['config']['voltage_' + loadph])
                            Sa = Va * Ia.conjugate()
                            Pa = Sa.real / 1000000
                            Qa = Sa.imag / 1000000
                            n = i.replace('"', '')
                            n = n.replace('-', '_')
                            Entry = 'type=customLoad, name=' + n + '_1ph_' + loadph + ', net_T1=' + conn + ', P=' + str(
                                Pa) + ', Q=' + str(Qa) + ', Vbase=' + str(
                                basevolt/1000) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                            Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 80))
                            Netlist.append(Entry)
                    else:
                        if ('A' in loadph):
                            conn = i + 'boA'
                            conn = conn.replace('"', '')
                            conn = conn.replace('-', '_')
                            n = i.replace('"', '')
                            n = n.replace('-', '_')

                            Entry = 'type=bus, name=' + conn + ', baseVolt=' + str(basevolt) + ', nb_phases=' + str(1) + ', lf_type=' + 'PV' + ', '
                            Entry = Entry + 'x=' + str(x) + ', y=' + str(y-30)
                            Netlist.append(Entry)
                            Entry = 'type=customMUXa, name=MUXa' + str(count) + ', bus=' + n + '_bus, phA=' + i +'boA' +', Vbase=' + str(
                                basevolt*1.73205080757 / 1000)
                            Entry = Entry + ', hypersim_type=bus2a, hypersim_lib=PNNL Loads.clf, x=' + str(x) + ', y=' + str(y-50)
                            count=count+1

                            Netlist.append(Entry)

                            Loads_added = Loads_added + 1
                            Load_addedlist.append(i)
                        elif ('B' in loadph):
                            conn = i + 'boB'
                            conn = conn.replace('"', '')
                            conn = conn.replace('-', '_')
                            n = i.replace('"', '')
                            n = n.replace('-', '_')

                            Entry = 'type=bus, name=' + conn + ', baseVolt=' + str(basevolt) + ', nb_phases=' + str(1) + ', lf_type=' + 'PV' + ', '
                            Entry = Entry + 'x=' + str(x) + ', y=' + str(y - 30)
                            Netlist.append(Entry)
                            Entry = 'type=customMUXb, name=MUXb' + str(count) + ', bus=' + n + '_bus, phB=' + i + 'boB, Vbase=' + str(
                                basevolt*1.73205080757 / 1000)
                            Entry = Entry + ', hypersim_type=bus2b, hypersim_lib=PNNL Loads.clf, x=' + str(x) + ', y=' + str(y-70)
                            count = count + 1

                            Netlist.append(Entry)

                            Loads_added = Loads_added + 1
                            Load_addedlist.append(i)
                        elif ('C' in loadph):
                            conn = i + 'boC'
                            conn = conn.replace('"', '')
                            conn = conn.replace('-', '_')
                            n = i.replace('"', '')
                            n = n.replace('-', '_')

                            Entry = 'type=bus, name=' + conn + ', baseVolt=' + str(basevolt) + ', nb_phases=' + str(1) + ', lf_type=' + 'PV' + ', '
                            Entry = Entry + 'x=' + str(x) + ', y=' + str(y - 30)
                            Netlist.append(Entry)
                            Entry = 'type=customMUXc, name=MUXc' + str(count) + ', bus=' + n + '_bus, phC=' + i + 'boC, Vbase=' + str(
                                basevolt*1.73205080757 / 1000)
                            Entry = Entry + ', hypersim_type=bus2c, hypersim_lib=PNNL Loads.clf, x=' + str(x) + ', y=' + str(y-90)
                            count = count + 1

                            Netlist.append(Entry)

                            Loads_added = Loads_added + 1
                            Load_addedlist.append(i)

                        if ('constant_power_' in configlist):
                            S = complex(G.nodes[i]['attr']['config']['constant_power_' + loadph])
                            Pa = S.real / 1000000
                            Qa = S.imag / 1000000
                            n = i.replace('"', '')
                            n = n.replace('-', '_')
                            Entry = 'type=customLoad, name=' + n + '_1ph_' + loadph + ', net_T1=' + conn + ', P=' + str(
                                Pa) + ', Q=' + str(Qa) + ', Vbase=' + str(
                                basevolt/1000) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                            Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 60))
                            Netlist.append(Entry)
                        if ('constant_impedance_' in configlist):
                            print('Impedance Load ' + i + ' converter to PQ')
                            Za = complex(G.nodes[i]['attr']['config']['constant_impedance_' + loadph])
                            Va = complex(G.nodes[i]['attr']['config']['voltage_' + loadph])
                            Ia_star = (Va / Za).conjugate()
                            Sa = Va * Ia_star
                            Pa = Sa.real / 1000000
                            Qa = Sa.imag / 1000000
                            n = i.replace('"', '')
                            n = n.replace('-', '_')
                            Entry = 'type=customLoad, name=' + n + '_1ph_' + loadph + ', net_T1=' + conn + ', P=' + str(
                                Pa) + ', Q=' + str(Qa) + ', Vbase=' + str(
                                basevolt/1000) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                            Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 70))
                            Netlist.append(Entry)
                        if ('current_' in configlist):
                            print('Current Load ' + i + ' converted to PQ')
                            Ia = complex(G.nodes[i]['attr']['config']['constant_current_' + loadph])
                            Va = complex(G.nodes[i]['attr']['config']['voltage_' + loadph])
                            Sa = Va * Ia.conjugate()
                            Pa = Sa.real / 1000000
                            Qa = Sa.imag / 1000000
                            n = i.replace('"', '')
                            n = n.replace('-', '_')
                            Entry = 'type=customLoad, name=' + n + '_1ph_' + loadph + ', net_T1=' + conn + ', P=' + str(
                                Pa) + ', Q=' + str(Qa) + ', Vbase=' + str(
                                basevolt/1000) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                            Entry = Entry + str(round(float(G.nodes[i]['attr']['x']))) + ', y=' + str(round(float(G.nodes[i]['attr']['y']) - 80))
                            Netlist.append(Entry)

                        #count = count + 1
                elif (len(loadph) == 2):
                    n = i.replace('"', '')
                    n = n.replace('-', '_')
                    if (pflag == 1):
                        busname = parent.replace('"', '')
                        busname = busname.replace('-', '_')
                    else:
                        busname = n + '_bus'
                    for lp in loadph:
                        conn = n + 'bo' + lp
                        Entry = 'type=bus, name=' + conn + ', baseVolt=' + str(basevolt) + ', nb_phases=' + str(1) + ', lf_type=' + 'PV' + ', '
                        Entry = Entry + 'x=' + str(x) + ', y=' + str(y - 30)
                        Netlist.append(Entry)
                        Entry = 'type=customMUX' + lp.lower() + ', name=MUX' + lp.lower() + str(count) + ', bus=' + busname + ', ph' + lp + '=' + conn + ', Vbase=' + str(
                            basevolt*1.73205080757 / 1000)
                        Entry = Entry + ', hypersim_type=bus2' + lp.lower() + ', hypersim_lib=PNNL Loads.clf, x=' + str(x) + ', y=' + str(y-50)
                        count = count + 1
                        Netlist.append(Entry)
                        S = complex(0)
                        if ('constant_power_' + lp in G.nodes[i]['attr']['config'].keys()):
                            S = S + complex(G.nodes[i]['attr']['config']['constant_power_' + lp])
                        if ('constant_impedance_' + lp in G.nodes[i]['attr']['config'].keys()):
                            print('Impedance Load ' + i + ' converter to PQ')
                            Za = complex(G.nodes[i]['attr']['config']['constant_impedance_' + lp])
                            Va = complex(G.nodes[i]['attr']['config']['voltage_' + lp])
                            S = S + Va * (Va / Za).conjugate()
                        if ('constant_current_' + lp in G.nodes[i]['attr']['config'].keys()):
                            print('Current Load ' + i + ' converted to PQ')
                            Ia = complex(G.nodes[i]['attr']['config']['constant_current_' + lp])
                            Va = complex(G.nodes[i]['attr']['config']['voltage_' + lp])
                            S = S + Va * Ia.conjugate()
                        Entry = 'type=customLoad, name=' + n + '_1ph_' + lp + ', net_T1=' + conn + ', P=' + str(
                            S.real / 1000000) + ', Q=' + str(S.imag / 1000000) + ', Vbase=' + str(
                            basevolt/1000) + ', Frequency=60, hypersim_type=PQsinglephase_solved, hypersim_lib=PNNL Loads.clf, x='
                        Entry = Entry + str(x) + ', y=' + str(y - 60)
                        Netlist.append(Entry)
                    Loads_added = Loads_added + 1
                    Load_addedlist.append(i)


    # Populate link elements
    Lines_added=0
    Xfmr_added=0
    Switch_added=0
    Regulator_added=0
    for i in range(len(Edgelist)):
        u = Edgelist[i][0]
        v = Edgelist[i][1]

        att=Edgelist[i][2]
        xu=float(G.nodes[u]['attr']['x'])
        yu=float(G.nodes[u]['attr']['y'])
        xv = float(G.nodes[v]['attr']['x'])
        yv = float(G.nodes[v]['attr']['y'])
        xline=round(min(xu,xv)+30)
        yline=round(min(yu,yv)+30)
        #print(u+','+v)
        #### NEED TO REWORK THIS SEVERELY add ld_as the check also
        if('Load' in u):
            u=u+'_bus'
        elif('voltage' in G.nodes[u]['attr'].keys()):
            baseVolt=abs(complex(G.nodes[u]['attr']['voltage']))
            # find the loadbus if it has been renamed
        if('Load' in v):
            v = v + '_bus'
            # find the loadbus if it has been renamed
        elif('voltage' in G.nodes[v]['attr'].keys()):
            baseVolt = abs(complex(G.nodes[v]['attr']['voltage']))

        if('component' in att['attr']):
            # Populate overhead lines
            if(att['attr']['component']=='overhead_line' or att['attr']['component']=='underground_line'):
                if ('ABC' in att['attr']['phases']):
                    n = att['attr']['name'].replace('"', '')
                    n = n.replace('-', '_')
                    u = u.replace('"', '')
                    u = u.replace('-', '_')
                    v = v.replace('"', '')
                    v = v.replace('-', '_')
                    Entry='type=line, name='+n+ ', net_1='+u+', net_2='+v+', length='+att['attr']['length']
                    Entry=Entry+', baseVolt='+str(baseVolt*1.73205080757)+', R_matrix='+att['attr']['R']+', L_matrix='+att['attr']['L']+', C_matrix='+att['attr']['C']+', x='+str(xline)+', y='+str(yline)
                    Netlist.append(Entry)
                    Lines_added=Lines_added+1
                else:
                    n = att['attr']['name'].replace('"', '')
                    n = n.replace('-', '_')
                    u = u.replace('"', '')
                    u = u.replace('-', '_')
                    v = v.replace('"', '')
                    v = v.replace('-', '_')
                    Entry='type=customPI, name='+n+', p2='+u+', p1='+v+', R='+att['attr']['R']+', L='+att['attr']['L']+', C=0.1177e-8, Vbase='+str(baseVolt)+', Freq=60, hypersim_type=PI section 1-ph, hypersim_lib=PNNL Loads.clf, x='+str(xline)+', y='+str(yline)
                    Netlist.append(Entry)
                    Lines_added = Lines_added + 1


            if(att['attr']['component']=='transformer'):
                if(len(att['attr']['phases'])>4):
                    config=att['attr']['config']
                    if(config['connect_type']=='WYE_WYE'):
                        connprim='Y ground'
                        connsec='Y ground'
                        u = u.replace('"', '')
                        u = u.replace('-', '_')
                        v = v.replace('"', '')
                        v = v.replace('-', '_')
                        Entry='type=transformer, name='+att['attr']['name']+', n1='+u+', n2='+v+', connexprim='+connprim+', connexsec='+connsec+', Vpri='+str(float(config['primary_voltage'])/1000)+', Vsec='+str(float(config['secondary_voltage'])/1000)
                        Entry=Entry+', Vbasepri='+str(float(config['primary_voltage']))+', Vbasesec='+str(float(config['secondary_voltage']))+', L1='+config['reactance']+', L2=0, Lmag=500, R1='+config['resistance']+', R2=0.05, Rmag=500, pbase='+config['power_rating']+', fbase=60, x='+str(xline)+', y='+str(yline)
                        Netlist.append(Entry)
                        Xfmr_added=Xfmr_added+1
                    else:
                        print('Please convert transformer '+att['attr']['name']+' to wye-wye')
                        #Netlist.append('Placeholder for transformer '+att['attr']['name'])
                        print('Placeholder for transformer '+att['attr']['name'])
                else:
                    # Treat transformer as regulator with limited phases
                    ph=''
                    if('A' in att['attr']['phases']):
                        ph=ph+'A'
                    if ('B' in att['attr']['phases']):
                        ph = ph + 'B'
                    if ('C' in att['attr']['phases']):
                        ph = ph + 'C'

                    if(len(ph)==1):
                        # find the relevant node names 'Nodexxx'+'_ph' for both sides
                        u = u.replace('"', '')
                        u = u.replace('-', '_')
                        v = v.replace('"', '')
                        v = v.replace('-', '_')
                        uu = u + '_' + ph
                        vv = v + '_' + ph
                        for x in range(len(Netlist)):
                            if(uu in Netlist[x]):
                                uu=Netlist[x].split('name=')[1].split(',')[0]
                            if (vv in Netlist[x]):
                                vv = Netlist[x].split('name=')[1].split(',')[0]

                        Entry='type=bus, name=gnd1_'+uu+vv+'reg'+ph+', baseVolt='+str(baseVolt)+', nb_phases=1, lf_type=PV, x='+str(xline-10)+', y='+str(yline-10)
                        Netlist.append(Entry)
                        Entry='type = ground1ph, name = '+'gnd1_'+uu+vv+'reg'+ph+', x = '+str(xline-10)+', y = '+str(yline-10)
                        Netlist.append(Entry)
                        Entry='type=bus, name=gnd2_'+uu+vv+'reg'+ph+', baseVolt='+str(baseVolt)+', nb_phases=1, lf_type=PV, x='+str(xline+40)+', y='+str(yline-10)
                        Netlist.append(Entry)
                        Entry='type = ground1ph, name = '+'gnd2_'+uu+vv+'reg'+ph+', x = '+str(xline-10)+', y = '+str(yline-10)
                        Netlist.append(Entry)

                        Entry='type=regulator, name='+uu+vv+'reg'+ph+', a1='+uu+', a2=gnd1_'+uu+vv+'reg'+ph+', b1=bus632_phase_a, b2=gnd2_'++uu+vv+'reg'+ph+', Vbasesec='+str(float(config['primary_voltage'])/1000)+', Vbaseprim='+str(float(config['secondary_voltage'])/1000)+', Pbase=100, Fbase=60, x='+str(xline)+', y'+str(yline)
                        Netlist.append(Entry)
                        Xfmr_added = Xfmr_added + 1
                    else:
                        print('Two phase transformers not currently supported')
                        #Netlist.append('Placeholder for 2 phase transformer between '+u+' and '+v)
                        print('Placeholder for 2 phase transformer between '+u+' and '+v)

            if(att['attr']['component']=='switch'):
                # Modelled as breaker

                brph=att['attr']['phases']
                if (att['attr']['status']=='CLOSED'):
                    brkstat='1 1 1'
                else:
                    brkstat = '0 0 0'
                if('A' in brph and 'B' in brph and 'C' in brph):
                    n = att['attr']['name'].replace('"', '')
                    n = n.replace('-', '_')
                    u = u.replace('"', '')
                    u = u.replace('-', '_')
                    v = v.replace('"', '')
                    v = v.replace('-', '_')
                    Entry='type=breaker, name='+n+', n1='+u+', n2='+v+', nb_phases=3, imargin=1, init_state=['+brkstat+'], x='+str(xline)+', y='+str(yline)
                    Netlist.append(Entry)
                    Switch_added=Switch_added+1
                elif(G.nodes[v]['attr']['phases']==G.nodes[u]['attr']['phases']):
                    if(att['attr']['status']=='CLOSED'):
                        brkstat='1'
                    else:
                        brkstat = '0'
                    n = att['attr']['name'].replace('"', '')
                    n = n.replace('-', '_')
                    u = u.replace('"', '')
                    u = u.replace('-', '_')
                    v = v.replace('"', '')
                    v = v.replace('-', '_')
                    Entry='type=customSW1ph, name='+n+', net_1='+u+', net_2='+v+', R=0.005, State=['+brkstat+'], hypersim_type=Disconnect Switch, hypersim_lib=Network Switches and Converters.clf, x='
                    Entry=Entry+str(xline)+', y='+str(yline)
                    Netlist.append(Entry)
                    Switch_added = Switch_added + 1
                    #print('Non 3 phase breakers currently not supported '+u+','+v)

            if (att['attr']['component'] == 'regulator'):

                # check phases - should already be split into 1 phase components
                if(len(att['attr']['phases'])==4):
                    # Need to enter 2 grounds and 1 regulator entry
                    if('phase_a' in u):
                        tag='_A'
                    elif('phase_b' in u):
                        tag='_B'
                    elif('phase_c' in u):
                        tag='_C'

                    ground1name='gnd1_reg'+tag
                    ground2name = 'gnd2_reg' + tag

                    Entry='type=bus, name='+ground1name+', baseVolt='+str(baseVolt)+', nb_phases=1, lf_type=PV, x='+str(xline-10)+', y='+str(yline-10)
                    Netlist.append(Entry)
                    Entry='type=ground1ph, name='+ground1name+', x='+str(xline-10)+', y='+str(yline-10)
                    Netlist.append(Entry)
                    Entry = 'type=bus, name=' + ground2name + ', baseVolt=' + str(baseVolt) + ', nb_phases=1, lf_type=PV, x=' + str(xline + 30) + ', y=' + str(yline - 10)
                    Netlist.append(Entry)
                    Entry = 'type=ground1ph, name=' + ground2name + ', x=' + str(xline + 30) + ', y=' + str(yline - 10)
                    Netlist.append(Entry)
                    Entry='type=regulator, name='+att['attr']['name']+tag+', a1='+u+', a2='+ground1name+', b1='+v+', b2='+ground2name+', Vbasesec='+ str(abs(complex(att['attr']['Vbase_sec'])))+', Vbaseprim='+ str(abs(complex(att['attr']['Vbase_prim'])))+', Pbase=100, Fbase=60, x='+str(xline)+', y='+str(yline)
                    Netlist.append(Entry)
                    Regulator_added=Regulator_added+1

    print(str(Nodes_added)+' Nodes populated')
    print(str(Loads_added)+' Loads populated')
    print(str(Capacitors_added)+' Capacitors populated')
    print(str(Inverters_added)+' Inverters populated')
    print(str(DG_Added)+' Diesel generators populated')
    print(str(Lines_added)+' Lines populated')
    print(str(Xfmr_added)+' Transformers populated')
    print(str(Switch_added)+' Switches populated')
    print(str(Regulator_added)+' Regulators populated')




    file=open('model6.netlist','w')
    for line in Netlist:
        file.write(line+"\n")
    file.close()
    x=1


if __name__ == '__main__':
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else None)
