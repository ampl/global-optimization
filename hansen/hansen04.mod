# Problem 4 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [1.9, 3.9];
maximize f: (16 * x^2 - 24 * x + 5) * exp(-x);
