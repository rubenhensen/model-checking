import scipy.stats as stats
import matplotlib.pyplot as plt
from enum import Enum

def bayesian_iter(traces):
    # Get all unique visited transitions using set comprehension
    transitions = {(state1, state2) for (state1, label, state2) in [item for sublist in traces for item in sublist]}

    alphas = dict()
    prior = 2

    for (source, target) in transitions:
        alphas[source][target] = prior

    for i, trace in enumerate(traces):
        alphas = run_bayesian(trace, alphas)


def run_bayesian(trace, alphas):
    for (state1, label, state2) in trace:
        alphas[state1][state2] += 1

    return alphas

def bayesian(states, prior):
    m = 5   # number of iterations
    s = 20  # number of states
    
    """
    {s0 : {
	        s1: 0.0,
	        s2: 0.0,
	        s3: 1.0,
	      }
    }
    """

    # dictionary {
    #     alfa1 : integernumber,
    #     ...
    #     alfan : integernumber
    # }
    dictionary = initialize_dictionary()

    for k in range(m):
        for i in range(s):
            for j in range(4):
                current_alfa = dictionary["s% s" % i]["s% s" % j]
                dictionary["s% s" % i]["s% s" % j] = current_alfa + calculate_probability(i, current_alfa, j) # TODO: second index should correspond to the correct (target) state number instead of 
                                                                                                              #   	0,..,4 for each transition within state i

    # P(s1, alfa, s) for each dictionary -> dictionary of alfa should be updated by: alfa = alfa + P(s1, alfa, s)


# calculate_probability(s0, {s0: α0, s1: α1, sm: αm})
# returns the probability for the transition to the target state, given all other successor states
def calculate_probability(target_state, target_states):
    # m: number of successor states
    m = len(target_states)
    # αi - 1
    numerator = target_states[target_state] - 1
    # Summation of αi to αm subtracted by m
    denominator = sum(list(target_states.values())) - m
    # Probability estimate
    probability = numerator / denominator
    
    return probability

def initialize_dictionary(number_of_states, number_of_states_per_row):
    dictionary = dict()

    for i in range(number_of_states):
        dictionary["s% s" % i] = dict()
        for j in Direction:
            if i < number_of_states_per_row:        # first row of grid
                print("first if: " + str(i) + " " + str(j.value))
                if j.value == 0:
                    continue
                if i == 0 and j.value == 3:
                    continue
                if i == number_of_states_per_row - 1 and j.value == 1:
                    continue

            elif i >= number_of_states - number_of_states_per_row - 1:  # last row of grid
                print("second if: " + str(i) + " " + str(j.value))
                if j.value == 2:
                    continue
                if i == number_of_states - number_of_states_per_row - 1 and j.value == 3:
                    continue
                if i == number_of_states - 1 and j.value == 1:
                    continue

            elif i % (number_of_states_per_row) == (number_of_states_per_row - 1) and j.value == 1:
                continue
                
            elif i % number_of_states_per_row == 0 and j.value == 3:
                continue

            dictionary["s% s" % i]["% s" % j.name] = 2      # TODO: second index should correspond to the correct (target) state number instead of 
                                                            #   	0,..,4 for each transition within state i
            
    return dictionary
                                                
# 0 = N
# 1 = E
# 2 = S
# 3 = W

class Direction(Enum):
    N = 0
    E = 1
    S = 2
    W = 3