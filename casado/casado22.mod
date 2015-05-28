# Problem 22 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: cos(x) + 2 * cos(2 * x) * exp(-x);
