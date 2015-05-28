# Problem 1 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0, 20];
minimize f: exp(-3 * x) - sin(x)^3;
