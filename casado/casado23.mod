# Problem 23 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [-10, 10];
minimize f: (x + sin(x)) * exp(-x^2);
