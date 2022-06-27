from grid_simulator_deterministic import grid_simulator_deterministic
from grid_simulator import grid_simulator
from parse import grid_parse
from frequentist import frequentist

# grid_simulator_deterministic(10, 50000) # Writes to file, uncomment to generate new file
x = grid_parse("export_simulator.txt") 
frequentist(x)

