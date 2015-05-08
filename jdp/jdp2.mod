# pinter_1.mod
# Author: Janos D. Pinter

# A one-dimensional, non-trivial box-constrained model with a composite
# trigonometric objective function
# The numerical global solution is
# objective = -3.7625014914
# x = 2.6669565697
# There exist many other (locally optimal) solutions

# variable bounds
var x in [-2,5];

# objective function
minimize objective: sin(11*x)+cos(13*x)-sin(17*x)-cos(19*x);
