# Problem 19 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [-5, 5];
minimize f: x^2 - cos(18 * x);
