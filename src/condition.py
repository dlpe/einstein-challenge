from src.universe import Universe

class InvalidMember(Exception):
    """Raised when a condition doesn't meet expected criteria."""

    MSG = "Invalid member {} in condition expression!"

    def __init__(self, member):
        super().__init__(InvalidMember.MSG.format(member))

class Condition(object):
    """Represents a condition and the members to whom it refers to"""

    def __init__(self, expression):
        self.a, self.b = expression.split()
        self.check_valid()
        self.link()

    def check_valid(self):
        universe = Universe.instance()
        vals = list(i for v in universe.dic.values() for i in v)
        keys = universe.dic.keys()

        for m in (self.a, self.b):
            if m not in vals:
                raise InvalidMember(m)

        for key, group in universe.dic.items():
            if self.a in group and self.b in group:
                raise InvalidMember(self.b)
            elif self.a in group:
                self.key_a = key
                self.group_a = group
            elif self.b in group:
                self.key_b = key
                self.group_b = group

    def link(self):
        universe = Universe.instance()
        for p in universe.permutations:
            if self.a in p and self.b not in p:
                if any(i in p for i in self.group_b):
                    universe.permutations.remove(p)
            elif self.b in p and self.a not in p:
                if any(i in p for i in self.group_a):
                    universe.permutations.remove(p)
