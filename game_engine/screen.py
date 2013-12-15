import event_responder
import keyboard
import mouse

class Screen(event_responder.EventResponder):
	"""Provides basic input handling and ticking functionality.

All methods from the GameEventResponder interface should either return True or False.  If they return True, they handled the event and no further processing is done.
if they return False and the property should_propagate is True, the parent screen also gets  a chance to process the event.  This also holds true for tick--it is trivial to make menus that allow gameplay to continue by returning true for the menu keystrokes but false for the tick.  Should_propagate is False by default.

All of the default implementations provided here return false.
"""

	def __init__(self):
		super(Screen, self).__init__()
		self.keyboard_handler = keyboard.KeyboardHandler()
		self.mouse_handler = mouse.MouseHandler()
		self._tickers = set()
		self._should_propagate = False
		self._associated_stack = None

	def key_down(self, key):
		self.keyboard_handler.process_keydown(key)

	def key_up(self, key):
		self.keyboard_handler.process_keyup(key)

	def mouse_button_down(self, button):
		"""Called when a mouse button is pressed.

:param button: an SDL_MouseButton event.
"""
		self.mouse_handler.process_buttondown(button)

	def mouse_button_up(self, button):
		"""Called when a mouse button is released.

:param button: An SDL_MouseButton event.
"""
		self.mouse_handler.process_buttonup(button)

	def mouse_move(self, x, y):
		"""Called when the mouse moves.  X and y are relative to the mouse's last position."""
		self.mouse_handler.process_mousemove(x, y)

	def tick(self, delta):
		for ticker in self._tickers:
			ticker.tick(delta)
		return False

	def removed_from_stack(self):
		"""Called when this screen is removed from a ScreenStack."""
		self._associated_stack = None

	def added_to_stack(self, stack):
		"""Called when this screen is added to a ScreenStack."""
		self._associated_stack = stack

	def register_ticker(self, ticker):
		"""Adds a ticker, an object which wishes to have tick called on it every game tick.  Each ticker should be an object with a method tick(delta); delta is the time since the last game tick."""
		self._tickers.add(ticker)

	def unregister_ticker(self, ticker):
		"""Removes ticker from the list of objects to have their tick method called every tick.  If ticker is not in the list, silently does nothing."""
		if ticker in self._tickers:
			self._tickers.remove(ticker)

	@property
	def should_propagate(self):
		"""Whether or not screens higher in this screen's ScreenStack should see events this screen doesn't handle>"""
		return self._should_propagate

	@should_propagate.setter
	def should_propagate(self, value):
		self._should_propagate = value

	@property
	def associated_stack(self):
		"""The ScreenStack which this screen is a part of.  Read-only"""
		return self._associated_stack

