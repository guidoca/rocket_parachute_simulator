import numpy as np
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.simulator import PhaseModel
    
    
class TrajectoryModel(): 
    def __init__(self,
                 *args,    
                 t_0        = cd.t_0,      # [s] Initial  Time
                 t_f_max    = cd.t_f_max,  # [s] Final  maximum Time
                 R_0        = cd.R_0,      # [m] Initial position 
                 V_0        = cd.V_0,      # [m/s] Initial speed 
                 h_s        = cd.h_s,      # [m] Switching altitude for parachute deployment
                 h_t        = cd.h_t,      # [m] Terminal altitude for touchdown
                 phaseModel_0 = None,      # Phase instance representing simulation without parachute
                 phaseModel_1 = None,      # Phase instance representing simulation with parachute
                 flag_evaluate_init=True,  # Flag to evaluate when trajectory object is initialized
                 **kwargs):  
        self.t_0 = t_0
        self.t_f_max = t_f_max
        self.R_0 = R_0
        self.V_0 = V_0
        self.h_s = h_s,
        self.h_t = h_t
        if phaseModel_0 is None:
            phaseModel_0 = PhaseModel(flag_evaluate_init=False)
        self.phaseModel_0= phaseModel_0
        if phaseModel_1 is None:
            phaseModel_1 = PhaseModel(flag_evaluate_init=False)
        self.phaseModel_1 = phaseModel_1
        if flag_evaluate_init:
            self.evaluate()
        
    def evaluate(self): 
        
        # First Phase
        # Load initial conditions, switching time, and solve phase
        self.phaseModel_0.t_0 = self.t_0
        self.phaseModel_0.R_0 = self.R_0
        self.phaseModel_0.V_0 = self.V_0
        self.phaseModel_0.t_f_max = self.t_f_max 
        self.phaseModel_0.h_e = self.h_s
        self.phaseModel_0.evaluate()
        
        # Second Phase 
        # Link second phase initial conditions with final conditions of first phase and solve
        self.phaseModel_1.t_0 = self.phaseModel_0.t_f
        self.phaseModel_1.R_0 = self.phaseModel_0.R_f
        self.phaseModel_1.V_0 = self.phaseModel_0.V_f
        self.phaseModel_1.t_f_max = self.t_f_max*2 
        self.phaseModel_1.h_e = self.h_t 
        self.phaseModel_1.evaluate()
        
        
        return 
        
        
    