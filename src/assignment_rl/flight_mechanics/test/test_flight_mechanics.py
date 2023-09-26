from assignment_rl.flight_mechanics import FlightMechanicsModel
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.utils import check_error
import unittest 
import numpy as np
class TestFlightMechanicsModel(unittest.TestCase):

    def setUp(self):
        """
        Test  Atmosphere
        """    
        self.FlightMechanicsModel = FlightMechanicsModel()

        
        self.FlightMechanicsModelOther = FlightMechanicsModel(t=cd.t_0,R=cd.R_0,V          =  cd.V_0   ,  ) 
         
    def test_equal_defaults(self):    
        check_error(self.FlightMechanicsModelOther.Rdot,self.FlightMechanicsModel.Rdot) 
        check_error(self.FlightMechanicsModelOther.Vdot,self.FlightMechanicsModel.Vdot) 
        self.Rdot,self.Vdot=self.FlightMechanicsModelOther.evaluate()
        check_error(self.Rdot,self.FlightMechanicsModelOther.Rdot) 
    def test_zero(self): 
        self.FlightMechanicsModelOther.evaluate(V=np.zeros(3))
        check_error(self.FlightMechanicsModelOther.Rdot,np.zeros(3))
    def test_north(self): 
        self.FlightMechanicsModelOther.evaluate(V=np.array([3.,0.,0.]))
        check_error(self.FlightMechanicsModelOther.Rdot,np.array([3.,0.,0.]))
    def test_gravity_only(self): 
        self.FlightMechanicsModelOther.wind.w_s_0=0.
        self.FlightMechanicsModelOther.evaluate(V=np.array([0.,0.,0.]))
        check_error(self.FlightMechanicsModelOther.Vdot,np.array([0.,0., -cd.g0]))
    def test_notgravity_only(self): 
        self.FlightMechanicsModelOther.evaluate(V=np.array([0.,0.,0.]))
        try:
            check_error(self.FlightMechanicsModelOther.Vdot,np.array([0.,0., -cd.g0]))
        except ValueError:
            pass
    def test_eastwind_and_gravity_only(self): 
        self.FlightMechanicsModelOther.atmosphere.dens_0=1.
        self.FlightMechanicsModelOther.wind.theta_w=np.deg2rad(180)
        self.FlightMechanicsModelOther.wind.w_s_0=2.
        self.FlightMechanicsModelOther.evaluate(V=np.array([0.,0.,0.]))
        K = self.FlightMechanicsModelOther.aerodynamics.c_d*self.FlightMechanicsModelOther.aerodynamics.A_r/self.FlightMechanicsModelOther.aerodynamics.m
 
        check_error(self.FlightMechanicsModelOther.Vdot,np.array([-K*2,0, -cd.g0]))
        
    # def test_ballistic_coef(self): 
    #     K = cd.c_d_0*cd.A_r_0/cd.m_0 
    #     self.AerodynamicModelOther.evaluate(dens=1.,V=np.array([1.,0.,0.]))
    #     check_error(self.AerodynamicModelOther.Da,np.array([-K/2,0.,0.]))
         
 

if __name__ == '__main__':  # pragma: no cover
    unittest.main()