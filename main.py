from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse
from frequentist import frequentist

grid_simulator_deterministic(10, 500) # Writes to file, uncomment to generate new file
(coupled, traces) = grid_parse("export_simulator.txt") 
print(coupled)
frequentist((coupled, traces))

