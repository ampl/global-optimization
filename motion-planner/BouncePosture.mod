# BOUNCE POSTURE MODEL FILE 
# Movement to plan: 
# Reaching, Arm: right, Object: , Object Engaged: , Pose: , Grip Type: 

# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
# PARAMETERS 

param pi := 4*atan(1); 
# Body info 
param body {i in 1..2}; 
# D-H parameters of the arm 
param alpha {i in 1..7} ; 
param a {i in 1..7} ; 
param d {i in 1..7} ; 
# Distance hand - target  
param dFH; 
# JOINT LIMITS 
# Lower Bounds 
param llim {i in 1..9} ; 
let llim[1] := -2.6005;
let llim[2] := -1.6406;
let llim[3] := -1.5533;
let llim[4] := -1.9373;
let llim[5] := -2.8623;
let llim[6] := -2.0769;
let llim[7] := -1.5533;
let llim[8] := 0.0175;
let llim[9] := 0.0175;
# Upper Bounds 
param ulim {i in 1..9} ; 
let ulim[1] := 1.5533;
let ulim[2] := 0.7679;
let ulim[3] := 2.4260;
let ulim[4] := 1.0821;
let ulim[5] := 2.8623;
let ulim[6] := 2.0769;
let ulim[7] := 2.8623;
let ulim[8] := 2.4260;
let ulim[9] := 2.4260;
# Initial posture 
param thet_init {i in 1..9} ; 
param Hand_init {i in 1..3} ; 
param x_H_init {i in 1..3} ; 
param y_H_init {i in 1..3} ; 
param z_H_init {i in 1..3} ; 
param Elbow_init {i in 1..3} ; 
param x_E_init {i in 1..3} ; 
param y_E_init {i in 1..3} ; 
param z_E_init {i in 1..3} ; 
param Wrist_init {i in 1..3} ; 
param x_W_init {i in 1..3} ; 
param y_W_init {i in 1..3} ; 
param z_W_init {i in 1..3} ; 
param swivel_init; 
# Final posture 
param thet_final {i in 1..9} ; 
# Final finger posture 
param joint_fingers {i in 1..4} ; 
# Joint Expense Factors 
param lambda {i in 1..9} ; 
param rk {i in 1..3} ; 
param jk {i in 1..3} ; 
param Aw; 
param A1; 
param A2; 
param A3; 
param D3; 
param phi_2; 
param phi_3; 
# Target Position 
param Tar_pos {i in 1..3}; 
# Target orientation 
param x_t {i in 1..3}; 
param y_t {i in 1..3}; 
param z_t {i in 1..3}; 
# Obstacles 
param n_Obstacles; 
param Obstacles {i in 1..n_Obstacles, j in 1..9}; 
# Object of the target 
param n_ObjTar; 
param ObjTar {i in 1..n_ObjTar, j in 1..9}; 
param Rot_obj {i1 in 1..3, i2 in 1..3};
# Boundary Conditions 
param vel_0 {i in 1..9} ; 
param vel_f {i in 1..9} ; 
param acc_0 {i in 1..9} ; 
param acc_f {i in 1..9} ; 
# Time and iterations
param Nsteps;
param TB;
param PHI;
param TotalTime;
set Iterations := 1..(Nsteps+1);
set nJoints := 1..9;
set Iterations_nJoints := Iterations cross nJoints;
param time {i in Iterations} = (i-1)/Nsteps;
# CONSTRAINTS LAGRANGE MULTIPLIERS 
param n_constr; 
param dual_in {i in 1..n_constr}; 
# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
# DECISION VARIABLES 
# Bounce Posture 
var theta_b {i in 1..9} >= llim[i], <= ulim[i]; 
# BOUNDS LAGRANGE MULTIPLIERS 
# Lower Bounds Multipliers 
param zL_in {i in 1..9} ; 
let zL_in[1] := 0.00000079;
let zL_in[2] := 0.00000249;
let zL_in[3] := 0.00000031;
let zL_in[4] := 0.00000694;
let zL_in[5] := 0.00000040;
let zL_in[6] := 0.00000039;
let zL_in[7] := 0.00000050;
let zL_in[8] := 0.00000083;
let zL_in[9] := 0.00000083;
suffix ipopt_zL_in, IN; 
let {i in 1..9} theta_b[i].ipopt_zL_in := zL_in[i]; 
# Upper Bounds Multipliers 
param zU_in {i in 1..9} ; 
let zU_in[1] := -0.00000035;
let zU_in[2] := -0.00000050;
let zU_in[3] := -0.00000128;
let zU_in[4] := -0.00000035;
let zU_in[5] := -0.00000031;
let zU_in[6] := -0.00000063;
let zU_in[7] := -0.00000042;
let zU_in[8] := 0.00000000;
let zU_in[9] := 0.00000000;
suffix ipopt_zU_in, IN; 
let {i in 1..9} theta_b[i].ipopt_zU_in := zU_in[i]; 
# Direct Movement 
param the_direct {(i,j) in Iterations_nJoints} := thet_init[j]+ 
( thet_final[j] - thet_init[j] ) * (10*(time[i])^3 -15*(time[i])^4 +6*(time[i])^5) 
+ 
vel_0[j] * TotalTime * (time[i] - 6 *(time[i])^3 +8*(time[i])^4 -3*(time[i])^5) 
+ 
vel_f[j] * TotalTime * (- 4 *(time[i])^3 +7*(time[i])^4 -3*(time[i])^5) 
+ 
(acc_0[j]/2) * TotalTime^2 * (time[i]^2 - 3 *(time[i])^3 +3*(time[i])^4 -(time[i])^5) 
+ 
(acc_f[j]/2) * TotalTime^2 * ((time[i])^3 -2*(time[i])^4 +(time[i])^5); 
# Back and forth Movement 
var the_bf 	{(i,j) in Iterations_nJoints} =  
((time[i]*(1-time[i]))/(TB*(1-TB)))*(theta_b[j] - thet_init[j])*(sin(pi*(time[i])^PHI))^2; 
# Composite Movement 
var theta 	{(i,j) in Iterations_nJoints} = 
the_direct[i,j] + the_bf[i,j];
# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
# Rotation matrix of the obstacles 
param c_roll {i in 1..n_Obstacles} := cos(Obstacles[i,7]); 
param s_roll {i in 1..n_Obstacles} := sin(Obstacles[i,7]); 
param c_pitch {i in 1..n_Obstacles} := cos(Obstacles[i,8]); 
param s_pitch {i in 1..n_Obstacles} := sin(Obstacles[i,8]); 
param c_yaw {i in 1..n_Obstacles} := cos(Obstacles[i,9]); 
param s_yaw {i in 1..n_Obstacles} := sin(Obstacles[i,9]); 
param Rot {i1 in 1..3, i2 in 1..3,i in 1..n_Obstacles} :=  
# 1st row 
if 		   ( i1=1 && i2=1 ) then 	c_roll[i]*c_pitch[i] 
else	if ( i1=1 && i2=2 ) then   -s_roll[i]*c_yaw[i]+c_roll[i]*s_pitch[i]*s_yaw[i] 
else	if ( i1=1 && i2=3 ) then 	s_roll[i]*s_yaw[i]+c_roll[i]*s_pitch[i]*c_yaw[i] 
# 2nd row 
else	if ( i1=2 && i2=1 ) then 	s_roll[i]*c_pitch[i] 
else	if ( i1=2 && i2=2 ) then 	c_roll[i]*c_yaw[i]+s_roll[i]*s_pitch[i]*s_yaw[i] 
else	if ( i1=2 && i2=3 ) then   -c_roll[i]*s_yaw[i]+s_roll[i]*s_pitch[i]*c_yaw[i] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then   -s_pitch[i] 
else	if ( i1=3 && i2=2 ) then	c_pitch[i]*s_yaw[i] 
else	if ( i1=3 && i2=3 ) then	c_pitch[i]*c_yaw[i] 
   ; 
# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
#  Direct Kinematics model of the arm 

param c_alpha {i in 1..7} := cos(alpha[i]); 
param s_alpha {i in 1..7} := sin(alpha[i]); 

param T_WorldToArm {i1 in 1..4, i2 in 1..4} =  
# 1st row 
if ( i1=1 && i2=1 ) then -1.00  
else	if ( i1=1 && i2=2 ) then 0.00  
else	if ( i1=1 && i2=3 ) then -0.00  
else	if ( i1=1 && i2=4 ) then -0.00  
# 2nd row 
else	if ( i1=2 && i2=1 ) then -0.00  
else	if ( i1=2 && i2=2 ) then -1.00  
else	if ( i1=2 && i2=3 ) then 0.00  
else	if ( i1=2 && i2=4 ) then 49.98  
# 3rd row 
else	if ( i1=3 && i2=1 ) then -0.00  
else	if ( i1=3 && i2=2 ) then 0.00  
else	if ( i1=3 && i2=3 ) then 1.00  
else	if ( i1=3 && i2=4 ) then 1500.00  
# 4th row 
else	if ( i1=4 && i2=1 ) then 0.00  
else	if ( i1=4 && i2=2 ) then 0.00  
else	if ( i1=4 && i2=3 ) then 0.00  
else	if ( i1=4 && i2=4 ) then 1.00  
;  
var T_0_1 {i1 in 1..4, i2 in 1..4, i in Iterations} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[i,1]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[i,1])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[1]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[i,1])*c_alpha[1] 
else	if ( i1=2 && i2=2 ) then cos(theta[i,1])*c_alpha[1] 
else	if ( i1=2 && i2=3 ) then -s_alpha[1] 
else	if ( i1=2 && i2=4 ) then -s_alpha[1]*d[1] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[i,1])*s_alpha[1] 
else	if ( i1=3 && i2=2 ) then cos(theta[i,1])*s_alpha[1] 
else	if ( i1=3 && i2=3 ) then c_alpha[1] 
else	if ( i1=3 && i2=4 ) then c_alpha[1]*d[1] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_1_2 {i1 in 1..4, i2 in 1..4, i in Iterations} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[i,2]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[i,2])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[2]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[i,2])*c_alpha[2] 
else	if ( i1=2 && i2=2 ) then cos(theta[i,2])*c_alpha[2] 
else	if ( i1=2 && i2=3 ) then -s_alpha[2] 
else	if ( i1=2 && i2=4 ) then -s_alpha[2]*d[2] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[i,2])*s_alpha[2] 
else	if ( i1=3 && i2=2 ) then cos(theta[i,2])*s_alpha[2] 
else	if ( i1=3 && i2=3 ) then c_alpha[2] 
else	if ( i1=3 && i2=4 ) then c_alpha[2]*d[2] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_2_3 {i1 in 1..4, i2 in 1..4, i in Iterations} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[i,3]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[i,3])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[3]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[i,3])*c_alpha[3] 
else	if ( i1=2 && i2=2 ) then cos(theta[i,3])*c_alpha[3] 
else	if ( i1=2 && i2=3 ) then -s_alpha[3] 
else	if ( i1=2 && i2=4 ) then -s_alpha[3]*d[3] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[i,3])*s_alpha[3] 
else	if ( i1=3 && i2=2 ) then cos(theta[i,3])*s_alpha[3] 
else	if ( i1=3 && i2=3 ) then c_alpha[3] 
else	if ( i1=3 && i2=4 ) then c_alpha[3]*d[3] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_3_4 {i1 in 1..4, i2 in 1..4, i in Iterations} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[i,4]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[i,4])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[4]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[i,4])*c_alpha[4] 
else	if ( i1=2 && i2=2 ) then cos(theta[i,4])*c_alpha[4] 
else	if ( i1=2 && i2=3 ) then -s_alpha[4] 
else	if ( i1=2 && i2=4 ) then -s_alpha[4]*d[4] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[i,4])*s_alpha[4] 
else	if ( i1=3 && i2=2 ) then cos(theta[i,4])*s_alpha[4] 
else	if ( i1=3 && i2=3 ) then c_alpha[4] 
else	if ( i1=3 && i2=4 ) then c_alpha[4]*d[4] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_4_5 {i1 in 1..4, i2 in 1..4, i in Iterations} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[i,5]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[i,5])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[5]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[i,5])*c_alpha[5] 
else	if ( i1=2 && i2=2 ) then cos(theta[i,5])*c_alpha[5] 
else	if ( i1=2 && i2=3 ) then -s_alpha[5] 
else	if ( i1=2 && i2=4 ) then -s_alpha[5]*d[5] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[i,5])*s_alpha[5] 
else	if ( i1=3 && i2=2 ) then cos(theta[i,5])*s_alpha[5] 
else	if ( i1=3 && i2=3 ) then c_alpha[5] 
else	if ( i1=3 && i2=4 ) then c_alpha[5]*d[5] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_5_6 {i1 in 1..4, i2 in 1..4, i in Iterations} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[i,6]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[i,6])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[6]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[i,6])*c_alpha[6] 
else	if ( i1=2 && i2=2 ) then cos(theta[i,6])*c_alpha[6] 
else	if ( i1=2 && i2=3 ) then -s_alpha[6] 
else	if ( i1=2 && i2=4 ) then -s_alpha[6]*d[6] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[i,6])*s_alpha[6] 
else	if ( i1=3 && i2=2 ) then cos(theta[i,6])*s_alpha[6] 
else	if ( i1=3 && i2=3 ) then c_alpha[6] 
else	if ( i1=3 && i2=4 ) then c_alpha[6]*d[6] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_6_7 {i1 in 1..4, i2 in 1..4, i in Iterations} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[i,7]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[i,7])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[7]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[i,7])*c_alpha[7] 
else	if ( i1=2 && i2=2 ) then cos(theta[i,7])*c_alpha[7] 
else	if ( i1=2 && i2=3 ) then -s_alpha[7] 
else	if ( i1=2 && i2=4 ) then -s_alpha[7]*d[7] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[i,7])*s_alpha[7] 
else	if ( i1=3 && i2=2 ) then cos(theta[i,7])*s_alpha[7] 
else	if ( i1=3 && i2=3 ) then c_alpha[7] 
else	if ( i1=3 && i2=4 ) then c_alpha[7]*d[7] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
param T_7_H {i1 in 1..4, i2 in 1..4} =  
# 1st row 
if ( i1=1 && i2=1 ) then 1.00  
else	if ( i1=1 && i2=2 ) then 0.00  
else	if ( i1=1 && i2=3 ) then 0.00  
else	if ( i1=1 && i2=4 ) then 0.00  
# 2nd row 
else	if ( i1=2 && i2=1 ) then 0.00  
else	if ( i1=2 && i2=2 ) then 1.00  
else	if ( i1=2 && i2=3 ) then 0.00  
else	if ( i1=2 && i2=4 ) then 0.00  
# 3rd row 
else	if ( i1=3 && i2=1 ) then 0.00  
else	if ( i1=3 && i2=2 ) then 0.00  
else	if ( i1=3 && i2=3 ) then 1.00  
else	if ( i1=3 && i2=4 ) then 0.00  
# 4th row 
else	if ( i1=4 && i2=1 ) then 0.00  
else	if ( i1=4 && i2=2 ) then 0.00  
else	if ( i1=4 && i2=3 ) then 0.00  
else	if ( i1=4 && i2=4 ) then 1.00  
;  
var T_W_1 {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}   T_WorldToArm[i1,j]*T_0_1[j,i2,i];
var T_W_2 {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}   T_W_1[i1,j,i]*T_1_2[j,i2,i];
var T_W_3 {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}   T_W_2[i1,j,i]*T_2_3[j,i2,i];
var T_W_4 {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}   T_W_3[i1,j,i]*T_3_4[j,i2,i];
var T_W_5 {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}   T_W_4[i1,j,i]*T_4_5[j,i2,i];
var T_W_6 {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}   T_W_5[i1,j,i]*T_5_6[j,i2,i];
var T_W_7 {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}   T_W_6[i1,j,i]*T_6_7[j,i2,i];
var T_W_H {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}   T_W_7[i1,j,i]*T_7_H[j,i2];

