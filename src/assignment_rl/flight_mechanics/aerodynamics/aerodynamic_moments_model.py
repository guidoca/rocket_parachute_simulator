import numpy as np
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.flight_mechanics.aerodynamics.aerodynamic_model import AerodynamicModel, drag_acceleration
### NOT WORKING
def normal_acceleration(V,dens,m,U_b,c_n,A_r_n): 
    K_n = c_n*A_r_n/m
    v = np.linalg.norm(V) 
    U_v = V/v
    
    U_p = np.cross(U_v,U_b)
    
    U_n = np.cross(U_p,U_b)
     
    v_r_n = v*np.sin(np.arccos(np.dot(U_v,U_b)))
    Na = 0.5*dens*v_r_n**2*K_n*U_n
def aerodynamic_forces_moments(V,dens,c_d,A_r,m,U_b,c_p,c_g,c_n,A_r_n): 
     
    
    Da = drag_acceleration(V,dens,c_d,A_r,m)
    Na = normal_acceleration(V,dens,m,U_b,c_n,A_r_n)
    
    d_arm = c_p-c_g
    Ma = np.cross(U_b*d_arm,Na)
    
    return Da,Na,Ma
    
    
class AerodynamicWithMomentsModel(AerodynamicModel): 
    def __init__(self,
                 *args,     
                 c_n        =  cd.c_n   , # [-] Normal force Coefficient
                 A_r_n      =  cd.A_r_n , # [m**2] Reference area for normal force
                 c_g        = cd.c_g,
                 c_p        = cd.c_p, 
                 **kwargs):  
        raise NotImplementedError('Not working')
        self.c_p   = c_p
        self.c_g   = c_g
        self.c_n = c_n
        self.A_r_n = A_r_n 
        super().__init__(*args,**kwargs)
        self.evaluate()
        
        
    def evaluate(self,V=None,dens=None,c_d = None,A_r = None,m=None,c_p=None,c_g=None,c_n=None,A_r_n=None): 
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
        if c_p is None:
            c_p = self.c_p
        else:
            self.c_p = c_p
        if c_g is None:
            c_g = self.c_g
        else:
            self.c_g = c_g
        if c_n is None:
            c_n = self.c_n
        else:
            self.c_n = c_n
        if A_r_n is None:
            A_r_n = self.A_r_n
        else:
            self.A_r_n = A_r_n
            
        
        Da,Na,Ma = aerodynamic_forces_moments(V=V,dens=dens,c_d = c_d,A_r = A_r,m=m,c_p=c_p,c_g=c_g,c_n=c_n,A_r_n=A_r_n)
        self.Da = Da
        self.Na = Na
        self.Ma = Ma
        return Da

        
        
    