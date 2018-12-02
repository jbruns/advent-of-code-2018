import itertools, sys, time
frequencies = [int(x) for x in sys.stdin]
print(sum(frequencies))
startTime = time.time()

# initialize frequency counter int at zero and occurrences set at zero
f = 0
o = {0: 1}

for i in itertools.cycle(frequencies):
    # maintain the frequency count as we loop
    f += i
    # add this frequency to the set and increment the number of occurrences for it
    result = o[f] = o.setdefault(f, 0) + 1
    # check to see if this is the first frequency result we've seen twice
    if result == 2:
        print(f)
        print("%s seconds" % (time.time() - startTime))
        break