# Problem 14 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

param pi = 4 * atan(1);
var x in [0, 4];
maximize f: exp(-x) * sin(2 * pi * x);
