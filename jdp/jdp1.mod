# jdp1.mod
# An illustrative global optimization model from the GOMODEL Library 
# AMPL code development by Janos D. Pinter
# 2015-01-08

# Key model characteristics 
# Number of variables: 1
# Number of (lower and upper) bound constraints: 2
# Number of general constraints: 0 
# Objective function: nonconvex 

# Global solution: 
# Optimum value:          f* = -2.85006480
# Optimal argument value: x* = 17.29903524

# Variables
var x{1..1}; # 1-variable model

# Objective function
minimize ObjFct: log(x[1])*sin(x[1]);
# Bound constraint[s]
s.t. Box1: 1 <= x[1] <= 20;
# General constraints
# Absent

# An illustrative list of solver options that can be tested 
# option solver couenne; # finds objfct = -2.85006
# option solver ipopt; # finds objfct = 0
option solver knitro; # finds objfct = 0
# option solver lgo;
# option solver loqo; # reports LOQO ERROR(50): cannot evaluate obj and/or constraint at initial solution 
# option solver minos; # finds objfct = 0
# option solver snopt; # finds objfct = 0

# Solve model as stated above
solve;

# Display results in AMPL command window
display ObjFct;
display _varname, _var;
display _conname, _con, _con.slack;

# Send results to output file
display ObjFct >> jdp1.out;
display _varname, _var >> jdp1.out;
display _conname, _con, _con.slack >> jdp1.out;
