import atexit

# If this is imported, it needs to init SDL, and sdl must only ever be initialized once.
import os
import os.path
import glob
dll_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dlls')
os.environ["PYSDL2_DLL_PATH"] = dll_path
import sdl2
sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
atexit.register(sdl2.SDL_Quit)

#for packing with py2exe:
def find_datafiles():
	"""Returns all the datafiles that must be packaged alongisde this module, along with the appropriate location for each."""
	dll_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dlls')
	dll_files = glob.glob(os.path.join(dll_path, '*'))
	return ('dlls', dll_files)

from .event_responder import *
from .main_loop import *
from .screen import *
from .screen_stack import *
