from src.universe import Universe
from src.condition.base_condition import Condition, InvalidMember

class LinkCondition(Condition):
    """The simplest of conditions is linking two attributes as belonging
       to the same element."""

    link_conditions = []
    Universe.resetters.append(link_conditions)
 
    def __init__(self, expression):
        super().__init__(expression)
        if self not in LinkCondition.link_conditions:
            LinkCondition.link_conditions.append(self)
            self.trigger()

        if self.has_changed():
            LinkCondition.check_orphans()
            self.invoke_boundaries()

    def link(self):
        """Linking two elements means removing the alternatives from the
           universe's permutations list."""

        universe = Universe.instance()
        should_invoke = False

        for element in self.group_a:
            if element == self.a: continue

            for sub_a in Condition.linked_to(element) | {element}:
                if {sub_a, self.b} not in universe.permutations: continue
                universe.permutations.remove({sub_a, self.b})
                should_invoke = True

        for element in self.group_b:
            if element == self.b: continue

            for sub_b in Condition.linked_to(element) | {element}:
                if {sub_b, self.a} not in universe.permutations: continue
                universe.permutations.remove({sub_b, self.a})
                should_invoke = True

        for linked in Condition.linked_to(self.a):
            if linked == self.b: continue
            if (linked, self.b) in LinkCondition.link_conditions: continue
            LinkCondition('{} {}'.format(self.b, linked))

        for linked in Condition.linked_to(self.b):
            if linked == self.a: continue
            if (linked, self.a) in LinkCondition.link_conditions: continue
            LinkCondition('{} {}'.format(self.a, linked))

        return should_invoke

    @staticmethod
    def check_orphans():
        vals = list(Universe.instance().dic.values())
        for i in range(len(vals)):
            for j in range(len(vals)):
                if i == j: continue
                for element in vals[i]:
                    LinkCondition.check_orphaned_element(element, vals[j])

    @staticmethod
    def check_orphaned_element(element, group):
        universe = Universe.instance().permutations
        opts_left = list(filter(lambda i: {element, i} in universe, group))

        links = LinkCondition.link_conditions
        if len(opts_left) == 1 and (opts_left[0], element) not in links:
            LinkCondition("{0} {1}".format(opts_left[0], element))

    def check_valid(self):
        super().check_valid()

        universe = Universe.instance()
        vals = list(i for v in universe.dic.values() for i in v)
        keys = universe.dic.keys()

        for key, group in universe.dic.items():
            if self.a in group and self.b in group:
                raise InvalidMember(self.b)

    def trigger(self):
        super().trigger()
        self.link()
