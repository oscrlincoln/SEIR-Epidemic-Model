import matplotlib.pyplot as plt
import random
import agents as ag
import lattice as lat
    
class Simulation:
    def __init__(self, lattice_size, num_agents, beta, sigma, gamma, p_exposed=0.05, p_reinfection=0.0, num_superspreaders=0, spread_radius=3):
        # validate integer parameters are positive
        if not all(isinstance(p, int) and p > 0 for p in [lattice_size, num_agents]):
            raise ValueError("Lattice size and number of agents must be positive integers")

        # validate rate parameters are numerical and non-negative
        if not all(isinstance(p, (int, float)) and p >= 0 for p in [beta, sigma, gamma, p_exposed, p_reinfection]):
            raise TypeError("Rate parameters and probability must be non-negative numerical values")

        # validate superspreader parameters
        if not isinstance(num_superspreaders, int) or num_superspreaders < 0:
            raise ValueError("Number of superspreaders must be a non-negative integer")

        # initialise the lattice and agents, and store the parameters for use in the simulation
        self.__lattice = lat.Lattice(lattice_size)
        self.__agents = []
        self.__beta = beta
        self.__sigma = sigma
        self.__gamma = gamma
        self.__p_exposed = p_exposed
        self.__p_reinfection = p_reinfection
        self.__history = {'S': [], 'E': [], 'I': [], 'R': []}
        
        # randomly place agents on the lattice, and  assign them to the exposed or susceptible compartment based on the initial exposure probability.
        for i in range(num_agents):
            while True:
                x, y = random.randint(0, lattice_size-1), random.randint(0, lattice_size-1)
                if self.__lattice.get_grid()[y][x] is None:
                    compartment = 'E' if random.random() < p_exposed else 'S'

                    # create superspreader or regular agent depending on index
                    if i < num_superspreaders:
                        agent = ag.SuperSpreader(x, y, compartment, spread_radius)
                    else:
                        agent = ag.Agent(x, y, compartment)
                    self.__lattice.place_agent(agent)
                    self.__agents.append(agent)
                    break

    def __count_compartments(self):
        
        # count the number of agents in each compartment and record the counts in the history for plotting later
        counts = {'S': 0, 'E': 0, 'I': 0, 'R': 0}
        for agent in self.__agents:
            counts[agent.get_compartment()] += 1
        for key in counts:
            self.__history[key].append(counts[key])
        return counts
    
    def __run_step(self):
        # carry out one monte carlo step by moving agents, checking neigbours, and updating compartments
        for agent in self.__agents:

            # move the agent to a random adjacent position on the lattice
            agent.move(self.__lattice.get_grid(), self.__lattice.get_size())

            # if the agent is infected, attempt to expose neighboring susceptible agents
            if agent.get_compartment() == 'I':
                # superspreaders infect over a larger radius, regular agents use radius 1
                radius = agent.get_spread_radius() if isinstance(agent, ag.SuperSpreader) else 1
                for neighbour in self.__lattice.get_neighbours(agent, radius):
                    if neighbour.get_compartment() == 'S' and random.random() < self.__beta:
                        neighbour.expose()

            # update the agents compartment based on the incubation and recovery rates
            agent.update_compartment(self.__sigma, self.__gamma, self.__p_reinfection)
   
    def run(self, num_steps):
        self.__count_compartments()  # record initial state
        for step in range(num_steps):

            # perform one Monte Carlo step
            self.__run_step()

            # record the compartment counts after each step
            self.__count_compartments()

            # print progress every 100 steps so the user can see that the simulation is running
            if step % 100 == 0:
                print(f"Completed {step}/{num_steps} steps")
        print(f"Simulation complete: {num_steps} steps finished")
    def plot(self, save_path=None):
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plotting the number of agents in each compartment over time
        ax.plot(self.__history['S'], label='Susceptible')
        ax.plot(self.__history['E'], label='Exposed')
        ax.plot(self.__history['I'], label='Infected')
        ax.plot(self.__history['R'], label='Recovered')

        # Setting plot attributes such as legend and title
        ax.set_xlabel('Monte Carlo Steps')
        ax.set_ylabel('Number of Agents')
        ax.set_title(f'Monte Carlo SEIR Simulation: beta={self.__beta}, sigma={self.__sigma}, gamma={self.__gamma}, R0={self.__beta/self.__gamma:.2f}')
        ax.legend()
        ax.grid(True)

        # Save the figure if a save path is provided
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show() 
    def plot_lattice(self, save_path=None):
        fig, ax = plt.subplots(figsize=(6, 6))

        # Create a color map for the compartments
        c_map = {'S': 'blue', 'E': 'orange', 'I': 'red', 'R': 'green'}

        # group agent positions by compartment for efficient plotting
        positions = {'S': [], 'E': [], 'I': [], 'R': []}
        for agent in self.__agents:
            positions[agent.get_compartment()].append((agent.get_x(), agent.get_y()))

        # plot the agents on the lattice with different colors for each compartment and a legend to indicate which color corresponds to which compartment
        for compartment, coords in positions.items():
            if coords:
                xs, ys = zip(*coords)
                ax.scatter(xs, ys, color=c_map[compartment], s=20)
                
        # ensures all compartments appear in the legend even if they have no agents in the final lattice state
        for compartment, color in c_map.items():
            ax.scatter([], [], color=color, label=compartment, s=20)
        ax.legend(loc='upper right')

        # Setting plot attributes such as title and limits
        ax.set_title('Final State of Lattice')
        ax.set_xlim(-1, self.__lattice.get_size())
        ax.set_ylim(-1, self.__lattice.get_size())
        ax.set_aspect('equal')
        ax.grid(True)
        
        # Save the figure if user provides a save path
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()