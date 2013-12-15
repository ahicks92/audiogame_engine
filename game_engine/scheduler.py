
class Scheduler(object):

	def __init__(self):
		self.tasks = set()

	def tick(self, delta):
		for task in self.tasks:
			task.tick(delta)
			if task.should_run():
				task.run()
				if not task.repeating:
					self.tasks.remove(task)

	def schedule(self, function, delay=0.0, repeating=False, *args, **kwargs):
		"""Schedule a task to run on the scheduler.
:param function:  The callable to schedule for future execution.
:param delay: The minimum time in seconds which should pass before this callable is called.
:param repeating: Should this task be called repeatedly.
:param *args: Positional arguments to be passed to the function when it is called.
:param **kwargs: Keyword arguments to be passed to the function when it is called.
"""
		task = ScheduledTask(function=function, delay=delay, repeating=repeating, *args, **kwargs)
		self.tasks.add(task)

class ScheduledTask(object):

	def __init__(self, function=None, delay=0.0, repeating=False, *args, **kwargs):
		self.delay = delay
		self.repeating = repeating
		self.function = function
		self.args = args
		self.kwargs = kwargs
		self.elapsed = 0

	def tick(self, delta):
		self.elapsed += delta

	def should_run(self):
		return self.elapsed >= self.delay

	def run(self):
		self.function(*self.args, **self.kwargs)
