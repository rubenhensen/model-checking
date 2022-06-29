from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse
from frequentist import frequentist
from frequentist_coupled import frequentist_coupled
from bayesian import bayesian_iter
from model_generator import generate_model
from bayesian import bayesian_iter
import stormpy

# Formula string to check
formula_str = 'P=? [X "a"]'

# Return the result of checking the formula string reachability
def reachability_probability(dtmc):
    properties = stormpy.parse_properties(formula_str)

    result = stormpy.model_checking(dtmc,properties[0])
    filter = stormpy.create_filter_initial_states_sparse(dtmc)
    result.filter(filter)

    return result

(original_prism_program, transitions) = grid_simulator_deterministic(1, 5)
(coupled, traces) = grid_parse("export_simulator.txt") 

# approx0 = frequentist(traces)
# approx1 = frequentist_coupled(coupled, traces)
# approx2 = bayesian_iter([], traces)
approx3 = bayesian_iter(coupled, traces, transitions)

print(approx3)

# print(f"Frequentist: {formula_str} {reachability_probability(generate_model(approx0))}")
# print(f"Frequentist coupled: {formula_str} {reachability_probability(generate_model(approx1))}")
# print(f"Bayesian: {formula_str} {reachability_probability(generate_model(approx2))}")
# print(f"Bayesian coupled: {formula_str} {reachability_probability(generate_model(approx3))}")
