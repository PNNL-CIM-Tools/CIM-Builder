import logging
import cimgraph.data_profile.cimhub_2023 as cim
from cimgraph.models import FeederModel
from cimbuilder.object_builder import new_analog, new_discrete
from cimgraph.databases import ConnectionParameters, RDFlibConnection
_log = logging.getLogger(__name__)

def create_all_analog_measurements(feeder_model: FeederModel):
    cim = feeder_model.cim


    analogs = FeederModel(container = cim.Feeder(), connection = feeder_model.connection, distributed=False)
    feeder_model.get_all_edges(cim.EnergyConsumer)
    feeder_model.get_all_edges(cim.EnergyConsumerPhase)
    feeder_model.get_all_edges(cim.PowerElectronicsConnection)
    feeder_model.get_all_edges(cim.PowerElectronicsConnectionPhase)
    feeder_model.get_all_edges(cim.LinearShuntCompensator)
    feeder_model.get_all_edges(cim.LinearShuntCompensatorPhase)
    feeder_model.get_all_edges(cim.SynchronousMachine)
    feeder_model.get_all_edges(cim.PowerTransformer)
    feeder_model.get_all_edges(cim.PowerTransformerEnd)
    feeder_model.get_all_edges(cim.TransformerTank)
    feeder_model.get_all_edges(cim.TransformerTankEnd)

    switch_classes = [cim.Breaker, cim.Sectionaliser,
                cim.Recloser, cim.LoadBreakSwitch, cim.Switch]
    
    for sw_cls in switch_classes:
        feeder_model.get_all_edges(sw_cls)

    feeder_model.get_all_edges(cim.Terminal)

    for inverter in feeder_model.graph.get(cim.PowerElectronicsConnection,{}).values():
        for power_electronics_unit in inverter.PowerElectronicsUnit:
            if isinstance(power_electronics_unit, cim.PhotovoltaicUnit):
                if inverter.PowerElectronicsConnectionPhases:
                    for inverter_phase in inverter.PowerElectronicsConnectionPhases:
                        phase = cim.PhaseCode(inverter_phase.phase.value)
                        for terminal in inverter.Terminals:
                            new_analog(analogs, inverter, terminal, phase, 'VA')
                            new_analog(analogs, inverter, terminal, phase, 'PNV')

                else:
                    for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                        for terminal in inverter.Terminals:
                            new_analog(analogs, inverter, terminal, phase, 'VA')
                            new_analog(analogs, inverter, terminal, phase, 'PNV')

            elif isinstance(power_electronics_unit, cim.BatteryUnit):
                if inverter.PowerElectronicsConnectionPhases:
                
                    for inverter_phase in inverter.PowerElectronicsConnectionPhases:
                            phase = cim.PhaseCode(inverter_phase.phase.value)
                            for terminal in inverter.Terminals:
                                new_analog(analogs, inverter, terminal, phase, 'VA')
                                new_analog(analogs, inverter, terminal, cim.PhaseCode.none, 'SoC')

                else:
                    for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                        for terminal in inverter.Terminals:
                            new_analog(analogs, inverter, terminal, phase, 'VA')
                            new_analog(analogs, inverter, terminal, phase, 'PNV')
                            new_analog(analogs, inverter, terminal, cim.PhaseCode.none, 'SoC')

    for capacitor in feeder_model.graph.get(cim.LinearShuntCompensator, {}).values():
        if capacitor.ShuntCompensatorPhase:
            for capacitor_phase in capacitor.ShuntCompensatorPhase:
                name = f'LinearShuntCompensator_{capacitor.name}'
                for terminal in capacitor.Terminals:
                    phase = cim.PhaseCode(capacitor_phase.phase.value)
                    new_analog(analogs, capacitor, terminal, phase, 'PNV', name)
                    new_analog(analogs, capacitor, terminal, phase, 'VA', name)

        else:
            for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                name = f'LinearShuntCompensator_{capacitor.name}'
                for terminal in capacitor.Terminals:
                    if int(terminal.sequenceNumber) == 1:
                        new_analog(analogs, capacitor, terminal, phase, 'PNV', name)
                        new_analog(analogs, capacitor, terminal, phase, 'VA', name)

    for load in feeder_model.graph.get(cim.EnergyConsumer, {}).values():
        name = f'EnergyConsumer_{load.name}'
        if load.EnergyConsumerPhase:
            for load_phase in load.EnergyConsumerPhase:
                for terminal in load.Terminals:
                    phase = cim.PhaseCode(load_phase.phase.value)
                    new_analog(analogs, load, terminal, phase, 'PNV', name)
                    new_analog(analogs, load, terminal, phase, 'VA', name)

        else:
            for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                for terminal in load.Terminals:
                    if int(terminal.sequenceNumber) == 1:
                        new_analog(analogs, load, terminal, phase, 'PNV', name)
                        new_analog(analogs, load, terminal, phase, 'VA', name)

    for generator in feeder_model.graph.get(cim.SynchronousMachine, {}).values():
        for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:  
            #CIM standard for SynchronousMachines assume transmission level so three phase only at this point.
            for terminal in generator.Terminals:
                new_analog(analogs, generator, terminal, phase, 'VA')
                new_analog(analogs, generator, terminal, phase, 'PNV')

    for transformer in feeder_model.graph.get(cim.PowerTransformer, {}).values():
        for transformer_tank in transformer.TransformerTanks:
            for tank_end in transformer_tank.TransformerTankEnds:
                terminal = tank_end.Terminal
                name = f'TransformerTank_{transformer.name}_Power'
                phases = tank_end.orderedPhases.value
                if "A" in phases:
                    # new_analog(analogs, transformer, terminal, cim.PhaseCode.A, 'PNV')
                    if int(terminal.sequenceNumber) == 1:
                        new_analog(analogs, transformer, terminal, cim.PhaseCode.A, 'VA', name)
                elif "B" in phases:
                    # new_analog(analogs, transformer, terminal, cim.PhaseCode.B, 'PNV')
                    if int(terminal.sequenceNumber) == 1:
                        new_analog(analogs, transformer, terminal, cim.PhaseCode.B, 'VA', name)
                elif "C" in phases:
                    # new_analog(analogs, transformer, terminal, cim.PhaseCode.C, 'PNV')
                    if int(terminal.sequenceNumber) == 1:
                        new_analog(analogs, transformer, terminal, cim.PhaseCode.C, 'VA', name)
                elif "s1" in phases:
                    # new_analog(analogs, transformer, terminal, cim.PhaseCode.C, 'PNV')
                    if int(terminal.sequenceNumber) == 1:
                        new_analog(analogs, transformer, terminal, cim.PhaseCode.s1, 'VA', name)
                elif "s2" in phases:
                    # new_analog(analogs, transformer, terminal, cim.PhaseCode.C, 'PNV')
                    if int(terminal.sequenceNumber) == 1:
                        new_analog(analogs, transformer, terminal, cim.PhaseCode.s2, 'VA', name)

        for power_transformer_end in transformer.PowerTransformerEnd:
            terminal = power_transformer_end.Terminal
            name = f'PowerTransformer_{transformer.name}_Power'

            for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                if int(terminal.sequenceNumber) in [1, 2]:
                    new_analog(analogs, transformer, terminal, phase, 'PNV')
                    new_analog(analogs, transformer, terminal, phase, 'VA', name)

    for cim_class in switch_classes:
        for switch in feeder_model.graph.get(cim_class, {}).values():
            if switch.SwitchPhase:
                for switch_phase in switch.SwitchPhase:
                    for terminal in switch.Terminals:
                        if int(terminal.sequenceNumber) == 1:
                            phase = cim.PhaseCode(switch_phase.phaseSide1.value)
                            new_analog(analogs, switch, terminal, phase, 'PNV')
                            new_analog(analogs, switch, terminal, phase, 'A')
                        elif int(terminal.sequenceNumber) == 2:
                            phase = cim.PhaseCode(switch_phase.phaseSide2.value)
                            new_analog(analogs, switch, terminal, phase, 'PNV')
            else:
                for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                    for terminal in switch.Terminals:
                        if int(terminal.sequenceNumber) == 1:
                            new_analog(analogs, switch, terminal, phase, 'PNV')
                            new_analog(analogs, switch, terminal, phase, 'A')
                        elif int(terminal.sequenceNumber) == 2:
                            new_analog(analogs, switch, terminal, phase, 'PNV')

    for line in feeder_model.graph.get(cim.ACLineSegment, {}).values():
        for ac_line_segment_phase in line.ACLineSegmentPhases:  #don't add current and SoC measurements for lines
            for terminal in line.Terminals:
                if terminal.sequenceNumber == 1:
                    phase = cim.PhaseCode(ac_line_segment_phase.phase.value)
                    new_analog(analogs, line, terminal, phase, 'VA')
                    new_analog(analogs, line, terminal, phase, 'PNV')
    return analogs

