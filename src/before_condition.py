from src.universe import Universe
from src.condition import Condition
from src.unlink_condition import UnlinkCondition


class BeforeCondition(Condition):
    """This condition means element a comes before element b. It is also
       considered a 'boundary', which means it implements a trigger when
       one of the elements is set to a position."""

    before_conditions = []
    Universe.resetters.append(before_conditions)

    def __init__(self, expression):
        super().__init__(expression)
        if self not in BeforeCondition.before_conditions:
            BeforeCondition.before_conditions.append(self)
            UnlinkCondition(expression)
            UnlinkCondition('1 {}'.format(self.b))
            UnlinkCondition('{} {}'.format(
                Universe.instance().dic['positions'][-1], 
                self.a, ))
            self.trigger()

    def __eq__(self, t):
        if isinstance(t, tuple):
            return self.a in t and self.b in t
        return super().__eq__(t)

    def trigger(self):
        count_a, count_b = 0, 0
        pos_a, pos_b = 0, 0

        for p in Universe.instance().permutations:
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

        for count, position, other, factor in (
                (count_a, pos_a, self.b, -1),
                (count_b, pos_b, self.a, 1)):

            if int(count) != 1: continue

            for i in Universe.instance().dic['positions']:
                is_before = int(i) * factor < int(position)
                if is_before: continue

                UnlinkCondition("{} {}".format(i, other)) 
