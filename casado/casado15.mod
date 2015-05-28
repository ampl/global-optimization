# Problem 15 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: sum{k in 0..5} k * cos((k + 1) * x + k) + 12;
