# clone the python_RVO2 repository
$ git clone https://github.com/sybrenstuvel/Python-RVO2.git


#Building requires [CMake](http://cmake.org/) and [Cython](http://cython.org/) to be installed.
#Run 
$ pip install -r requirements.txt          #to install the tested version of Cython, 
#or 
#Run
$ pip install Cython                          #to install the latest version.

#Run 
$ python setup.py build                     # to build, and 
$ python setup.py install                   # to install.

#Alternatively, if you want an in-place build that puts the compiled library right in
#the current directory, run 
$ python setup.py build_ext --inplace

##Only tested with Python 2.7, 3.4,3.6 and 3.10.12 on Ubuntu Linux. The setup.py script uses CMake to build
##the RVO2 library itself, before building the Python wrappers.

#To build on Mac OSX, give an `export MACOSX_DEPLOYMENT_TARGET=10.xx` command first, before
#running `python setup.py build`. Replace `10.xx` with your version of OSX, for example `10.11`.


----------------------------------
# Install pygame
$ pip install pygame

#Run the python File
python3 imple_pygame.py
