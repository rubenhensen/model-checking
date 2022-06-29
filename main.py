from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse
from frequentist import frequentist
from frequentist_coupled import frequentist_coupled
from bayesian import bayesian_iter
from model_generator import generate_model, generate_model2
from bayesian import bayesian_iter
import stormpy
import sys
import argparse
from enum import Enum

class LearningMethod(Enum):
    frequentist = 'frequentist'
    bayesian = 'bayesian'

    def __str__(self):
        return self.value

def run(use_coupled, learningMethod, trace_length, nr_of_traces, reachability_predicate):
    prism_file_path = "prism_models/grid_5x5.prism"

    if use_coupled:
        prism_file_path = "prism_models/grid_5x5_coupled.prism"

    (original_prism_program, transitions) = grid_simulator_deterministic(nr_of_traces, trace_length, prism_file_path) # Writes to file, uncomment to generate new file

    # Calculate eachability probability on original model
    original_properties = stormpy.parse_properties(reachability_predicate, original_prism_program)
    original_model = stormpy.build_symbolic_model(original_prism_program, original_properties)
    original_result = stormpy.model_checking(original_model,original_properties[0])
    original_filter = stormpy.create_filter_initial_states_symbolic(original_model)
    original_result.filter(original_filter)

    print(f"Result original model: {original_result}")

    # calculate reachability probability on approximated model using useer defined configuration
    (variables, coupled, traces) = grid_parse("export_simulator.txt") 

    if learningMethod == LearningMethod.frequentist:
        method_type = "Frequentist coupled" if use_coupled else "Frequentist non-coupled"
        approx = frequentist_coupled(coupled, traces)
        print(approx)
        print(f"{method_type}: {reachability_predicate} {reachability_probability(generate_model2(approx, prism_file_path, variables), reachability_predicate)}")
    
    elif learningMethod == LearningMethod.bayesian:
        method_type = "Bayesian coupled" if use_coupled else "Bayesian non-coupled"
        approx = bayesian_iter(coupled, traces, transitions)
        print(approx)
        print(f"{method_type}: {reachability_predicate} {reachability_probability(generate_model2(approx, prism_file_path, variables), reachability_predicate)}")

# Return the result of checking the formula string reachability
def reachability_probability(dtmc, reachability_predicate):
    properties = stormpy.parse_properties(reachability_predicate)

    result = stormpy.model_checking(dtmc,properties[0])
    filter = stormpy.create_filter_initial_states_sparse(dtmc)
    result.filter(filter)

    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Probability learner for DTMC')
    parser.add_argument('--coupled', type=bool, help='Use the grid world model with coupled transitions', default=False, required=False)
    parser.add_argument('--learning_method', type=LearningMethod, help='The learning method to be used for approximating the transition probabilities', default=LearningMethod.bayesian, required=False, choices=list(LearningMethod))
    parser.add_argument('--nr_of_traces', type=int, help='an integer for the number of traces created by the simulator', default=10, required=False)
    parser.add_argument('--trace_length', type=int, help='an integer for the length of traces created by the simulator', default=50, required=False)
    parser.add_argument('--reachability_formula', type=str, help='The reachability formula', default='P=? [X "a"]', required=False)

    args = vars(parser.parse_args())

    # Map command line arguments to function arguments.
    run(*args.values())