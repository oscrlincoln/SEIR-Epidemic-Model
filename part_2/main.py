import argparse
import random
import matplotlib.pyplot as plt
import simulation as simul

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Monte Carlo SEIR simulation")
    
    # lattice and agent parameters including superspreaders
    parser.add_argument("--lattice_size", type=int, default=100, help="Size of the lattice grid")
    parser.add_argument("--num_agents", type=int, default=250, help="Number of agents")
    parser.add_argument("--num_superspreaders", type=int, default=0, help="Number of superspreaders")
    parser.add_argument("--spread_radius", type=int, default=3, help="How many more people a superspreader can infect compared to a regular infected agent")
    
    # disease parameters
    parser.add_argument("--beta", type=float, default=1.0, help="Infection rate per MCS")
    parser.add_argument("--sigma", type=float, default=0.1, help="Incubation rate per MCS")
    parser.add_argument("--gamma", type=float, default=0.005, help="Recovery rate per MCS")
    parser.add_argument("--p_exposed", type=float, default=0.05, help="Initial fraction of exposed agents")
    parser.add_argument("--p_reinfection", type=float, default=0.0, help="Probability of reinfection per MCS")
    
    # simulation parameters
    parser.add_argument("--num_steps", type=int, default=2000, help="Number of Monte Carlo steps")
    
    # specify the random generator seed
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")

    # output
    parser.add_argument("--save", type=str, default=None, help="Path to save population plot")
    parser.add_argument("--save_lattice", type=str, default=None, help="Path to save lattice plot")
    
    args = parser.parse_args()

    # implement the seed
    if args.seed is not None:
        random.seed(args.seed)
    
    # instantiate and run simulation - all validation handled by classes
    sim = simul.Simulation(args.lattice_size, args.num_agents, args.beta, args.sigma, args.gamma, args.p_exposed, args.p_reinfection, args.num_superspreaders, args.spread_radius)
    sim.run(args.num_steps)
    sim.plot(save_path=args.save)
    sim.plot_lattice(save_path=args.save_lattice)
    
    
       