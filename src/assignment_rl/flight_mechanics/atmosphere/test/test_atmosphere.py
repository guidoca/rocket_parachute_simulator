from assignment_rl.flight_mechanics.atmosphere import AtmosphereModel, LinearAtmosphereModel
import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.utils import check_error
import unittest 

class TestAtmosphereModel(unittest.TestCase):

    def setUp(self):
        """
        Test  Atmosphere
        """    
        self.atmosphereModelDefault = AtmosphereModel()

        
        self.atmosphereModelOther = AtmosphereModel( dens_0=cd.dens_0,)
        
        self.atmosphereModelOther.evaluate(h = cd.R_0[2],)
         
    def test_equal_defaults(self):    
        if self.atmosphereModelDefault.__dict__ != self.atmosphereModelOther.__dict__:
            raise ValueError('Dictionaries not equal' )
    def test_top_density(self): 
        check_error(self.atmosphereModelDefault.dens,cd.dens_0)
        
class TestLinearAtmosphereModel(unittest.TestCase):

    def setUp(self):
        """
        Test Linear Atmosphere
        """    
        self.atmosphereModelDefault = LinearAtmosphereModel()

        
        self.atmosphereModelOther = LinearAtmosphereModel(h = cd.R_0[2],
                                                          dens_top=cd.dens_top,
                                                          h_top=cd.h_top,
                                                          dens_0=cd.dens_0,)
         
    def test_equal_defaults(self):    
        if self.atmosphereModelDefault.__dict__ != self.atmosphereModelOther.__dict__:
            raise ValueError('Dictionaries not equal' )
    def test_top_density(self): 
        check_error(self.atmosphereModelDefault.dens,cd.dens_top)
    def test_ground_density(self): 
        self.atmosphereModelOther.evaluate(h=0.)
        check_error(self.atmosphereModelOther.dens,cd.dens_0)
    def test_midway_density(self): 
        self.atmosphereModelOther.evaluate(h=cd.h_top/2)
        check_error(self.atmosphereModelOther.dens,(cd.dens_0+cd.dens_top)/2)
 

if __name__ == '__main__':  # pragma: no cover
    unittest.main()