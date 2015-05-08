model branin.mod;

# This constraint, added by Janos D. Pinter, guarantees the unique solution
# x*=(pi,2.275)
s.t. UniqueSoln: x[1]+x[2] <= 6;
