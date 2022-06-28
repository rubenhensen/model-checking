from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse
from frequentist import frequentist
from frequentist_coupled import frequentist_coupled
from bayesian import bayesian_iter
from model_generator import generate_model

grid_simulator_deterministic(10, 50) # Writes to file, uncomment to generate new file
(coupled, traces) = grid_parse("export_simulator.txt") 
# print(coupled)
approx0 = frequentist(traces)
approx1 = frequentist_coupled(coupled, traces)
approx2 = bayesian_iter([], traces)
approx3 = bayesian_iter(coupled, traces)
generate_model(approx0)
generate_model(approx1)
generate_model(approx2)
generate_model(approx3)

