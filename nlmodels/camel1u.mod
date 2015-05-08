model camel1.mod;

# This constraint, added by Janos D. Pinter, guarantees the unique solution
# x*=(0.089842,-0.712656)
s.t. UniqueSoln: x[1] >= x[2];
