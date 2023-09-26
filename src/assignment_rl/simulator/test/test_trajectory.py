from assignment_rl.simulator import PhaseModel , TrajectoryModel
from assignment_rl.simulator.integrator import RK4Integrator
from assignment_rl.flight_mechanics import FlightMechanicsModel
from assignment_rl.flight_mechanics.aerodynamics import AerodynamicModel
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.utils import check_error
import unittest 
import numpy as np
class TestPhaseModelDefault(unittest.TestCase):

    def setUp(self):
        """
        Test  Phase
        """    
        import warnings
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        self.TrajectoryModel = TrajectoryModel()

        self.TrajectoryModelOther = TrajectoryModel(t_0=cd.t_0,R_0=cd.R_0,V_0 =  cd.V_0   , 
                 h_s        = cd.h_s,
                 h_t        = cd.h_t, ) 
         
    def test_equal_defaults(self):    
        check_error(self.TrajectoryModelOther.phaseModel_1.R,self.TrajectoryModel.phaseModel_1.R) 
        check_error(self.TrajectoryModelOther.phaseModel_1.V,self.TrajectoryModel.phaseModel_1.V)  
    def test_final_altitude(self): 
        check_error(float(self.TrajectoryModelOther.phaseModel_1.R_f[2]) ,cd.h_t) 

class TestTrajectory2Integrators(unittest.TestCase):

    def setUp(self):
        """
        Test  Phase
        """    
        self.TrajectoryModel = TrajectoryModel()
        self.TrajectoryModel.phaseModel_0.integrator=RK4Integrator
        self.TrajectoryModel.phaseModel_1.integrator=RK4Integrator
        self.TrajectoryModel.evaluate()

        self.TrajectoryModelOther = TrajectoryModel(t_0=cd.t_0,R_0=cd.R_0,V_0 =  cd.V_0   , 
                 h_s        = cd.h_s,
                 h_t        = cd.h_t, ) 
         
    def test_equal_defaults(self):    
        check_error(self.TrajectoryModelOther.phaseModel_0.R[-1,:],self.TrajectoryModel.phaseModel_0.R[-1,:],tol=5.0) 
        check_error(self.TrajectoryModelOther.phaseModel_0.V[-1,:],self.TrajectoryModel.phaseModel_0.V[-1,:]) 
        check_error(self.TrajectoryModelOther.phaseModel_1.R[-1,:],self.TrajectoryModel.phaseModel_1.R[-1,:],tol=6.) 
        check_error(self.TrajectoryModelOther.phaseModel_1.V[-1,:],self.TrajectoryModel.phaseModel_1.V[-1,:])  
    def test_final_altitude(self):  
        check_error(self.TrajectoryModelOther.phaseModel_1.R_f[2],cd.h_t) 

