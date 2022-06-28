from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse
from frequentist import frequentist
from frequentist_coupled import frequentist_coupled
from bayesian import bayesian_iter
from model_generator import generate_model
from bayesian import bayesian_iter
import stormpy

grid_simulator_deterministic(10, 50) # Writes to file, uncomment to generate new file
(coupled, traces) = grid_parse("export_simulator.txt") 
# print(coupled)
approx0 = frequentist(traces)
approx1 = frequentist_coupled(coupled, traces)
approx2 = bayesian_iter([], traces)
approx3 = bayesian_iter(coupled, traces)
dtmc = generate_model(approx0)
print(dtmc)
print(type(dtmc))
# formula_str = 'P=? [X "a"]'

# properties = stormpy.parse_properties(formula_str)
# print(properties[0])

# result = stormpy.model_checking(dtmc,properties[0])
# filter = stormpy.create_filter_initial_states_symbolic(dtmc)
# result.filter(filter)

# print(result)



# dtmc = generate_model(approx1)
# print(dtmc)
# formula_str = "P=? [F s=7]"
# properties = stormpy.parse_properties(formula_str, dtmc)

# dtmc = generate_model(approx2)
# print(dtmc)
# formula_str = "P=? [F \"a\"]"
# properties = stormpy.parse_properties(formula_str, dtmc)

# dtmc = generate_model(approx3)
# print(dtmc)
# formula_str = "P=? [F \"a\"]"
# properties = stormpy.parse_properties(formula_str, dtmc)
