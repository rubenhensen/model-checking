from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse
from frequentist import frequentist
from frequentist_coupled import frequentist_coupled
from bayesian import bayesian_iter
from model_generator import generate_model, generate_model2
from bayesian import bayesian_iter
import stormpy
import sys

def run(use_coupled, trace_length, nr_of_traces, reachability_predicate = 'P=? [X "a"]'):
    prism_file_path = "prism_models/grid_5x5.prism"

    if bool(use_coupled):
        prism_file_path = "prism_models/grid_5x5_coupled.prism"

    (original_prism_program, transitions) = grid_simulator_deterministic(int(nr_of_traces), int(trace_length), prism_file_path) # Writes to file, uncomment to generate new file

    # Calculate eachability probability on original model
    original_properties = stormpy.parse_properties(reachability_predicate, original_prism_program)
    original_model = stormpy.build_symbolic_model(original_prism_program, original_properties)
    original_result = stormpy.model_checking(original_model,original_properties[0])
    original_filter = stormpy.create_filter_initial_states_symbolic(original_model)
    original_result.filter(original_filter)

    print(f"Result original model: {original_result}")

    # calculate reachability probability on approximated model using useer defined configuration
    (variables, coupled, traces) = grid_parse("export_simulator.txt") 

    # approx0 = frequentist(traces)
    approx1 = frequentist_coupled(coupled, traces)
    print(approx1)
    # approx2 = bayesian_iter([], traces)
    # approx3 = bayesian_iter(coupled, traces, transitions)

    print(f"Bayesian coupled: {reachability_predicate} {reachability_probability(generate_model2(approx1, prism_file_path, variables), reachability_predicate)}")

# Return the result of checking the formula string reachability
def reachability_probability(dtmc, reachability_predicate):
    properties = stormpy.parse_properties(reachability_predicate)

    result = stormpy.model_checking(dtmc,properties[0])
    filter = stormpy.create_filter_initial_states_sparse(dtmc)
    result.filter(filter)

    return result

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    run(*sys.argv[1:])
