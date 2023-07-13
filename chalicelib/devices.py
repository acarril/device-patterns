import numpy as np
from itertools import combinations_with_replacement
from fractions import Fraction

class Pattern:
    def __init__(self, p, d_min, n_max=4, tolerance_factor=1.1):
        self.p = p
        self.d_min = d_min
        self.n_max = n_max  # maximum number of hileras
        self.tolerance_factor = tolerance_factor    # tolerance factor for max density

        self.patterns = [1.0, 4/5, 2/3, 3/5] + [1/i for i in range(2, 6)]
        self.X = self.compute_densities_over_solution_space()

    def convert2fractions(self, x):
        return [str(Fraction(i).limit_denominator()) for i in x]

    def gen_solution_space(self):
        """Generate solution space with all possible combinations of patterns.
        This function is completely independent of the problem, and just depends on two user-defined parameters: 
        `n_max` (maximum number of patterns) and `patterns` (list of possible patterns)."""                
        def generate_combinations(elements, n):
            combinations = []
            for r in range(1, n+1):
                combinations.extend(combinations_with_replacement(elements, r))
            return combinations
        
        all_R = generate_combinations(self.patterns, self.n_max)
        return all_R


    def compute_densities_over_solution_space(self):
        """Compute real densities (objective function) over solution space.
        """        
        def compute_real_density(R, p):
            """Compute the real density of a solution vector R.

            Args:
                R (tuple): Solution vector.
                p (int): Number of plants.

            Returns:
                d (int): Number of installed devices.
            """            
            n = len(R)
            n_ = np.floor(p/n)  # still haven't thought through what to do if this is not an integer
            R_frac = [Fraction(f).limit_denominator() for f in R]
            d_full_pattern = [np.floor((n_)/f.as_integer_ratio()[1])*f.as_integer_ratio()[0] for f in R_frac]
            d_partial_pattern = [min(np.mod(n_, f[1]), f[0]) for f in [f.as_integer_ratio() for f in R_frac]]
            return int(np.sum(d_full_pattern) + np.sum(d_partial_pattern))
        
        all_R = self.gen_solution_space()
        X = []
        for R in all_R:
            d = compute_real_density(R, self.p)
            X.append((d, R))
        return X

    def find_optimal_solutions(self, fractions=False):
        # Keep only the feasible solutions (within density bounds)
        solutions = [x for x in self.X if x[0] >= self.d_min and x[0] <= self.d_min*self.tolerance_factor]
        # Get solution with minimum number of patters, and then with minimum density
        sol_min_h_n = sorted(solutions, key=lambda element: (len(element[1]), element[0]))[0]
        # Get solution with minimum density, and then with minimum number of patterns
        sol_min_d = sorted(solutions, key=lambda element: (element[0], len(element[1])))[0]
        if fractions:
            sol_min_h_n = (sol_min_h_n[0], self.convert2fractions(sol_min_h_n[1]))
            sol_min_d = (sol_min_d[0], self.convert2fractions(sol_min_d[1]))
        return sol_min_h_n, sol_min_d
    