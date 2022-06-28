from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse

def bayesian_iter(coupled, traces):
    print(coupled)
    print(traces)

    # Get all unique visited transitions using set comprehension
    transitions = {(state1, state2) for (state1, state2) in [item for sublist in traces for item in sublist]}

    alphas = dict()
    prior = 2

    for (source, target) in transitions:
        if not source in alphas:
            alphas[source] = {}
        alphas[source][target] = prior

    for i, trace in enumerate(traces):
        alphas = run_bayesian(trace, alphas, coupled)

        print(f"Probabilities after iteration {i}")
        for (source_state, target) in alphas.items():
            for (target_state, alpha) in target.items():
                p = calculate_probability(target_state, target)
                print(f"{source_state} {round(p, 2)} --> {target_state}")


def run_bayesian(trace, alphas, coupled):
    for (state1, state2) in trace:
        alphas[state1][state2] += 1

        for c in coupled:
            print(f"Checking if {[state1.state, state2.state]} in {c}")
            if [state1.state, state2.state] in c:
                print(f"Matching c {c}")
                for l in c:
                    if l[0] == state1.state and l[1] == state2.state:
                        continue
                    alphas[l[0]][l[1]] += 1

    return alphas


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

def main():
    grid_simulator_deterministic(2, 5)
    coupled, traces = grid_parse("export_simulator.txt")
    bayesian_iter(coupled, traces)

if __name__ == "__main__":
    main()
