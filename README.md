# SMR-Demobot
Demonstration robot for the Smart Manufacturing and Robotics course in The Hague University of Applied Sciences in Delft.

# install dependencies
pip install -r requirements.txt

# error ModuleNotFoundError: No module named 'moviepy.editor'
It will also show a file location that looks something like this
File "C:\Users\anton\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\fer\classes.py", line 7, in <module>
open the file and go to the line number (Here it is 7).
change the line from:
	from moviepy.editor import *
to:
	from moviepy import *

moviepy.editor is deprecated and fer did not change there import so we need to do it our selfs.