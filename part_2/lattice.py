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

    def get_neighbours(self, agent, radius=1):
        neighbours = []
        x, y = agent.get_x(), agent.get_y()
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                # skip own cell and diagonal neighbours using Manhattan distance
                if abs(dx) + abs(dy) == 0 or abs(dx) + abs(dy) > radius:
                    continue
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