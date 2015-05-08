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

# No general constraints

# Set the solver option
option solver lgo;
# objective = -3.762501491
# x = 2.66696

# Try also the solver options shown below 

# option solver knitro;
# objective = -0.0826814
# x = 0.0264637

# option solver loqo;
# objective = -0.0826814
# x = 0.0264637

# option solver minos;
# objective = -2.479027828
# x = 4.96432

# option solver snopt;
# objective = -1.451159601
# x = 0.363561

# Solve the model as stated above
solve;

# Display results in command window
display objective;
display _varname, _var; 
