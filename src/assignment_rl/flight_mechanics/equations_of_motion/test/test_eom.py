from assignment_rl.flight_mechanics.equations_of_motion import EquationsOfMotion3DoFModel
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.utils import check_error
import unittest 
import numpy as np
class TestAEquationsOfMotion3DoFModel(unittest.TestCase):

    def setUp(self):
        """
        Test  Atmosphere
        """    
        self.EquationsOfMotion3DoFModel = EquationsOfMotion3DoFModel()

        
        self.EquationsOfMotion3DoFModelOther = EquationsOfMotion3DoFModel(V          =  cd.V_0   , A          =  cd.A_d ,   ) 
         
    def test_equal_defaults(self):    
        check_error(self.EquationsOfMotion3DoFModelOther.Rdot,self.EquationsOfMotion3DoFModel.Rdot) 
        check_error(self.EquationsOfMotion3DoFModelOther.Vdot,self.EquationsOfMotion3DoFModel.Vdot) 
        self.Rdot,self.Vdot=self.EquationsOfMotion3DoFModelOther.evaluate()
        check_error(self.Rdot,self.Rdot) 
    def test_zero(self): 
        self.EquationsOfMotion3DoFModelOther.evaluate(V=np.zeros(3))
        check_error(self.EquationsOfMotion3DoFModelOther.Rdot,np.zeros(3))
    def test_north_a(self): 
        self.EquationsOfMotion3DoFModelOther.evaluate(A=np.array([3.,0.,0.]))
        check_error(self.EquationsOfMotion3DoFModelOther.Vdot,np.array([3.,0.,0.]))
    # def test_ballistic_coef(self): 
    #     K = cd.c_d_0*cd.A_r_0/cd.m_0 
    #     self.AerodynamicModelOther.evaluate(dens=1.,V=np.array([1.,0.,0.]))
    #     check_error(self.AerodynamicModelOther.Da,np.array([-K/2,0.,0.]))
         
 

if __name__ == '__main__':  # pragma: no cover
    unittest.main()