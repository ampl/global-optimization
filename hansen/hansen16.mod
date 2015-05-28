# Problem 16 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [-3, 3];

# There appears to be a minus sign before x^2 in the paper, but the optimal
# value and the solution suggest that there shouldn't be one.
maximize f: -2 * (x - 3)^2 - exp(x^2 / 2);
