# jdp3.mod
# Author: Janos D. Pinter

# A 3-variable constrained nonlinear programming model
# with a non-smooth objective function

# The numerical global solution is
# objective = -3.7625014914
# x = 2.6669565697
# There exist more than 20 other (locally optimal) solutions

# Variables and bounds
var x in [1,8];
var y in [2,5];
var z in [3,10];

# Objective function
minimize objective: abs(x^2 + y^2 - z^2);

# Constraints
s.t. eq1: x^2 + y^2 + z^2 + x - y - z - 44 == 0;
s.t. eq2: x*y*z + x*y - 3*x - y - 2*z - 49 == 0;
s.t. eq3: x*z + 2*x*y + x + z - 47 <= 0;

# Set the solver option
option solver lgo;
# objective = 0
# x = 3
# y = 4
# z = 5

# Try also the solver options shown below 

# option solver knitro;
# objective = 3.36962e-08

# option solver loqo;
# objective = 30.7738

# option solver minos;
# objective = 6.33862

# option solver snopt;
# objective = 7.24754e-13

# Solve the model as stated above
solve;

# Display results in command window
display objective;
display _varname, _var; 
display _conname, _con, _con.slack;
