# Problem 13 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

# Same as hansen07 formulated as minimization except for a missing constant
# term in objective.
var x in [2.7, 7.5];
minimize f: sin(x) + sin(10/3 * x) + log(x) - 0.84 * x;
