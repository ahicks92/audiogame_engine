import sdl2

def list_modifiers(key):
	modifier_mask = key.mod
	if modifier_mask == sdl2.KMOD_NONE:
		return []
	MODIFIERS = [sdl2.KMOD_CTRL, sdl2.KMOD_SHIFT, sdl2.KMOD_ALT, sdl2.KMOD_LSHIFT, sdl2.KMOD_RSHIFT, sdl2.KMOD_LALT, sdl2.KMOD_RALT, sdl2.KMOD_LCTRL, sdl2.KMOD_RCTRL, sdl2.KMOD_NUM, sdl2.KMOD_CAPS]
	return [i for i in MODIFIERS if i & modifier_mask != 0]

def sdl_key(keyname):
	for i in dir(sdl2):
		if i.startswith('SDLK_') and (i[5:] == keyname.upper() or i[5:] == keyname.lower()):
			return getattr(sdl2, i)
	raise KeyError("Key %s not found." % keyname)

class KeyboardHandler(object):

	def __init__(self):
		self.pressed = set()
		self.keydown_map= {}
		self.keyup_map = {}
		self.keyheld_map = {}
		self.held_keys = set()

	def register_keydown(self, key, function):
		"""registers a function to be called when a keydown event is received and the key is keycode.

Note that keydown events are continually generated so long as the key keycode is pressed.

:param key: a string representing the key
:param function: The function to call.  This must take one argument.  It is passed a list of the modifiers that were pressed when the key was.  This is a list of the KMOD_* constants from sdl2; the most common of these are KMOD_ALT, KMOD_CTRL, and KMOD_SHIFT.
"""
		self.keydown_map[sdl_key(key)] = function

	def register_keyup(self, key, function):
		"""registers a function to be called when a keyup event is received and the key is keycode.

Exactly one keyup event will be generated for each key release.

:param key: A string representing the key.
:param function: The function to call.  This must take one argument.  It is passed a list of the modifiers that were pressed when the key was.  This is a list of the KMOD_* constants from sdl2; the most common of these are KMOD_ALT, KMOD_CTRL, and KMOD_SHIFT.
"""
		self.keyup_map[sdl_key(key)] = function

	def register_keyheld(self, key, start, end):
		"""Register a pair of funtions to be called, the first when a key is pressed and the second when it is released.
:param key: A string representing the key.
:param start: The function to call when the key is pressed.  This must take one argument.  It is passed a list of the modifiers that were pressed when the key was.  This is a list of the KMOD_* constants from sdl2; the most common of these are KMOD_ALT, KMOD_CTRL, and KMOD_SHIFT.
:param end: The function to call when the key is released.  This must take one argument.  It is passed a list of the modifiers that were pressed when the key was.  This is a list of the KMOD_* constants from sdl2; the most common of these are KMOD_ALT, KMOD_CTRL, and KMOD_SHIFT.
"""
		self.keyheld_map[sdl_key(key)] = start, end

	def process_keydown(self, key):
		key = key.keysym
		symbol = key.sym
		if symbol in self.keydown_map:
			self.keydown_map[symbol](list_modifiers(key))
		if symbol in self.keyheld_map and symbol not in self.held_keys:
			self.keyheld_map[symbol][0](list_modifiers(key))
			self.held_keys.add(symbol)

	def process_keyup(self, key):
		key = key.keysym
		symbol = key.sym
		if symbol in self.keyup_map:
			self.keyup_map[symbol](list_modifiers(key))
		if symbol in self.keyheld_map and symbol in self.held_keys:
			self.keyheld_map[symbol][1](list_modifiers(key))
			self.held_keys.remove(symbol)
