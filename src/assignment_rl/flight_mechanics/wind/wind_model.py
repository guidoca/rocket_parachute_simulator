from assignment_rl.constants_and_defaults.constants_and_defaults import w_s_0,theta_w
import numpy as np
def wind(theta_w=theta_w,w_s_0=w_s_0):
    
    Vw = w_s_0*np.array([np.cos(theta_w),np.sin(theta_w),0.])
    
    return Vw
    
    
    
class WindModel(): 
    def __init__(self,
                 *args,    
                 theta_w     =  theta_w , # [rad] Wind shear angle
                 w_s_0       =  w_s_0   , # [m/s] Wind shear speed at ground or constant
                 **kwargs):  
        self.theta_w = theta_w
        self.w_s_0   = w_s_0 
        super().__init__(*args,**kwargs)
        self.evaluate()
    def evaluate(self,theta_w=None,w_s_0=None ,**kwargs): 
        if theta_w is None:
            theta_w = self.theta_w
        else:
            self.theta_w = theta_w 
        if w_s_0 is None:
            w_s_0 = self.w_s_0
        else:
            self.w_s_0 = w_s_0 
            
        Vw = wind(theta_w=theta_w,w_s_0=w_s_0)
        self.Vw=Vw
        return Vw

        
        
    