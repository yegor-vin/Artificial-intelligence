class Actuator:
    """Carries out the agent's chosen action in the environment."""
    def __init__(self, environment):
        self._environment = environment

    def act(self, action):
        self._environment.applyAction(action)