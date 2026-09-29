class Actuator:
    def __init__(self, environment):
        self._environment = environment

    def act(self, action):
        self._environment.applyAction(action)