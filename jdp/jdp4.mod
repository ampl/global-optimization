# jdp4.mod;

# variable bounds
var x in [-5,5];
var y in [-5,5];

# Objective function
minimize objective: sin(x^2 - y^2);

# Constraints
s.t. c1: y^2 + cos(x-y) >= 0.5;
s.t. c2: x*(y + sin(y)) == 2;

# Set the solver option
option solver lgo;
# objective = -1
#  _varname     _var       :=
# 1   x        -0.804509
# 2   y        -1.48931
#  _conname _con    _con.slack     :=
# 1   c1       0     2.49258
# 2   c2       0    -1.35691e-12

# option solver knitro;
# KNITRO 4.0.2: Current solution estimate cannot be improved.
# objective = 0

# option solver loqo;
# LOQO 6.01: iteration limit (500 iterations, 5712 evaluations)
# objective = 0

# option solver minos;
# MINOS 5.51: optimal solution found.
# objective = -0.174639

# option solver snopt;
# SNOPT 7.2-8 : Nonlinear infeasibilities minimized.
# objective = 0

# Solve the model as stated above
solve;

# Display results in command window
display objective;
display _varname, _var; 
display _conname, _con, _con.slack;