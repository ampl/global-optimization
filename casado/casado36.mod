# Problem 36 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: (x + 1)^3 / x^2 - 7.1;
