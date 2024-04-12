from chalicelib.devices import Pattern
import matplotlib.pyplot as plt
import numpy as np




P = range(400, 601, 1)
solutions = [s.run() for s in [Pattern(p, 500, 12, 1.1) for p in P]]
X_min_n = np.array([np.array([s[0][0], len(s[0][1])]) if s is not None else (0, 0) for s in solutions ]).transpose()
gen_eval_plot(P, X_min_n[0], X_min_n[1], 500, 'min. hileras')


X_min_n = np.array([np.array([s[0][0], len(s[0][1])]) for s in solutions]).transpose()
X_min_d = np.array([(s[1][0], len(s[1][1])) for s in solutions]).transpose()

def gen_solutions_linrange(d_min, n_h, tolerance_factor, p_ub=1000):
    P = range(d_min, p_ub, 1)
    solutions = [s.run() for s in [Pattern(p, d_min, n_h, tolerance_factor) for p in P]]
    X_min_n = np.array([np.array([s[0][0], len(s[0][1])]) for s in solutions if s is not None]).transpose()
    X_min_d = np.array([(s[1][0], len(s[1][1])) for s in solutions if s is not None]).transpose()
    return X_min_n, X_min_d, P


def gen_eval_plot(P, D, N, d_min, note=''):

    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('plantas (p)')
    ax1.set_ylabel('densidad real (d)', color=color)
    ax1.plot(P, D, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:green'
    ax2.set_ylabel('número de hileras (n)', color=color)  # we already handled the x-label with ax1
    ax2.scatter(P, N, color=color, s=1)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.yticks(np.arange(1, 11, 1))

    # horizontal line indicating D
    ax1.axhline(y=d_min, color='tab:gray', linestyle='-', alpha=0.5)
    ax1.axhline(y=d_min*1.1, color='tab:gray', linestyle='-', alpha=0.5)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title(f'densidad {d_min} ({note})'.format(d_min))
    return plt



X_min_n, X_min_d, P = gen_solutions_linrange(d_min=500, n_h=4, tolerance_factor=1.1, p_ub=600)
fig1 = gen_eval_plot(P, X_min_d[0], X_min_d[1], 200, 'min. densidad')
fig2 = gen_eval_plot(P, X_min_n[0], X_min_n[1], 500, 'min. hileras')



# Plot a 2x2 grid of plots

fig, axs = plt.subplots(2, 2)
fig.suptitle('densidad 200')






###########

def gen_eval_plot(ax, P, D, N, d_min, title=''):

    color = 'tab:blue'
    ax.set_xlabel('plantas (p)')
    ax.set_ylabel('densidad real (d)', color=color)
    ax.plot(P, D, color=color)
    ax.tick_params(axis='y', labelcolor=color)

    ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:green'
    ax2.set_ylabel('número de hileras (n)', color=color)  # we already handled the x-label with ax1
    ax2.scatter(P, N, color=color, s=1)
    ax2.tick_params(axis='y', labelcolor=color)
    plt.yticks(np.arange(1, 7, 1))

    # horizontal line indicating D
    ax.axhline(y=d_min, color='tab:gray', linestyle='-', alpha=0.5)
    ax.axhline(y=d_min*1.1, color='tab:gray', linestyle='-', alpha=0.5)

    plt.title(title)
    return ax


for d_min in [200, 300, 500]:
    X_min_n, X_min_d, P = gen_solutions_linrange(d_min, 4, 1.1, d_min*4)
    fig, axs = plt.subplots(1, 2, sharey=True)
    fig.suptitle(f'densidad={d_min}')


    axs[0] = gen_eval_plot(axs[0], P, X_min_d[0], X_min_d[1], d_min, 'min. densidad')
    axs[1] = gen_eval_plot(axs[1], P, X_min_n[0], X_min_n[1], d_min, 'min. hileras')
    plt.subplots_adjust(wspace=.5)

    plt.savefig(f'assets/algo_eval_dmin_{d_min}.png')


