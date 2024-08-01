import numpy as np
from itertools import combinations_with_replacement
from fractions import Fraction
from bisect import bisect_left
from collections import Counter

class Pattern:
    def __init__(
            self,
            p:int,
            d:int,
            tol_hi:float=1,
            tol_lo=None,
            ):
        self.p = int(p)
        self.d = int(d)
        self.r = self.d/self.p
        self.d_min = self.determine_d_min(self.d) if tol_lo is None else round(self.d * tol_lo)
        self.d_max = round(self.d * float(tol_hi))
        self.patterns = self.gen_patterns()

    def determine_d_min(self, d:int) -> int:
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

    def gen_patterns(self) -> list:
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
        

    def gen_solution_space(self, n:int, max_unique_patterns:int=3) -> list:
        """Generate solution space with all admissible combinations of patterns.
        This function is completely independent of the problem, and just depends on two parameters:
        A list of unique `patterns` to combine, and the length of the combinations with replacement `n`."""
        
        def generate_combinations(elements:list, n:int) -> list:
            """Generate all possible combinations of values in `elements` of length `n`, removing 'reducible' combinations."""
            def is_reducible(combination) -> bool:
                """Determine wether a combination of patterns is 'reducible' or not.
                A combination is reducible if the count of all elements can be reduced by a common divisor greater than 1.
                Ex. 1: [1/2, 1/2, 1/3, 1/3] is reducible because both counts can be reduced by 2 --> [1/2, 1/3]."""
                if len(combination) > 1:
                    counts = Counter(combination).values()
                    if 1 not in counts and len(set(counts)) == 1:
                            return True
                return False

            combinations = combinations_with_replacement(elements, n)
            return [combo for combo in combinations if not is_reducible(combo)]

        # Generate all possible non-reducible combinations of patterns of length `n`
        solution_space = generate_combinations(self.patterns, n)
        
        # Filter out solutions with more than `max_unique_patterns` unique patterns
        # i.e. we don't want solutions that have "too many" distinct patterns (e.g. [1/2, 1/3, 1/4, 1/5])
        solution_space = [s for s in solution_space if len(set(s)) <= max_unique_patterns]
        return solution_space
    
    def reorder_solution(self, solution: list) -> list:
        """Reorder the solution to start with the largest non-zero value and distribute zeros evenly."""
        if not solution or all(x == 0 for x in solution):
            return solution  # No reordering needed if all are zeros

        # Count zeros and find non-zero values
        zeros = solution.count(0)
        non_zero_values = [x for x in solution if x != 0]

        if not non_zero_values:
            return solution  # No non-zero values to reorder

        # Sort non-zero values in descending order
        non_zero_values.sort(reverse=True)

        # Create a new list to hold the reordered solution
        new_solution = []

        # Start with the largest non-zero value
        new_solution.append(non_zero_values[0])

        # Interleave the remaining non-zero values with zeros
        for i in range(1, len(non_zero_values)):
            new_solution.append(0)  # Add a zero before the next non-zero value
            new_solution.append(non_zero_values[i])

        # If there are remaining zeros after interleaving, append them
        remaining_zeros = zeros - (len(non_zero_values) - 1)
        if remaining_zeros > 0:
            new_solution.extend([0] * remaining_zeros)

        return new_solution


    def compute_densities_over_solution_space(self, solution_space:list) -> list:
        """Compute real densities (objective function) over solution space."""

        def compute_real_density(R:tuple) -> int:
            """Compute the real density of a solution vector R.

            Args:
                R (tuple): Solution vector.
                p (int): Number of plants.

            Returns:
                (int): Number of installed devices.
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

        # Compute densities over solution space and couple them with their corresponding solution
        solutions = [(compute_real_density(R), R) for R in solution_space]
        return solutions


    def find_optimal_solution(self, solutions:list, criterion:str, fractions:bool) -> tuple:
        def convert2fractions(x):
            return [str(Fraction(i).limit_denominator()) for i in x]
        
        # Filter out unfeasible solutions
        # i.e. those that don't meet the density constraints (d_min, d_max)
        filtered_solutions = [sol for sol in solutions if (self.d_min <= sol[0] <= self.d_max)]
        
        # Check number of solutions & short circuit if 0
        if len(solutions) == 0 or len(filtered_solutions) == 0:
            return None
        
        # Get solution with minimum number of patterns, and then with minimum density
        if criterion == 'min_h' or criterion is None:
            optimal_solution = sorted(filtered_solutions, key=lambda element: (len(element[1]), element[0]))[0]
       
        # Get solution with minimum density, and then with minimum number of patterns
        if criterion == 'min_d':
            optimal_solution = sorted(filtered_solutions, key=lambda element: (element[0], len(element[1])))[0]
        # Reorder the optimal solution if it contains zeros
        reordered_solution = self.reorder_solution(optimal_solution[1])
        # Convert solutions to fractions if requested
        if fractions:
            optimal_solution = (optimal_solution[0], convert2fractions(reordered_solution))
        else:
            optimal_solution = (optimal_solution[0], reordered_solution)
        
        return optimal_solution


    def run(self, criterion:str='min_h', fractions:bool=False) -> tuple:
        n = 0
        optimal_solution = None
        while not optimal_solution:
            n += 1
            solution_space = self.gen_solution_space(n)
            solutions = self.compute_densities_over_solution_space(solution_space)
            optimal_solution = self.find_optimal_solution(solutions, criterion, fractions)

        return (*optimal_solution, criterion)

# Example values for p and d
#p = 4420  # Number of plants
#d = 200 # Number of devices

# Create an instance of the Pattern class
#pattern_instance = Pattern(p, d)

# Run the optimization to find the optimal solution
#optimal_density, optimal_patterns, criterion = pattern_instance.run(criterion='min_h', fractions=True)

# Print the results
#print(f"Optimal Density: {optimal_density}")
#print(f"Optimal Patterns: {optimal_patterns}")
#print(f"Criterion Used: {criterion}")