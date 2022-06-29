import stormpy
from transition import Transition
import re

#State(x: 0, y: 4) 0.49 --> State(x: 0, y: 3)
#print(f"{a[0]} {round(approx[a], 2)} --> {str(a[1])}")
def create_transitions(model):
    transitions = []

    for a in model:
        #print(f"{str(a[0])[6:len(str(a[0])) -1]}, {str(a[1])[6:len(str(a[1])) -1]}, {round(model[a], 2)}")
        source_state = a[0]
        target_state = a[1]
        probability = round(model[a], 2)

        transitions.append(
            Transition(source_state, target_state, probability)
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

    state_labeling.add_label('a')
    state_labeling.add_label('init')
    state_labeling.add_label('deadlock')

    state_labeling.add_label_to_state('a', 5)
    state_labeling.add_label_to_state('init', 0)

    #build sparse model
    components = stormpy.SparseModelComponents(transition_matrix=transition_matrix, state_labeling=state_labeling)

    #build dtmc
    dtmc = stormpy.storage.SparseDtmc(components)

    return dtmc

def generate_model2(model_dict, path):
    prism_program1 = stormpy.parse_prism_program(path)  # type: ignore
    valuation = ""
    regex = r'\(([a-z]+)\)\/\(1\)'
    
    for key in model_dict:
        compiled_regex = re.compile(regex)
        if (compiled_regex.search(key)):
            variable = re.search(regex, key).group(1)
            valuation = valuation + str(variable) + "=" + str(model_dict[key]) + ","

    valuation = valuation[0:len(valuation) - 1] #remove last comma
    print(valuation)

    prism_program = stormpy.preprocess_symbolic_input(prism_program1, [], valuation)[0].as_prism_program()

    options = stormpy.BuilderOptions()
    options.set_build_state_valuations()
    options.set_build_choice_labels(True)
    # parameters = model.collect_probability_parameters()
    model = stormpy.build_sparse_model_with_options(prism_program, options)
    print("Approximated model")
    print(model)

    return model

    # prism_program = stormpy.preprocess_symbolic_input(prism_program1, [], valuation)[0].as_prism_program()
    # options = stormpy.BuilderOptions()
    # options.set_build_state_valuations()
    # options.set_build_choice_labels(True)
    # # parameters = model.collect_probability_parameters()
    # model = stormpy.build_sparse_model_with_options(prism_program, options)

    # print("model")
    # print(model)