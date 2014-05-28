#an interface for a generic game,.

class EventResponder(object):
	"""Responsible for handling a subset of SDL events in a way that abstractts the main game loop.  MainLoop passes SDL events to the functions defined here.  To actually receive input, derive from this class and create a MainLoop passing your derived class into the constructor.  You probably want to use Screen, instead of this class.

There is no need to respond to all types of SDL event; inheriting from this class and not overriding all functions is a reasonable thing to do.

_loop stores the associated MainLoop. This gives access to _loop.quit, the way in which subclasses may end the game."""

	def key_down(self, key):
		"""Called when a key is pressed.
:param key: The key.  This should always be an SDL keyevent.
"""
		pass

	def key_up(self, key):
		"""Called when a key is released.

:param key: The key.  This should always be an SDl key event.
"""
		pass

	def quit(self):
		"""Called when the SDL window closes or when quit is called on the associated MainLoop."""
		pass

	def tick(self, delta):
		"""Called every so often.

:param delta:  The time since the last tick.  Note that this is 0 for the first tick.
"""
		pass

	def set_associated_loop(self, loop):
		"""Internal method used by MainLoop.  Sets _loop to the loop which is feeding us events so that we can ask it to shut down, i.e. quit menus."""
		self._loop = loop
