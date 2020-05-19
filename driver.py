#!/usr/bin/python3

from src import universe
from src.condition import (
    left_condition,
    next_condition,
    link_condition,
    unlink_condition)

perms = universe.Universe.instance().permutations
not_num = lambda s: not s.isnumeric()

def chk():
    print('-' * 20)

    for i in range(1, 6):
        it = (list(filter(not_num, x)) for x in perms if str(i) in x)
        print('{}: {}'.format(i, list(it)))

    print(len(list(perms)))

def wrap(f):
    def ff(exp):
        f(exp)
        chk()
    return ff

link = wrap(link_condition.LinkCondition)
nex = wrap(next_condition.NextCondition)
left = wrap(left_condition.LeftCondition)

link('Brit red')
link('Swede dogs')
link('Dane tea')
left('green white')
link('green coffee')
link('PallMall birds')
link('yellow Dunhill')
link('3 milk')
link('1 Norwegian')
nex('blends cats')
nex('horses Dunhill')
link('BlueMaster beer')
link('German Prince')
nex('Norwegian blue')
nex('blends water')
