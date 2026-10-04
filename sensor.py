class Sensor:
    def __init__(self, environment):
        self._env = environment

    def sense(self):
        return self._env.getPerception()