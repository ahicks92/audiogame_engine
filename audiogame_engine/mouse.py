import sdl2

#this really does have to b written like this. There are other constants with the prefix SDL_BUTTON that aren't mouse buttons.
def sdl_mouse(button):
	button = button.lower()
	if button == 'left': return sdl2.SDL_BUTTON_LEFT
	elif button == 'right': return sdl2.SDL_BUTTON_RIGHT
	elif button == 'middle': return SDL2.SDL_BUTTON_MIDDLE
	else: raise KeyError("Button %s not found" % button)

class MouseHandler(object):
	"""Use this class to be notified about mouse events.  Inheriting from Screen gives you one for free.

recognized mouse buttons are 'left', 'middle', and 'right'.

Actual mouse movements needs to be done by overriding mouse_move on the Screen.  This class does not handle it."""

	def __init__(self):
		self.pressed = set()
		self.buttondown_map = {}
		self.buttonup_map = {}
		self.buttonheld_map = {}
		self.held_buttons = set()
		self.movement_handlers = set()
	def register_buttondown(self, button, function):
		"""registers a function to be called when a mouse button is pressed.

:param button: a string representing the mouse button.
:param function: The function to call.  This must take one argument.  It is passed a list of the modifiers that were pressed when the key was.  This is a list of the KMOD_* constants from sdl2; the most common of these are KMOD_ALT, KMOD_CTRL, and KMOD_SHIFT.
"""
		self.buttondown_map[sdl_mouse(button)] = function

	def register_buttonup(self, button, function):
		"""registers a function to be called when a mouse button is released.

:param button: A string representing the mouse button.
:param function: The function to call.  This must take no arguments.
"""
		self.buttonup_map[sdl_mouse(button)] = function

	def register_buttonheld(self, button, start, end):
		"""Register a pair of funtions to be called, the first when a muse button is pressed and the second when it is released.
:param button: A string representing the button.
:param start: The function to call when the key is pressed.  This must take one argument.  It is passed a list of the modifiers that were pressed when the key was.  This is a list of the KMOD_* constants from sdl2; the most common of these are KMOD_ALT, KMOD_CTRL, and KMOD_SHIFT.
:param end: The function to call when the key is released.  This must take one argument.  It is passed a list of the modifiers that were pressed when the key was.  This is a list of the KMOD_* constants from sdl2; the most common of these are KMOD_ALT, KMOD_CTRL, and KMOD_SHIFT.
"""
		self.buttonheld_map[sdl_key(key)] = start, end

	def process_buttondown(self, button):
		symbol = button.button
		if symbol in self.buttondown_map:
			self.buttondown_map[symbol]()
		if symbol in self.buttonheld_map and symbol not in self.held_buttons:
			self.buttonheld_map[symbol][0]()
			self.held_buttons.add(symbol)

	def process_buttonup(self, button):
		symbol = button.button
		if symbol in self.buttonup_map:
			self.buttonup_map[symbol]()
		if symbol in self.buttonheld_map and symbol in self.held_buttons:
			self.buttonheld_map[symbol][1]()
			self.held_buttons.remove(symbol)

	def register_movement(self, function):
		"""Registers function to be called when the mouse moves.  No guarantees are made as to how often it will be called.  It must take to parameters, x and y.  These will be the amount the mouse has moved since the previous call."""
		self.movement_handlers.add(function)

	def process_mousemove(self, x, y):
		for i in self.movement_handlers:
			i(x, y)