def create_all_discrete_measurements(feeder_model: FeederModel):
    cim = feeder_model.cim


    discretes = FeederModel(container = cim.Feeder(), connection = feeder_model.connection, distributed=False)

    
    switch_classes = [cim.Breaker, cim.Sectionaliser,
                cim.Recloser, cim.LoadBreakSwitch, cim.Switch]
    counter = 0
    for cim_class in switch_classes:
        for switch in feeder_model.graph.get(cim_class, {}).values():
            if switch.SwitchPhase:
                for switch_phase in switch.SwitchPhase:
                    for terminal in switch.Terminals:
                        if int(terminal.sequenceNumber) == 1:
                            phase = cim.PhaseCode(getattr(switch_phase,'phaseSide'+str(terminal.sequenceNumber)).value)
                            new_discrete(discretes, switch, terminal, phase, 'Pos')
                            counter += 1
                            
            else:
                for terminal in switch.Terminals:
                    if int(terminal.sequenceNumber) == 1:
                        new_discrete(discretes, switch, terminal, cim.PhaseCode.A, 'Pos')
                        new_discrete(discretes, switch, terminal, cim.PhaseCode.B, 'Pos')
                        new_discrete(discretes, switch, terminal, cim.PhaseCode.C, 'Pos')
                        counter += 3

    _log.info(f'Created {counter} Discrete measurements for Switch objects')

    counter = 0
    for capacitor in feeder_model.graph.get(cim.LinearShuntCompensator, {}).values():
        if capacitor.ShuntCompensatorPhase:
            for shuntCompensatorPhase in capacitor.ShuntCompensatorPhase:
                phase = cim.PhaseCode(shuntCompensatorPhase.phase.value)
                for terminal in capacitor.Terminals:
                    new_discrete(discretes, capacitor, terminal, phase, 'Pos')
                    counter += 1
        else:
            for phase in [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]:
                for terminal in capacitor.Terminals:
                    meas = new_discrete(discretes, capacitor, terminal, phase, 'Pos')
                    counter += 1
    _log.info(f'Created {counter} Discrete measurements for Capacitor objects')
                    

    counter = 0
    for transformer in feeder_model.graph.get(cim.PowerTransformer, {}).values():
        isRegulator = False
        for powerTransformerEnd in transformer.PowerTransformerEnd:
            if powerTransformerEnd.RatioTapChanger is not None:
                isRegulator = True
                break
        if isRegulator:
            for powerTransformerEnd in transformer.PowerTransformerEnd:
                if int(powerTransformerEnd.Terminal.sequenceNumber) == 1:
                    phases = [cim.PhaseCode.A, cim.PhaseCode.B, cim.PhaseCode.C]
                    for phase in phases:
                        new_discrete(discretes, transformer, terminal, phase, 'Pos')
                        counter += 1

            for transformerTank in transformer.TransformerTanks:
                for transformerTankEnd in transformerTank.TransformerTankEnds:
                    if int(transformerTankEnd.Terminal.sequenceNumber) == 1:
                        phase = transformerTankEnd.orderedPhases.value.replace("N","")
                        phase = cim.PhaseCode(phase)
                        new_discrete(discretes, transformer, terminal, phase, 'Pos')
                        counter += 1
    _log.info(f'Created {counter} Discrete measurements for Recloser objects')
    return discretes