var Shoulder {i in 1..4,j in Iterations} = #xyz+radius 
if ( i<4 ) then 	T_W_1[i,4,j] 
else	if ( i=4 ) then  80.00
;  
var Elbow {i in 1..4,j in Iterations} = #xyz+radius 
if ( i<4 ) then 	T_W_3[i,4,j] 
else	if ( i=4 ) then  70.00
;  
# Elbow orientation 
var x_E {j in 1..3,i in Iterations} = T_W_3 [j,1,i]; 
var y_E {j in 1..3,i in Iterations} = T_W_3 [j,2,i]; 
var z_E {j in 1..3,i in Iterations} = T_W_3 [j,3,i]; 
var Rot_E {j in 1..3,k in 1..3,i in Iterations} = T_W_3 [j,k,i]; 
 
# Wrist position 
var Wrist {i in 1..4,j in Iterations} = #xyz+radius 
if ( i<4 ) then 	T_W_5[i,4,j] 
else	if ( i=4 ) then  150.00
;  
# Wrist orientation 
var x_W {j in 1..3,i in Iterations} = T_W_5 [j,1,i]; 
var y_W {j in 1..3,i in Iterations} = T_W_5 [j,2,i]; 
var z_W {j in 1..3,i in Iterations} = T_W_5 [j,3,i]; 
var Rot_W {j in 1..3,k in 1..3,i in Iterations} = T_W_5 [j,k,i]; 
 
