from assignment_rl.applications.low_fidelity import low_fidelity 
import os as os 
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
image_dir = os.path.join(os.path.dirname(__file__),'images')
import numpy as np

from assignment_rl.utils import check_error
import unittest  
class TestMonteCarlo0Mean(unittest.TestCase):

    def setUp(self):
        """
        Test  Phase
        """    
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        from tqdm import tqdm
        from functools import partialmethod 
        tqdm.__init__ = partialmethod(tqdm.__init__, disable=True)
        V_0 = np.array([0.,0.,-280.]) 
        self.trajectoryModel,self.monteCarloModel=low_fidelity(Ns=800,V_0=V_0,image_dir=False)
        
    def test_final_landing_mean(self): 
        Rxy=self.monteCarloModel.Rxy
        Rx_m = np.mean(Rxy[:,0])
        Ry_m = np.mean(Rxy[:,1])
        
        check_error(Rx_m ,0.,tol=70) 
        check_error(Ry_m ,0.,tol=55) 
        check_error(self.trajectoryModel.phaseModel_0.R_f ,np.array([0.,self.trajectoryModel.phaseModel_0.R_f[1],cd.h_s])) 
        check_error(self.trajectoryModel.phaseModel_1.R_f ,np.array([0.,self.trajectoryModel.phaseModel_1.R_f[1],cd.h_t])) 
        
if __name__ == '__main__':  # pragma: no cover
    unittest.main()