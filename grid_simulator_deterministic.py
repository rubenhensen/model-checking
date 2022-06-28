import stormpy
import stormpy.core
import stormpy.simulator

import pprint
import stormpy.examples
import stormpy.examples.files
import random
import json

"""
Simulator for nondeterministic models
"""
def grid_simulator_deterministic(nr_traces, len_traces):
    path = "prism_models/grid_5x5_coupled.prism"
    prism_program1 = stormpy.parse_prism_program(path)  # type: ignore
    prism_program = stormpy.preprocess_symbolic_input(prism_program1, [], "p=0.5,q=0.33,r=0.33,s=0.25,t=0.25,v=0.25")[0].as_prism_program()

    options = stormpy.BuilderOptions()
    options.set_build_state_valuations()
    options.set_build_choice_labels(True)
    # parameters = model.collect_probability_parameters()
    model = stormpy.build_sparse_model_with_options(prism_program, options)
    model2 = stormpy.build_sparse_parametric_model_with_options(prism_program1, options)

    coupled_transitions = {}

    print(model)
    print("model2#####################################################################")
    print(model2)
    for state in model2.states:
        for action in state.actions:
            for transition in action.transitions:
                probability = str(transition.value)

                if probability.isnumeric():
                    continue

                # Only add if contains parameter
                if probability not in coupled_transitions:
                    coupled_transitions[probability] = []

                coupled_transitions[probability].append((int(state), transition.column))

    simulator = stormpy.simulator.create_simulator(model, seed=42)
    simulator.set_observation_mode(stormpy.simulator.SimulatorObservationMode.STATE_LEVEL)
    simulator.set_action_mode(stormpy.simulator.SimulatorActionMode.GLOBAL_NAMES)
    # 5 paths of at most 50 steps.
    paths = []
    for m in range(nr_traces):
        path = []
        state, reward, labels = simulator.restart()
        path = [f"{state}"]
        for n in range(len_traces):
            actions = simulator.available_actions()
            select_action = random.randint(0,len(actions)-1)
            state, reward, labels = simulator.step(actions[select_action])

            
            path.append(f"{state}")
            if simulator.is_done():
                #print("Trapped!")
                break
        paths.append(path)


    jsonobj = {
        "coupled": list(coupled_transitions.values()),
        "paths": paths
    }
    # dump the dict contents using json 
    with open("export_simulator.txt", 'w') as outfile:
        json.dump(jsonobj, outfile, indent=4, separators=(',', ':'))


if __name__ == '__main__':
    grid_simulator_deterministic(5, 4)
