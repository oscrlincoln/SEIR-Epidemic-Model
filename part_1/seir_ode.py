import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import argparse

class SEIRModel:
    def __init__(self, beta, sigma, gamma):
        # Validate types before assigning to avoid errors
        if not all(isinstance(p, (int, float)) for p in [beta, sigma, gamma]):
            raise TypeError("Rate parameters must be numerical values")
        if any(p < 0 for p in [beta, sigma, gamma]):
            raise ValueError("Rate parameters must be non-negative")
        # Encapsulation of parameters to prevent external modification
        self.__beta = beta 
        self.__sigma = sigma
        self.__gamma = gamma

    def __seir_ode(self, t, y):
        # Reduced SEIR equations (s, e, i, r are fractions of the population which sum to 1)
        s, e, i, r = y
        dsdt = -self.__beta * s * i # susceptible individuals become exposed decreasing their number
        dedt = self.__beta * s * i - self.__sigma * e # exposed grows as susceptible individuals become exposed, but decreases as they become infected
        didt = self.__sigma * e - self.__gamma * i # infected grows as exposed individuals become infected, but decreases as they recover
        drdt = self.__gamma * i # recovered individuals grow as infected individuals recover
        return [dsdt, dedt, didt, drdt]
    
    # public method to solve the SEIR model ODEs given initial conditions and time span
    def solve(self, S0, E0, I0, R0, t_span, num_points):
        # Validates initial conditions before solving the ODE
        if not all(isinstance(x, (int, float)) and x >= 0 for x in [S0, E0, I0, R0]):
            raise TypeError("Initial conditions must be non-negative numerical values")
        # Initial conditions should sum to 1
        if not abs(S0 + E0 + I0 + R0 - 1) < 1e-9: # 1e-9 allows for floating-point precision issues
            raise ValueError("Initial conditions must sum to 1 (representing fractions of the population)")

        initial_conditions = [S0, E0, I0, R0]

        # solve the coupled ODEs using solve_ivp because it is more efficient than Euler methods
        # t_eval is used to specify the time points at which to store the calculated solution
        # t_span is the time range for the simulation, and num_points determines how many points to evaluate within that range
        solution = solve_ivp(self.__seir_ode, t_span, initial_conditions, t_eval=np.linspace(t_span[0], t_span[1], num_points))
        
        # checks that the solver ran successfully
        if not solution.success:
            raise RuntimeError("ODE solver failed to converge")

        return solution.t, solution.y
    
    def plot(self, t, y, save_path=None):
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plotting each SEIR component as a fraction of the population group
        ax.plot(t, y[0], label='Susceptible')
        ax.plot(t, y[1], label='Exposed')
        ax.plot(t, y[2], label='Infected')
        ax.plot(t, y[3], label='Recovered')
        
        # Setting plot attributes such as legend and title
        ax.set_xlabel('Time (days)')
        ax.set_ylabel('Fraction of Population')

        # Includes the model parameters and the basic reproduction number R0 for documentation
        ax.set_title(f'SEIR Model: beta={self.__beta}, sigma={self.__sigma}, gamma={self.__gamma}, R0={self.__beta/self.__gamma:.2f}')
        ax.legend()
        ax.grid(True)

        # save the figure if user provides a save path
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')

        plt.show()   
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SEIR model simulation")

    # model rate parameters with default values that can be overridden by a user when running the script from the command line
    parser.add_argument("--beta", type=float, default=1.0, help="Infection rate")
    parser.add_argument("--sigma", type=float, default=1.0, help="Incubation rate")
    parser.add_argument("--gamma", type=float, default=0.1, help="Recovery rate")
    
    # Initial conditions - again can be overriden by the user
    parser.add_argument("--S0", type=float, default=0.99, help="Initial fraction of susceptible population")
    parser.add_argument("--E0", type=float, default=0.01, help="Initial fraction of exposed population")
    parser.add_argument("--I0", type=float, default=0.0, help="Initial fraction of infected population")
    parser.add_argument("--R0", type=float, default=0.0, help="Initial fraction of recovered population")

    # Number of points that should be evaluated within the time range (e.g. 1000 points within a time range of 100 is 10 points per second)
    parser.add_argument("--num_points", type=int, default=1000, help="Number of time points to evaluate within the time span")

    # Simulation time parameters and save path for the figure
    parser.add_argument("--t_end", type=float, default=100.0, help="End time for simulation")
    parser.add_argument("--save", type=str, default=None, help="File path to save figure")

    args = parser.parse_args()

    # Create the SEIRModel with the specified parameters, solve the ODEs, and plot the results
    model = SEIRModel(args.beta, args.sigma, args.gamma)
    t, y = model.solve(args.S0, args.E0, args.I0, args.R0, (0, args.t_end), args.num_points)
    model.plot(t, y, save_path=args.save)
