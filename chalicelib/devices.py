import numpy as np
from itertools import combinations_with_replacement, product
from fractions import Fraction
from bisect import bisect_left
from collections import Counter
from math import gcd
from functools import reduce

class Pattern:
    def __init__(
            self,
            p:int,
            d:int,
            n_max:int=9,
            tol_hi:float=1.05,
            tol_lo=None,
            ):
        self.p = int(p)
        self.d = int(d)
        self.r = self.d/self.p
        self.d_min = self.determine_d_min(self.d) if tol_lo is None else round(self.d * tol_lo)
        self.d_max = round(self.d * tol_hi)
        self.n_max = int(n_max)  # maximum number of hileras
        self.patterns = self.gen_patterns()

    def determine_d_min(self, d):
        """Determine the minimum number of devices to install."""
        if d == 500:
            tol = 0.04
        elif d == 1000:
            tol = 0.03
        elif d == 50:
            tol = 0.06
        else:
            tol = 0.05
        return round((1 - tol) * d)

    def gen_patterns(self):
        """Generate list of admissible patterns."""
        # Find pair of neighboring patterns around r
        if self.r <= 1:
            # Generate list of patterns that satisfy r <= 1
            all_patterns = [0.0] + [1/i for i in range(10, 0, -1)]
            # Find index of r in the list of patterns
            i = bisect_left(all_patterns, self.r)
            # Get the four neighboring patterns around r, avoiding index out of bounds
            patterns = all_patterns[max(i-1, 0):i+1] + all_patterns[max(i-2, 0):i-1] + all_patterns[i+1:i+2]
        elif self.r > 1:
            # Find two pairs of neighboring patterns around r
            patterns = (np.floor(self.r), np.ceil(self.r), np.floor(self.r) - 1, np.ceil(self.r) + 1)
            # remove patterns below 1, if any
            patterns = [p for p in patterns if p >= 1]
        return patterns
        

    def gen_solution_space(self, max_unique_patterns:int=3):
        """Generate solution space with all possible combinations of patterns.
        This function is completely independent of the problem, and just depends on two user-defined parameters: 
        `n_max` (maximum number of patterns) and `patterns` (list of possible patterns)."""
        def generate_combinations(elements, n_max):
            # Helper function to calculate the GCD of a list of numbers
            def find_gcd(list):
                x = reduce(gcd, list)
                return x

            # Generate all unique combinations up to length n_max
            result = set()
            for n in range(1, n_max + 1):
                for combo in combinations_with_replacement(elements, n):
                    # Count elements and reduce their counts by the GCD to find their simplest proportional form
                    counts = Counter(combo)
                    gcd_counts = find_gcd(counts.values())
                    reduced_counts = tuple(sorted((element, count // gcd_counts) for element, count in counts.items()))
                    # Add the reduced form to the result set to ensure uniqueness
                    result.add(reduced_counts)
            
            # Convert the reduced forms back to the original format (as tuples of elements)
            final_result = []
            for reduced in result:
                combo = []
                for element, count in reduced:
                    combo.extend([element] * count)
                final_result.append(tuple(combo))
            
            return final_result 
        
        # Generate all possible combinations of patterns up to length `n_max`
        solution_space = generate_combinations(self.patterns, self.n_max)
        
        # Filter out solutions with more than `max_unique_patterns` unique patterns
        # i.e. we don't want solutions that have "too many" distinct patterns (e.g. [1/2, 1/3, 1/4, 1/5])
        solution_space = [s for s in solution_space if len(set(s)) <= max_unique_patterns]
        
        # Finally, we want to filter solutions that are clearly off the mark from `self.r`
        # i.e. discard solutions if _all_ patterns are above or below `self.r`
        # e.g. if `r`==0.67, we don't want solutions that only contain 1/2 and 1/3, because they can't reach 0.67
        # NOTE: This is a very loose filter, on purpose
        solution_space = [s for s in solution_space if (min(s) <= self.r <= max(s))]

        return solution_space


    def compute_densities_over_solution_space(self, solution_space):
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
            n_ = np.floor(self.p/n)
            # Convert the entire R to ratios at once
            numerators = []
            denominators = []
            for f in R:
                num, denom = Fraction(f).limit_denominator().as_integer_ratio()
                numerators.append(num)
                denominators.append(denom)
            # Cast as numpy arrays for vectorized operations
            numerators = np.array(numerators)
            denominators = np.array(denominators)
            # Compute densities of "full" and "partial" patterns
            d_full_pattern = np.floor(n_ / denominators) * numerators
            d_partial_pattern = np.minimum(np.mod(n_, denominators), numerators)
            # Return total density
            return int(np.sum(d_full_pattern) + np.sum(d_partial_pattern))

        # Compute densities over solution space and couple them with their corresponding R
        # NOTE: we immediately filter out solutions with density below the required minimum
        solutions = [(density, R) for R in solution_space if (density := compute_real_density(R, self.p)) >= self.d_min]
        return solutions


    def find_optimal_solutions(self, solutions, fractions:bool=False):
        def convert2fractions(x):
            return [str(Fraction(i).limit_denominator()) for i in x]
        
        # Filter solutions with density above the maximum
        filtered_solutions = [sol for sol in solutions if sol[0] <= self.d_max]
        
        # Check number of solutions
        if len(solutions) == 0 or len(filtered_solutions) == 0:
            return None
        
        # Get solution with minimum number of patterns, and then with minimum density
        sol_min_h_n = sorted(filtered_solutions, key=lambda element: (len(element[1]), element[0]))[0]
       
        # Get solution with minimum density, and then with minimum number of patterns
        sol_min_d = sorted(filtered_solutions, key=lambda element: (element[0], len(element[1])))[0]
        
        # Convert solutions to fractions if requested
        if fractions:
            sol_min_h_n = (sol_min_h_n[0], convert2fractions(sol_min_h_n[1]))
            sol_min_d = (sol_min_d[0], convert2fractions(sol_min_d[1]))
        return sol_min_h_n, sol_min_d


    def run(self, fractions:bool=False):
        solution_space = self.gen_solution_space()
        solutions = self.compute_densities_over_solution_space(solution_space)
        optimal_sols = self.find_optimal_solutions(solutions, fractions=fractions)
        return optimal_sols
