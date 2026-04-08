import random
import matplotlib.pyplot as plt
import argparse

class Agent:
    def __init__(self, x, y, compartment):

        # validate that the coordinates are numerical and non-negative
        if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
            raise TypeError("Coordinates must be numerical values")
        if x < 0 or y < 0:
            raise ValueError("Coordinates must be non-negative")
        
        # validate that the compartment is one of the expected values
        valid_compartments = ['S', 'E', 'I', 'R']
        if compartment not in valid_compartments:
            raise ValueError("Compartment must be one of 'S', 'E', 'I', 'R'")
        
        # encapsulates the agent's attributes to prevent external changes
        self.__x = x
        self.__y = y
        self.__compartment = compartment

    # public getter methods so that other classes can access the agent's attributes despite being private
    def get_x(self):
        return self.__x
    def get_y(self):
        return self.__y
    def get_compartment(self):
        return self.__compartment
    
    def move(self,lattice_grid, lattice_size):
        
        # randomly chooses a direction to move (up, down, left, right)
        dx, dy = random.choice([(-1,0), (1,0), (0,-1), (0,1)])
        
        # check that the new position is within the bounds of the lattice
        if 0 <= (self.__x + dx) < lattice_size and 0 <= (self.__y + dy) < lattice_size and lattice_grid[self.__y + dy][self.__x + dx] is None:
            # update the agent and lattice positions
            lattice_grid[self.__y][self.__x] = None  # clear old position
            self.__x += dx # update x coordinate
            self.__y += dy # update y coordinate
            lattice_grid[self.__y][self.__x] = self  # move to new position
        
    def update_compartment(self, sigma, gamma):
        if self.__compartment == 'E':
            # Exposed individuals become infected with probability sigma
            if random.random() < sigma:
                self.__compartment = 'I'
        elif self.__compartment == 'I':
            # Infected individuals recover with probability gamma
            if random.random() < gamma:
                self.__compartment = 'R'

    def expose(self):

        # Susceptible individuals become exposed if they are adjacent to an infected individual
        if self.__compartment == 'S':
            self.__compartment = 'E'
    

class Lattice:
    def __init__(self, size):
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Size must be a positive integer")
        
        # create a 2D grid of the specified size with None to represent empty spaces
        self.__size = size
        self.__grid = [[None for _ in range(size)] for _ in range(size)]
    
    def place_agent(self, agent):
        
        # place the agent on the lattice grid at its coordinates and check that the position is not already occupied by another agent
        if self.__grid[agent.get_y()][agent.get_x()] is None:
            self.__grid[agent.get_y()][agent.get_x()] = agent
        else:
            raise ValueError("Position already occupied by another agent")
    
    def remove_agent(self, agent):

        # remove the agent from the lattice grid 
        self.__grid[agent.get_y()][agent.get_x()] = None
    def get_neighbours(self, agent):

        # get the neighboring agents (up, down, left, right) of the given agent
        neighbours = []
        x, y = agent.get_x(), agent.get_y()
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.__size and 0 <= ny < self.__size:
                neighbour = self.__grid[ny][nx]
                if neighbour is not None:
                    neighbours.append(neighbour)
        return neighbours
    
    def get_grid(self):
        return self.__grid
    
    def get_size(self):
        return self.__size
    
class Simulation:
    def __init__(self, lattice_size, num_agents, beta, sigma, gamma, p_exposed=0.05):
        if not isinstance(lattice_size, int) or lattice_size <= 0:
            raise ValueError("Lattice size must be a positive integer")
        if not isinstance(num_agents, int) or num_agents <= 0:
            raise ValueError("Number of agents must be a positive integer")
        if not all(isinstance(p, (int, float)) for p in [beta, sigma, gamma, p_exposed]):
            raise TypeError("Rate parameters and probability must be numerical values")

        self.__lattice = Lattice(lattice_size)
        self.__agents = []
        self.__beta = beta
        self.__sigma = sigma
        self.__gamma = gamma
        self.__p_exposed = p_exposed
        self.__history = {'S': [], 'E': [], 'I': [], 'R': []}
        
        # randomly place agents on the lattice and assign them to the susceptible compartment
        for _ in range(num_agents):

            # randomly select an empty position on the lattice to place the agent
            while True:
                x, y = random.randint(0, lattice_size-1), random.randint(0, lattice_size-1)
                if self.__lattice.get_grid()[y][x] is None:

                    # assign compartment based on p_exposed probability
                    compartment = 'E' if random.random() < p_exposed else 'S'
                    agent = Agent(x, y, compartment)

                    # place the agent on the lattice and add it to the list of agents
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
                for neighbour in self.__lattice.get_neighbours(agent):
                    if neighbour.get_compartment() == 'S' and random.random() < self.__beta:
                        neighbour.expose()

            # update the agents compartment based on the incubation and recovery rates
            agent.update_compartment(self.__sigma, self.__gamma)
   
    def run(self, num_steps):
        self.__count_compartments()  # record initial state
        for _ in range(num_steps):
            self.__run_step()

            # record the compartment counts after each step
            self.__count_compartments()
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Monte Carlo SEIR simulation")
    
    # lattice and agent parameters
    parser.add_argument("--lattice_size", type=int, default=100, help="Size of the lattice grid")
    parser.add_argument("--num_agents", type=int, default=250, help="Number of agents")
    
    # disease parameters
    parser.add_argument("--beta", type=float, default=1.0, help="Infection rate per MCS")
    parser.add_argument("--sigma", type=float, default=0.1, help="Incubation rate per MCS")
    parser.add_argument("--gamma", type=float, default=0.005, help="Recovery rate per MCS")
    parser.add_argument("--p_exposed", type=float, default=0.05, help="Initial fraction of exposed agents")
    
    # simulation parameters
    parser.add_argument("--num_steps", type=int, default=2000, help="Number of Monte Carlo steps")
    
    # output
    parser.add_argument("--save", type=str, default=None, help="Path to save population plot")
    parser.add_argument("--save_lattice", type=str, default=None, help="Path to save lattice plot")
    
    args = parser.parse_args()
    
    # instantiate and run simulation - all validation handled by classes
    sim = Simulation(args.lattice_size, args.num_agents, args.beta, args.sigma, args.gamma, args.p_exposed)
    sim.run(args.num_steps)
    sim.plot(save_path=args.save)
    sim.plot_lattice(save_path=args.save_lattice)
    
    
       