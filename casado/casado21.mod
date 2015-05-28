# Problem 21 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [-20, 20];
minimize f: x^2 / 20 - cos(x) + 2;