class TestTrajectoryRandomParachuteTerminalVelocity(unittest.TestCase):

    def setUp(self):
        """
        Test  Phase
        """     
        np.random.seed(20)
        Nsize= 5
        self.Nsize=Nsize
        c_d_1 = np.random.uniform(cd.c_d_1*0.8,cd.c_d_1*1.2,Nsize)
        A_r_1 = np.random.uniform(cd.A_r_1*0.8,cd.A_r_1*1.2,Nsize)
        m_1   = np.random.uniform(cd.m_1*0.8,cd.m_1*1.2,Nsize)
        self.w_s_0 =np.random.uniform(10*0.8,10*1.2,Nsize)
        self.theta_w=np.random.uniform(0,np.pi*2,Nsize)
        self.h_f = np.empty(Nsize)
        self.Vt = np.empty(Nsize)
        self.V_f = np.empty((Nsize,3))
        trajectoryModel = TrajectoryModel(t_0=cd.t_0,R_0=cd.R_0,V_0 =  cd.V_0   , 
                h_s        = cd.h_s,
                h_t        = cd.h_t, ) 
        for ii in range(Nsize):
            trajectoryModel.phaseModel_1.flightMechanics.wind.w_s_0=self.w_s_0[ii]
            trajectoryModel.phaseModel_1.flightMechanics.wind.theta_w=self.theta_w[ii]
            trajectoryModel.phaseModel_1.flightMechanics.aerodynamics=AerodynamicModel(c_d=c_d_1[ii],A_r=A_r_1[ii],m=m_1[ii])
            K = c_d_1[ii]*A_r_1[ii]/m_1[ii]
            self.Vt[ii] = np.sqrt(2*cd.g0/trajectoryModel.phaseModel_1.flightMechanics.atmosphere.dens_0/K)
            trajectoryModel.evaluate()
            self.V_f[ii,:]=trajectoryModel.phaseModel_1.V_f
            self.h_f[ii]=trajectoryModel.phaseModel_1.R_f[2] 
          
    def test_final_altitude(self):  
        check_error(self.h_f,0.) 
    def test_speed(self):   
        for ii in range(self.Nsize):
            V_f_correct=np.array([self.w_s_0[ii]*np.cos(self.theta_w[ii]),self.w_s_0[ii]*np.sin(self.theta_w[ii]),-self.Vt[ii]])
            check_error(self.V_f[ii,:] ,V_f_correct)

class TestTrajectoryNoDrag(unittest.TestCase):

    def setUp(self):
        """
        Test  Phase
        """     
        np.random.seed(3)
        Nsize= 5
        self.Nsize=Nsize
        c_d_1 = 0*np.random.uniform(cd.c_d_1*0.8,cd.c_d_1*1.2,Nsize)
        A_r_1 = np.random.uniform(cd.A_r_1*0.8,cd.A_r_1*1.2,Nsize)
        m_1   = np.random.uniform(cd.m_1*0.8,cd.m_1*1.2,Nsize)
        self.w_s_0 =np.random.uniform(10*0.8,10*1.2,Nsize)
        self.theta_w=np.random.uniform(0,np.pi*2,Nsize)
        self.t_f = np.empty(Nsize)
        self.h_f = np.empty(Nsize)
        self.Vt = np.empty(Nsize)
        self.V_f = np.empty((Nsize,3))
        trajectoryModel = TrajectoryModel(t_0=cd.t_0,R_0=cd.R_0,V_0 =  np.array([1.,2.,0.])   , 
                h_s        = cd.h_s,
                h_t        = cd.h_t, ) 
        for ii in range(Nsize):
            trajectoryModel.phaseModel_1.flightMechanics.wind.w_s_0=self.w_s_0[ii]
            trajectoryModel.phaseModel_1.flightMechanics.wind.theta_w=self.theta_w[ii]
            trajectoryModel.phaseModel_1.flightMechanics.aerodynamics=AerodynamicModel(c_d=c_d_1[ii],A_r=A_r_1[ii],m=m_1[ii])
            trajectoryModel.phaseModel_0.flightMechanics.aerodynamics=AerodynamicModel(c_d=0.,A_r=cd.A_r_0,m=cd.m_0)
              
            trajectoryModel.evaluate()
            self.V_f[ii,:]=trajectoryModel.phaseModel_1.V_f
            self.h_f[ii]=trajectoryModel.phaseModel_1.R_f[2] 
            self.t_f[ii]=trajectoryModel.phaseModel_1.t_f
          
        self.t_fall = np.sqrt(cd.h_top/(0.5*cd.g0))
        self.Vt = self.t_fall*cd.g0
    def test_final_altitude(self):  
        check_error(self.h_f,0.) 
    def test_final_time(self):  
        for ii in range(self.Nsize): 
            check_error(self.t_f[ii] ,self.t_fall)
    def test_speed(self):   
        V_f_correct=np.array([1.,2.,-self.Vt]) 
        for ii in range(self.Nsize):
            check_error(self.V_f[ii,:] ,V_f_correct)
if __name__ == '__main__':  # pragma: no cover
    unittest.main()