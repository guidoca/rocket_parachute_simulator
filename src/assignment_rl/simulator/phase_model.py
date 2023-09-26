import numpy as np
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.flight_mechanics import FlightMechanicsModel
from assignment_rl.simulator.integrator import RK4Integrator
from scipy.integrate import solve_ivp
    
    
class PhaseModel(): 
    def __init__(self,
                 *args,    
                 t_0        = cd.t_0     , # [s] Initial Phase Time
                 t_f_max    = cd.t_f_max , # [s] Maximum final time
                 R_0        = cd.R_0     , # [m] Initial phase position
                 V_0        = cd.V_0     , # [m] Initial phase velocity
                 flightMechanics = None  , # Flight Mechanics Model Instance
                 h_e        = cd.h_s     , # [m] Altitude at which event is triggered
                 integrator = None       , # Integration Instance or solve_ivp function
                 flag_evaluate_init=True,  # Flag to evaluate when phase object is initialized
                 **kwargs):  
        self.t_0 = t_0
        self.t_f_max = t_f_max
        self.R_0 = R_0
        self.V_0 = V_0
        self.h_e = h_e
        if flightMechanics is None:
            flightMechanics = FlightMechanicsModel()
        self.flightMechanics= flightMechanics 
        
        if integrator is None:
            integrator = solve_ivp#RK4Integrator
        self.integrator = integrator 
        if flag_evaluate_init:
            self.evaluate()
    def evaluate(self): 
        
        # Define dynamics and parachute deployment event from problem model
        
        def dynamics(t, X,flightMechanicsModel):  
            Rdot,Vdot = flightMechanicsModel.evaluate(t=t,R=X[0:3],V=X[3:6])
            return np.concatenate((Rdot,Vdot))
        def parachute_deployment(t, X,flightMechanicsModel):  
            h = X[2] 
            return h-self.h_e
        parachute_deployment.terminal = True 
    
        # Propagate
        sol = self.integrator(dynamics,
                              [self.t_0, self.t_f_max], 
                              np.concatenate((self.R_0,self.V_0)), 
                              events=parachute_deployment, 
                              args=(self.flightMechanics,),
                              first_step = 0.01,
                              max_step = 1.)
        
        # Retrieve Output
        self.t = sol.t  
        self.R = np.transpose(sol.y[0:3,:])
        self.V = np.transpose(sol.y[3:6,:])
        self.t_f = self.t[-1]
        self.R_f = self.R[-1,:]
        self.V_f = self.V[-1,:]
        return self.t, self.R, self.V
        
        
    