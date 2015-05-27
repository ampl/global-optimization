# Problem 5 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [0, 1.2];
maximize f: (-3 * x + 1.4) * sin(18 * x);
