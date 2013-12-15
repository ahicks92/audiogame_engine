import sdl2
import sdl2.ext
import time
import atexit # a convenient way to deinitialize SDL

class MainLoop(object):
	"""The main loop is the heart of a game.  This class is responsible for creating a game window, dispatching SDL events, and periodically calling tick on the associated GameEventResponder."""

	def __init__(self, event_responder, title="untitled", size=(800, 600)):
		"""Initialize the GameLoop.
:param event_responder:  Any object meeting the GameEventResponder interface.  This object shall be notified of SDL events.
:param title: The title of the window this game loop creates when run.
:param size: the size of the window.
"""
		self._title = title
		self._size = size
		self._event_responder = event_responder
		self._event_responder.set_associated_loop(self)

	def run(self, tick_speed = 1/60.0):
		"""Runs the game loop.

:param tick_speed: How often to tick.
"""
		self._window = sdl2.SDL_CreateWindow(self._title, SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, self._size[0], self._size[1], SDL_WINDOW_RESIZABLE | SDL_WINDOW_HIDDEN)
		self._renderer = sdl2.SDL_CreateRenderer(self._window, -1, 0)
		self._running = True
		delta = 0 #used to record the time it takes the loop to run.
		sdl2.SDL_ShowWindow(self._window)
		sdl2.SDL_SetRelativeMouseMode(True)
		while(self._running):
			start_time = time.time()
			self._event_responder.tick(delta) #time since the last time tick was called.  This should always be very close to tick_speed.  If the loop takes longer to run than tick_speed, this will increase accordingly.
			events = sdl2.ext.get_events()
			for event in events:
				if event.type == SDL_QUIT:
					self.quit() #this is responsible for handling quitting.  No need to do anything else.
				elif event.type == SDL_KEYDOWN:
					self._event_responder.key_down(event.key)
				elif event.type == SDL_KEYUP:
					self._event_responder.key_up(event.key)
				elif event.type == SDL_MOUSEMOTION:
					self._event_responder.mouse_move(event.motion.xrel, event.motion.yrel)
				elif event.type == SDL_MOUSEBUTTONDOWN:
					self._event_responder.mouse_button_down(event.button)
				elif event.type == SDL_MOUSEBUTTONUP:
					self._event_responder.mouse_button_up(event.button)
			end_time = time.time()
			processing_time = end_time-start_time
			sdl2.SDL_RenderPresent(self._renderer)
			sdl2.SDL_SetRenderDrawColor(self._renderer, 0, 0, 0, 255)
			sdl2.SDL_RenderClear(self._renderer)
			#this lets us see the framerate.
			sdl2.SDL_SetWindowTitle(self._window, self._title + " " + str( 1 / delta if delta > 0 else 0))
			if tick_speed - processing_time >= 0:
				time.sleep(tick_speed-processing_time)
			delta = time.time()-start_time
		sdl2.SDL_DestroyRenderer(self._renderer)
		sdl2.SDL_DestroyWindow(self._window)

	def quit(self, should_notify_responder = True):
		"""Stops the game loop.

:param should_notify_responder: Whether or not to notify the GameEventResponder that we are quitting.
"""
		if should_notify_responder:
			self._event_responder.quit()
		self._running = False

	@property
	def event_responder(self):
		"""The associated GameEventResponder.  Read-only."""
		return self._event_responder
