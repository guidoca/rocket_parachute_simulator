from assignment_rl.simulator.integrator import solve_ivp_rk4
import numpy as np
class RK4Integrator(): 
    def __init__(self, 
                 fun         , # ODE
                 t_span      , # [a,b]  Ranges
                 y0          , # Initial state
                 args=None   , # () tuple of additional arguments to ODE
                 t_step=0.1  , # Time step
                 events=None , # Events function
                 **kwargs):  
        if args is None:
            args=()
        if events is None:
            events=()
        self.fun = fun
        self.t_span = t_span
        self.y0 = y0
        self.args = args
        self.t_step = t_step
        self.events = events  
        self.evaluate()
    def evaluate(self): 
         
        t,y=solve_ivp_rk4(fun=self.fun,t_span=self.t_span,y0=self.y0,args=self.args,t_step=self.t_step,events=self.events)
        self.t = t
        self.y = y
        return self
        
        
    