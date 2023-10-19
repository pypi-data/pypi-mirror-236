# utility classes and functions
import numpy as np
from scipy.optimize import bisect


def projCappedSimplex(w, w_sum):
    a = np.min(w) - 1.0
    b = np.max(w) - 0.0

    def f(x):
        return np.sum(np.maximum(np.minimum(w - x, 1.0), 0.0)) - w_sum

    x = bisect(f, a, b)

    return np.maximum(np.minimum(w - x, 1.0), 0.0)
