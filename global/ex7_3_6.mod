#  NLP written by GAMS Convert at 06/20/02 11:57:00
#  
#  Equation counts
#     Total       E       G       L       N       X
#        18      11       0       7       0       0
#  
#  Variable counts
#                 x       b       i     s1s     s2s      sc      si
#     Total    cont  binary integer    sos1    sos2   scont    sint
#        18      18       0       0       0       0       0       0
#  FX     0       0       0       0       0       0       0       0
#  
#  Nonzero counts
#     Total   const      NL     DLL
#        80      26      54       0
# 
#  Reformualtion has removed 1 variable and 1 equation


var x1 <= 3.4329;
var x2 <= 0.1627;
var x3 <= 0.1139;
var x4 := 0.2539, >= 0.2539;
var x5 <= 0.0208;
var x6 := 2.0247, >= 2.0247;
var x7 := 1, >= 1;
var x8 >= 0, <= 10;
var x9 >= 0, <= 1;
var x10;
var x11;
var x12;
var x13;
var x14;
var x15;
var x16;
var x17;

minimize obj:    x9;

subject to

e2: x14*x8^4 - x16*x8^6 - x12*x8^2 + x10 = 0;

e3: x17*x8^6 - x15*x8^4 + x13*x8^2 - x11 = 0;

e4:  - x1 - 1.2721*x9 <= -3.4329;

e5:  - x2 - 0.06*x9 <= -0.1627;

e6:  - x3 - 0.0782*x9 <= -0.1139;

e7:    x4 - 0.3068*x9 <= 0.2539;

e8:  - x5 - 0.0108*x9 <= -0.0208;

e9:    x6 - 2.4715*x9 <= 2.0247;

e10:    x7 + 9*x9 <= 1;

e11:  - (6.82079e-5*x1*x3*x4^2 + 6.82079e-5*x1*x2*x4*x5) + x10 = 0;

e12:  - (0.00076176*x2^2*x5^2 + 0.00076176*x3^2*x4^2 + 0.000402141*x1*x2*x5^2
      + 0.00337606*x1*x3*x4^2 + 6.82079e-5*x1*x4*x5 + 0.00051612*x2^2*x5*x6 + 
     0.00337606*x1*x2*x4*x5 + 6.82079e-5*x1*x2*x4*x7 + 6.28987e-5*x1*x2*x5*x6
      + 0.000402141*x1*x3*x4*x5 + 6.28987e-5*x1*x3*x4*x6 + 0.00152352*x2*x3*x4*
     x5 + 0.00051612*x2*x3*x4*x6) + x11 = 0;

e13:  - (0.000402141*x1*x5^2 + 0.00152352*x2*x5^2 + 0.0552*x2^2*x5^2 + 0.0552*
     x3^2*x4^2 + 0.0189477*x1*x2*x5^2 + 0.034862*x1*x3*x4^2 + 0.00336706*x1*x4*
     x5 + 6.82079e-5*x1*x4*x7 + 6.28987e-5*x1*x5*x6 + 0.00152352*x3*x4*x5 + 
     0.00051612*x3*x4*x6 - 0.00234048*x3^2*x4*x6 + 0.034862*x1*x2*x4*x5 + 
     0.0237398*x2^2*x5*x6 + 0.00152352*x2^2*x5*x7 + 0.00051612*x2^2*x6*x7 + 
     0.00336706*x1*x2*x4*x7 + 0.00287416*x1*x2*x5*x6 + 0.000804282*x1*x2*x5*x7
      + 6.28987e-5*x1*x2*x6*x7 + 0.0189477*x1*x3*x4*x5 + 0.00287416*x1*x3*x4*x6
      + 0.000402141*x1*x3*x4*x7 + 0.1104*x2*x3*x4*x5 + 0.0237398*x2*x3*x4*x6 + 
     0.00152352*x2*x3*x4*x7 - 0.00234048*x2*x3*x5*x6 + 0.00103224*x2*x5*x6)
      + x12 = 0;

