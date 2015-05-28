"""
Acquisition functions based on the probability or expected value of
improvement.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

__all__ = ['EI', 'PI', 'UCB', 'Thompson']

import numpy as np


def EI(model, _, xi=0.0):
    """
    Expected improvement policy with an exploration parameter of `xi`.
    """
    X = model.data[0]
    x = X[model.predict(X)[0].argmax()]

    def index(X, grad=False):
        """EI policy instance."""
        return model.get_improvement(X, x, xi, grad)

    return index


def PI(model, _, xi=0.05):
    """
    Probability of improvement policy with an exploration parameter of `xi`.
    """
    X = model.data[0]
    x = X[model.predict(X)[0].argmax()]

    def index(X, grad=False):
        """PI policy instance."""
        return model.get_improvement(X, x, xi, grad, pi=True)

    return index


def Thompson(model, _, n=100, rng=None):
    """
    Thompson sampling policy.
    """
    return model.sample_f(n, rng).get


def UCB(model, _, delta=0.1, xi=0.2):
    """
    The (GP)UCB acquisition function where `delta` is the probability that the
    upper bound holds and `xi` is a multiplicative modification of the
    exploration factor.
    """
    d = model.ndata
    a = xi * 2 * np.log(np.pi**2 / 3 / delta)
    b = xi * (4 + d)

    def index(X, grad=False):
        """UCB policy instance."""
        posterior = model.predict(X, grad=grad)
        mu, s2 = posterior[:2]
        beta = a + b * np.log(model.ndata + 1)
        if grad:
            dmu, ds2 = posterior[2:]
            return (mu + np.sqrt(beta * s2),
                    dmu + 0.5 * np.sqrt(beta / s2[:, None]) * ds2)
        else:
            return mu + np.sqrt(beta * s2)

    return index
