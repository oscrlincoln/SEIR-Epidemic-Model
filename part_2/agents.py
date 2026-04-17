import random

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
        
    def update_compartment(self, sigma, gamma, p_reinfection=0.0):
        if self.__compartment == 'E':
            # Exposed individuals become infected with probability sigma
            if random.random() < sigma:
                self.__compartment = 'I'
        elif self.__compartment == 'I':
            # Infected individuals recover with probability gamma
            if random.random() < gamma:
                self.__compartment = 'R'
        elif self.__compartment == 'R':
            # recovered individuals can be reinfected with probability p_reinfection
            if random.random() < p_reinfection:
                self.__compartment = 'S'

    def expose(self):

        # Susceptible individuals become exposed if they are adjacent to an infected individual
        if self.__compartment == 'S':
            self.__compartment = 'E'

class SuperSpreader(Agent):
    def __init__(self, x, y, compartment, spread_radius=2):

        # validate that the spread radius is a non-negative numerical value
        if not isinstance(spread_radius, (int, float)) or spread_radius < 1:
            raise ValueError("Spread radius must be a positive integer")
        
        # call the parent constructor to initialise shared attributes of the agent
        super().__init__(x, y, compartment)

        # private attribute which is unique to the superspreader agent
        self.__spread_radius = spread_radius  # the radius within which this agent can infect others

    def get_spread_radius(self):
        return self.__spread_radius