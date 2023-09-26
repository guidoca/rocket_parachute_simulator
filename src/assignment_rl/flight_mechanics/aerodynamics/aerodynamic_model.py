import numpy as np
import assignment_rl.constants_and_defaults.constants_and_defaults as cd

def drag_acceleration(V,dens,c_d,A_r,m): 
    K = c_d*A_r/m
    
    
    v = np.linalg.norm(V)
    
    q_dyn =  0.5*dens*v**2
    
    Da = -K*0.5*dens*v*V
     
    return Da
    
    
class AerodynamicModel(): 
    def __init__(self,
                 *args,    
                 dens       =  cd.dens_0   , # [kg/m**3] Density
                 V          =  cd.V_0      , # [m(s)] Aerodynamic Speed
                 c_d        =  cd.c_d_0    , # [-] Drag Coefficient
                 A_r        =  cd.A_r_0    , # [m**2] Reference area
                 m          =  cd.m_0      , # [kg] Mass
                 **kwargs):  
        self.dens   = dens
        self.V   = V
        self.c_d = c_d
        self.A_r = A_r
        self.m   = m
        super().__init__(*args,**kwargs)
        self.evaluate()
        
    def evaluate(self,V=None,dens=None,c_d = None,A_r = None,m=None): 
        if V is None:
            V = self.V
        else:
            self.V = V
        if dens is None:
            dens = self.dens
        else:
            self.dens = dens
        if c_d is None:
            c_d = self.c_d
        else:
            self.c_d = c_d
        if A_r is None:
            A_r = self.A_r
        else:
            self.A_r = A_r
        if m is None:
            m = self.m
        else:
            self.m = m
            
        
        Da = drag_acceleration(V=V,dens=dens,c_d = c_d,A_r = A_r,m=m)
        self.Da = Da
        return Da

        
        
    