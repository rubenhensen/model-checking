import stormpy
import stormpy.core
import stormpy.simulator

import stormpy.examples
import stormpy.examples.files
import random
import json

"""
Simulator for nondeterministic models
"""
def grid_simulator_deterministic(nr_traces, len_traces):
    path = "prism_models/grid_5x5_coupled.prism"
    prism_program = stormpy.parse_prism_program(path)  # type: ignore
    prism_program = stormpy.preprocess_symbolic_input(prism_program, [], "p=0.5,q=0.33,r=0.33,s=0.25,t=0.25,v=0.25")[0].as_prism_program()

    options = stormpy.BuilderOptions()
    options.set_build_state_valuations()
    options.set_build_choice_labels(True)
    # parameters = model.collect_probability_parameters()
    model = stormpy.build_sparse_model_with_options(prism_program, options)

    print(model)
    
    simulator = stormpy.simulator.create_simulator(model, seed=42)
    simulator.set_observation_mode(stormpy.simulator.SimulatorObservationMode.PROGRAM_LEVEL)
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
            #print(f"Randomly select action nr: {select_action} from actions {actions}")
            path.append(f"--act={actions[select_action]}-->")
            state, reward, labels = simulator.step(actions[select_action])
            # print(state.dict)
            
            path.append(f"{state}")
            if simulator.is_done():
                #print("Trapped!")
                break
        paths.append(path)

    # dump the dict contents using json 
    with open("export_simulator.txt", 'w') as outfile:
        json.dump(paths, outfile, indent=4, separators=(',', ':'))


if __name__ == '__main__':
    grid_simulator_deterministic(5, 4)
