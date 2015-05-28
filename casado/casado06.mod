# Problem 6 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: cos(x) - sin(5 * x) + 1;
