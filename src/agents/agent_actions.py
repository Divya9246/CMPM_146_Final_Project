# the conditions + actions the settlement tree is built from
# every function takes ctx = {"settlement": s, "world": w}

from src.agents.agent_constants import (
	MAX_POPULATION, GROWTH_RATE, DECLINE_RATE,
	STATE_GROWING, STATE_STABLE, STATE_DECLINING,
)


# conditions

def is_thriving(ctx):
	# enough food AND water
	return ctx["settlement"].conditions_good()


def is_struggling(ctx):
	# short on food OR water
	return ctx["settlement"].conditions_bad()


def is_in_crisis(ctx):
	return ctx["settlement"].conditions_critical()


def wants_to_migrate(ctx):
	# been in crisis long enough to give up on this spot
	return ctx["settlement"].wants_to_migrate()


# actions

def sense_environment(ctx):
	ctx["settlement"].assess_environment(ctx["world"])


def track_crisis(ctx):
	# count consecutive crisis years, migration uses this
	s = ctx["settlement"]
	if s.conditions_critical():
		s.critical_years += 1
	else:
		s.critical_years = 0


def grow(ctx):
	s = ctx["settlement"]
	s.population = min(MAX_POPULATION, int(s.population * (1 + GROWTH_RATE)) + 1)
	s._transition(ctx["world"], STATE_GROWING)


def decline(ctx):
	s = ctx["settlement"]
	s.population = int(s.population * (1 - DECLINE_RATE))
	s._transition(ctx["world"], STATE_DECLINING)


def hold_steady(ctx):
	# nothing interesting happened this year
	s = ctx["settlement"]
	s._transition(ctx["world"], STATE_STABLE)