import numpy as np
from numba import vectorize


@vectorize
def gamma(z):
    """
    Lanczos approximation according to https://en.wikipedia.org/wiki/Lanczos_approximation
    """
    g = 7
    p = [
        0.99999999999980993,
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.61502916214059,
        12.507343278686905,
        -0.13857109526572012,
        9.9843695780195716e-6,
        1.5056327351493116e-7
    ]
    if z.real < 0.5:
        gamma_arg = 1 - z
    else:
        gamma_arg = z

    gamma_arg -= 1
    x = p[0]
    for i in range(1, len(p)):
        x += p[i] / (gamma_arg + i)
    t = gamma_arg + g + 0.5
    y = np.sqrt(2 * np.pi) * t ** (gamma_arg + 0.5) * np.exp(-t) * x

    if z.real < 0.5:
        y = np.pi / (np.sin(np.pi * z) * y)
    return y
