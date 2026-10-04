class Sensor:
    """The agent's only way to observe the environment. The percept contains price,
       ATH, ATL, budget and holdings, but not the hidden regime (partial observability)."""
    def __init__(self, environment):
        self._env = environment

    def sense(self):
        return self._env.getPerception()