from src import universe
from src.condition import (
    left_condition,
    next_condition,
    link_condition,
    unlink_condition)

import copy
from pprint import pprint

def chk():
    print('-------------------------------')
    for i in range(1, 6):
        print(list((list(x)[0] if list(x)[1].isnumeric() else list(x)[1])
              for x in universe.Universe.instance().permutations if str(i) in x))
    print(len(list(universe.Universe.instance().permutations)))

def link(exp):
    link_condition.LinkCondition(exp)
    chk()

def ne(exp):
    next_condition.NextCondition(exp)
    chk()

def left(exp):
    left_condition.LeftCondition(exp)
    chk()

def cant(exp):
    unlink_condition.UnlinkCondition(exp)
    chk()


print('-------------------------------')
link('Brit red')
print('-------------------------------')
link('Swede dogs')
print('-------------------------------')
link('Dane tea')
print('-------------------------------')
left('green white')
print('-------------------------------')
link('green coffee')
print('-------------------------------')
link('PallMall birds')
print('-------------------------------')
link('yellow Dunhill')
print('-------------------------------')
link('3 milk')
print('-------------------------------')
link('1 Norwegian')
print('-------------------------------')
ne('blends cats')
print('-------------------------------')
ne('horses Dunhill')
print('-------------------------------')
link('BlueMaster beer')
print('-------------------------------')
link('German Prince')
print('-------------------------------')
ne('Norwegian blue')
print('-------------------------------')
ne('blends water')


perms = lambda: universe.Universe.instance().permutations
print('-------------------------------')
for i in range(1, 6):
    print(list(x for x in perms() if str(i) in x))
