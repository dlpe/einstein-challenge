from src.universe import Universe
from src.condition import Condition


class LinkCondition(Condition):
    """The simplest of conditions is linking two attributes as belonging
       to the same element."""

    link_conditions = []
    def __init__(self, expression):
        super().__init__(expression)
        LinkCondition.link_conditions.append(self)
        self.link()

    def __eq__(self, t):
        if isinstance(t, tuple):
            return self.a in t and self.b in t
        return super().__eq__(t)

    def link(self):
        """Linking two elements means removing the alternatives from the
           universe's permutations list."""

        universe = Universe.instance()

        for element in self.group_a:
            if element == self.a: continue
            if {element, self.b} not in universe.permutations: continue
            universe.permutations.remove({element, self.b})

        for element in self.group_b:
            if element == self.b: continue
            if {element, self.a} not in universe.permutations: continue
            universe.permutations.remove({element, self.a})

        for linked in Condition.linked_to(self.a):
            if linked == self.b: continue
            if (linked, self.b) in LinkCondition.link_conditions: continue
            LinkCondition('{} {}'.format(self.b, linked))
        for linked in Condition.linked_to(self.b):
            if linked == self.a: continue
            if (linked, self.a) in LinkCondition.link_conditions: continue
            LinkCondition('{} {}'.format(self.a, linked))

        for boundary in Condition.conditions:
            if boundary.a in self.related() or boundary.b in self.related():
                boundary.trigger()

