import numpy as np
from itertools import combinations_with_replacement
from fractions import Fraction
from bisect import bisect_left

class Pattern:
    def __init__(
            self,
            p: int,
            d_min: int,
            n_max: int = 2,
            tolerance_factor: float = 1.05,
            sag_compliant: bool = True
            ):
        self.p = int(p)
        self.d_min = int(d_min)
        self.n_max = int(n_max)  # maximum number of hileras
        self.tolerance_factor = float(tolerance_factor)  # tolerance factor for max density
        self.sag_compliant = bool(int(sag_compliant))  # whether to use sag-compliant patterns or not
        self.r = self.d_min / self.p
        self.patterns = self.gen_patterns()

    def gen_patterns(self):
        """Generate list of admissible patterns."""
        r = self.d_min / self.p
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
        def generate_combinations(elements, n):
            return list(combinations_with_replacement(elements, n))

        # Find patterns around r
        if r <= 1:
            patterns = [0.0] + [1/i for i in range(15, 0, -1)]
            i = bisect_left(patterns, r)
            neighbors = (patterns[i], patterns[i - 1], patterns[i - 2])
        elif r > 1:
            neighbors = (np.floor(r), np.ceil(r), np.floor(r) + 1)

        solution_space = []
        for num_patterns in range(1, n_max + 1):
            for combo in generate_combinations(neighbors, num_patterns):
                # Ensure no redundant patterns are added
                if len(set(combo)) > 1 or combo.count(combo[0]) == 1:
                    solution_space.append(combo)

        return solution_space


    def gen_solution_space(self):
        """Generate solution space with all possible combinations of patterns."""
        def generate_combinations(elements, n):
            return list(combinations_with_replacement(elements, n))

        return generate_combinations(self.patterns, self.n_max)

    def compute_densities_over_solution_space(self, solution_space, p, d_min):
        def compute_real_density(R, p):
            n = len(R)
            n_ = np.floor(p/n)
            numerators = []
            denominators = []
            for f in R:
                num, denom = Fraction(f).limit_denominator().as_integer_ratio()
                numerators.append(num)
                denominators.append(denom)
            numerators = np.array(numerators)
            denominators = np.array(denominators)
            d_full_pattern = np.floor(n_ / denominators) * numerators
            d_partial_pattern = np.minimum(np.mod(n_, denominators), numerators)
            return int(np.sum(d_full_pattern) + np.sum(d_partial_pattern))

        # Determine tolerance_factor_down based on d_min
        if d_min == 500:
            tolerance_factor_down = 0.04
        elif d_min == 1000:
            tolerance_factor_down = 0.03
        elif d_min == 50:
            tolerance_factor_down = 0.06
        else:
            tolerance_factor_down = 0.05

        solutions = [(density, R) for R in solution_space if
                     (density := compute_real_density(R, p)) >= (d_min - (d_min * tolerance_factor_down))]
        return solutions

    def find_optimal_solutions(self, solutions, d_max, fractions: bool = False):
        def convert2fractions(x):
            return [str(Fraction(i).limit_denominator()) for i in x]

        filtered_solutions = [sol for sol in solutions if sol[0] <= d_max]

        if len(filtered_solutions) == 0:
            return (), ()

        def sorting_key(element):
            return (abs(element[0] - self.d_min), len(element[1]), element[0])

        sol_min_h_n = min(filtered_solutions, key=sorting_key)
        sol_min_d = min(filtered_solutions, key=sorting_key)

        if fractions:
            sol_min_h_n = (sol_min_h_n[0], convert2fractions(sol_min_h_n[1]))
            sol_min_d = (sol_min_d[0], convert2fractions(sol_min_d[1]))

        return sol_min_h_n, sol_min_d

    def run(self):
        while self.n_max <= 13:
            solution_space = self.gen_solution_space_sag(self.r, self.n_max) if self.sag_compliant else self.gen_solution_space()
            solutions = self.compute_densities_over_solution_space(solution_space, self.p, self.d_min)

            optimal_sols = self.find_optimal_solutions(solutions, self.d_min * self.tolerance_factor)

            if optimal_sols[0] or optimal_sols[1]:
                return optimal_sols

            # If no solution is found, increment n_max and try again
            self.n_max += 1

        return (), ()  # Return empty tuples if no solution is found after trying up to n_max=9


def convert2fractions(x):
    return [str(Fraction(i).limit_denominator()) for i in x]


def parse_solutions(solutions: tuple) -> dict:
    sol_min_h_n, sol_min_d = solutions

    result = {}

    if sol_min_d:
        result["min_densidad"] = {
            "densidad": sol_min_d[0],
            "patrones": convert2fractions(sol_min_d[1])
        }

    return result


fu = Pattern(p=255, d_min=500, tolerance_factor=1.05)
solutions = parse_solutions(fu.run())
print(solutions)
