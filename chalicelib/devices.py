import numpy as np
from itertools import combinations_with_replacement

class Pattern:
    def __init__(self, p, d_min, n_h=4, tolerance_factor=1.1):
        self.p = p
        self.d_min = d_min
        self.n_h = n_h  # maximum number of hileras
        self.tolerance_factor = tolerance_factor    # tolerance factor for max density

        self.patterns = [1.0, 4/5, 2/3, 3/5] + [1/i for i in range(2, 6)]
        self.X = self.compute_densities_over_solution_space()


    def gen_solution_space(self):
        """Generate solution space with all possible combinations of patterns.
        This function is completely independent of the problem, and just depends on two user-defined parameters: 
        `n_h` (maximum number of patterns) and `patterns` (list of possible patterns)."""                
        def generate_combinations(elements, n):
            combinations = []
            for r in range(1, n+1):
                combinations.extend(combinations_with_replacement(elements, r))
            return combinations
        
        solution_space = generate_combinations(self.patterns, self.n_h)
        return solution_space


    def compute_densities_over_solution_space(self):
        """Compute real densities (objective function) over solution space.
        """        
        def compute_real_density(R_i, p):
            """Compute the real density of a solution vector R_i.

            Args:
                R_i (tuple): Solution vector.
                p (int): Number of plants.

            Returns:
                X (list): List of tuples with computed density and solution vector.
            """            
            n = len(R_i)
            d = np.sum(np.round(np.array(R_i)*p/n))
            return d
        
        R = self.gen_solution_space()
        X = []
        for R_i in R:
            d = compute_real_density(R_i, self.p)
            X.append((d, R_i))
        return X

    def find_optimal_solutions(self):
        # First we keep only the feasible solutions (within density bounds)
        solutions = [x for x in self.X if x[0] >= self.d_min and x[0] <= self.d_min*self.tolerance_factor]
        # Get solution with minimum number of patters, and then with minimum density
        sol_min_h_n = sorted(solutions, key=lambda element: (len(element[1]), element[0]))[0]
        # Get solution with minimum density, and then with minimum number of patterns
        sol_min_d = sorted(solutions, key=lambda element: (element[0], len(element[1])))[0]
        return sol_min_h_n, sol_min_d
    
