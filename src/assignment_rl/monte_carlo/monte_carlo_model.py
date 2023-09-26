import numpy as np
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.simulator import TrajectoryModel 
from functools import partial
from multiprocessing import Pool
from tqdm import tqdm 
class MonteCarloModel(): 
    def __init__(self,
                 *args,   
                 Ns                     = cd.Ns ,    # [-] Sampling points
                 theta_w_u              = cd.theta_w_u,# [rad] Uncertain Wind Direction
                 w_s_0_u                = cd.w_s_0_u,# [m/s] Uncertain Wind soeed at surface
                 trajectoryModel        = None  ,  # Trajectory Instance
                 multiprocessing        = True  ,  # [bool] Multiprocessing flag
                 seed                   = 10    ,  # [int] Seed
                 **kwargs):  
        
        self.seed = seed
        self.Ns = Ns
        self.theta_w_u = theta_w_u
        self.w_s_0_u   = w_s_0_u 
        if trajectoryModel is None:
            trajectoryModel = TrajectoryModel()
        self.trajectoryModel= trajectoryModel 
        self.multiprocessing = multiprocessing
        self.evaluate()
    def evaluate(self): 
        
        np.random.seed(self.seed)
        theta_w_all =  np.random.uniform(self.theta_w_u['lb'],self.theta_w_u['ub'],size=self.Ns)
        w_s_0_all   =  np.random.uniform(self.w_s_0_u['lb'],self.w_s_0_u['ub'],size=self.Ns)
        X = zip(theta_w_all, w_s_0_all)
        
        if self.multiprocessing: 
            with Pool(processes=12) as pool:  
                result_list = list(tqdm(pool.imap(partial(MonteCarloModel.uncertainty_model,trajectoryModel=self.trajectoryModel),zip(theta_w_all, w_s_0_all)),total=self.Ns)) 
            Rxy = np.vstack(result_list)
        else:  
            Rxy = np.zeros((self.Ns,2))
            for ii in range(self.Ns): 
                Rxy[ii,:] = MonteCarloModel.uncertainty_model([theta_w_all[ii],w_s_0_all[ii]] ,trajectoryModel=self.trajectoryModel)

        self.Rxy=Rxy
        return Rxy

    @staticmethod 
    def uncertainty_model(X,trajectoryModel): 
        theta_w = X[0]
        w_s_0   = X[1]
        trajectoryModel_ins = trajectoryModel  
        trajectoryModel_ins.phaseModel_0.flightMechanics.wind.theta_w = theta_w
        trajectoryModel_ins.phaseModel_1.flightMechanics.wind.theta_w = theta_w
        
        trajectoryModel_ins.phaseModel_0.flightMechanics.wind.w_s_0 = w_s_0 
        trajectoryModel_ins.phaseModel_1.flightMechanics.wind.w_s_0 = w_s_0
        
        trajectoryModel_ins.evaluate()
        Rxy=trajectoryModel_ins.phaseModel_1.R_f[0:2]
        return Rxy
            
            
        
         
        
        
    