import sys
from collections import Counter

inputs = []
count = Counter()

# read one line at at time (i) from stdin. working backwards, split the line at the comma, map the results to ints, and return a list to be appended to the overall inputs list.
# this results in a list of lists, each individual list being a coordinate pair [x, y]
for i in sys.stdin.readlines():
    inputs.append(tuple(map(int,i.split(","))))

# define grid bounds
xmin = min([x for x,y in inputs])
xmax = max([x for x,y in inputs])
ymin = min([y for x,y in inputs])
ymax = max([y for x,y in inputs])

# given coords [x1,y1] and [x2,y2], computes Manhattan distance. returns int as all inputs are int. (x1 - x2) + (y1 - y2)
def md(lc1,lc2):
    return int(abs(lc1[0]-lc2[0]) + abs(lc1[1]-lc2[1]))

# true/false: given coords [x,y], x is somewhere between the left and rightmost bounds of the grid, 
# and y is somewhere between the top and bottom bounds
def isInGrid(lc):
    return xmin < lc[0] < xmax and ymin < lc[1] < ymax

# true/false: given Manhattan distance calcs [n1,n2,n3,...], sort ascending such that the closest two distances are evaluated.
# if the distances are different, return true. this eliminates both x and y self-comparisons with the coordinate position being compared.
def isNotSelf(mdc):
    s = sorted(mdc)
    return s[0] != s[1]

# returns the list index value of the closest neighboring coordinate.
def minDist(mdc):
    mdst = min(mdc)
    return mdc.index(mdst)

print("grid bounds:",xmin,"x",ymin,"..",xmax,"x",ymax)

# build a complete distance table between all points within the bounds of the grid, and each coordinate given as input.
# i = somewhere between the bounds of x, j = somewhere within bounds of y, lc = coords [x,y] from the input list
for i in range(xmin,xmax):
    for j in range(ymin,ymax):
        dt = [md((i,j),lc) for lc in inputs]
        # count closest unique neighbors to this position on the grid.
        if isNotSelf(dt):
            count[inputs[minDist(dt)]] += 1

# Part 1: size of the largest area that is finite, or stays within bounds of the grid
opt = int()
for c in inputs:
    # check to see if the area stays within the bounds of the grid
    if isInGrid(c):
        # return the larger of either opt, or the count of grid spaces for this coordinate
        opt = max(opt,count[c])

print("Part1 answer:",opt)

# Part 2: size of region containing all locations where total dist to all input coords is < 10000
# re-using the logic to calc distance between every point on the grid and all the coordinates in the input,
# we calc the sum of all distances and look for each one to be less than 10000. if it is, add 1 to a simple counter.
opt = 0
for i in range(xmin,xmax):
    for j in range(ymin,ymax):
        dt = [md((i,j),c) for c in inputs]
        if sum(dt) < 10000:
            opt += 1

print("Part2 answer:",opt)