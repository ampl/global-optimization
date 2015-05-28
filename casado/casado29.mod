# Problem 29 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: 2 * (x - 3)^2 - exp(x / 2) + 5;
