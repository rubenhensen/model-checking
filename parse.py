import json

def grid_parse(file_path):
    f = open(file_path)

    data = json.load(f)

    coupled = data['coupled']

    paths = data['paths']
    transitions = []
    for trace in paths:
        tracelist = []
        for id, state in enumerate(trace):
            if id == len(trace) -1:
                break 
            tracelist.append((int(state),int(trace[id+1])))
        transitions.append(tracelist)
    return (coupled, transitions)


if __name__ == '__main__':
    grid_parse("export_simulator.txt")
