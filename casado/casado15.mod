# Problem 15 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

# Objective function is the same as in hansen08 except for a constant term,
# but this is a minimization problem.
# The difference in indexing doesn't matter because k = 0 gives 0 term.
var x in [0.2, 7];
minimize f: sum{k in 0..5} k * cos((k + 1) * x + k) + 12;
