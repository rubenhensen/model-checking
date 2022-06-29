from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse

def bayesian_iter(coupled, traces, transitions):
    #print(coupled)
    #print(traces)

    alphas = dict()
    prior = 2

    for (source, target) in transitions:
        if not source in alphas:
            alphas[source] = {}
        alphas[source][target] = prior

    for i, trace in enumerate(traces):
        alphas = run_bayesian(trace, alphas, coupled, prior)

        #print(f"Probabilities after iteration {i}")
        for (source_state, target) in alphas.items():
            for (target_state, alpha) in target.items():
                p = calculate_probability(target_state, target)
                #print(f"{source_state} {round(p, 2)} --> {target_state}")

    approx = {}

    for (source_state, target) in alphas.items():
        for (target_state, alpha) in target.items():
            #print(f"Source: {source_state} Target: {target}")

            for prob,couples in coupled.items():
                if prob not in approx and [source_state, target_state] in couples:
                    approx[prob] = round(calculate_probability(target_state, target), 2)

    return approx

def run_bayesian(trace, alphas, coupled, prior):
    for (state1, state2) in trace:
        alphas[state1][state2] += 1

        source = state1
        target = state2

        t = [source, target]

        for couples in coupled.values():
            if t in couples:
                for transition in couples:
                    if transition == [source, target]:
                        continue

                    coupled_source = transition[0]
                    coupled_target = transition[1]

                    if not coupled_source in alphas:
                        alphas[coupled_source] = {}

                    if not coupled_target in alphas[coupled_source]:
                        alphas[coupled_source][coupled_target] = prior

                    alphas[coupled_source][coupled_target] += 1

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
    grid_simulator_deterministic(10, 50)
    coupled, traces = grid_parse("export_simulator.txt")
    approx = bayesian_iter(coupled, traces)
    for (transition_label, value) in approx.items():
        print(f"{transition_label}: {value}")

if __name__ == "__main__":
    main()
