from src.universe import Universe
from src.condition.base_condition import Condition
from src.condition.unlink_condition import UnlinkCondition
from src.condition.link_condition import LinkCondition


class LeftCondition(Condition):
    """This condition means element a is next to and to the left of element b
       are next to each other. It is also considered a 'boundary', which
       means it implements a trigger when one of the elements is set to
       a position."""

    left_conditions = []
    Universe.resetters.append(left_conditions)

    def __init__(self, expression):
        super().__init__(expression)
        if self not in LeftCondition.left_conditions:
            LeftCondition.left_conditions.append(self)
            UnlinkCondition(expression)
            UnlinkCondition('1 {}'.format(self.b))
            UnlinkCondition('{} {}'.format(
                Universe.instance().dic['positions'][-1],
                self.a, ))
            self.trigger()

        if self.has_changed():
            self.invoke_boundaries()
            LinkCondition.check_orphans()

    def trigger(self):
        super().trigger()
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
                if {self.b, str(int(position) + 1)} in permutations:
                    count_a += 1
                    pos_a = position
                else:
                    UnlinkCondition('{} {}'.format(self.a, position))
            else:
                if {self.a, str(int(position) - 1)} in permutations:
                    count_b += 1
                    pos_b = position
                else:
                    UnlinkCondition('{} {}'.format(self.b, position))

        for count, position, other, factor in (
                (count_a, pos_a, self.b, -1),
                (count_b, pos_b, self.a, 1)):

            if int(count) != 1: continue

            for i in Universe.instance().dic['positions']:
                is_neighbor = int(i) + (1 * factor) == int(position)
                if is_neighbor: continue

                UnlinkCondition("{} {}".format(i, other))

