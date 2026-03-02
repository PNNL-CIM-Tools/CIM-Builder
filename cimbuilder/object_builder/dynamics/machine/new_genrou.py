from __future__ import annotations
import logging
from cimgraph.models import GraphModel
from cimgraph.databases import get_cim_profile
import cimgraph.data_profile.cim17v40 as cim

_log = logging.getLogger(__name__)

def add_genrou_model(network: GraphModel, 
                     sync_machine: cim.SynchronousMachine,
                     h: float = 3.0,
                     d: float = 0.0,
                     ra: float = 0.0,
                     xd: float = 2.1,
                     xq: float = 0.5,
                     xdp: float = 0.2,
                     xqp: float = 0.5,
                     xdpp: float = 0.18,
                     xl: float = 0.15,
                     tdop: float = 7.0,
                     tqop: float = 0.75,
                     tdopp: float = 0.04,
                     tqopp: float = 0.05,
                     s1: float = 0.0,
                     s12: float = 0.0,
                     rcomp: float = 0.0,
                     xcomp: float = 0.0,
                     model_type: str = "roundRotor",
                     enabled: bool = True) -> cim.SynchronousMachineTimeConstantReactance:
    """
    Add a GENROU (Round Rotor Generator) machine model to a synchronous machine.
    
    Args:
        network: The CIM graph model
        sync_machine: The synchronous machine to attach the GENROU model to
        h: Inertia constant (s) - default 3.0
        d: Damping coefficient - default 0.0
        ra: Armature resistance (pu) - default 0.0
        xd: d-axis synchronous reactance (pu) - default 2.1
        xq: q-axis synchronous reactance (pu) - default 0.5
        xdp: d-axis transient reactance (pu) - default 0.2
        xqp: q-axis transient reactance (pu) - default 0.5
        xdpp: d-axis subtransient reactance (pu) - default 0.18
        xl: Leakage reactance (pu) - default 0.15
        tdop: d-axis open circuit transient time constant (s) - default 7.0
        tqop: q-axis open circuit transient time constant (s) - default 0.75
        tdopp: d-axis open circuit subtransient time constant (s) - default 0.04
        tqopp: q-axis open circuit subtransient time constant (s) - default 0.05
        s1: Saturation factor at 1.0 pu - default 0.0
        s12: Saturation factor at 1.2 pu - default 0.0
        rcomp: Resistance for load compensation - default 0.0
        xcomp: Reactance for load compensation - default 0.0
        model_type: Rotor kind (roundRotor or salientPole) - default "roundRotor"
        enabled: Enable the dynamics model - default True
    
    Returns:
        The created GENROU model
    """
    
    cim_profile, cim_module = get_cim_profile()
    cim: cim = cim_module
    
    # Create GENROU model as SynchronousMachineTimeConstantReactance
    genrou = cim.SynchronousMachineTimeConstantReactance(name=f"{sync_machine.name}_GENROU")
    
    # Set enabled flag (from DynamicsFunctionBlock)
    genrou.enabled = enabled
    
    # Set inertia and damping (from RotatingMachineDynamics)
    genrou.inertia = h  # In CIM, this is called 'inertia' not 'h'
    genrou.damping = d
    genrou.statorResistance = ra
    genrou.statorLeakageReactance = xl
    
    # Set model type
    genrou.modelType = model_type  # SynchronousMachineModelKind enumeration
    genrou.rotorType = model_type   # RotorKind enumeration
    
    # Set reactances (per unit)
    genrou.xDirectSync = xd      # xd
    genrou.xQuadSync = xq        # xq
    genrou.xDirectTrans = xdp    # x'd
    genrou.xQuadTrans = xqp      # x'q
    genrou.xDirectSubtrans = xdpp  # x"d
    # Note: xQuadSubtrans (x"q) is not shown in screenshot but typically equals xdpp for round rotor
    
    # Set time constants (seconds)
    genrou.tpdo = tdop           # T'do
    genrou.tpqo = tqop           # T'qo
    genrou.tppdo = tdopp         # T"do
    genrou.tppqo = tqopp         # T"qo
    
    # Set saturation parameters
    # Note: CIM uses saturationFactor, saturationFactor120
    # The diagram shows these should map to machine saturation curve
    
    # Set equivalent circuit parameters
    genrou.ks = 0.0  # Saturation loading correction factor
    genrou.tc = 0.0  # May need to be set based on system requirements
    
    # Associate with synchronous machine
    genrou.SynchronousMachine = sync_machine
    
    # Add to network graph
    network.add_to_graph(genrou)
    
    _log.info(f"Added GENROU model to synchronous machine {sync_machine.name}")
    
    return genrou