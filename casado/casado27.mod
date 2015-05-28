# Problem 27 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: sin(x) * cos(x) - 1.5 * sin(x)^2 + 1.2;
