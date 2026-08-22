# small behavior tree framework
# tick the tree once per year, nodes return SUCCESS or FAILURE
# Sequence = AND (stop at first fail), Selector = OR (stop at first success)
# ctx is just a dict like {"settlement": s, "world": w}

SUCCESS = "success"
FAILURE = "failure"


class Node:
	def tick(self, ctx):
		raise NotImplementedError


class Sequence(Node):
	# succeeds only if all children succeed
	def __init__(self, *children):
		self.children = list(children)

	def tick(self, ctx):
		for child in self.children:
			if child.tick(ctx) == FAILURE:
				return FAILURE
		return SUCCESS


class Selector(Node):
	# tries children in order, first one that succeeds wins
	def __init__(self, *children):
		self.children = list(children)

	def tick(self, ctx):
		for child in self.children:
			if child.tick(ctx) == SUCCESS:
				return SUCCESS
		return FAILURE


class Condition(Node):
	# wraps a bool check
	def __init__(self, fn, name=None):
		self.fn = fn
		self.name = name or fn.__name__

	def tick(self, ctx):
		return SUCCESS if self.fn(ctx) else FAILURE


class Action(Node):
	# wraps a function that does something. fails only if it returns False
	def __init__(self, fn, name=None):
		self.fn = fn
		self.name = name or fn.__name__

	def tick(self, ctx):
		result = self.fn(ctx)
		return FAILURE if result is False else SUCCESS


class Inverter(Node):
	# flips the child result, for "if not X" branches
	def __init__(self, child):
		self.child = child

	def tick(self, ctx):
		return FAILURE if self.child.tick(ctx) == SUCCESS else SUCCESS