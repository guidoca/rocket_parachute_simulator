import numpy as np

def solve_ivp_rk4(fun,t_span,y0,args,t_step,events): 
    # Uses RK4 integration to propagate a dynamical system
    # Allows for variable step size
        # fun   function  (dynamic system)
        # y0    Initial State (column vector)
        # time  Time vector (step size obtained here)
        # Param Vector with Parameters for the dynamical problem
    #  Initial values
    t = np.arange(t_span[0],t_span[1],t_step)
    h = np.diff(t)    # [T] Vector of step sizes
    N = len(t)-1   # [ ] Number of steps 
    J = len(y0)       # [ ] Number of equations
    # Create vectors
    y      = np.zeros((J,N+1))  ; 
    y[:,0] = y0
    # Propagation
    for ii in range(N): 
        # for event in events: 
        # If events function is negative, then stop integration
        if events(t[ii] ,y[:,ii],*args)<=0: 
            return t[:ii+1],y[:,:ii+1]
        ydot1 = fun(t[ii] ,y[:,ii],*args)
        ydot2 = fun(t[ii] +h[ii]/2,y[:,ii]+h[ii]/2*ydot1,*args)
        ydot3 = fun(t[ii] +h[ii]/2,y[:,ii]+h[ii]/2*ydot2,*args)
        ydot4 = fun(t[ii] +h[ii],y[:,ii]+h[ii]*ydot3,*args)
        
        ydot  = 1/6*(ydot1+2*ydot2+2*ydot3+ydot4)
        
        y[:,ii+1]  = y[:,ii] + ydot*h[ii] 
    return t, y, 