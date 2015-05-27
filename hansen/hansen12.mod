# Problem 12 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [0, 6.28];
maximize f: -sin(x)^3 - cos(x)^3;
