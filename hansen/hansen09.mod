# Problem 9 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [3.1, 20.4];
maximize f: -sin(x) - sin(2/3 * x);
