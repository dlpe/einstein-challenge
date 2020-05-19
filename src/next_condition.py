from src.universe import Universe
from src.condition import Condition
from src.unlink_condition import UnlinkCondition
from src.link_condition import LinkCondition


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
            #self.invoke_boundaries()
            #LinkCondition.check_orphans()

    def trigger(self):
        count_a, count_b = 0, 0
        pos_a, pos_b = 0, 0
        permutations = Universe.instance().permutations

        for p in permutations:
            if not any(i.isnumeric() for i in p):
                continue

            if not (self.a in p or self.b in p):
                continue
             
            p1, p2 = list(p)
            position = p1 if p1.isnumeric() else p2

            if self.a in p:
                if ({self.b, str(int(position) + 1)} in permutations or
                    {self.b, str(int(position) - 1)} in permutations):
                    count_a += 1
                    pos_a = position
                else:
                    UnlinkCondition('{} {}'.format(self.a, position))
            else:
                if ({self.a, str(int(position) + 1)} in permutations or
                    {self.a, str(int(position) - 1)} in permutations):
                    count_b += 1
                    pos_b = position
                else:
                    UnlinkCondition('{} {}'.format(self.b, position))

        for count, position, other in (
                (count_a, pos_a, self.b),
                (count_b, pos_b, self.a)):

            if int(count) != 1: continue

            possible_pos = []
            for i in Universe.instance().dic['positions']:
                # is_neighbor = int(i) + 1 == int(position)
                # is_neighbor |= int(i) - 1 == int(position)
                # if is_neighbor: continue

                if int(i) + 1 == int(position):
                    possible_pos.append(i)
                    continue

                if int(i) - 1 == int(position):
                    possible_pos.append(i)
                    continue

                UnlinkCondition("{} {}".format(i, other))

            if len(possible_pos) == 1:
                LinkCondition('{} {}'.format(possible_pos[0], other))