# Hand position 
var Hand {i in 1..4,j in Iterations} = #xyz+radius 
if ( i<4 ) then 	T_W_H[i,4,j] 
else	if ( i=4 ) then  100.00
;  
# Hand orientation 
var x_H {j in 1..3,i in Iterations} = T_W_H [j,1,i]; 
var y_H {j in 1..3,i in Iterations} = T_W_H [j,2,i]; 
var z_H {j in 1..3,i in Iterations} = T_W_H [j,3,i]; 
var Rot_H {j in 1..3,k in 1..3,i in Iterations} = T_W_H [j,k,i]; 
 
# Swivel angle 
param basez {j in 1..3} = T_WorldToArm [j,3]; 
var WS {j in 1..3,i in Iterations} = Wrist [j,i] - Shoulder [j,i]; 
var v_WS {j in 1..3,i in Iterations} = WS [j,i]/ sqrt(sum{i1 in 1..3}(WS [i1,i])^2); 
var ES {j in 1..3,i in Iterations} = Elbow [j,i] - Shoulder [j,i]; 
var p {j in 1..3,i in Iterations} = (1.00 - (v_WS [j,i])^2)*ES [j,i]; 
var s1 {i in Iterations} = sum{j in 1..3} (basez [j] * p [j,i]); 
var s2 {i in Iterations} = ((basez [2] * p [3,i]) - (basez [3] * p [2,i])) * v_WS [1,i] + ((basez [3] * p [1,i]) - (basez [1] * p [3,i])) * v_WS [2,i] + ((basez [1] * p [2,i]) - (basez [2] * p [1,i])) * v_WS [3,i]; 
var swivel {i in Iterations} = atan2(s2[i],s1[i]); 
# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
#  Direct Kinematics model of the fingers 

