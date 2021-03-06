# Problem 7 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [2.7, 7.5];
maximize f: -sin(x) - sin(10/3 * x) - log(x) + 0.84 * x - 3;
