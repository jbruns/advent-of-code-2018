import sys
from datetime import datetime
from collections import defaultdict
inputs = [x for x in sys.stdin]
inputs.sort()

def timestampParse(event):
    # [1518-06-16 00:49] falls asleep
    words = event.replace("[","").split("]")
    return datetime.strptime(words[0],"%Y-%m-%d %H:%M")

# defaultdict with nested list for minute tracking, initialize the list for 60 minutes 
guardSleepTracker = defaultdict(lambda:[0 for x in range(60)])
guardId = None
asleep = None

for event in inputs:
    # print("parsing event:",event)
    # parse out the event's time
    eventTime = timestampParse(event)
    # possible events
    if 'begins shift' in event:
        # new guard, we assume they show up awake..
        # parse out the guard ID
        guardId = int(event.split()[3][1:])
        print("guard",guardId,"beginning shift at",eventTime.strftime('%H:%M'))
        asleep = None
    elif 'falls asleep' in event:
        # start the clock at this event's time
        asleep = eventTime
        print("guard",guardId,"fell asleep at",asleep.strftime('%H:%M'))
    elif 'wakes up' in event:
        # calc the time that this guard was asleep and add 1 to their overall clock each iteration
        asleepDelta = (eventTime - asleep)
        asleepMins = (asleepDelta.seconds//60)%60
        print("guard",guardId,"woke up at",eventTime.strftime('%H:%M'),", adding",asleepMins,"minutes to their clock")
        sleepStartMin = int(asleep.strftime('%M'))
        sleepEndMin = int(eventTime.strftime('%M'))
        for m in range(sleepStartMin,sleepEndMin):
            # add individual minute frequency to tracker by keys = guardId and clock minute 
            guardSleepTracker[guardId][m] += 1

# part 1, guard id that has the most minutes asleep: sum all of the minutes per guard, sort, and return only the top result
r1 = sorted(guardSleepTracker.keys(), key=lambda g:-sum(guardSleepTracker[g]))[0]
# part 2, guard id that is most frequently asleep at the same minute: get the max of minute occurrences per guard, sort, and return only the top result
r2 = sorted(guardSleepTracker.keys(), key=lambda g:-max(guardSleepTracker[g]))[0]

# we have our guard ids, so now we need:
# -for the guard that spends the most time asleep, what minute do they specifically spend asleep the most
# -for the guardid that has the most frequent occurrences of the same minute, find the minute that occurs most often
# these are both max(), so we can use the same strategy for both cases:
# loop over the sleepTracker for the two guard ids we care about (r1 and r2). grab their minutes and counter. return max().
for g in [r1,r2]:
    gh = guardSleepTracker[g]
    minute = gh.index(max(gh))
    print(g*minute)