# Finger 1 

param TF1_1{i1 in 1..4, i2 in 1..4,i in Iterations} =   
 if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos(-1*0-(pi/2)*(-1)) 
else 	if (i1=1&&i2=2)					then   -sin(-1*0-(pi/2)*(-1)) 
else 	if (i1=2&&i2=1)					then 	sin(-1*0-(pi/2)*(-1))  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2>2 )||( i1=3 && i2<3 )||( i1=4 && i2<4 )) then 	0 
else	if (( i1=3 && i2=3 )||( i1=4 && i2=4 ) ) then 								1 
else	if ( i1=1 && i2=4 ) then 				-1*Aw 	 				 
else	if ( i1=3 && i2=4 ) then 										0 
; 
var TF1_2{i1 in 1..4, i2 in 1..4,i in Iterations} =   
if ((i1=1&&i2=1)||(i1=3&&i2=2)) then 	cos(theta[i,9]+phi_2)  
else 	if (i1=1&&i2=2)					then   -sin(theta[i,9]+phi_2)  
else 	if (i1=3&&i2=1)					then    sin(theta[i,9]+phi_2)  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=4 && i2<4 )||( i1=2 && i2=4 )) then 	0 
else	if ( i1=4 && i2=4 )  then 								1 
else	if ( i1=2 && i2=3 )  then 								-1 
else	if ( i1=1 && i2=4 ) then 								A1 
; 
var TF1_3{i1 in 1..4, i2 in 1..4,i in Iterations} =   
if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos((theta[i,9])/3+phi_3) 
else 	if (i1=1&&i2=2)					then   -sin((theta[i,9])/3+phi_3) 
else 	if (i1=2&&i2=1)					then    sin((theta[i,9])/3+phi_3) 
else 	if (( i1=1 && i2=3 )||( i1=3 && i2<3 )||( i1=2 && i2>2 )||( i1=4 && i2<4 )||( i1=3 && i2=4 )) then 	0 
else	if (( i1=4 && i2=4 )||( i1=3 && i2=3 ))  then 														1 
else	if ( i1=1 && i2=4 ) then 								A2 
; 
param TF1_4{i1 in 1..4, i2 in 1..4,i in Iterations} :=   
if ((i1=1&&i2=1)||(i1=2&&i2=3)||(i1=4&&i2=4)) then 	  1
else 	if (i1=3&&i2=2)								  then   -1 
else 	if (i1=1&&i2=4)					              then    A3 
else 	if (i1=2&&i2=4)					              then    D3 
else 	if (( i1=1 && i2=2 )||( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=3 && i2=1 )||( i1=4 && i2<4 )) then 	0 
;

var F1_0   {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4} T_W_H[i1,j,i]*TF1_1[j,i2,i]; 
var F1_1   {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}  F1_0[i1,j,i]*TF1_2[j,i2,i]; 
var F1_2   {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}  F1_1[i1,j,i]*TF1_3[j,i2,i]; 
var F1_tip {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}  F1_2[i1,j,i]*TF1_4[j,i2,i]; 

