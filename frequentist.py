from parse import grid_parse

def frequentist(traces):
    flat_list = [item for sublist in traces for item in sublist]
    states = {state1 for (state1, label, state2) in flat_list} # set comprehension
    print(states)
    # print(flat_list)


