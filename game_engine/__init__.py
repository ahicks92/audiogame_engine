from .event_responder import *
from .main_loop import *
from .screen import *
from .screen_stack import *
import atexit

# If this is imported, it needs to init SDL, and sdl must only ever be initialized once.
import sdl2
sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
atexit.register(sdl2.SDL_Quit)
