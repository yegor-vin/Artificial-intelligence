class Actuator:
    def __init__(self, environment):
        """Carries out the agent's chosen action in the environment."""
        self._environment = environment

    def act(self, action):
        self._environment.applyAction(action)