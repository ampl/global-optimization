# Problem 34 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: (x^2 - 5 * x + 6) / (x^2 + 1) - 0.5;
