# Problem 9 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

# Same as hansen14 formulated as minimization except for x interval which is
# [0, 4] in hansen14 and a constant term in objective here.
param pi = 4 * atan(1);
var x in [0.2, 7];
minimize f: -exp(-x) * sin(2 * pi * x) + 1;
