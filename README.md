# NpInterval #

Numpy computation of PDF intervals.

See `tests.py` for a more complete explanation of the algorithms.

### Interval ###

`npinterval.interval`: given a sequence of samples drawn from any distribution (mutli-modal, skewed...), this method finds the shortest interval between two sample values, which contains a given fraction of the samples.

### Half Sample Mode ###

`npinterval.half_sample_mode`: simple implementation of the so-called half sample mode described in:

Cryer, J. D., Robertson, T., Wright, F. T., & Casady, R. J. (1972). Monotone median regression. _The Annals of Mathematical Statistics_, 1459-1469.

The algorithm is robust against outliers, so long as less than half the samples are outliers. It is fairly insensitive to statistical fluctuations. It's real strength is that it has no parameters to tune.
