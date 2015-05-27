# Problem 19 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [0, 6.5];
maximize f: x - sin(3 * x) + 1;
