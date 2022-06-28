from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse
from frequentist import frequentist
from frequentist_coupled import frequentist_coupled

grid_simulator_deterministic(10, 500) # Writes to file, uncomment to generate new file
(coupled, traces) = grid_parse("export_simulator.txt") 
# print(coupled)
# frequentist(traces)
frequentist_coupled((coupled, traces))

