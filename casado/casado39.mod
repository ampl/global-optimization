# Problem 39 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [-10, 20];
minimize f: x^4 - 10 * x^3 + 35 * x^2 - 50 * x + 24;
