# Problem 3 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [-10, 10];
maximize f: sum{k in 1..5} k * sin((k + 1) * x + k);
