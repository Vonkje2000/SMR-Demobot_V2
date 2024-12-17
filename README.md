# SMR-Demobot
Demonstration robot for the Smart Manufacturing and Robotics course in The Hague University of Applied Sciences in Delft.

# install dependencies
pip install -r requirements.txt

If there is an error about long paths and you run windows then you need to go to this folder on your computer and run the windows_enable_long_paths.reg as an administrator and restart the installation. 

# error ModuleNotFoundError: No module named 'moviepy.editor'
It will also show a file location that looks something like this
File "C:\Users\anton\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\fer\classes.py", line 7, in <module>
open the file and go to the line number (Here it is 7).
change the line from:
	from moviepy.editor import *
to:
	from moviepy import *

moviepy.editor is deprecated and fer did not change there import so we need to do it our selfs.

# module 'serial' has no attribute 'Serial'
open a teminal and run the commands:
pip uninstall serial
pip install --upgrade --force-reinstall pyserial