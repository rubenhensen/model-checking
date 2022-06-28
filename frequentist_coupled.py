from parse import grid_parse
import collections
def frequentist_coupled(coupled,traces):
    flat_list = [(st1,st2) for sublist in traces for (st1, st2) in sublist]    # Create a flat list out of multiple traces. [[],[],[]] -> []
    states = {state1 for (state1, state2) in flat_list}      # get all unique visited states using set comprehension



    nr_total_samples = collections.Counter(state1 for (state1, state2) in flat_list) # For every state, calculate the amount of times a state is a starting state in the traces.
    # print(nr_total_samples)
    nr_transitions = collections.Counter((state1, state2) for (state1, state2) in flat_list) # For every transition, calculate the amount of time that transition is taken in the traces.
    print(nr_transitions)
    coupled_summed = []
    for l in coupled:
        sum_trans = 0
        sum_states = 0
        print("------------")
        for trans in l:
            print(trans)
            sum_trans = sum_trans + nr_transitions[(trans[0],trans[1])]
            sum_states = sum_states + nr_total_samples[trans[0]]

        coupled_summed.append((sum_states,sum_trans))

    print(coupled_summed)
    approx = {}
    # # Calculate the approximation by dividing the transition by the total. (st1->st2) / st1 

    for i, l in enumerate(coupled):
        for trans in l:
            probability = coupled_summed[i][1] / coupled_summed[i][0]
            approx.update({(trans[0],trans[1]):probability})
    
    for a in approx:
        #State(x: 0, y: 4) 0.49 --> State(x: 0, y: 3)
        print(f"{a[0]} {round(approx[a], 2)} --> {str(a[1])}")

    return approx

