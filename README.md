# Model Checking: Learning Probabilities with Storm(py)

## Introduction

This repository contains the implementation of the practical project _probability learning_ for the course Model Checking (NWI-IMC046). In this project, the frequentist and bayesian approaches are exploited to estimate the probabilities of a DTMC. We also exploit _coupled transitions_, which are transitions whose probability is not yet known, but from which we know that they are equal. For coupled transitions, we require that if a state _s1_ has a transition _t1_ which is coupled with transition _t2_ of state _s2_, then all other transitions _t'_ of _s1_ and _s2_ must also be coupled. This requirement gives rise to the notion of _coupled states_ (e.g. _s1_ and _s2_ in the example from before).

## Prerequisites
We strongly advice to run the experiment inside the Docker envrionment, provided in `.devcontainer`. Using Visual Studio Code's extension `Remote Containers` from Mirosoft works particulary well. `stormpy` at version `1.6.4` is used for this project. The python intepreter at version `3.9.7.` is used for executing the code.

## Usage

The `prism_models` directory contains two examples of a 5x5 grid world. `grid_5x5_coupled.prism` contains the model in which certain states are coupled. These are the **corner states** (e.g. `x=0&y=0`) which have only two outgoing transitions, the **edge state** (e.g. `x=0&y=1`) which are the non-corner states located at the edge of the grid and have three outgoing transitions, and the **center states** which are all other states and have four outgoing transitions. `grid_5x5.prism` contains the model in which no states are coupled.

A call to main with the help flag, `python main.py -h`, gives the following information about running the script:
```
Probability learner for DTMC

optional arguments:
  -h, --help            show this help message and exit
  --coupled COUPLED     Use the grid world model with coupled transitions
  --learning_method {frequentist,bayesian}
                        The learning method to be used for approximating the transition probabilities
  --nr_of_traces NR_OF_TRACES
                        an integer for the number of traces created by the simulator
  --trace_length TRACE_LENGTH
                        an integer for the length of traces created by the simulator
  --reachability_formula REACHABILITY_FORMULA
                        The reachability formula
```

This shows how the demo can be ran. Every option has a default value as well: `coupled` is `False` by default, `learning_method` is `bayesian` by default, `nr_of_traces` is `10` by default, `trace_length` is `50` by default and the `reachability_formula` is `P=? [X "a"]` by default.

An example of running an experiment using the frequentist approach, coupled transitions, 10 simulator traces of length 50 and comparing the probability of reaching the next state were `a` holds can be done using the command:

`python main.py --coupled True --learning_method frequentist --nr_of_traces 10 --trace_length 50 --reachability_formula 'P=? [X "a"]'`
