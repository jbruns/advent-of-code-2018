import sys, time
from collections import defaultdict
inputs = [x for x in sys.stdin]
coordinateGrid = defaultdict(int)

for a in inputs:
    a1 = a.split(" ")
    # #1 @ 265,241: 16x26
    print("parsing claim", a1[0], a1[2])
    x,y = a1[2].split(",")
    x,y = int(x), int(y[:-1])
    w,h = a1[3].split("x")
    w,h = int(w), int(h)
    print("X=",x,"Y=",y,"width=",w,"height=",h)
    for gridx in range(w):
        for gridy in range(h):
            coordinateGrid[(x+gridx),(y+gridy)] += 1

for a in inputs:
    a1 = a.split(" ")
    x,y = a1[2].split(",")
    x,y = int(x), int(y[:-1])
    w,h = a1[3].split("x")
    w,h = int(w), int(h)
    # test case
    ok = True
    for gridx in range(w):
        for gridy in range(h):
            if coordinateGrid[(x+gridx),(y+gridy)] > 1:
                ok = False
    if ok == True:
        # this claim doesn't conflict
        print("claimId:",a1[0])


result = 0
for (d,e),f in coordinateGrid.items():
    if f >= 2:
        result += 1
print(result)

