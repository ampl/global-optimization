# Problem 32 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.02, 1];
minimize f: sin(1 / x);
