import json
import re

class State:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def parseGridFile(file_path):
    file_text = ''
    with open(file_path, 'rt') as file_placeholder:
        lines = file_placeholder.readlines()
        file_text = '\n'.join(lines)  # This provides the whole file data as string


    arr = re.split(r'\[|\]', file_text)
    arr = arr[2:-2:2]
    l1 = []
    for idx, trace in enumerate(arr):
        l2 = []
        line = re.split(r'\r?\n', trace)
        # print(f"-------{idx}\n")
        for idx, line in enumerate(line):
            matches = re.findall('\d|north|west|east|south', line, re.DOTALL)
            # print(matches)
            if matches:
                if len(matches) == 2:
                    l2.append(State(matches[0], matches[1]))
                else:
                    l2.append(matches[0])
        l1.append(l2)

    l3 = []
    for tr in l1:
        trace = []
        length = len(tr)
        for i, item in enumerate(tr):
            if length - i < 3:
                break
            if i % 2 == 0:
                trace.append((tr[i],tr[i+1],tr[i+2]))
        l3.append(trace)
            # if i % 2 == 1:
            #     print()
        
    return l3
