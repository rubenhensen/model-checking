import stormpy
import re

def generate_model(model_dict, path, variables):
    prism_program1 = stormpy.parse_prism_program(path)  # type: ignore
    valuation = ""
    regex = r'\(([a-z]+)\)\/\(1\)'
    valuated_variables = []
    
    for key in model_dict:
        compiled_regex = re.compile(regex)
        if (compiled_regex.search(key)):
            variable = re.search(regex, key).group(1)
            valuated_variables.append(variable)
            valuation = valuation + variable + "=" + str(model_dict[key]) + ","

    unvaluated_variables = list(set(variables) - set(valuated_variables))

    for var in unvaluated_variables:
        valuation = valuation + var + "=0,"

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