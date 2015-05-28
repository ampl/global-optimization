# Problem 31 from "Support functions using gradient information" by Casado et al.
# AMPL coding by Victor Zverovich.

set I;
param a{I};
param k{I};
param c{I};
var x in [0, 10];
minimize f: -sum{i in I} 1 / ((k[i] * (x - a[i]))^2 + c[i]);

data;

param:
 I:    a     k     c :=
 1 3.040 2.983 0.192
 2 1.098 2.378 0.140
 3 0.674 2.439 0.127
 4 3.537 1.168 0.132
 5 6.173 2.406 0.125
 6 8.679 1.236 0.189
 7 4.503 2.868 0.187
 8 3.328 1.378 0.171
 9 6.937 2.348 0.188
10 0.700 2.268 0.176;
