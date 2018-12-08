import sys,time, networkx as nx

inputs = [x for x in sys.stdin]

# day 7 starts with a lexicographical topological sort (https://networkx.github.io/documentation/stable/reference/algorithms/generated/networkx.algorithms.dag.lexicographical_topological_sort.html)
# networkx provides this out of the box, where we simply need to feed into a DiGraph() object, edges/vertices as provided in the input stream.
# I found this AFTER I had already created a queue-based brute-force method, so it is included mostly to laugh at.
def LTSort(lines):
    # initialize a networkx.DiGraph object
    graph = nx.DiGraph()
    for line in lines:
        # Step I must be finished before step P can begin.
        parts = line.split(" ")
        graph.add_edge(parts[1], parts[7])
    # networkx does the sorting for us, so we just ask it to do so and poof, our part1 answer
    print("Part1 answer:",''.join(nx.lexicographical_topological_sort(graph)))
    # Part2: With 5 workers and the 60+ second step durations described above, how long will it take to complete all of the steps?
    # steps are (60 + (chr(ord(step))) seconds long
    task_times = []
    tasks = []
    time = 0
    while task_times or graph:
        available_tasks = [t for t in graph if t not in tasks and graph.in_degree(t) == 0]
        if available_tasks and len(task_times) < 5:
            task = min(available_tasks)  # min gets smallest task alphabetically
            task_times.append(ord(task) - 4)
            tasks.append(task)
        else:
            min_time = min(task_times)
            completed = [tasks[i] for i, v in enumerate(task_times) if v == min_time]
            task_times = [v - min_time for v in task_times if v > min_time]
            tasks = [t for t in tasks if t not in completed]
            time += min_time
            graph.remove_nodes_from(completed)

    print("Part2 answer:",time)

LTSort(inputs)

# brute force method follows.

def bf(lines):
    depsmap = []
    deps = {}
    eo = ""

    for line in inputs:
        p = [line[2],line[7]]
        depsmap.append(p)
        eo = eo + ''.join(p)

    print("exec order:",eo)
    # create prereq table
    for i in range(26):
        st = chr(ord("A") + i)
        deps[st] = ""
        for j in depsmap:
            if j[0] == st:
                deps[st] = deps[st] + j[1]
        print(st,"dependencies:",deps[st]) 


    # put the initial step in the block queue for evaluation
    initStep = inputs[0][:1]
    q = ["",deps[initStep]]
    res = initStep
    eo = eo.replace(initStep,"")
    deps[initStep] = ""

    while len(eo) > 0:
        time.sleep(1)
        # evaluate the blocked queue
        # set a variable here to ensure that the blocked queue changes. if it doesn't, we have no option but to commit the ready queue.
        bqd = False
        for s in q[1]:
            print("from blocked queue, eval:",s)
            if isStepReady(s):
                print(s,"is ready")
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
        # compare the ready queue for alphabetical priority against the blocked queue.
        if len(res) > 0:
            if len(q[0]) < 1 and len(q[1]) > 1:
                q[1] = q[1] + eo[:1]
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
    print("done")