import numpy as np

def check_error(val1,val2,tol=1e-6): 
    error = np.abs(val1 - val2)  
    error = np.atleast_1d(error).flatten() 
    for err in error:
        if err>tol:
            raise ValueError('Error between values is large '+ str(err) )