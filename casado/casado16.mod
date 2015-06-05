# Problem 16 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

# Same as hansen03 formulated as minimization except for x interval which is
# [-10, 10] in hansen14 and a constant term in objective here.
var x in [0.2, 7];
minimize f: -sum{k in 1..5} k * sin((k + 1) * x + k) + 3;
