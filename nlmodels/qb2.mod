# qb2.mod
# A toy model received from David Gay
# Solution: x*=1, objf*=0.16
 
var x binary;
minimize objf: (x - .6)^2;
s.t. box: 0 <= x <= 1;
s.t. bin: x*(1-x) <= 0;
