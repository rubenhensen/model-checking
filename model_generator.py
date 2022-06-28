import stormpy
from transition import Transition

#State(x: 0, y: 4) 0.49 --> State(x: 0, y: 3)
#print(f"{a[0]} {round(approx[a], 2)} --> {str(a[1])}")
def create_transitions(model):
    transitions = []

    for a in model:
        #print(f"{str(a[0])[6:len(str(a[0])) -1]}, {str(a[1])[6:len(str(a[1])) -1]}, {round(model[a], 2)}")
        source_state = str(a[0])[6:len(str(a[0])) -1]
        target_state = str(a[1])[6:len(str(a[1])) -1]
        probability = round(model[a], 2)

        transitions.append(
            Transition(int(source_state), int(target_state), probability)
        )
    
    return transitions

def generate_model(model):
    builder = stormpy.SparseMatrixBuilder(rows = 0, columns = 0, entries = 0, force_dimensions = False, has_custom_row_grouping = False)
    
    #create transitions 
    transitions = create_transitions(model)
    transitions.sort(key = lambda x: (x.source, x.target))

    #build transition matrix
    for transition in transitions:
        builder.add_next_value(row = transition.source, column = transition.target, value = transition.probability)

    transition_matrix = builder.build()

    #create state labels
    state_labeling = stormpy.storage.StateLabeling(len(transition_matrix))

    #build sparse model
    components = stormpy.SparseModelComponents(transition_matrix=transition_matrix, state_labeling=state_labeling)

    #build dtmc
    dtmc = stormpy.storage.SparseDtmc(components)

    print(dtmc)