import assignment_rl.constants_and_defaults.constants_and_defaults as cd
from assignment_rl.utils import check_error
import unittest 


class TestCheckError(unittest.TestCase):

    def setUp(self):
        """
        Test Check Error
        """     
         
    def test_equal(self):    
        check_error(0.,0.)
    def test_error(self):  
        try:
            check_error(0.,1E-6*10) 
        except ValueError:
            pass
        



if __name__ == '__main__':  # pragma: no cover
    unittest.main()