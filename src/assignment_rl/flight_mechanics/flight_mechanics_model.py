import numpy as np
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.flight_mechanics.aerodynamics import AerodynamicModel
from assignment_rl.flight_mechanics.atmosphere import AtmosphereModel
from assignment_rl.flight_mechanics.equations_of_motion import EquationsOfMotion3DoFModel
from assignment_rl.flight_mechanics.wind import WindModel

def flight_mechanics(t,R,Vr,g0,atmosphere,aerodynamics,wind,equationsOfMotion):
    
    # Retrieve Altitude
    h = R[2] 
    
    # Evaluate gravity acceleration
    g  = np.array([0.,0.,-g0])
    
    # Evaluate Atmosphere
    dens = atmosphere.evaluate(h=h)
    
    
    # Evaluate Wind
    Vw = wind.evaluate(h=h)
    
    # Compute aerodynamic speed
    Va = Vr - Vw
    
    # Evaluate Aerodynamics
    Da = aerodynamics.evaluate(V=Va,dens=dens)
     
    # Compute total acceleration
    A = g + Da
    
    # Evaluate Equations of Motion
    Rdot , Vdot  = equationsOfMotion.evaluate(V=Vr,A=A)
    return Rdot , Vdot 
    
    
class FlightMechanicsModel(): 
    def __init__(self,
                 *args,    
                 t                 = cd.t_0,  # [s] Time
                 R                 = cd.R_0,  # [m] Position
                 V                 = cd.V_0,  # [m/s] Velocity
                 g0                = cd.g0,   # [m/s**2] Graivty Acceleration
                 atmosphere        = None,    # Atmosphere model instance
                 aerodynamics      = None,    # Aerodynamics model instance
                 wind              = None,    # Wind model instance
                 equationsOfMotion = None,    # Equations of Motion model instance
                 **kwargs):  
        self.t= t
        self.R= R
        self.V= V
        self.g0= g0
        if equationsOfMotion is None:
            equationsOfMotion = EquationsOfMotion3DoFModel()
        self.equationsOfMotion= equationsOfMotion
        if aerodynamics is None:
            aerodynamics = AerodynamicModel()
        self.aerodynamics = aerodynamics
        if wind is None:
            wind = WindModel()
        self.wind = wind
        if atmosphere is None:
            atmosphere = AtmosphereModel()
        self.atmosphere = atmosphere
        self.evaluate()
        
    def evaluate(self,t=None,R=None,V=None): 
        if t is None:
            t=self.t
        else:
            self.t=t
        if R is None:
            R=self.R
        else:
            self.R=R
        if V is None:
            V=self.V
        else:
            self.V=V
        Rdot,Vdot = flight_mechanics(t,R,V,self.g0,self.atmosphere,self.aerodynamics,self.wind,self.equationsOfMotion,)
        self.Rdot=Rdot
        self.Vdot=Vdot
        return Rdot, Vdot
        
        
    