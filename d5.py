import sys
inputs = str(sys.stdin.read())

def react(units):
    prevunits = None
    # this part of the function eliminates "reactive" polymers of same letter/opposite case.
    # continue crunching the string until the length does not change.
    while prevunits != units:
        # store the initial string value so we can compare length to ensure something changed
        prevunits = units
        # iterate over the current string value, replacing matching characters aA, Aa thru zZ, Zz with nothing
        for i in range(26):
            # aA..zZ
            units = units.replace(chr(ord("a") + i) + chr(ord("A") + i),"")
            # Aa..Zz
            units = units.replace(chr(ord("A") + i) + chr(ord("a") + i),"")
    # when the length of the units string no longer changes, we are done
    return units

# do the initial reaction before we try removing "bad" polymers
inputs = react(inputs)
# get the initial length, our part1 answer
opt = len(inputs)
print("Part 1 answer:",opt)

# remove a single set of polymers entirely from the string, A..Z and a..z
for i in range(26):
    # reset back to the original input string for length evaluation minus a new polymer
    u2 = inputs
    # remove lowercase polymers one at a time
    u2 = u2.replace(chr(ord("a") + i),"")
    # remove uppercase polymers one at a time
    u2 = u2.replace(chr(ord("A") + i),"")
    # call react, and record the resulting length
    res = len(react(u2))
    # evaluate whether we got a shorter length. if so, store that as the best one so far
    if res < opt:
        opt = res
# when all the possible polymers are eliminated and tested, we have the optimal result
print("Part 2 answer:",opt)
