


import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.simulator import TrajectoryModel, PhaseModel
from assignment_rl.flight_mechanics import FlightMechanicsModel
from assignment_rl.flight_mechanics.atmosphere import LinearAtmosphereModel
from assignment_rl.flight_mechanics.wind import LinearWindModel
from assignment_rl.monte_carlo import MonteCarloModel
from assignment_rl.flight_mechanics.aerodynamics import AerodynamicModel
import matplotlib.pyplot as plt
from copy import deepcopy
import os as os  

def low_fidelity(c_d_0=cd.c_d_0,
                 m_0  =cd.m_0,
                 A_r_0=cd.A_r_0,
                 V_0  =cd.V_0,
                 c_d_1=cd.c_d_1,
                 m_1  =cd.m_1, 
                 A_r_1=cd.A_r_1,
                 Ns   = cd.Ns,
                 image_dir=None,**kwargs):
    if image_dir is None:
        image_dir = os.path.join(os.path.dirname(__file__),'images')
    if image_dir:
        os.makedirs(image_dir,exist_ok=True)
    ################ Define Problem ######################
    ### First phase without parachute

    # Define atmosphere model 
    atmosphere = LinearAtmosphereModel()

    # Define aerodynamics model
    aerodynamics = AerodynamicModel(c_d=c_d_0,m=m_0,A_r=A_r_0)

    # Define wind model 
    wind = LinearWindModel()

    # Define flight mechahnics model
    flightMechanics_0 = FlightMechanicsModel(atmosphere=atmosphere,aerodynamics=aerodynamics,wind=wind)
    # Define phase
    phase_0 = PhaseModel(flightMechanics=flightMechanics_0)

    ### Second Phase with parachute
    # Define atmosphere model 
    atmosphere = LinearAtmosphereModel()

    # Define aerodynamics model
    aerodynamics = AerodynamicModel(c_d=c_d_1,m=m_1,A_r=A_r_1)


    # Define wind model 
    wind = LinearWindModel()

    # Define flight mechahnics model
    flightMechanics_1 = FlightMechanicsModel(atmosphere=atmosphere,aerodynamics=aerodynamics,wind=wind)
    # Define phase
    phase_1 = PhaseModel(flightMechanics=flightMechanics_1)


    #################### Part 1 #########################
    # Construct Trajectory
    trajectoryModel = TrajectoryModel(V_0=V_0,phaseModel_0=phase_0, phaseModel_1=phase_1)


    ## Plot
    t_p0 = trajectoryModel.phaseModel_0.t
    R_p0 = trajectoryModel.phaseModel_0.R
    V_p0 = trajectoryModel.phaseModel_0.V


    t_p1 = trajectoryModel.phaseModel_1.t
    R_p1 = trajectoryModel.phaseModel_1.R
    V_p1 = trajectoryModel.phaseModel_1.V
    if image_dir:
        plt.figure(0) 
        plt.plot(t_p0,R_p0[:,0]/1000,'-',color='r',linewidth=2,label='Before Parachute X')
        plt.plot(t_p0,R_p0[:,1]/1000,'-',color='b',linewidth=2,label='Before Parachute Y')
        plt.plot(t_p0,R_p0[:,2]/1000,'-',color='g',linewidth=2,label='Before Parachute Z')
        plt.plot(t_p1,R_p1[:,0]/1000,'--',color='r',linewidth=2,label='After Parachute X')
        plt.plot(t_p1,R_p1[:,1]/1000,'--',color='b',linewidth=2,label='After Parachute Y')
        plt.plot(t_p1,R_p1[:,2]/1000,'--',color='g',linewidth=2,label='After Parachute Z')
        plt.xlabel('Time [s]')
        plt.ylabel('Position [km]')
        plt.grid(True)
        plt.legend(loc="best")
        plt.savefig(os.path.join(image_dir,'position.jpg'))
        plt.savefig(os.path.join(image_dir,'position.pdf'))

        plt.figure(1)


        plt.plot(t_p0,V_p0[:,0],'-',color='r',linewidth=2,label='Before Parachute X')
        plt.plot(t_p0,V_p0[:,1],'-',color='b',linewidth=2,label='Before Parachute Y')
        plt.plot(t_p0,V_p0[:,2],'-',color='g',linewidth=2,label='Before Parachute Z')
        plt.plot(t_p1,V_p1[:,0],'--',color='r',linewidth=2,label='After Parachute X')
        plt.plot(t_p1,V_p1[:,1],'--',color='b',linewidth=2,label='After Parachute Y')
        plt.plot(t_p1,V_p1[:,2],'--',color='g',linewidth=2,label='After Parachute Z')
        plt.xlabel('Time [s]')
        plt.ylabel('Velocity [m/s]')
        plt.grid(True)
        plt.legend(loc="best")
        plt.savefig(os.path.join(image_dir,'velocity.jpg'))
        plt.savefig(os.path.join(image_dir,'velocity.pdf'))

    ################## Part 2 ###############################
    if os.name == 'posix':
        monteCarloModel = MonteCarloModel(Ns=Ns,trajectoryModel=deepcopy(trajectoryModel))
        
        if image_dir:
            plt.figure(2)

            plt.plot(monteCarloModel.Rxy[:,0]/1000,monteCarloModel.Rxy[:,1]/1000,'*')
            plt.xlabel('Final X Position [km]')
            plt.ylabel('Final Y Position [km]')
            plt.grid(True)
            # plt.legend(loc="best")
            plt.savefig(os.path.join(image_dir,'mc_final_position.jpg'))
            plt.savefig(os.path.join(image_dir,'mc_final_position.pdf'))
    return trajectoryModel , monteCarloModel
        
if __name__ == '__main__':  # pragma: no cover
    low_fidelity()