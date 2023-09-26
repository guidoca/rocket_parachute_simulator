import numpy as np
from assignment_rl.flight_mechanics.atmosphere import AtmosphereModel
from assignment_rl.constants_and_defaults.constants_and_defaults import dens_top , h_top, R_0

def linear_atmosphere(h,dens_0,dens_top,h_top):
    
    dens = h/h_top*(dens_top - dens_0) + dens_0
     
    return dens
    
    
class LinearAtmosphereModel(AtmosphereModel): 
    def __init__(self,
                 *args,    
                 h        = R_0[2]   , # [m] Altitude
                 dens_top = dens_top , # [kg/m**3] Density at top interpolation point
                 h_top    = h_top    , # [m] Altitude at top interpolation point
                 **kwargs):  
        self.h  = h
        self.dens_top   = dens_top 
        self.h_top      = h_top 
        super().__init__(*args,**kwargs)
    def evaluate(self,h=None,dens_0=None ,dens_top=None ,h_top=None ,**kwargs): 
        if h is None:
            h = self.h
        else:
            self.h = h 
        if dens_0 is None:
            dens_0 = self.dens_0
        else:
            self.dens_0 = dens_0 
        if dens_top is None:
            dens_top = self.dens_top
        else:
            self.dens_top = dens_top 
        if h_top is None:
            h_top = self.h_top
        else:
            self.h_top = h_top 
            
        dens = linear_atmosphere(h=h,dens_0=dens_0,dens_top= dens_top,h_top=h_top)
        self.dens = dens
        return dens

        
        
    