var Finger1_0   {i1 in 1..4,i in Iterations} =  if i1<4 then F1_0[i1,4,i] 	else 25.00; 
var Finger1_1   {i1 in 1..4,i in Iterations} =  if i1<4 then F1_1[i1,4,i] 	else 25.00; 
var Finger1_2   {i1 in 1..4,i in Iterations} =  if i1<4 then F1_2[i1,4,i] 	else 20.00; 
var Finger1_tip {i1 in 1..4,i in Iterations} =  if i1<4 then F1_tip[i1,4,i] else 15.00; 

# Finger 2 

param TF2_1{i1 in 1..4, i2 in 1..4,i in Iterations} =   
 if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos(1*0-(pi/2)*(1)) 
else 	if (i1=1&&i2=2)					then   -sin(1*0-(pi/2)*(1)) 
else 	if (i1=2&&i2=1)					then 	sin(1*0-(pi/2)*(1))  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2>2 )||( i1=3 && i2<3 )||( i1=4 && i2<4 )) then 	0 
else	if (( i1=3 && i2=3 )||( i1=4 && i2=4 ) ) then 								1 
else	if ( i1=1 && i2=4 ) then 				1*Aw 	 				 
else	if ( i1=3 && i2=4 ) then 										0 
; 
var TF2_2{i1 in 1..4, i2 in 1..4,i in Iterations} =   
if ((i1=1&&i2=1)||(i1=3&&i2=2)) then 	cos(theta[i,9]+phi_2)  
else 	if (i1=1&&i2=2)					then   -sin(theta[i,9]+phi_2)  
else 	if (i1=3&&i2=1)					then    sin(theta[i,9]+phi_2)  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=4 && i2<4 )||( i1=2 && i2=4 )) then 	0 
else	if ( i1=4 && i2=4 )  then 								1 
else	if ( i1=2 && i2=3 )  then 								-1 
else	if ( i1=1 && i2=4 ) then 								A1 
; 
var TF2_3{i1 in 1..4, i2 in 1..4,i in Iterations} =   
if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos((theta[i,9])/3+phi_3) 
else 	if (i1=1&&i2=2)					then   -sin((theta[i,9])/3+phi_3) 
else 	if (i1=2&&i2=1)					then    sin((theta[i,9])/3+phi_3) 
else 	if (( i1=1 && i2=3 )||( i1=3 && i2<3 )||( i1=2 && i2>2 )||( i1=4 && i2<4 )||( i1=3 && i2=4 )) then 	0 
else	if (( i1=4 && i2=4 )||( i1=3 && i2=3 ))  then 														1 
else	if ( i1=1 && i2=4 ) then 								A2 
; 
param TF2_4{i1 in 1..4, i2 in 1..4,i in Iterations} :=   
if ((i1=1&&i2=1)||(i1=2&&i2=3)||(i1=4&&i2=4)) then 	  1
else 	if (i1=3&&i2=2)								  then   -1 
else 	if (i1=1&&i2=4)					              then    A3 
else 	if (i1=2&&i2=4)					              then    D3 
else 	if (( i1=1 && i2=2 )||( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=3 && i2=1 )||( i1=4 && i2<4 )) then 	0 
;

var F2_0   {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4} T_W_H[i1,j,i]*TF2_1[j,i2,i]; 
var F2_1   {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}  F2_0[i1,j,i]*TF2_2[j,i2,i]; 
var F2_2   {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}  F2_1[i1,j,i]*TF2_3[j,i2,i]; 
var F2_tip {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}  F2_2[i1,j,i]*TF2_4[j,i2,i]; 

var Finger2_0   {i1 in 1..4,i in Iterations} =  if i1<4 then F2_0[i1,4,i] 	else 25.00; 
var Finger2_1   {i1 in 1..4,i in Iterations} =  if i1<4 then F2_1[i1,4,i] 	else 25.00; 
var Finger2_2   {i1 in 1..4,i in Iterations} =  if i1<4 then F2_2[i1,4,i] 	else 20.00; 
var Finger2_tip {i1 in 1..4,i in Iterations} =  if i1<4 then F2_tip[i1,4,i] else 15.00; 

# Finger 3 

param TF3_1{i1 in 1..4, i2 in 1..4,i in Iterations} =   
 if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos(0*0-(pi/2)*(0)) 
