from .event_responder import *
from .main_loop import *
from .screen import *
from .screen_stack import *

# If this is imported, it needs to init SDL, and sdl must only ever be initialized once.
SDL_Init(SDL_INIT_VIDEO)
atexit.register(SDL_Quit)
