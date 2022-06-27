import json

class State:
    def __init__(self, state):
        self.state = state

    def __eq__(self, other):
        if isinstance(other, State):
            return self.state == other.state
        return False
    
    def __lt__(self, other):
        if isinstance(other, State):
            if self.state < other.state:
                return True
        return False
        

    def __repr__(self):
        return f"State({self.state})"

    def __key(self):
        return (self.state)

    def __hash__(self):
        return hash(self.__key())

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
            st1 = str(state).replace("\n", "")
            st1 = str(st1).replace(" ", "")
            st2 = str(trace[id+1]).replace("\n", "")
            st2 = str(st2).replace(" ", "")
            tracelist.append((State(st1),State(st2)))
        transitions.append(tracelist)
    return (coupled, transitions)


if __name__ == '__main__':
    grid_parse("export_simulator.txt")