e14:  - (0.189477*x1*x5^2 + 0.1104*x2*x5^2 + 0.00051612*x5*x6 + x2^2*x5^2 + 
     0.00076176*x2^2*x7^2 + x3^2*x4^2 + 0.1586*x1*x2*x5^2 + 0.000402141*x1*x2*
     x7^2 + 0.0872*x1*x3*x4^2 + 0.034862*x1*x4*x5 + 0.00336706*x1*x4*x7 + 
     0.00287416*x1*x5*x6 + 6.28987e-5*x1*x6*x7 + 0.00103224*x2*x6*x7 + 0.1104*
     x3*x4*x5 + 0.0237398*x3*x4*x6 + 0.00152352*x3*x4*x7 - 0.00234048*x3*x5*x6
      + 0.1826*x2^2*x5*x6 + 0.1104*x2^2*x5*x7 + 0.0237398*x2^2*x6*x7 - 0.0848*
     x3^2*x4*x6 + 0.0872*x1*x2*x4*x5 + 0.034862*x1*x2*x4*x7 + 0.0215658*x1*x2*
     x5*x6 + 0.0378954*x1*x2*x5*x7 + 0.00287416*x1*x2*x6*x7 + 0.1586*x1*x3*x4*
     x5 + 0.0215658*x1*x3*x4*x6 + 0.0189477*x1*x3*x4*x7 + 2*x2*x3*x4*x5 + 
     0.1826*x2*x3*x4*x6 + 0.1104*x2*x3*x4*x7 - 0.0848*x2*x3*x5*x6 - 0.00234048*
     x2*x3*x6*x7 + 0.00076176*x5^2 + 0.0474795*x2*x5*x6 + 0.000804282*x1*x5*x7
      + 0.00304704*x2*x5*x7) + x13 = 0;

e15:  - (0.1586*x1*x5^2 + 0.000402141*x1*x7^2 + 2*x2*x5^2 + 0.00152352*x2*x7^2
      + 0.0237398*x5*x6 + 0.00152352*x5*x7 + 0.00051612*x6*x7 + 0.0552*x2^2*x7^
     2 + 0.0189477*x1*x2*x7^2 + 0.0872*x1*x4*x5 + 0.034862*x1*x4*x7 + 0.0215658
     *x1*x5*x6 + 0.00287416*x1*x6*x7 + 0.0474795*x2*x6*x7 + 2*x3*x4*x5 + 0.1826
     *x3*x4*x6 + 0.1104*x3*x4*x7 - 0.0848*x3*x5*x6 - 0.00234048*x3*x6*x7 + 2*x2
     ^2*x5*x7 + 0.1826*x2^2*x6*x7 + 0.0872*x1*x2*x4*x7 + 0.3172*x1*x2*x5*x7 + 
     0.0215658*x1*x2*x6*x7 + 0.1586*x1*x3*x4*x7 + 2*x2*x3*x4*x7 - 0.0848*x2*x3*
     x6*x7 + 0.0552*x5^2 + 0.3652*x2*x5*x6 + 0.0378954*x1*x5*x7 + 0.2208*x2*x5*
     x7) + x14 = 0;

e16:  - (0.0189477*x1*x7^2 + 0.1104*x2*x7^2 + 0.1826*x5*x6 + 0.1104*x5*x7 + 
     0.0237398*x6*x7 + x2^2*x7^2 + 0.1586*x1*x2*x7^2 + 0.0872*x1*x4*x7 + 
     0.0215658*x1*x6*x7 + 0.3652*x2*x6*x7 + 2*x3*x4*x7 - 0.0848*x3*x6*x7 + x5^2
      + 0.00076176*x7^2 + 0.3172*x1*x5*x7 + 4*x2*x5*x7) + x15 = 0;

e17:  - (0.1586*x1*x7^2 + 2*x2*x7^2 + 2*x5*x7 + 0.1826*x6*x7 + 0.0552*x7^2)
      + x16 = 0;

e18:  - x7^2 + x17 = 0;
