# Problem 3 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [-10, 10];
minimize f: (x - x^2)^2 + (x - 1)^2;
