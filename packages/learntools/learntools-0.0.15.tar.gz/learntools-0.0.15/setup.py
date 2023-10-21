from setuptools import setup, find_packages

VERSION = '0.0.15' 
DESCRIPTION = 'Reinforcement Learning with Numpy'
LONG_DESCRIPTION = 'Reinforcement Learning with Numpy'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="learntools", 
        version=VERSION,
        author="William Dennis",
        author_email="wwdennis.home@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['learntools','numpy'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'neural network','learning'],
        
)