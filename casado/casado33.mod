# Problem 33 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

# Same as hansen03 formulated as minimization.
var x in [-10, 10];
minimize f: -sum{k in 1..5} k * sin((k + 1) * x + k);
