import itertools

# The grid_size x grid_size (min 3)
grid_size = 5

# Number of variables required for a state located at the corner of the grid
nr_of_corner_vars = 1

# Number of variables required for a state located at the edge of the grid, but no a corner
nr_of_edge_vars = 2

# Number of variables required for a state located in the middle of the grid
nr_of_center_vars = 3

# Allowed characters for variable names
chars = "abcdefghijklmnopqrstuvwz"

# Generate a list of n unique (sequential) lowercase strings
def var_names(n):
    names = []

    while n > 0:
        for i in range(1, 3):
            for item in itertools.product(chars, repeat=i):
                names.append("".join(item))
                n -= 1

                if n == 0:
                    break

    return names

# Generate a prism file for a grid_size x grid_size grid
def generate(file):
    file.write("dtmc\n\n")

    nr_of_transitions = nr_of_corner_vars * 4
    nr_of_transitions += nr_of_edge_vars * 4 * (grid_size - 2)
    nr_of_transitions += nr_of_center_vars * (grid_size - 2) * (grid_size - 2)

    names = var_names(nr_of_transitions)

    for v in names:
        file.write(f"const double {v};\n")

    file.write("\n")
    file.write("module main\n")
    file.write(f"   x : [0..{grid_size - 1}] init 0;\n")
    file.write(f"   y : [0..{grid_size - 1}] init 0;\n")
    file.write("\n")

    corner_vars = []
    edge_vars = []
    center_vars = []

    for x in range(grid_size):
        for y in range(grid_size):
            file.write(f"   [] x={x} & y={y} -> ")

            # Bottom left
            if x == 0 and y == 0:
                v = names.pop()
                corner_vars.append(v)

                file.write(f"{v} : (x'=1) + (1 - {v}) : (y'=1);\n")

            # Top left
            elif x == 0 and y == grid_size-1:
                v = names.pop()
                corner_vars.append(v)

                file.write(f"{v} : (x'=1) + (1 - {v}) : (y'={grid_size-2});\n")

            # Bottom right
            elif x == grid_size-1 and y == 0:
                v = names.pop()
                corner_vars.append(v)

                file.write(f"{v} : (x'={grid_size-2}) + (1 - {v}) : (y'=1);\n")

            # Top right
            elif x == grid_size-1 and y == grid_size-1:
                v = names.pop()
                corner_vars.append(v)

                file.write(f"{v} : (x'={grid_size-2}) + (1 - {v}) : (y'={grid_size-2});\n")

            # Left edge
            elif x == 0:
                v = names.pop()
                q = names.pop()

                edge_vars.append(v)
                edge_vars.append(q)

                file.write(f"{v} : (x'=1) + {q} : (y'=y+1) + (1-{v}-{q}) : (y'=y-1);\n")

            # Right edge
            elif x == grid_size - 1:
                v = names.pop()
                q = names.pop()

                edge_vars.append(v)
                edge_vars.append(q)

                file.write(f"{v} : (x'={grid_size - 2}) + {q} : (y'=y+1) + (1-{v}-{q}) : (y'=y-1);\n")

            # Bottom edge
            elif y == 0:
                v = names.pop()
                q = names.pop()

                edge_vars.append(v)
                edge_vars.append(q)

                file.write(f"{v} : (y'=1) + {q} : (x'=x+1) + (1-{v}-{q}) : (x'=x-1);\n")

            # Top edge
            elif y == grid_size - 1:
                v = names.pop()
                q = names.pop()

                edge_vars.append(v)
                edge_vars.append(q)

                file.write(f"{v} : (y'={grid_size - 2}) + {q} : (x'=x+1) + (1-{v}-{q}) : (x'=x-1);\n")

            # Center
            else:
                v = names.pop()
                q = names.pop()
                r = names.pop()

                center_vars.append(v)
                center_vars.append(q)
                center_vars.append(r)

                file.write(f"{v} : (y'=y-1) + {q} : (y'=y+1) + {r} : (x'=x+1) + (1-{v}-{q}-{r}) : (x'=x-1);\n")

    file.write("\n")
    file.write("endmodule\n")

    corner_vars_assigned = [f"{e}=0.5" for e in corner_vars]
    edge_vars_assigned = [f"{e}=0.333" for e in edge_vars]
    center_vars_assigned = [f"{e}=0.25" for e in center_vars]

    var_spec = ",".join([*corner_vars_assigned, *edge_vars_assigned, *center_vars_assigned])
    print(var_spec)
    

def main():
    file_name = f"prism_models/grid_{grid_size}x{grid_size}.prism"
    file = open(file_name, "w")

    generate(file)

    file.close()

if __name__ == "__main__":
    main()
