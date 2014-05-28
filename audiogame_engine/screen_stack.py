import event_responder
import collections

class ScreenStack(event_responder.EventResponder, collections.MutableSequence):
	"""Represents a stack of screens.  The screen at the top of the stack receives all events and may choose to let screens below them respond.

Each screen defines special methods (see GameEventResponder).  Unlike GameEventResponder, the methods on the Screen implementation either return true or false:
* If the method returns True, no further processing is done.
* If the method returns false then:
  * If screen.should_propagate is false, no further processing is done; or
  * If screen.should_propagate is True the next screen up in the stack is given the event to process.

In general, this class acts very similarly to a list.
"""

	def __init__(self):
		super(ScreenStack, self).__init__()
		self._screens = []

	def __getitem__(self, key):
		return self._screens[key]

	def __len__(self):
		return len(self._screens)

	def __setitem__(self, key, value):
		oldval = self._screens[key]
		self._screens[key] = value
		if oldval is value:
			value.added_to_stack(self, stack)

	def __delitem__(self, key):
		oldval = self._screens[key]
		del self._screens[key]
		oldval.removed_from_stack(self)

	def insert(self, i, item):
		self._screens.insert(i, item)
		item.added_to_stack(self)

	def push(self, screen):
		"""Push a screen on the top of the stack."""
		self.insert(len(self._screens), screen)

	def is_top(self, screen):
		"returns True if screen is the topmost screen."""
		return self._screens[-1] is screen

	def tick(self, delta):
		#we iterate through the list backwards.
		for i in reversed(xrange(len(self._screens))):
			screen = self._screens[i]
			result = screen.tick(delta)
			if result == False and screen.should_propagate == False:
				break

	def key_down(self, key):
		#we iterate through the list backwards.
		for i in reversed(xrange(len(self._screens))):
			screen = self._screens[i]
			result = screen.key_down(key)
			if result == False and screen.should_propagate == False:
				break

	def key_up(self, key):
		#we iterate through the list backwards.
		for i in reversed(xrange(len(self._screens))):
			screen = self._screens[i]
			result = screen.key_up(key)
			if result == False and screen.should_propagate == False:
				break

	def mouse_button_down(self, button):
		"""Handles mouse buttons being pressed."""
		#we iterate through the list backwards.
		for i in reversed(xrange(len(self._screens))):
			screen = self._screens[i]
			result = screen.mouse_button_down(button)
			if result == False and screen.should_propagate == False:
				break

	def mouse_button_up(self, button):
		"""Handles mouse buttons being released."""
		#we iterate through the list backwards.
		for i in reversed(xrange(len(self._screens))):
			screen = self._screens[i]
			result = screen.mouse_button_up(button)
			if result == False and screen.should_propagate == False:
				break

	def mouse_move(self, x, y):
		"""Handles the mouse moving."""
		#we iterate through the list backwards.
		for i in reversed(xrange(len(self._screens))):
			screen = self._screens[i]
			result = screen.mouse_move(x, y)
			if result == False and screen.should_propagate == False:
				break

	def quit(self):
		#we iterate through the list backwards.
		for i in reversed(xrange(len(self._screens))):
			screen = self._screens[i]
			result = screen.quit()
			if result == False and screen.should_propagate == False:
				break

	def set_associated_loop(self, loop):
		super(ScreenStack, self).set_associated_loop(loop)
		for i in self._screens:
			i.set_associated_loop(loop)

