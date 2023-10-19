# -*- coding: utf-8 -*-
'''
EXPOsan: Exposition of sanitation and resource recovery systems

This module is developed by:
    
    Yalin Li <mailto.yalin.li@gmail.com>
    
    Joy Zhang <joycheung1994@gmail.com>

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/EXPOsan/blob/main/LICENSE.txt
for license details.
'''

import os, numpy as np, qsdsan as qs
from biosteam.utils import ignore_docking_warnings
from qsdsan import System
from qsdsan.sanunits import ADMtoASM, ASMtoADM
from exposan.bsm1 import create_system as create_bsm1_system
from exposan.bsm2 import results_path
from exposan.adm import default_init_conds

__all__ = ('create_system',)

# fermenters = ('X_su', 'X_aa', 'X_fa', 'X_c4', 'X_pro')
# methanogens = ('X_ac', 'X_h2')
# biomass_IDs = (*fermenters, *methanogens)

@ignore_docking_warnings # avoid stream replacement warning
def create_system(flowsheet=None):
    flowsheet = flowsheet or qs.Flowsheet('interface')
    qs.main_flowsheet.set_flowsheet(flowsheet)

    bsm1_sys = create_bsm1_system(flowsheet=flowsheet)
    unit = flowsheet.unit
    stream = flowsheet.stream

    thermo_asm1 = qs.get_thermo() # ASM1 components loaded by the bsm1 module
    cmps_asm1 = thermo_asm1.chemicals
    
    # Subsequent units should be using ADM1 components
    cmps_adm1 = qs.processes.create_adm1_cmps()
    thermo_adm1 = qs.get_thermo()
    adm1 = qs.processes.ADM1()
    cmps_adm1.X_I.i_N = cmps_asm1.X_I.i_N    
    
    J1 = ASMtoADM('J1', upstream=stream.WAS, thermo=thermo_adm1, isdynamic=True, adm1_model=adm1) # WAS is C1.outs[2]
    AD1 = qs.sanunits.AnaerobicCSTR('AD1', ins=J1.outs[0], outs=('biogas', 'ad_eff'), isdynamic=True ,model=adm1,                                    
                                    retain_cmps=[i for i in cmps_adm1.IDs if i.startswith('X_')])
    AD1.set_init_conc(**default_init_conds)
    J2 = ADMtoASM('J2', upstream=AD1-1, thermo=thermo_asm1, isdynamic=True, adm1_model=adm1)
    
    # Subsequent units should be using ASM1 components
    qs.set_thermo(thermo_asm1)
    # stream.RWW.disconnect_sink() # disconnect from A1 to avoid replacement warning
    
    # !!! Unsure why the following can work:
    #     S1. Use M1 to mix all streams, then pass to A1
    #     S2. Completely eliminate M1 and directly pass all streams to A1
    #     S3. Use a HydraulicDelay to connect RWW then to A1
    # but the following does not work:
    #     F1. Use M1 to connect RWW then to A1
    #     F2. Use M1 to connect RWW and J2.outs[0] and send both to A1
    # currently setup S1 is used
    A1 = unit.A1
    M1 = qs.sanunits.Mixer('M1',
                           ins=[stream.wastewater, stream.RWW, J2.outs[0], stream.RAS],
                           isdynamic=True)
    A1.ins[0] = M1.outs[0]
    # Otherwise these two spots will be filled with `Stream` insteand of `WasteStream`
    A1.ins[1:] = qs.WasteStream('filler0'), qs.WasteStream('filler1')
    
    sys = flowsheet.create_system('interface_sys')
    sys.set_tolerance(mol=1e-5, rmol=1e-5)
    sys.maxiter = 5000
    sys.set_dynamic_tracker(unit.A1, unit.C1, J1, AD1, J2)
    # sys.set_dynamic_tracker(unit.A1, unit.C1, J1, AD1, J2, M1)
    
    return sys


if __name__ == '__main__':
    t = 50
    t_step = 1
    t_eval = np.arange(0, t+t_step, t_step)
    method = 'BDF'
    sys = create_system()
    sys.simulate(
        state_reset_hook='reset_cache',
        t_span=(0, t),
        # t_eval=t_eval,
        method=method,
        )
    
    # # Just to test a random state
    # states = ('S_su',)
    # AD1 = sys.flowsheet.unit.AD1
    # fig, ax = AD1.scope.plot_time_series(states)
    
    # Output all states, #!!! seems to have problems
    sys.scope.export(os.path.join(results_path, f'states_{t}_{method}.xlsx'), 
                      t_eval=t_eval)