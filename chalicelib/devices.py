import numpy as np
from itertools import groupby, combinations_with_replacement
from fractions import Fraction
from bisect import bisect_left

class Pattern:
    def __init__(
            self,
            p,
            d_min,
            n_max=8,
            tolerance_factor=1.5,
            sag_compliant=True
            ):
        self.p = int(p)
        self.d_min = int(d_min)
        self.n_max = int(n_max)  # maximum number of hileras
        self.tolerance_factor = float(tolerance_factor)    # tolerance factor for max density
        self.sag_compliant = bool(int(sag_compliant))  # whether to use sag-compliant patterns or not
        self.r = self.d_min/self.p
        self.patterns = self.gen_patterns()
        self.X = self.compute_densities_over_solution_space()

    def gen_patterns(self):
        """Generate list of admissible patterns."""
        r = self.d_min/self.p
        # Patterns for r <= 1
        if r <= 1:
            if self.sag_compliant:
                patterns = [1/i for i in range(1, 11)] + [0.0]
            else:
                patterns = [1.0, 4/5, 2/3, 3/5] + [1/i for i in range(2, 6)]
        # Patterns for r > 1
        if r > 1:
            patterns = [np.floor(r), np.ceil(r)]
        return patterns

    def gen_solution_space_sag(self, r, n_max):
        def generate_combinations(pair, n_max):
            if n_max == 1:
                return [(pair[0],), (pair[1],)]
            
            combinations = [(pair[0],), (pair[1],), tuple(pair)]
            
            for n in range(3, n_max + 1):
                for combo in product(pair, repeat=n):
                    if len(set(combo)) > 1:  # Ensure both numbers are present
                        combinations.append(combo)
                        
            return combinations

        # Find pair of neighboring patterns around r
        if r <= 1:
            # Here the tricky part is to leave out patterns ∈ (0.5, 1);
            # otherwise, we could use the same method as for r > 1
            patterns = [0.0] + [1/i for i in range(10, 0, -1)]
            i = bisect_left(patterns, r)
            pair = (patterns[i], patterns[i-1])
        elif r > 1:
            pair = (np.floor(r), np.ceil(r))
        
        # Generate all possible combinations of patterns up to length `n_max`
        return generate_combinations(pair, n_max)


    def gen_solution_space(self):
        """Generate solution space with all possible combinations of patterns.
        This function is completely independent of the problem, and just depends on two user-defined parameters: 
        `n_max` (maximum number of patterns) and `patterns` (list of possible patterns)."""
        
        def all_equal(iterable):
            """"Check that all elements of iterable are equal"""
            g = groupby(iterable)
            return next(g, True) and not next(g, False)
                   
        def generate_combinations(elements, n):
            """Generate all possible combinations of `elements` with up to length `n`."""
            all_combinations = []
            for r in range(1, n+1):
                all_combinations.extend(combinations_with_replacement(elements, r))
            return all_combinations
        
        # Generate all possible combinations of patterns up to length `n_max`
        # NOTE: we filter out combinations of length>1 that are all equal
        all_R = [p for p in generate_combinations(self.patterns, self.n_max) if not len(p)==1 or all_equal(p)]
        
        # Filter out solutions that are not SAG-compliant
        # SAG-compliant solutions must use (i) no more than 2 patterns,
        # and (ii) the patterns must be consecutive in the list of patterns
        if self.sag_compliant:
            filtered_R = []
            for R in all_R:
                R_unique = set(R)
                if len(R_unique) <= 2:
                    indexes = tuple(self.patterns.index(r) for r in R_unique)
                    indexes_diff = max(indexes) - min(indexes)
                    if abs(indexes_diff) <= 1:
                        filtered_R.append(R)
            
            return filtered_R

        else:
            return all_R


    def compute_densities_over_solution_space(self):
        """Compute real densities (objective function) over solution space.
        """        
        def compute_real_density(R):
            """Compute the real density of a solution vector R.

            Args:
                R (tuple): Solution vector.

            Returns:
                d (int): Number of installed devices.
            """            
            n = len(R)
            n_ = np.floor(self.p/n)  # still haven't thought through what to do if this is not an integer
            ratios = [Fraction(f).limit_denominator().as_integer_ratio() for f in R]
            d_full_pattern = [np.floor((n_)/ratio[1]) * ratio[0] for ratio in ratios]
            d_partial_pattern = [min(np.mod(n_, ratio[1]), ratio[0]) for ratio in ratios]
            return int(np.sum(d_full_pattern) + np.sum(d_partial_pattern))
        
        all_R = self.gen_solution_space()
        densities = [compute_real_density(R) for R in all_R]
        return list(zip(densities, all_R))

    def find_optimal_solutions(self, fractions=False):
        # Keep only the feasible solutions (within density bounds)
        solutions = [x for x in self.X if x[0] >= self.d_min and x[0] <= self.d_min*self.tolerance_factor]
        # Check number of solutions
        if len(solutions) == 0:
            return None
        # Get solution with minimum number of patters, and then with minimum density
        sol_min_h_n = sorted(solutions, key=lambda element: (len(element[1]), element[0]))[0]
        # Get solution with minimum density, and then with minimum number of patterns
        sol_min_d = sorted(solutions, key=lambda element: (element[0], len(element[1])))[0]
        # Convert solutions to fractions if requested
        if fractions:
            sol_min_h_n = (sol_min_h_n[0], self.convert2fractions(sol_min_h_n[1]))
            sol_min_d = (sol_min_d[0], self.convert2fractions(sol_min_d[1]))
        return sol_min_h_n, sol_min_d
