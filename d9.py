import sys
from collections import defaultdict, deque
from itertools import cycle

inputs = [x for x in sys.stdin.read().split()]
p = int(inputs[0])
lm = int(inputs[6])

# Day 9 "Marble Mania:" an elf game where marbles are arranged in a circle.
# Marbles are numbered starting at 0, =+ 1 until every marble has a number
# The first marble is initially the "current marble".
def marbleGame(p, lm):
    # initialize a defaultdict of marble scores with the default being 0
    elves = defaultdict(int)
    # deque = double-ended queue. this is our game circle. we put 0 into the circle initially to start the game.
    circle = deque([0])
    
    # the game is played using two identifiers per run of this loop:
    # elf: the id of the player. we keep this consistent so that we can track their score. This cycles from 0 to the number of players given by the input.
    # marble: the id of the marble (also the marble's "worth" or score). this starts from 1 (since the initial marble 0 is already in the circle),
    # and continues to the last marble (as defined in the input).
    for elf, marble in zip(cycle(range(p)), range(1, lm+1)):
        # debug: print the current content and order of the deque
        # print(circle)
        # debug: print the marble id currently being evaluated
        # print("marble:",marble)

        # the following conditional statements are a little overcomplicated, but intended to improve
        # readability and explain the game rules:

        # normally, we rotate the circle clockwise (move pointer 1 to the left), and add a new marble 
        # to the circle after the now "current marble". 
        if marble % 23 != 0:
            circle.rotate(-1)
            circle.append(marble)
        
        # per the game rules, if the marble about to be placed has a number which is a multiple of 23:
        elif marble % 23 == 0:
            # -from the current marble (location of circle pointer), move 7 marbles counter-clockwise
            circle.rotate(7)
            # -the player keeps their marble (no circle.append() statement this time), and adds it to their score.
            # -remove this marble, and also add its score (which is returned by the circle.pop() operation)
            # debug: print scoring event details. we retain circle.pop() here so we can use it twice
            i = circle.pop()
            # print("score:",elf,"marble kept:",i)
            elves[elf] += marble + i
            # -finally, rotate the circle clockwise 1 marble to the new current marble.
            circle.rotate(-1)
    
    # we have an 'if scores' conditional here as the game must be long enough to result in a scoring activity (at least one occurrence of marble % 23 == 0).
    return max(elves.values()) if elves else 0

print("inputs:",p,lm)
# helpful visual aid for this game: https://static.aperiodic.net/aoc/2018-09.mp4

# Part 1: what is the winning elf's score?
print("part1 answer:",marbleGame(p,lm))
# Part 2 simply asks, What would the new winning Elf's score be if the number of the last marble were 100 times larger?
print("part2 answer:",marbleGame(p,lm * 100))