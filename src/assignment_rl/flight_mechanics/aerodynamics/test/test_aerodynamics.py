from assignment_rl.flight_mechanics.aerodynamics import AerodynamicModel
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.utils import check_error
import unittest 
import numpy as np
class TestAerodynamicModel(unittest.TestCase):

    def setUp(self):
        """
        Test  Atmosphere
        """    
        self.AerodynamicModelDefault = AerodynamicModel()

        
        self.AerodynamicModelOther = AerodynamicModel(dens       =  cd.dens_0   ,  
                                                      V          =  cd.V_0   , 
                                                      c_d        =  cd.c_d_0 , 
                                                      A_r        =  cd.A_r_0 , 
                                                      m          =  cd.m_0   , ) 
        
         
    def test_equal_defaults(self):    
        check_error(self.AerodynamicModelDefault.Da,self.AerodynamicModelOther.Da) 
    def test_zero(self): 
        self.AerodynamicModelOther.evaluate(V=np.zeros(3))
        check_error(self.AerodynamicModelOther.Da,np.zeros(3))
    def test_ballistic_coef(self): 
        K = cd.c_d_0*cd.A_r_0/cd.m_0 
        self.AerodynamicModelOther.evaluate(dens=1.,V=np.array([1.,0.,0.]))
        check_error(self.AerodynamicModelOther.Da,np.array([-K/2,0.,0.]))
    def test_parachute_ballistic_coef_def(self): 
        K = cd.c_d_1*cd.A_r_1/cd.m_1
        self.AerodynamicModelOther=AerodynamicModel(dens       =  0.5   ,  
                                                      V          =  np.array([0.,0.,2.])   , 
                                                      c_d        =  cd.c_d_1 , 
                                                      A_r        =  cd.A_r_1 , 
                                                      m          =  cd.m_1   , ) 
        check_error(self.AerodynamicModelOther.Da,np.array([0,0.,-2*K/2]))
    def test_parachute_ballistic_coef(self): 
        K = cd.c_d_1*cd.A_r_1/cd.m_1
        self.AerodynamicModelOther.evaluate(dens=1.,V=np.array([1.,0.,0.]),
                                                      c_d        =  cd.c_d_1 , 
                                                      A_r        =  cd.A_r_1 , 
                                                      m          =  cd.m_1   , )
        check_error(self.AerodynamicModelOther.Da,np.array([-K/2,0.,0.]))
    def test_vertical_drag(self): 
        K = cd.c_d_0*cd.A_r_0/cd.m_0 
        self.AerodynamicModelOther.evaluate(dens=0.5,V=np.array([0.,0.,2.]))
        check_error(self.AerodynamicModelOther.Da,np.array([0,0.,-2*K/2]))
         
 

if __name__ == '__main__':  # pragma: no cover
    unittest.main()