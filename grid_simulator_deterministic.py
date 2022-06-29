import stormpy
import stormpy.core
import stormpy.simulator

import pprint
import stormpy.examples
import stormpy.examples.files
import random
import json
import re

"""
Simulator for nondeterministic models
"""
def grid_simulator_deterministic(nr_traces, len_traces, path):
    prism_program1 = stormpy.parse_prism_program(path)  # type: ignore
    valuation = "bg=0.5,az=0.5,h=0.5,a=0.5,bf=0.333,be=0.333,bd=0.333,bc=0.333,bb=0.333,ba=0.333,aw=0.333,av=0.333,al=0.333,ak=0.333,aj=0.333,ai=0.333,w=0.333,v=0.333,u=0.333,t=0.333,j=0.333,i=0.333,g=0.333,f=0.333,e=0.333,d=0.333,c=0.333,b=0.333,au=0.25,at=0.25,as=0.25,ar=0.25,aq=0.25,ap=0.25,ao=0.25,an=0.25,am=0.25,ah=0.25,ag=0.25,af=0.25,ae=0.25,ad=0.25,ac=0.25,ab=0.25,aa=0.25,z=0.25,s=0.25,r=0.25,q=0.25,p=0.25,o=0.25,n=0.25,m=0.25,l=0.25,k=0.25"
    valuations = valuation.split(",")
    expression = r'[a-z]+'
    regex = re.compile(expression)
    variables = []

    for assignment in valuations:
        variables.append(regex.search(assignment, expression))

    prism_program = stormpy.preprocess_symbolic_input(prism_program1, [], valuation)[0].as_prism_program()

    options = stormpy.BuilderOptions()
    options.set_build_state_valuations()
    options.set_build_choice_labels(True)
    # parameters = model.collect_probability_parameters()
    model = stormpy.build_sparse_model_with_options(prism_program, options)
    model2 = stormpy.build_sparse_parametric_model_with_options(prism_program1, options)

    # All transitions of the model
    transitions = []
    # Transitions that are coupled. The transition label is the key,
    # the value if the list of pairs of states which represent coupled transitions.
    coupled_transitions = {}
    print("model")
    print(model)
    print("model2")
    print(model2)
    for state in model2.states:
        for action in state.actions:
            for transition in action.transitions:
                transitions.append((int(state), transition.column))

                probability = str(transition.value())
                # print(probability)

                if probability.isnumeric():
                    continue

                # Only add if contains parameter
                if probability not in coupled_transitions:
                    coupled_transitions[probability] = []

                coupled_transitions[probability].append((int(state), transition.column))

    simulator = stormpy.simulator.create_simulator(model, seed=42)
    simulator.set_observation_mode(stormpy.simulator.SimulatorObservationMode.STATE_LEVEL)
    # simulator.set_action_mode(stormpy.simulator.SimulatorActionMode.GLOBAL_NAMES)
    # 5 paths of at most 50 steps.
    paths = []
    for m in range(nr_traces):
        path = []
        state, reward, labels = simulator.restart()
        path = [f"{state}"]
        for n in range(len_traces):
            # actions = simulator.available_actions()
            # select_action = random.randint(0,len(actions)-1)
            # state, reward, labels = simulator.step(actions[select_action])
            state, reward, labels = simulator.step()

            
            path.append(f"{state}")
            if simulator.is_done():
                #print("Trapped!")
                break
        paths.append(path)


    jsonobj = {
        "coupled": coupled_transitions,
        "paths": paths
    }
    # dump the dict contents using json 
    with open("export_simulator.txt", 'w') as outfile:
        json.dump(jsonobj, outfile, indent=4, separators=(',', ':'))

    return (prism_program, transitions)


if __name__ == '__main__':
    grid_simulator_deterministic(5, 4)
