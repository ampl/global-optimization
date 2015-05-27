# Problem 15 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [-5, 5];
maximize f: (-x^2 + 5 * x - 6) / (x^2 + 1);
