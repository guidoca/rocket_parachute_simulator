from assignment_rl.constants_and_defaults.constants_and_defaults import dens_0


    
    
class AtmosphereModel(): 
    def __init__(self,
                 *args,    
                 dens_0       =  dens_0   , # [kg/m**3] Density at Ground or Constant
                 **kwargs):  
        self.dens_0   = dens_0 
        super().__init__(*args,**kwargs)
        self.evaluate()
    def evaluate(self,dens_0=None ,**kwargs): 
        if dens_0 is None:
            dens_0 = self.dens_0
        else:
            self.dens_0 = dens_0 
            
        dens = dens_0
        self.dens = dens
        return dens

        
        
    