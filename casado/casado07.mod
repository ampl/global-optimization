# Problem 7 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: -x - sin(3 * x) + 1.6;
