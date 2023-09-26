import numpy as np

# Gravity parameters
g0     = 9.81      # [m/s**2] Gravity acceleration at sea level

# Atmosphere parameters
dens_0   = 1.2   # [kg/m**3] Air Density at Sea level
dens_top = 0.02  # [kg/m**3] Air Density at 60 km
h_top    = 60E3  # [km] Top altitude

# Aerodynmic parameters
m_0    = 700           # [kg] Initial stage mass
m_1    = 700           # [kg] Final stage mass
c_d_0  = 1.4           # [-] Clean drag coefficient
c_d_1  = 2.0           # [-] Stage with parachute drag coefficient
A_r_0  = 1.14          # [m**2] Clean Reference area
A_r_1  = 18.0          # [m**2] Stage with parachute reference area

A_d    = np.zeros(3)   # [m/s**2] default acceleration (just used for defaults)  

# Wind parameters
w_s_0      = 15        # [m/s] Wind shear at ground or during descent
w_s_0_u    = {'lb':0,'ub':30.}    # [m/s] Uncertain Wind shear at ground or during descent
w_s_top    = 0.        # [m/s] Wind shear at ground or during descent
theta_w    = np.deg2rad(270.) # [rad] Angle of wind shear  
theta_w_u  = {'lb':0,'ub':np.deg2rad(360)}    #[rad] Uncertain Angle of wind shear 

# Boundary Values
t_0      = 0.                            # [s] Initial time
t_f_max  = np.sqrt(h_top/(0.5*g0))*10    # [s] Maximum Final time
pitch_0  = np.deg2rad(0.)                # [rad] Initial Pitch Angle
yaw_0    = np.deg2rad(0.)                # [rad] Initial Yaw Angle
R_0      = np.array([0.,0.,60E3])        # [m] Initial position 
V_0      = np.array([70.,70.,-280.])     # [m/s] Initial velocity vector     
h_s      = 10E3                          # [m] Swith altitude
h_t      = 0.                            # [m] Termination Altitude

# Infor for Aerodynamic Moments
c_n    = 0.6    # [-] Normal aerodnymic coefficient
A_r_n  = 14.4   # [m**2] Normal reference area
H      = 12.    # [m] Stage height
c_g    = 2.     # [m] Center of gravity from bottom
c_p    = 6.     # [m] Center of pressure from bottom
r_s    = 0.6    # [m] Stage radius
t_s    = 0.8    # [cm] Stage thickness
dens_s = 1940.  # [kg/m**3] Stage density
# mass = dens_s*t_s/100*2*np.pi*r_s
# I_xx = m_0*r_s**2  # Assuming thin hoop
I_xx = (m_0/2) * ((r_s+t_s/100/2)**2+(r_s-t_s/100/2)**2)  # Exact https://amesweb.info/inertia/hollow-cylinder-moment-of-inertia.aspx
# I_yy = m_0*H**2/12 # Assuming thin rod
I_yy = m_0*(3*((r_s+t_s/100/2)**2+(r_s-t_s/100/2)**2) + H**2)/12 + m_0*(c_p-c_g)**2# Exact https://amesweb.info/inertia/hollow-cylinder-moment-of-inertia.aspx


# Monte Carlo sampling Rate
Ns = 200