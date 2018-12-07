import sys,time
from collections import OrderedDict

inputs = [x.replace("Step ","").replace("must be finished before step","").replace(" can begin.\n","") for x in sys.stdin]
depsmap = []
deps = {}

for i in inputs:
    depsmap.append(i.split("  "))

eo = ''.join(inputs).replace(" ","")

print("exec order:",eo)
# create prereq table
for i in range(26):
    st = chr(ord("A") + i)
    deps[st] = ""
    for j in depsmap:
        if j[0] == st:
            deps[st] = deps[st] + j[1]
    print(st,"dependencies:",deps[st]) 

def isStepReady(s):
    # walking across the eval queue, determine whether each step is "ready" by virtue
    # of its prerequisites being completed (no other step declares that it must be completed before this one)
    r = True
    for i in range(26):
        st = chr(ord("A") + i)
        if s in deps[st]:
                print(s,"blocked by",st)
                r = False
    return r

# put the initial step in the block queue for evaluation
initStep = inputs[0][:1]
q = ["",deps[initStep]]
res = initStep
eo = eo.replace(initStep,"")
deps[initStep] = ""

while len(eo) > 0:
    time.sleep(2)
    # evaluate the blocked queue
    # set a variable here to ensure that the blocked queue changes. if it doesn't, we have no option but to commit the ready queue.
    bqd = False
    for s in q[1]:
        if isStepReady(s):
            bqd = True
            # remove the step from the blocked queue
            q[1] = q[1].replace(s,"")
            # add the step to the ready queue
            q[0] = q[0] + s
            # put this step's dependencies, as they are now possibilities, into the blocked queue for evaluation. clear the dependencies that are already satisfied.
            for t in deps[s]:
                if t not in q[1]:
                    q[1] = q[1] + t

    if bqd is False:
        print("out of blocked options, committing ready queue")
        q[0] = ''.join(sorted(q[0]))
        for s in q[0]:
            q[0] = q[0].replace(s,"")
            res = res + s
            eo = eo.replace(s,"")
            deps[s] = ""
    print("---before---")
    print("exec order: ",eo)
    print("ready q:",q[0])
    print("blocked q:",q[1])
    print("commit:",res)
    # compare the ready queue for alphabetical priority against the blocked queue.
    if len(res) > 0:
        if len(q[0]) < 1 and len(q[1]) > 1:
            q[1] = q[0]
            q[1] = ""
        for s in q[0]:
            w = True
            for t in q[1]:
                if chr(ord(s)) > chr(ord(t)):
                    print(s,"loses against",t)
                    # loses against the block queue
                    w = False
            # if this condition is still true, the step in the ready queue wins against all of the block queue, so we commit it
            if w is True:
                print(s,"wins against the blocked queue, committing")
                q[0] = q[0].replace(s,"")
                res = res + s
                eo = eo.replace(s,"")
                deps[s] = ""
            else:
                print("keeping queues")
    print("---after---")
    print("exec order: ",eo)
    print("ready q:",q[0])
    print("blocked q:",q[1])
    print("commit:",res)
print("done")