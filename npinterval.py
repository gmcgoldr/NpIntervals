from __future__ import division
import warnings

import numpy as np


def interval(x, f):
    """
    Find the shorest interval between two samples in `x`, which contains `f`
    fraction of samples.

    :param x: [float]
        samples for which to compute the interval
    :param f: float
        fraction of samples to include in the interval

    :return: x1, x2, i1, i2
        x1: lower interval value of x
        x2: upper interval value of x
        i1: sorted index of lower interval value
        i2: sorted index of lupper interval value
    """
    if f <= 0 or f > 1:
        raise ValueError("f must be bound by [0, 1)")

    x = np.asarray(x)
    isort = np.argsort(x)
    xsort = x[isort]

    # Number of samples inside the interval. Don't alow less than 1
    nin = max(1, int(f*len(x))) 
    # Warn if the interval contains only one sample, as this is meaningless
    if nin == 1:
        warnings.warn(
            "Insufficient samples for proper interval",
            RuntimeWarning)
    # Number of samples outside the interval
    nout = len(x) - nin

    if nout <= 0:
        # Interval includes all points
        i1 = 0
        i2 = len(x)
    else:
        # Possible left interval edges are 0..nout+1 (i.e. interval contains
        # all left points ... excludes up to nout points on the left). Likewise
        # for the right interval edges
        intervals = xsort[-(nout+1):] - xsort[:nout+1]
        # Get the index of the shortest interval
        i1 = np.argmin(intervals)
        i2 = i1 + nin

    # Values inside the interval, at the edges
    x1 = xsort[i1]
    x2 = xsort[i2-1]

    return x1, x2, i1, i2


def half_sample_mode(x):
    """
    Compute the half sample mode of the data samples `x`.

    Algorithm iteratively finds the region of highest density, halving the 
    samples to search each time. The algorithm is linear time in x, though
    it first sorts.

    :param x: [float]
        samples for which to compute the half sample mode
    :return: float
        estimated mode
    """
    x = np.asarray(x)
    isort = np.argsort(x)
    xsort = x[isort]

    # The points being considered in current interval
    xpart = xsort

    # Shorten the interval iteratively until at most two points are left
    while len(xpart) > 2:
        # Don't allow interval to contain less than 2 samples; i.e. if second
        # last interval is of 3 samples, next interval will contain 2.
        nin = max(2, int(0.5*len(xpart)))
        nout = len(xpart) - nin
        intervals = xpart[-(nout+1):] - xpart[:nout+1]
        i1 = np.argmin(intervals)
        i2 = i1 + nin
        xpart = xpart[i1:i2]

    mode = np.mean(xpart)

    return mode
