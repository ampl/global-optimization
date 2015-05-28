# Problem 37 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [-1, 7];
minimize f: x^4 - 12 * x^3 + 47 * x^2 - 60 * x - 20 * exp(-x);
