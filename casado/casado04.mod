# Problem 4 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: (3 * x - 1.4) * sin(18 * x) + 1.7;
