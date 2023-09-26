import numpy as np
from assignment_rl.flight_mechanics.wind import WindModel, wind
from assignment_rl.constants_and_defaults.constants_and_defaults import  w_s_top , h_top, R_0

def linear_wind(h,theta_w,w_s_0,w_s_top,h_top):
    
    w_s = h/h_top*(w_s_top - w_s_0) + w_s_0
    
    Vw = wind(theta_w,w_s)
    return Vw
    
    
class LinearWindModel(WindModel): 
    def __init__(self,
                 *args,    
                 h        = R_0[2]   , # [m] Altitude
                 w_s_top  = w_s_top  , # [m/s] Wind shear speed at top or interpolation altitude
                 h_top    = h_top    , # [m] Altitude at top interpolation point
                 **kwargs):  
        self.h          = h
        self.w_s_top    = w_s_top 
        self.h_top      = h_top 
        super().__init__(*args,**kwargs)
    def evaluate(self,h=None,theta_w=None ,w_s_0=None,w_s_top=None ,h_top=None ,**kwargs): 
        if h is None:
            h = self.h
        else:
            self.h = h 
        if theta_w is None:
            theta_w = self.theta_w
        else:
            self.theta_w = theta_w 
        if w_s_0 is None:
            w_s_0 = self.w_s_0
        else:
            self.w_s_0 = w_s_0 
        if w_s_top is None:
            w_s_top = self.w_s_top
        else:
            self.w_s_top = w_s_top 
        if h_top is None:
            h_top = self.h_top
        else:
            self.h_top = h_top 
            
        Vw = linear_wind(h=h,theta_w=theta_w,w_s_0=w_s_0,w_s_top= w_s_top,h_top=h_top)
        self.Vw=Vw
        return Vw

        
        
    