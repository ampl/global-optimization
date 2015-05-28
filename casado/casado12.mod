# Problem 12 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: x * sin(x) + sin(10/3 * x) + log(x) - 0.84 * x + 1.3;
