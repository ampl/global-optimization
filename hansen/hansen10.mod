# Problem 10 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [0, 10];
maximize f: x * sin(x);
