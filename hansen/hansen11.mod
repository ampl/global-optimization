# Problem 11 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [-1.57, 6.28];
maximize f: -2 * cos(x) - cos(2 * x);
