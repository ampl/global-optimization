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
var x; # 1-variable model

# Objective function
minimize ObjFct: log(x)*sin(x);
# Bound constraint[s]
s.t. Box1: 1 <= x <= 20;
