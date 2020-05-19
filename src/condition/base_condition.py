from src.universe import Universe


class InvalidMember(Exception):
    """Raised when a condition doesn't meet expected criteria."""

    MSG = "Invalid member {} in condition expression!"

    def __init__(self, member):
        super().__init__(InvalidMember.MSG.format(member))


class NoMatchLeftException(Exception):
    """Raised when a condition is impossible."""

    MSG = "No match for element {}!"

    def __init__(self, element, group):
        super().__init__(NoMatchLeftException.MSG.format((element, group, )))


class Condition(object):
    """Represents a condition and the members to whom it refers to"""

    conditions = []
    Universe.resetters.append(conditions)

    def __init__(self, expression):
        self.set_members(expression)
        self.check_valid()
        Condition.conditions.append(self)
        self.before_perms = len(list(Universe.instance().permutations))

    def __eq__(self, other):
        if isinstance(other, tuple):
            return self.a in other and self.b in other
        if self.__class__.__name__ != other.__class__.__name__:
            return False
        if self.a == other.a and self.b == other.b:
            return True
        if self.b == other.a and self.a == other.b:
            return True

        return False

    def __repr__(self):
        return self.expression

    def has_changed(self):
        return len(list(Universe.instance().permutations)) != self.before_perms

    def set_members(self, expression):
        self.expression = expression
        self.a, self.b = expression.split()

    def check_valid(self):
        universe = Universe.instance()
        vals = list(i for v in universe.dic.values() for i in v)
        keys = universe.dic.keys()

        for m in (self.a, self.b):
            if m not in vals:
                raise InvalidMember(m)

        for key, group in universe.dic.items():
            if self.a in group:
                self.key_a = key
                self.group_a = group
            elif self.b in group:
                self.key_b = key
                self.group_b = group

    def related(self):
        return Condition.linked_to(self.a) | Condition.linked_to(self.b)

    @staticmethod
    def linked_to(element):
        linked_elements = set()
        for group in Universe.instance().dic.values():
            if element in group: continue
            
            possible_combinations = []
            candidate = None

            for item in group:
                if {item, element} in Universe.instance().permutations:
                    candidate = item
                    possible_combinations.append({item, element})

            if len(possible_combinations) == 0:
                raise NoMatchLeftException(element, group)
            elif len(possible_combinations) == 1:
                linked_elements |= {candidate}

        return linked_elements

    def invoke_boundaries(self):
        for boundary in Condition.conditions:
            if boundary != self: boundary.trigger()

    def trigger(self):
        """Trigger method. Should be implemented by boundary 
           type conditions."""
        self.before_perms = len(list(Universe.instance().permutations))

