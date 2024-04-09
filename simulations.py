from chalicelib.devices import Pattern
import numpy as np
import pandas as pd

# Parameters
P = range(200, 4001, 1)  # range of plants
d = 500
n_max = 12

# Run simulations
solutions = [s.run(fractions=True) for s in [Pattern(p, d, n_max) for p in P]]
df_sols = np.array([np.array([s[0][0], len(s[0][1]), len(set(s[0][1])), str(s[0][1])]) if s is not None else (0, 0, 0, 0) for s in solutions ])
df = pd.concat([pd.DataFrame(P, columns=['p']), pd.DataFrame(df_sols, columns=['d', 'n', 'n_unique', 'pattern'])], axis=1)

# Write to file
df.to_csv('data/simulations_d500.csv', index=False)
