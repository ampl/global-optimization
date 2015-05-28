# Problem 40 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0, 3];
minimize f: 24 * x^4 - 142 * x^3 + 303 * x^2 - 276 * x + 3;
