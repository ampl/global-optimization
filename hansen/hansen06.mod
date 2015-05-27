# Problem 6 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [-10, 10];
maximize f: (x + sin(x)) * exp(-x^2);
