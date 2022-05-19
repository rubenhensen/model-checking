from grid_simulator import grid_simulator
from parse import grid_parse
from frequentist import frequentist

# grid_simulator(20, 20) # Writes to file, uncomment to generate new file
x = grid_parse("export_simulator.txt") 
frequentist(x)

