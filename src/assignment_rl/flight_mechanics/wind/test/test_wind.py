from assignment_rl.flight_mechanics.wind import WindModel, LinearWindModel
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.utils import check_error
import unittest 
import numpy as np
w_avr = (cd.w_s_0+cd.w_s_top)/2
class TestWindModel(unittest.TestCase):

    def setUp(self):
        """
        Test  Wind
        """    
        self.WindModelDefault = WindModel()

        
        self.WindModelOther = WindModel( w_s_0=cd.w_s_0,theta_w=cd.theta_w)
        
        self.WindModelOther.evaluate(h = cd.R_0[2],)
         
    def test_equal_defaults(self):    
        check_error(self.WindModelDefault.Vw,self.WindModelOther.Vw)
    def test_top_wind(self): 
        check_error(np.linalg.norm(self.WindModelDefault.Vw),cd.w_s_0)
        
class TestLinearWindModel(unittest.TestCase):

    def setUp(self):
        """
        Test Linear Wind
        """    
        self.WindModelDefault = LinearWindModel()

        
        self.WindModelOther = LinearWindModel(h = cd.R_0[2],
                                                          w_s_top=cd.w_s_top,
                                                          h_top=cd.h_top,
                                                          w_s_0=cd.w_s_0,
                                                          theta_w=cd.theta_w)
        
    def test_equal_defaults(self):    
        check_error(self.WindModelDefault.Vw,self.WindModelOther.Vw)
    def test_top_wind(self): 
        check_error(np.linalg.norm(self.WindModelDefault.Vw),cd.w_s_top)
    def test_ground_wind(self): 
        self.WindModelOther.evaluate(h=0.)
        check_error(np.linalg.norm(self.WindModelOther.Vw),cd.w_s_0)
    def test_midway_wind(self): 
        self.WindModelOther.evaluate(h=cd.h_top/2)
        check_error(np.linalg.norm(self.WindModelOther.Vw),w_avr)
    def test_north_wind(self): 
        self.WindModelOther.evaluate(h=cd.h_top/2,theta_w=np.deg2rad(90))
        check_error(self.WindModelOther.Vw,np.array([0.,w_avr,0.]))
    def test_south_wind(self): 
        self.WindModelOther.evaluate(h=cd.h_top/2,theta_w=np.deg2rad(270))
        check_error(self.WindModelOther.Vw,np.array([0.,-w_avr,0.]))
    def test_east_wind(self): 
        self.WindModelOther.evaluate(h=cd.h_top/2,theta_w=np.deg2rad(0))
        check_error(self.WindModelOther.Vw,np.array([w_avr,0.,0.]))
    def test_west_wind(self): 
        self.WindModelOther.evaluate(h=cd.h_top/2,theta_w=np.deg2rad(180))
        check_error(self.WindModelOther.Vw,np.array([-w_avr,0.,0.]))
    def test_incorrectnorth_wind(self):  
        self.WindModelOther.evaluate(h=cd.h_top/2,theta_w=np.deg2rad(377)) 
        try:
            check_error(self.WindModelOther.Vw,np.array([0.,w_avr,0.]))
        except ValueError:
            pass
 

if __name__ == '__main__':  # pragma: no cover
    unittest.main()