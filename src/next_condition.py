from src.universe import Universe
from src.condition import Condition
from src.unlink_condition import UnlinkCondition


class InvalidPairException(Exception):
    def __init__(self, pair):
        super().__init__('Invalid pair {0, 1}'.format(pair))

class NextCondition(Condition):
    """This condition means element a and element b are next to each other
       in any order. It is also considered a 'boundary', which means it
       implements a trigger when one of the elements is set to a position."""

    next_conditions = []
    Universe.resetters.append(next_conditions)

    def __init__(self, expression):
        super().__init__(expression)
        if self not in NextCondition.next_conditions:
            NextCondition.next_conditions.append(self)
            UnlinkCondition(expression)
            self.trigger()

    def __eq__(self, t):
        if isinstance(t, tuple):
            return self.a in t and self.b in t
        return super().__eq__(t)

    def trigger(self):
        count_a, count_b = 0, 0
        pos_a, pos_b = 0, 0

        for p in Universe.instance().permutations:
            if all(i.isnumeric() for i in p):
                raise InvalidPairException(p)

            if not any(i.isnumeric() for i in p):
                continue

            if not (self.a in p or self.b in p):
                continue
             
            p1, p2 = list(p)
            position = p1 if p1.isnumeric() else p2

            if self.a in p:
                count_a += 1
                pos_a = position
            else:
                count_b += 1
                pos_b = position

        for count, position, other in (
                (count_a, pos_a, self.b),
                (count_b, pos_b, self.a)):

            if int(count) != 1: continue

            for i in Universe.instance().dic['positions']:
                is_neighbor = int(i) + 1 == int(position)
                is_neighbor |= int(i) - 1 == int(position)

                if is_neighbor: continue

                UnlinkCondition("{} {}".format(i, other)) 
