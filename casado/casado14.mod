# Problem 14 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: log(3 * x) * log(2 * x) - 0.1;
