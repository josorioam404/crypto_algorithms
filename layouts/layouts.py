import numpy as np
import plotly.graph_objects as go
from math import factorial


def combinations(n, r):
    if r > n:
        return 0
    return factorial(n) / (factorial(r) * factorial(n - r))


print(combinations(100 - 1, 26 - 1))
n_values = np.arange(1, 25)
r_values = np.arange(0, 25)

Z = [[combinations(n, r) if r <= n else 0 for n in n_values] for r in r_values]

fig = go.Figure(data=[go.Surface(z=Z, x=n_values, y=r_values)])

fig.update_layout(
    title="Combinations Surface",
    scene=dict(xaxis_title="n", yaxis_title="r", zaxis_title="C(n,r)"),
)

fig.show()