else 	if (i1=1&&i2=2)					then   -sin(0*0-(pi/2)*(0)) 
else 	if (i1=2&&i2=1)					then 	sin(0*0-(pi/2)*(0))  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2>2 )||( i1=3 && i2<3 )||( i1=4 && i2<4 )) then 	0 
else	if (( i1=3 && i2=3 )||( i1=4 && i2=4 ) ) then 								1 
else	if ( i1=1 && i2=4 ) then 				0*Aw 	 				 
else	if ( i1=3 && i2=4 ) then 										0 
; 
var TF3_2{i1 in 1..4, i2 in 1..4,i in Iterations} =   
if ((i1=1&&i2=1)||(i1=3&&i2=2)) then 	cos(theta[i,8]+phi_2)  
else 	if (i1=1&&i2=2)					then   -sin(theta[i,8]+phi_2)  
else 	if (i1=3&&i2=1)					then    sin(theta[i,8]+phi_2)  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=4 && i2<4 )||( i1=2 && i2=4 )) then 	0 
else	if ( i1=4 && i2=4 )  then 								1 
else	if ( i1=2 && i2=3 )  then 								-1 
else	if ( i1=1 && i2=4 ) then 								A1 
; 
var TF3_3{i1 in 1..4, i2 in 1..4,i in Iterations} =   
if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos((theta[i,8])/3+phi_3) 
else 	if (i1=1&&i2=2)					then   -sin((theta[i,8])/3+phi_3) 
else 	if (i1=2&&i2=1)					then    sin((theta[i,8])/3+phi_3) 
else 	if (( i1=1 && i2=3 )||( i1=3 && i2<3 )||( i1=2 && i2>2 )||( i1=4 && i2<4 )||( i1=3 && i2=4 )) then 	0 
else	if (( i1=4 && i2=4 )||( i1=3 && i2=3 ))  then 														1 
else	if ( i1=1 && i2=4 ) then 								A2 
; 
param TF3_4{i1 in 1..4, i2 in 1..4,i in Iterations} :=   
if ((i1=1&&i2=1)||(i1=2&&i2=3)||(i1=4&&i2=4)) then 	  1
else 	if (i1=3&&i2=2)								  then   -1 
else 	if (i1=1&&i2=4)					              then    A3 
else 	if (i1=2&&i2=4)					              then    D3 
else 	if (( i1=1 && i2=2 )||( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=3 && i2=1 )||( i1=4 && i2<4 )) then 	0 
;

var F3_0   {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4} T_W_H[i1,j,i]*TF3_1[j,i2,i]; 
var F3_1   {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}  F3_0[i1,j,i]*TF3_2[j,i2,i]; 
var F3_2   {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}  F3_1[i1,j,i]*TF3_3[j,i2,i]; 
var F3_tip {i1 in 1..4, i2 in 1..4,i in Iterations} =  sum {j in 1..4}  F3_2[i1,j,i]*TF3_4[j,i2,i]; 

var Finger3_0   {i1 in 1..4,i in Iterations} =  if i1<4 then F3_0[i1,4,i] 	else 25.00; 
var Finger3_1   {i1 in 1..4,i in Iterations} =  if i1<4 then F3_1[i1,4,i] 	else 25.00; 
var Finger3_2   {i1 in 1..4,i in Iterations} =  if i1<4 then F3_2[i1,4,i] 	else 20.00; 
var Finger3_tip {i1 in 1..4,i in Iterations} =  if i1<4 then F3_tip[i1,4,i] else 15.00; 

var Points_Arm {j in 1..15, i in 1..4,k in Iterations} = 
if ( j=1 ) then 	(Shoulder[i,k]+Elbow[i,k])/2  
else	if ( j=2 ) then 	Elbow[i,k] 
else    if ( j=3 ) then 	(Wrist[i,k]+Elbow[i,k])/2  
else	if ( j=4 ) then 	Wrist[i,k] 
else	if ( j=5 ) then 	Wrist[i,k]+0.45*(Hand[i,k]-Wrist[i,k]) 
else	if ( j=6 ) then 	Wrist[i,k]+0.75*(Hand[i,k]-Wrist[i,k]) 
else	if ( j=7 ) then 	Finger1_1[i,k] 
else	if ( j=8 ) then 	Finger2_1[i,k] 
else	if ( j=9 ) then 	Finger3_1[i,k]
else	if ( j=10 ) then 	 Finger1_2[i,k] 
else	if ( j=11 ) then 	 Finger2_2[i,k] 
else	if ( j=12 ) then 	 Finger3_2[i,k] 
else	if ( j=13 ) then 	Finger1_tip[i,k]
else	if ( j=14 ) then 	Finger2_tip[i,k] 
else	if ( j=15 ) then 	Finger3_tip[i,k] 
; 

# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
#  
#		       Objective function          # 
#  
minimize z: sum {j in nJoints} (lambda[j]*(thet_init[j]-theta_b[j])^2); 
# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
#  
#		     Constraints                  # 
#  
param tol_obs_xx1 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 10.00
else if (i > (Nsteps/2)) then 10.00; 
param tol_obs_xx2 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 10.00
else if (i > (Nsteps/2)) then 10.00; 
param tol_obs_xx3 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 10.00
else if (i > (Nsteps/2)) then 10.00; 
param tol_obs_yy1 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 10.00
else if (i > (Nsteps/2)) then 10.00; 
param tol_obs_yy2 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 10.00
else if (i > (Nsteps/2)) then 10.00; 
param tol_obs_yy3 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 10.00
else if (i > (Nsteps/2)) then 10.00; 
param tol_obs_zz1 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 150.00
else if (i > (Nsteps/2)) then 150.00; 
param tol_obs_zz2 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 150.00
else if (i > (Nsteps/2)) then 150.00; 
param tol_obs_zz3 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 150.00
else if (i > (Nsteps/2)) then 150.00; 
param tol_obs_xy1 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 5.00
else if (i > (Nsteps/2)) then 5.00; 
param tol_obs_xy2 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 5.00
else if (i > (Nsteps/2)) then 5.00; 
param tol_obs_xy3 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 5.00
else if (i > (Nsteps/2)) then 5.00; 
param tol_obs_xz1 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 5.00
else if (i > (Nsteps/2)) then 5.00; 
param tol_obs_xz2 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 5.00
else if (i > (Nsteps/2)) then 5.00; 
param tol_obs_xz3 {i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 5.00
else if (i > (Nsteps/2)) then 5.00; 
param tol_obs_yz1{i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 5.00
else if (i > (Nsteps/2)) then 5.00; 
param tol_obs_yz2{i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 5.00
else if (i > (Nsteps/2)) then 5.00; 
param tol_obs_yz3{i in 1..Nsteps+1} :=  
if 		(i < (Nsteps/2)+1) then 5.00
else if (i > (Nsteps/2)) then 5.00; 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
subject to obst_Arm{j in 1..15, i in 1..(n_Obstacles), l in 2..Nsteps+1} := dual_in[((j-1)*n_Obstacles*11)+((i-1)*11)+l-1+0] :
(((Rot[1,1,i]*Points_Arm[j,1,l]+Rot[2,1,i]*Points_Arm[j,2,l]+Rot[3,1,i]*Points_Arm[j,3,l]
-Obstacles[i,1]*Rot[1,1,i]-Obstacles[i,2]*Rot[2,1,i]-Obstacles[i,3]*Rot[3,1,i])
/(Obstacles[i,4]+Points_Arm[j,4,l]+tol_obs_xx1[l]))^2
+
((Rot[1,2,i]*Points_Arm[j,1,l]+Rot[2,2,i]*Points_Arm[j,2,l]+Rot[3,2,i]*Points_Arm[j,3,l]
-Obstacles[i,1]*Rot[1,2,i]-Obstacles[i,2]*Rot[2,2,i]-Obstacles[i,3]*Rot[3,2,i])
/(Obstacles[i,5]+Points_Arm[j,4,l]+tol_obs_yy1[l]))^2
+
((Rot[1,3,i]*Points_Arm[j,1,l]+Rot[2,3,i]*Points_Arm[j,2,l]+Rot[3,3,i]*Points_Arm[j,3,l]
-Obstacles[i,1]*Rot[1,3,i]-Obstacles[i,2]*Rot[2,3,i]-Obstacles[i,3]*Rot[3,3,i])
/(Obstacles[i,6]+Points_Arm[j,4,l]+tol_obs_zz1[l]))^2)
>= 1;
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# 
# Constraints with the body: the body is modeled as a cylinder 
subject to BodyArm_Elbow{l in Iterations} := dual_in[l+165] : (Elbow[1,l]/(body[1]+Elbow[4,l]))^2 + (Elbow[2,l]/(body[2]+Elbow[4,l]))^2 >= 1; 
subject to BodyArm_Wrist{l in Iterations} := dual_in[l+177]: (Wrist[1,l]/(body[1]+Wrist[4,l]))^2 + (Wrist[2,l]/(body[2]+Wrist[4,l]))^2 >= 1; 
subject to BodyArm_Hand{l in Iterations} := dual_in[l+189]:  (Hand[1,l]/(body[1]+Hand[4,l]))^2  + (Hand[2,l]/(body[2]+Hand[4,l]))^2  >= 1; 

  
# joint limits for all the trajectory 
subject to co_JointLimits {i in Iterations, j in nJoints} := dual_in[((i-1)*9)+j+201] : llim[j] <= theta[i,j]  <= ulim[j]; 

# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 


