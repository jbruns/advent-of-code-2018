import sys, collections, time
from itertools import combinations, compress
startTime = time.time()
inputs = [x for x in sys.stdin]

count2 = 0
count3 = 0

for i in inputs:
    charsCount = collections.Counter(i)
    if 3 in charsCount.values():
        count3 += 1
    if 2 in charsCount.values():
        count2 += 1

checksum = count2 * count3
print(count2, "boxIds where a character occurs exactly twice,", count3, "boxIds where a character occurs exactly three times, checksum: ", checksum)
print("part1 time: %s seconds" % (time.time() - startTime))

#part2
# reset the clock
startTime = time.time()
# test all possible combinations of boxIds, 2 at a time
for x, y in combinations(inputs, 2):
    # returns true/false as a single-character comparison between boxIds zipped x/y
    delta = [a == b for a,b in zip(x,y)]
    # test for and then produce a string that is exactly one character different, dropping the different characters from each string
    # sum(delta) = sum of "True"s
    if sum(delta) == (len(x) - 1):
        # use the true/false array as selector for compress() and output it as a consolidated string, rather than a list
        result = ''.join(list(compress(x,delta)))
        # no point in continuing to evaluate as we know we have one string we are looking for
        break
print(result)
print("part2 time: %s seconds" % (time.time() - startTime))