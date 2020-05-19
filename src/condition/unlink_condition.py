from src.universe import Universe
from src.condition.base_condition import Condition
from src.condition.link_condition import LinkCondition


class UnlinkCondition(Condition):
    """This condition means two attributes do not belong to the same
       element."""

    unlink_conditions = []
    Universe.resetters.append(unlink_conditions)

    def __init__(self, expression):
        super().__init__(expression)
        if self not in UnlinkCondition.unlink_conditions:
            UnlinkCondition.unlink_conditions.append(self)
            self.trigger()

        if self.has_changed():
            self.invoke_boundaries()
            LinkCondition.check_orphans()

    def unlink(self):
        """Linking two elements means removing the alternatives from the
           universe's permutations list."""

        universe = Universe.instance()

        should_invoke = False
        if {self.a, self.b} in universe.permutations:
            universe.permutations.remove({self.a, self.b})
            should_invoke = True

        for el_a in Condition.linked_to(self.a) | {self.a}:
            for el_b in Condition.linked_to(self.b) | {self.b}:
                if (el_a, el_b) in UnlinkCondition.unlink_conditions:
                    continue

                if {el_a, el_b} not in universe.permutations:
                    continue

                UnlinkCondition("{} {}".format(el_a, el_b))

        return should_invoke

    def trigger(self):
        super().trigger()
        self.unlink()
