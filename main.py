from grid_simulator_deterministic import grid_simulator_deterministic
from parse import grid_parse
from frequentist import frequentist
from model_generator import generate_model

grid_simulator_deterministic(10, 50) # Writes to file, uncomment to generate new file
(coupled, traces) = grid_parse("export_simulator.txt") 
print(coupled)
approx = frequentist((coupled, traces))
generate_model(approx)

