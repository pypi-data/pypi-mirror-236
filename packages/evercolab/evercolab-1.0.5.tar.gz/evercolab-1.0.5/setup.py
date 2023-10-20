from setuptools import setup, find_packages

VERSION = '1.0.5' 
DESCRIPTION = 'Data sharing between projects'
LONG_DESCRIPTION = 'Data sharing between projects'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="evercolab", 
        version=VERSION,
        author="Afendin Ilya",
        author_email="afendin.ilya@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'colabarative'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)