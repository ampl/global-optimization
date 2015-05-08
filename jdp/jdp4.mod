# jdp4.mod;

# variable bounds
var x in [-5,5];
var y in [-5,5];

# Objective function
minimize objective: sin(x^2 - y^2);

# Constraints
s.t. c1: y^2 + cos(x-y) >= 0.5;
s.t. c2: x*(y + sin(y)) == 2;
