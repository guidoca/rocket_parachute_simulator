from assignment_rl.simulator import PhaseModel
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
        self.PhaseModel = PhaseModel()

        
        self.PhaseModelOther = PhaseModel(t_0=cd.t_0,R_0=cd.R_0,V_0 =  cd.V_0   ,  ) 
         
    def test_equal_defaults(self):    
        check_error(self.PhaseModelOther.R,self.PhaseModel.R) 
        check_error(self.PhaseModelOther.V,self.PhaseModel.V) 
        self.t, self.R, self.V=self.PhaseModelOther.evaluate()
        check_error(self.t,self.PhaseModel.t) 
        check_error(self.R,self.PhaseModel.R) 
        check_error(self.V,self.PhaseModel.V) 
    def test_final_altitude(self):  
        check_error(self.PhaseModelOther.R_f[2],cd.h_s) 


class TestPhaseModelFinishGround(unittest.TestCase):

    def setUp(self):
        """
        Test  Phase
        """  
          
        self.PhaseModelOther = PhaseModel(t_0=cd.t_0,R_0=cd.R_0,V_0 =  cd.V_0   ,h_e=0.  ) 
          
    def test_final_altitude(self):  
        check_error(self.PhaseModelOther.R_f[2],0.) 
        

class TestPhaseGFall(unittest.TestCase):

    def setUp(self):
        """
        Test  Phase
        """    
        flightMechanics=FlightMechanicsModel(aerodynamics=AerodynamicModel(c_d=0.))
        self.PhaseModel = PhaseModel(flightMechanics=flightMechanics,t_0=cd.t_0,R_0=cd.R_0,V_0 =  np.zeros(3)   ,h_e=0.  ) 
          
    def test_final_altitude(self):  
        check_error(self.PhaseModel.R_f[2],0.) 
    def test_time(self):  
        t_fall = np.sqrt(cd.h_top/(0.5*cd.g0))
        check_error(self.PhaseModel.t_f ,t_fall) 
        
class TestPhaseCleanTerminalVelocity(unittest.TestCase):

    def setUp(self):
        """
        Test  Phase
        """    
        self.flightMechanics=FlightMechanicsModel(aerodynamics=AerodynamicModel(c_d=cd.c_d_0,A_r=cd.A_r_0,m=cd.m_0))
        self.flightMechanics.wind.w_s_0=0.
        self.K = self.flightMechanics.aerodynamics.c_d*self.flightMechanics.aerodynamics.A_r/self.flightMechanics.aerodynamics.m
        self.Vt = np.sqrt(2*cd.g0/self.flightMechanics.atmosphere.dens_0/self.K)
        self.PhaseModel = PhaseModel(flightMechanics=self.flightMechanics,t_0=cd.t_0,R_0=cd.R_0,V_0 =  cd.V_0  ,h_e=0.  ) 
          
    def test_final_altitude(self):  
        check_error(self.PhaseModel.R_f[2],0.) 
    def test_speed(self):   
        check_error(self.PhaseModel.V_f ,np.array([0.,0.,-self.Vt]))
    def test_terminal_speed_with_wind(self):   
        self.flightMechanics.wind.w_s_0=10.
        self.flightMechanics.wind.theta_w=0.
        self.PhaseModel = PhaseModel(flightMechanics=self.flightMechanics,t_0=cd.t_0,R_0=cd.R_0,V_0 =  cd.V_0  ,h_e=0.  ) 
        check_error(self.PhaseModel.V_f ,np.array([self.flightMechanics.wind.w_s_0,0.,-self.Vt]))

class TestPhaseCleanTerminalVelocityRK4(unittest.TestCase):

    def setUp(self):
        """
        Test  Phase
        """    
        self.flightMechanics=FlightMechanicsModel(aerodynamics=AerodynamicModel(c_d=cd.c_d_0,A_r=cd.A_r_0,m=cd.m_0))
        self.flightMechanics.wind.w_s_0=0.
        self.K = self.flightMechanics.aerodynamics.c_d*self.flightMechanics.aerodynamics.A_r/self.flightMechanics.aerodynamics.m
        self.Vt = np.sqrt(2*cd.g0/self.flightMechanics.atmosphere.dens_0/self.K)
        self.PhaseModel = PhaseModel(flightMechanics=self.flightMechanics,t_0=cd.t_0,R_0=cd.R_0,V_0 =  cd.V_0  ,h_e=0.  ,
                                     integrator=RK4Integrator) 
          
    def test_final_altitude(self):  
        check_error(self.PhaseModel.R_f[2],0.,tol=5.) 
    def test_speed(self):   
        check_error(self.PhaseModel.V_f ,np.array([0.,0.,-self.Vt]))
    def test_terminal_speed_with_wind(self):   
        self.flightMechanics.wind.w_s_0=10.
        self.flightMechanics.wind.theta_w=0.
        self.PhaseModel = PhaseModel(flightMechanics=self.flightMechanics,t_0=cd.t_0,R_0=cd.R_0,V_0 =  cd.V_0  ,h_e=0.  ) 
        check_error(self.PhaseModel.V_f ,np.array([self.flightMechanics.wind.w_s_0,0.,-self.Vt]))

class TestPhaseParachuteTerminalVelocity(unittest.TestCase):

    def setUp(self):
        """
        Test  Phase
        """    
        self.flightMechanics=FlightMechanicsModel(aerodynamics=AerodynamicModel(c_d=cd.c_d_1,A_r=cd.A_r_1,m=cd.m_1))
        self.flightMechanics.wind.w_s_0=0.
        self.K = cd.c_d_1*cd.A_r_1/cd.m_1
        self.Vt = np.sqrt(2*cd.g0/self.flightMechanics.atmosphere.dens_0/self.K)
        self.PhaseModel = PhaseModel(flightMechanics=self.flightMechanics,t_0=cd.t_0,R_0=cd.R_0,V_0 =  cd.V_0  ,h_e=0.,t_f_max=10000  ) 
          
    def test_final_altitude(self):  
        check_error(self.PhaseModel.R_f[2],0.) 
    def test_speed(self):   
        check_error(self.PhaseModel.V_f ,np.array([0.,0.,-self.Vt]))
    def test_terminal_speed_with_wind(self):   
        self.flightMechanics.wind.w_s_0=10.
        self.flightMechanics.wind.theta_w=0.
        self.PhaseModel = PhaseModel(flightMechanics=self.flightMechanics,t_0=cd.t_0,R_0=cd.R_0,V_0 =  cd.V_0  ,h_e=0.  ) 
        check_error(self.PhaseModel.V_f ,np.array([self.flightMechanics.wind.w_s_0,0.,-self.Vt]))
if __name__ == '__main__':  # pragma: no cover
    unittest.main()