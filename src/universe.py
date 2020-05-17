import json
from functools import reduce

UNIVERSE_FILE = 'universe.json'

class BrokenUniverseException(Exception):
    """Raised when universe doesn't make sense."""

    MISMATCHING_LEN = "Length of attributes in dictionary doesn't match!"

    def __init__(self):
        super().__init__(BrokenUniverseException.MISMATCHING_LEN)


class Universe(object):
    """Reads the universe and creates the possible permutations."""

    def __init__(self):
        self.load()
        self.permute()

    def load(self):
        """Loads universe from UNIVERSE_FILE and checks for errors"""

        universe_candidate = {}
        universe_file = open(UNIVERSE_FILE, 'r')
        universe_candidate = json.loads(universe_file.read())
        universe_file.close()

        vals = list(universe_candidate.values())
        length = lambda i: len(vals[i])

        # attribute categories should have matching lengths
        if any(length(i) != length(i - 1) for i in range(1, len(vals))):
            raise BrokenUniverseException()

        self.universe = universe_candidate

    def permute(self):
        """Creates a list of all possible combinations in the beggining."""

        self.permutations = []
        attributes = self.universe.keys()
        universe_length = len(attributes)

        for i in range(universe_length - 1):
            for j in range(i + 1, universe_length):
                a1, a2 = list(attributes)[i], list(attributes)[j]
                self.permutations += [{x, y}
                    for x in self.universe[a1]
                    for y in self.universe[a2]]

