# Problem 18 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [0.2, 7];
minimize f: sqrt(x) * sin(x)^2;
