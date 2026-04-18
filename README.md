# SEIR Epidemiological Model
## Overview

This project file is split up into two parts which, respectively, take two different approaches to a SEIR (Susceptible, Exposed, Infected, Recovered) infection simulation. The model is governed by three rate parameters: beta (infection rate), sigma (incubation rate) and gamma (recovery rate). The basic reproduction number R₀ = beta/gamma determines whether an outbreak occurs (R₀ > 1) or dies out (R₀ < 1).

### Part 1 Overview
Solves the SEIR model as an initial value problem by implementing the scipy `solve_ivp` function to integrate the four coupled, reduced rate equations that govern the susceptible, exposed, infected and recovered population fractions. The model allows the user to customise the rate parameters: `beta`, `sigma` and `gamma` in the command line and then produces a savable plot of each compartment over time.

### Part 2 Overview
Uses the Monte Carlo method, simulating individual agents moving randomly across a 2D lattice. Disease spreads when susceptible agents come into contact with infected neighbours. The simulation is built using object-oriented programming, with separate classes in separate module files: `Agent` handling individual state, `Lattice` managing the grid, and `Simulation` coordinating the Monte Carlo steps. The model allows the same customisable parameters and save options as part 1, which is implemented using argparse, and outputs a similar plot as well as the final state of the lattice with each agent plotted and colour coded according to their compartment. A reinfection parameter was added as an optional extension for the user in which recovered individuals can become reinfected. A `SuperSpreader` class was also added inside of the `agents.py` file which uses OOP inheritance to inherit from `Agent`, adding a private `spread_radius` parameter which allows an infected superspreader to infect susceptible neighbours over a customisable enhanced radius (default=3).

- Python was used to execute these tasks and version controlled using git.

## Project Structure
+ Y2_MINIPROJECT
    + part_1
        + seir_ode.py
    + part_2
        + agents.py
        + lattice.py
        + simulation.py
        + main.py
    + .gitignore
    + LICENSE
    + README.md

## Dependencies
python, numpy, scipy, matplotlib
- installed via:
```bash
pip install numpy scipy matplotlib
```
python library modules: `argparse` and `random` are also used which do not require installation.
## Usage - Part 1

A default run can be carried out on the code base by entering the following into the command line:
```bash
python seir_ode.py
```
The default run should produce a plot that resembles the one provided in the brief.

The user can also provide a save file, customise parameters and change initial conditions in the command line by code such as:
```bash
python seir_ode.py --beta 0.9 --sigma 0.9 --gamma 0.2 --S0 0.98 --E0 0.02 --I0 0.00 --R0 0.00 --num_points 1000 --t_end 12 --save output.png
```
- Beta, sigma and gamma are the respective rates for infection, incubation and recovery. S0, E0, I0 and R0 are the fractions of the population that are initially susceptible, exposed, infected and recovered respectively. Num_points Number of time points to evaluate within the time span. T_end is the time span after which the simulation ends and save is the file path that the user wishes to save the output.

## Usage - Part 2

A default run can be carried out on part 2 by entering the following in the command line:
```bash
python main.py
```
### Output
- This run should produce two plots that resemble the ones given in the brief: a final lattice plot with 250 agents that shows the state of the infection simulation at the end of the run time and a graph which shows the progress of the different compartment for each step in the simulation. The plot will not be identical to the one in the brief as it relies on randomly generated probabilities.

### Customisable parameters
Custom runs including adding reinfection parameters and superspreaders as well as save options can be run using (example using default parameters):
```bash
python main.py --lattice_size 100 --num_agents 250 --num_superspreaders 10 --spread_radius 3 --beta 1.0 --sigma 0.1 --gamma 0.005 --p_exposed 0.05 --p_reinfection 0.01 --num_steps 2000 --save output.png --save_lattice lattice.png
```
- Beta, sigma and gamma are the respective rates for infection, incubation and recovery. Lattice_size defines the dimensions of the 2D grid. Num_agents is the total number of agents placed on the lattice. Num_superspreaders and spread_radius define the number of superspreader agents and the radius within which they can infect others respectively. P_exposed is the initial fraction of agents assigned to the exposed compartment. P_reinfection is the optional probability of a recovered agent becoming susceptible again. Num_steps is the number of Monte Carlo steps to simulate. Save and save_lattice are the file paths the user wishes to save the population plot and lattice plot respectively.

## Design and Object-Oriented Approach

This project uses object-oriented programming (OOP) throughout the Monte Carlo simulation in Part 2. The code is organised into three core classes: `Agent`, `Lattice` and `Simulation`, each with a single, well-defined responsibility.

### Composition (OOP)
The three classes interact through **composition**, `Simulation` owns a `Lattice` object and a list of `Agent` objects, coordinating their interaction at each Monte Carlo step. 

This models a "has-a" relationship: a `Simulation` *has* a `Lattice` and *has* agents. The classes are fundamentally different entities that interact with each other rather than extending each other's behaviour and therefore composition was more appropriate than inheritance.

### Class Responsibilities
- **`Agent`** — stores and manages the state of an individual agent, including its position on the lattice and its current SEIR compartment. Handles movement, compartment transitions (E->I, I->R, R->S) and exposure logic.
- **`Lattice`** — manages the 2D grid, tracking which sites are occupied and providing spatial lookups such as neighbour checking within a given radius.
- **`Simulation`** — coordinates the Monte Carlo simulation. Initialises the lattice and agents, runs the MCS loop, records population history and handles plotting.

### Inheritance — SuperSpreader
The `SuperSpreader` class demonstrates OOP inheritance by extending `Agent`. It models the epidemiological concept of a superspreader which is an individual capable of infecting others over a larger radius than a regular agent. `SuperSpreader` inherits all attributes and methods of `Agent` by using `super().__init__()`, and extends it with a private `__spread_radius` attribute. This is an appropriate use of inheritance as `SuperSpreader` *is an* `Agent` with additional behaviour, rather than a fundamentally different entity.

### Encapsulation
All class attributes are private, using python name mangling (e.g. `self.__x`, `self.__compartment`). Public getter methods are used for other classes to read an attribute. This prevents external code from directly modifying an agent's state so all changes go through the class's own methods where validation can be applied consistently.

### Separation into Files
The Part 2 code is separated into four files: `agents.py`, `lattice.py`, `simulation.py` and `main.py`. Each file contains one class (or related classes in the case of `Agent` and `SuperSpreader`), making the codebase easier to navigate and maintain. Classes are imported where needed using e.g. `import agents as ag`.

## Testing
As mentioned earlier, part 1 can be verified by running the default parameters (beta=1, sigma=1, gamma=0.1) which should reproduce the figure provided in the brief. Part 2 can be verified similarly by running with default parameters (100×100 lattice, 250 agents, σ=0.1, γ=0.005). Testing of part 2 revealed an error with the legend figure of part 2 where it would only display a compartment in the legend when it had a non-zero population of agents.

A detailed analysis of the model behaviour under different parameters is provided in the accompanying report. 

## Contributing

Git branching is utilised to manage development. The `main` branch contains stable, finished code and isn't developed on directly. All development is carried out on the `dev` branch or on feature branches created from `dev` (e.g. `feature/part1-ode`, `feature/part2-monte-carlo`).

To contribute:
1. Create a new feature branch from `dev`:
```bash
   git checkout -b feature/feature-name
```
2. commit changes with commit messages and descriptions (e.g. `Add reinfection extension`)
3. Merge feature branch into `dev` when complete
4. Merge `dev` into `main` when the code is stable and verified
5. Tag stable releases using git tags (e.g. `v1.0-part1`) for flagging important versions or milestones






