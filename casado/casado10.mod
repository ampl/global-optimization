# Problem 10 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

param pi = 4 * atan(1);
var x in [0.2, 7];
minimize f: exp(-x) * sin(2 * pi * x);
