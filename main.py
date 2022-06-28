from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse
from frequentist import frequentist
from model_generator import generate_model
from bayesian import bayesian_iter

grid_simulator_deterministic(10, 50) # Writes to file, uncomment to generate new file
(coupled, traces) = grid_parse("export_simulator.txt") 
print(coupled)

#approximate using frequentist
approx_frequentist = frequentist(coupled, traces)
dtmc = generate_model(approx_frequentist)
print(dtmc)

#approximate using bayesian
approx_bayesian = bayesian_iter(coupled, traces)
dtmc = generate_model(approx_bayesian)
print(dtmc)
