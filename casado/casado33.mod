# Problem 33 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [-10, 10];
# Same as hansen03 with objective sense reversed.
minimize f: -sum{k in 1..5} k * sin((k + 1) * x + k);
