from parse import grid_parse
import collections
def frequentist(obj):
    coupled,traces = obj
    flat_list = [item for sublist in traces for item in sublist]    # Create a flat list out of multiple traces. [[],[],[]] -> []
    states = {state1 for (state1, state2) in flat_list}      # get all unique visited states using set comprehension
    nr_total_samples = collections.Counter(state1 for (state1, state2) in flat_list) # For every state, calculate the amount of times a state is a starting state in the traces.
    nr_transitions = collections.Counter((state1, state2) for (state1, state2) in flat_list) # For every transition, calculate the amount of time that transition is taken in the traces.
    approx = {}
    # Calculate the approximation by dividing the transition by the total. (st1->st2) / st1 
    for (st1, st2) in nr_transitions:
        nr_total = nr_total_samples.get(st1)
        nr_trans = nr_transitions.get((st1, st2))
        probability = nr_trans / nr_total
        approx.update({(st1, st2):probability})
    
    for a in approx:
        #State(x: 0, y: 4) 0.49 --> State(x: 0, y: 3)
        print(f"{a[0]} {round(approx[a], 2)} --> {str(a[1])}")


