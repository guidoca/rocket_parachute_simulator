from assignment_rl.applications.low_fidelity import low_fidelity 
import os as os 

image_dir = os.path.join(os.path.dirname(__file__),'images')

low_fidelity(image_dir=image_dir)

