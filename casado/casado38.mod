# Problem 38 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

# Same hansen17 formulated as minimization.
var x in [-4, 4];
minimize f: x^6 - 15 * x^4 + 27 * x^2 + 250;
