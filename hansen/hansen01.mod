# Problem 1 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [-1.5, 11];
maximize f:
  -1/6 * x^6 + 52/25 * x^5 - 39/80 * x^4 - 71/10 * x^3 + 79/20 * x^2 + x - 1/10;
