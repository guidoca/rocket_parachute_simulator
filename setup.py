from setuptools import setup 

with open("README.md", "r") as fh:
    long_description = fh.read()
#omitting basics
with open('requirements.txt',encoding='UTF-16') as f: 
    requirements = f.read().splitlines()
    

setup(
   name='assignment_rl',
   version='1.0',
   description='Assignment',
   url='https://github.com/guidoca/assignment_rl.git',
   author='Guillermo J. Dominguez C.', 
   packages=['assignment_rl'], 
   package_dir={'':'src'},
   install_requires=requirements,
)
