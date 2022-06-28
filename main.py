from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse
from frequentist import frequentist
from frequentist_coupled import frequentist_coupled
from bayesian import bayesian_iter
from model_generator import generate_model
from bayesian import bayesian_iter
import stormpy

formula_str = 'P=? [X "a"]'

def reachability_probability(dtmc):
    properties = stormpy.parse_properties(formula_str)

    result = stormpy.model_checking(dtmc,properties[0])
    filter = stormpy.create_filter_initial_states_sparse(dtmc)
    result.filter(filter)

    return result


# original_prism_program = grid_simulator_deterministic(10, 50) # Writes to file, uncomment to generate new file


# state_labeling = stormpy.storage.StateLabeling(5)
# state_labeling.add_label_to_state('a', 1)

# original_properties = stormpy.parse_properties(formula_str, original_prism_program)
# original_model = stormpy.build_model(original_prism_program, original_properties)
# original_result = stormpy.model_checking(original_model,original_properties[0])

# filter = stormpy.create_filter_initial_states_sparse(original_model)
# original_result.filter(filter)

# print(f"Result original model: {original_result}")

(coupled, traces) = grid_parse("export_simulator.txt") 
# print(coupled)
# approx0 = frequentist(traces)
approx1 = frequentist_coupled(coupled, traces)
# approx2 = bayesian_iter([], traces)
# approx3 = bayesian_iter(coupled, traces)

print(approx1)

# print(f"Frequentist: {formula_str} {reachability_probability(generate_model(approx0))}")
# print(f"Frequentist coupled: {formula_str} {reachability_probability(generate_model(approx1))}")
# print(f"Bayesian: {formula_str} {reachability_probability(generate_model(approx2))}")
# print(f"Bayesian coupled: {formula_str} {reachability_probability(generate_model(approx3))}")
