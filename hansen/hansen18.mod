# Problem 18 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [0, 6];
maximize f: if x <= 3 then -(x - 2)^2 else -2 * log(x - 2) - 1;
