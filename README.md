# Einstein Challenge

1 Introduction

1.1 The Zebra Puzzle, Eistein Puzzle, Eistein Riddle, Five Houses Riddle etc

The zebra puzzle is a well-known logic puzzle. Many versions of the puzzle exist, including a version published in Life International magazine on December 17, 1962. The March 25, 1963, issue of Life contained the solution and the names of several hundred successful solvers from around the world.

The puzzle is often called Einstein's Puzzle or Einstein's Riddle because it is said to have been invented by Albert Einstein as a boy; it is also sometimes attributed to Lewis Carroll. However, there is no known evidence for Einstein's or Carroll's authorship and the Life International version of the puzzle mentions brands of cigarette, such as Kools, that did not exist during Carroll's lifetime or Einstein's boyhood.

Source: https://en.wikipedia.org/wiki/Zebra_Puzzle


2 This project

This is a very simple project in Python that I developed in order to tackle this problem. It falls under the category of the Constraint Satisfaction Problems (CSP), which means you are given a number of constraints and you have to find a set up or a set of set ups that can meet all the constraints.


2.1 Basic Usage

If you just want to check out how it works you can read and run driver.py. It simply creates the conditions according to what is described in the original riddle and prints the current status of the universe after each iteration.


2.2 Universe

The universe class and object holds all permutations possible on a given moment after t conditions have been handled. It is represented as a set of sets. In the very beginning, all permutations are possible, so it holds all sets made by crossing the different characteristics e.g. {{'red', 'Brit'}, {'red', 'Dane'}, etc }. The data structure chosen here was a set since the order shouldn't matter and it makes easier for built in comparisons in Python.

The dictionary used to build this universe together with its permutations can be changed in universe.json. Theoretically any set of characteristics could be used instead of houses, colors, nationalities, beverages etc. This can be found in the unit tests. There is a caveat, hoewever, that is the use of numeric values. This will break parts of the code that evaluate if an attribute isnumeric() or not. A small restructuring of the code will make this dispensable so it's bound to be an easy fix.


2.3 Conditions

Here I named all the constraints as conditions during one of my daily lapses of stupidity instead of constraints. They are implicitly separated into a) "Linking and "Unlinking" constraints, i.e. red is Brit or yellow can't have cats, and b) "boundary"constraints, which implement a trigger() method that is called when there's an update to the universe and the constraint should check and update according to its boundaries.

2.3.1 Base Condition

2.3.2 Link Condition

2.3.3 Unlink Condition

2.3.4 Neighbour Condition

2.3.5 Left Condition

2.3.6 Before Condition


2.4 Test Driver

This test driver was built to run the exact conditions of the original riddle while printing the status of the universe after each condition is applied and the number of permutations possible still within it. Should become superfluous once I have the unit tests where I want them, since they are 100% coverage but don't really evaluate the behaviour for all the complex scenarios and preexistent conditions.


2.5 Performance

Yes, performance here is still clearly underwhelming. Consider the status this solution is at right now as a "mold" to perfect the unit tests, that are my real solution here. As soon as my test suite is where I want it to be, playing with the conditions to make them more performatic should be a breeze.

