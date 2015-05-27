# Problem 17 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [-4, 4];
maximize f: -x^6 + 15 * x^4 - 27 * x^2 - 250;
