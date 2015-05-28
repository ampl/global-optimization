# Problem 13 from "Univariate Lipschitz optimization II" by Hansen et al.
# AMPL coding by Victor Zverovich.

var x in [0.001, 0.99];

# The original objective has `- (x^2 - 1)^(1/3)` as a second term, but since
# b^e (pow) requires e to be integer if b is negative, the sign was moved
# outside of the base expression to make sure that it is positive.
maximize f: x^(2/3) + (1 - x^2)^(1/3);
