import numpy as np
import assignment_rl.constants_and_defaults.constants_and_defaults as cd

def equations_of_motion_3dof(V,A):
    
    Rdot = V
    
    Vdot = A
     
    return Rdot,Vdot
    
    
class EquationsOfMotion3DoFModel(): 
    def __init__(self,
                 *args,     
                 V          =  cd.V_0   , # [m/s] Velocity
                 A          =  cd.A_d   , # [m/s**2] Acceleration
                 **kwargs):   
        self.V = V
        self.A = A 
        super().__init__(*args,**kwargs)
        self.evaluate()
        
    def evaluate(self,V=None,A = None): 
        if V is None:
            V = self.V
        else:
            self.V = V 
        if A is None:
            A = self.A
        else:
            self.A = A 
            
        
        Rdot, Vdot = equations_of_motion_3dof(V=V,A=A)
        self.Rdot=Rdot
        self.Vdot=Vdot
        return Rdot, Vdot

        
        
    