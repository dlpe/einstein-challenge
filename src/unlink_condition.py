from src.universe import Universe
from src.condition import Condition
from src.link_condition import LinkCondition


class UnlinkCondition(Condition):
    """This condition means two attributes do not belong to the same
       element."""

    unlink_conditions = []
    Universe.resetters.append(unlink_conditions)

    def __init__(self, expression):
        super().__init__(expression)
        if self not in UnlinkCondition.unlink_conditions:
            UnlinkCondition.unlink_conditions.append(self)
            self.unlink()

    def __eq__(self, t):
        if isinstance(t, tuple):
            return self.a in t and self.b in t
        return super().__eq__(t)

    def unlink(self):
        """Linking two elements means removing the alternatives from the
           universe's permutations list."""

        universe = Universe.instance()

        if {self.a, self.b} in universe.permutations:
            universe.permutations.remove({self.a, self.b})
            LinkCondition.check_orphans()

        for el_a in Condition.linked_to(self.a) | {self.a}:
            for el_b in Condition.linked_to(self.b) | {self.b}:
                if (el_a, el_b) in UnlinkCondition.unlink_conditions:
                    continue
                if {el_a, el_b} not in universe.permutations:
                    continue
                UnlinkCondition("{} {}".format(el_a, el_b))

