# Problem 34 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

# Same as hansen15 formulated as minimization except for x interval which is
# [-5, 5] in hansen15 and a constant term in objective here.
var x in [0.2, 7];
minimize f: (x^2 - 5 * x + 6) / (x^2 + 1) - 0.5;
