# Problem 35 from "Support functions using gradient information" by Casado et al.
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
 1 4.696 2.871 0.149
 2 4.885 2.328 0.166
 3 0.800 1.111 0.175
 4 4.986 1.263 0.183
 5 3.901 2.399 0.128
 6 2.395 2.629 0.117
 7 0.945 2.853 0.115
 8 8.371 2.344 0.148
 9 6.181 2.592 0.188
10 5.713 2.929 0.198;
