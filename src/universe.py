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

    singleton = None

    def __init__(self):
        self.load()
        self.permute()

    def load(self):
        """Loads universe from UNIVERSE_FILE and checks for errors"""

        dic_candidate = {}
        dic_file = open(UNIVERSE_FILE, 'r')
        dic_candidate = json.loads(dic_file.read())
        dic_file.close()

        vals = list(dic_candidate.values())
        length = lambda i: len(vals[i])

        # attribute categories should have matching lengths
        if any(length(i) != length(i - 1) for i in range(1, len(vals))):
            raise BrokenUniverseException()

        self.dic = dic_candidate

    def permute(self):
        """Creates a list of all possible combinations in the beggining."""

        self.permutations = []
        attributes = self.dic.keys()
        dic_length = len(attributes)

        for i in range(dic_length - 1):
            for j in range(i + 1, dic_length):
                a1, a2 = list(attributes)[i], list(attributes)[j]
                self.permutations += [{x, y}
                    for x in self.dic[a1]
                    for y in self.dic[a2]]

    @staticmethod
    def instance():
        if not Universe.singleton:
            Universe.singleton = Universe()
        return Universe.singleton
