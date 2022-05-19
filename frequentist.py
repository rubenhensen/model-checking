from parse import grid_parse
import collections
def frequentist(traces):
    flat_list = [item for sublist in traces for item in sublist]
    states = {state1 for (state1, label, state2) in flat_list} # set comprehension
    # combinations = {(m, n) for n in states for m in states}
    # for state in states:
    nr_total_samples = collections.Counter(state[0] for state in flat_list)
    nr_transitions = collections.Counter((state[0], state[2]) for state in flat_list)
    approx = {}
    for (st1, st2) in nr_transitions:
        nr_total = nr_total_samples.get(st1)
        nr_trans = nr_transitions.get((st1, st2))
        probability = nr_trans / nr_total
        approx.update({(st1, st2):probability})
    print(approx)

    # print(flat_list)


