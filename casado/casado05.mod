# Problem 5 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

var x in [-10, 10];
minimize f: 2 * x^2 - 3/100 * exp(-(200 * (x - 0.0675))^2);
