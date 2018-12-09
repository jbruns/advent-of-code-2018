import sys
inputs = [int(x) for x in sys.stdin.read().split()]

# credit: sciyoshi on reddit, https://old.reddit.com/r/adventofcode/comments/a47ubw/2018_day_8_solutions/ebc7ol0/
# not having worked with tree data structures enough to formulate a working solution, I attempted an overly complicated,
# failure prone series of loops: I was recursing through and trying to parse the data one integer at a time. 
# This strategy completely broke down in parent nodes with multiple children, for example. 

# the solution below was a significant learning experience, especially given the simplicity, and I felt the need to preserve
# it in the name of learning. The in-line code comments are mine, added as I interpreted.

# Problem presented by the game: read a tree data structure that amounts to a license key.
# Part 1: sum all of the metadata entries contained in the license key.
# Part 2: score the value of the root node:
# -if a node has 0 child nodes, its value is the sum of its metadata entries
# -if a node has >0 child nodes, its metadata entries become indexes which refer to its child nodes, which in turn are summed together

def parse(data):
    # format of the input string: 
    # -a two-integer header: 
    # --the first int is the number of child nodes this node has 0..n,
    # --the second int is the number of metadata entries for this node 1..n.
    # -child nodes follow the header (each with their own header).
    # -metadata entries follow any child nodes.
    
    # store the number of child nodes and metadata entries that this node possesses
    children, metas = data[:2]
    # remove the header from the data, keeping the rest
    data = data[2:]
    # initialize:
    # -scores: a list of values for each child node (part2 answer)
    # totals: int, a running sum of all metadata nodes parsed (part1 answer)
    scores = []
    totals = 0

    # for each child node that this node possesses, also parse its header and metadata entries.
    # this whittles down the series of input data, and outputs:
    # -total, a sum of the metadata entries for this node and all its child nodes (and all other child nodes too as it loops on itself)
    # -score, the value of this node
    for i in range(children):
        total, score, data = parse(data)
        # add the sum of metadata entries from this run to the overall running total
        totals += total
        scores.append(score)

    # add to the running total the sum of metadata entries for the parent node
    # the header data is removed and number of metadata entries is stored in metas, so
    # we can grab the next several numbers in the data stream equal to the number of metadata entries
    totals += sum(data[:metas])

    # if there are no child nodes for the parent node passed in, return:
    # -the current running total
    # -sum of this node's metadata entries
    # -the metadata entries for this node
    if children == 0:
        return (totals, sum(data[:metas]), data[metas:])
    
    # if this parent node has child nodes, return:
    # -the current running total (for part 1)
    # -the value of all metadata entries for this node and all of its children, so long as the metadata entries:
    # --do not refer to a child node that does not exist (k - 1 where k is both greater than 0, and is less than or equal to the number of scores we've tracked for all children)
    # -the metadata entries for this node
    else:
        return (
            totals,
            # we only need to track the value of the root node, so we do not have to keep a running total of 'value' like we do for 'totals.' 
            # the function will complete the last time with the value of the root node, so that's all we want!
            sum(scores[k - 1] for k in data[:metas] if k > 0 and k <= len(scores)),
            data[metas:]
        )

total, value, remaining = parse(inputs)

print('part 1:', total)
print('part 2:', value)