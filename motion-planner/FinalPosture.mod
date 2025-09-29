# FINAL POSTURE MODEL FILE 
# Movement to plan: 
# Reaching, Arm: right, Object: , Object Engaged: , Pose: , Grip Type: 

# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
# PARAMETERS 

set nJoints := 1..7;
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
param llim {i in 1..7} ; 
let llim[1] := -2.6005;
let llim[2] := -1.6406;
let llim[3] := -1.5533;
let llim[4] := -1.9373;
let llim[5] := -2.8623;
let llim[6] := -2.0769;
let llim[7] := -1.5533;
# Upper Bounds 
param ulim {i in 1..7} ; 
let ulim[1] := 1.5533;
let ulim[2] := 0.7679;
let ulim[3] := 2.4260;
let ulim[4] := 1.0821;
let ulim[5] := 2.8623;
let ulim[6] := 2.0769;
let ulim[7] := 2.8623;
# Initial configuration 
param thet_init {i in 1..7} ; 
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
# Final finger posture 
param joint_fingers {i in 1..4} ; 
# Joint Expense Factors 
param lambda {i in 1..7} ; 
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
# CONSTRAINTS LAGRANGE MULTIPLIERS 
param n_constr; 
param dual_in {i in 1..n_constr}; 
# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
# DECISION VARIABLES 
var theta {i in 1..7} >= llim[i], <= ulim[i]; 
# BOUNDS LAGRANGE MULTIPLIERS 
# Lower Bounds Multipliers 
param zL_in {i in 1..7} ; 
let zL_in[1] := 0.00000009;
let zL_in[2] := 3.10272909;
let zL_in[3] := 0.00000003;
let zL_in[4] := 0.00000009;
let zL_in[5] := 0.00000003;
let zL_in[6] := 0.00000006;
let zL_in[7] := 0.00000006;
suffix ipopt_zL_in, IN; 
let {i in 1..7} theta[i].ipopt_zL_in := zL_in[i]; 
# Upper Bounds Multipliers 
param zU_in {i in 1..7} ; 
let zU_in[1] := -0.00000003;
let zU_in[2] := -0.00000004;
let zU_in[3] := -0.00000011;
let zU_in[4] := -0.00000004;
let zU_in[5] := -0.00000003;
let zU_in[6] := -0.00000003;
let zU_in[7] := -0.00000003;
suffix ipopt_zU_in, IN; 
let {i in 1..7} theta[i].ipopt_zU_in := zU_in[i]; 
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
var T_0_1 {i1 in 1..4, i2 in 1..4} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[1]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[1])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[1]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[1])*c_alpha[1] 
else	if ( i1=2 && i2=2 ) then cos(theta[1])*c_alpha[1] 
else	if ( i1=2 && i2=3 ) then -s_alpha[1] 
else	if ( i1=2 && i2=4 ) then -s_alpha[1]*d[1] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[1])*s_alpha[1] 
else	if ( i1=3 && i2=2 ) then cos(theta[1])*s_alpha[1] 
else	if ( i1=3 && i2=3 ) then c_alpha[1] 
else	if ( i1=3 && i2=4 ) then c_alpha[1]*d[1] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_1_2 {i1 in 1..4, i2 in 1..4} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[2]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[2])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[2]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[2])*c_alpha[2] 
else	if ( i1=2 && i2=2 ) then cos(theta[2])*c_alpha[2] 
else	if ( i1=2 && i2=3 ) then -s_alpha[2] 
else	if ( i1=2 && i2=4 ) then -s_alpha[2]*d[2] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[2])*s_alpha[2] 
else	if ( i1=3 && i2=2 ) then cos(theta[2])*s_alpha[2] 
else	if ( i1=3 && i2=3 ) then c_alpha[2] 
else	if ( i1=3 && i2=4 ) then c_alpha[2]*d[2] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_2_3 {i1 in 1..4, i2 in 1..4} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[3]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[3])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[3]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[3])*c_alpha[3] 
else	if ( i1=2 && i2=2 ) then cos(theta[3])*c_alpha[3] 
else	if ( i1=2 && i2=3 ) then -s_alpha[3] 
else	if ( i1=2 && i2=4 ) then -s_alpha[3]*d[3] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[3])*s_alpha[3] 
else	if ( i1=3 && i2=2 ) then cos(theta[3])*s_alpha[3] 
else	if ( i1=3 && i2=3 ) then c_alpha[3] 
else	if ( i1=3 && i2=4 ) then c_alpha[3]*d[3] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_3_4 {i1 in 1..4, i2 in 1..4} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[4]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[4])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[4]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[4])*c_alpha[4] 
else	if ( i1=2 && i2=2 ) then cos(theta[4])*c_alpha[4] 
else	if ( i1=2 && i2=3 ) then -s_alpha[4] 
else	if ( i1=2 && i2=4 ) then -s_alpha[4]*d[4] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[4])*s_alpha[4] 
else	if ( i1=3 && i2=2 ) then cos(theta[4])*s_alpha[4] 
else	if ( i1=3 && i2=3 ) then c_alpha[4] 
else	if ( i1=3 && i2=4 ) then c_alpha[4]*d[4] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_4_5 {i1 in 1..4, i2 in 1..4} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[5]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[5])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[5]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[5])*c_alpha[5] 
else	if ( i1=2 && i2=2 ) then cos(theta[5])*c_alpha[5] 
else	if ( i1=2 && i2=3 ) then -s_alpha[5] 
else	if ( i1=2 && i2=4 ) then -s_alpha[5]*d[5] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[5])*s_alpha[5] 
else	if ( i1=3 && i2=2 ) then cos(theta[5])*s_alpha[5] 
else	if ( i1=3 && i2=3 ) then c_alpha[5] 
else	if ( i1=3 && i2=4 ) then c_alpha[5]*d[5] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_5_6 {i1 in 1..4, i2 in 1..4} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[6]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[6])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[6]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[6])*c_alpha[6] 
else	if ( i1=2 && i2=2 ) then cos(theta[6])*c_alpha[6] 
else	if ( i1=2 && i2=3 ) then -s_alpha[6] 
else	if ( i1=2 && i2=4 ) then -s_alpha[6]*d[6] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[6])*s_alpha[6] 
else	if ( i1=3 && i2=2 ) then cos(theta[6])*s_alpha[6] 
else	if ( i1=3 && i2=3 ) then c_alpha[6] 
else	if ( i1=3 && i2=4 ) then c_alpha[6]*d[6] 
# 4th row 
else	if ( i1=4 && i2=1 ) then 0 
else	if ( i1=4 && i2=2 ) then 0  
else	if ( i1=4 && i2=3 ) then 0  
else	if ( i1=4 && i2=4 ) then 1  
;  
var T_6_7 {i1 in 1..4, i2 in 1..4} =  
# 1st row 
if ( i1=1 && i2=1 ) then cos(theta[7]) 
else	if ( i1=1 && i2=2 ) then -sin(theta[7])  
else	if ( i1=1 && i2=3 ) then 0  
else	if ( i1=1 && i2=4 ) then a[7]  
# 2st row 
else	if ( i1=2 && i2=1 ) then sin(theta[7])*c_alpha[7] 
else	if ( i1=2 && i2=2 ) then cos(theta[7])*c_alpha[7] 
else	if ( i1=2 && i2=3 ) then -s_alpha[7] 
else	if ( i1=2 && i2=4 ) then -s_alpha[7]*d[7] 
# 3rd row 
else	if ( i1=3 && i2=1 ) then sin(theta[7])*s_alpha[7] 
else	if ( i1=3 && i2=2 ) then cos(theta[7])*s_alpha[7] 
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
var T_W_1 {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}   T_WorldToArm[i1,j]*T_0_1[j,i2];
var T_W_2 {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}   T_W_1[i1,j]*T_1_2[j,i2];
var T_W_3 {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}   T_W_2[i1,j]*T_2_3[j,i2];
var T_W_4 {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}   T_W_3[i1,j]*T_3_4[j,i2];
var T_W_5 {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}   T_W_4[i1,j]*T_4_5[j,i2];
var T_W_6 {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}   T_W_5[i1,j]*T_5_6[j,i2];
var T_W_7 {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}   T_W_6[i1,j]*T_6_7[j,i2];
var T_W_H {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}   T_W_7[i1,j]*T_7_H[j,i2];

var Shoulder {i in 1..4} = #xyz+radius 
if ( i<4 ) then 	T_W_1[i,4] 
else	if ( i=4 ) then  80.00
;  
var Elbow {i in 1..4} = #xyz+radius 
if ( i<4 ) then 	T_W_3[i,4] 
else	if ( i=4 ) then  70.00
;  
# Elbow orientation 
var x_E {j in 1..3} = T_W_3 [j,1]; 
var y_E {j in 1..3} = T_W_3 [j,2]; 
var z_E {j in 1..3} = T_W_3 [j,3]; 
var Rot_E {j in 1..3,k in 1..3} = T_W_3 [j,k]; 
 
# Wrist position 
var Wrist {i in 1..4} = #xyz+radius 
if ( i<4 ) then 	T_W_5[i,4] 
else	if ( i=4 ) then  150.00
;  
# Wrist orientation 
var x_W {j in 1..3} = T_W_5 [j,1]; 
var y_W {j in 1..3} = T_W_5 [j,2]; 
var z_W {j in 1..3} = T_W_5 [j,3]; 
var Rot_W {j in 1..3,k in 1..3} = T_W_5 [j,k]; 
 
# Hand position 
var Hand {i in 1..4} = #xyz+radius 
if ( i<4 ) then 	T_W_H[i,4] 
else	if ( i=4 ) then  100.00
;  
# Hand orientation 
var x_H {j in 1..3} = T_W_H [j,1]; 
var y_H {j in 1..3} = T_W_H [j,2]; 
var z_H {j in 1..3} = T_W_H [j,3]; 
var Rot_H {j in 1..3,k in 1..3} = T_W_H [j,k]; 
 
# Swivel angle 
param basez {j in 1..3} = T_WorldToArm [j,3]; 
var WS {j in 1..3} = Wrist [j] - Shoulder [j]; 
var v_WS {j in 1..3} = WS [j]/ sqrt(sum{i in 1..3}(WS [i])^2); 
var ES {j in 1..3} = Elbow [j] - Shoulder [j]; 
var p {j in 1..3} = (1.00 - (v_WS [j])^2)*ES [j]; 
var s1 = sum{i in 1..3} (basez [i] * p [i]); 
var s2 = ((basez [2] * p [3]) - (basez [3] * p [2])) * v_WS [1] + ((basez [3] * p [1]) - (basez [1] * p [3])) * v_WS [2] + ((basez [1] * p [2]) - (basez [2] * p [1])) * v_WS [3]; 
var swivel = atan2(s2,s1); 
# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
#  Direct Kinematics model of the fingers 

# Finger 1 

param TF1_1{i1 in 1..4, i2 in 1..4} :=   
 if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos(-1*joint_fingers[1]-(pi/2)*(-1)) 
else 	if (i1=1&&i2=2)					then   -sin(-1*joint_fingers[1]-(pi/2)*(-1)) 
else 	if (i1=2&&i2=1)					then 	sin(-1*joint_fingers[1]-(pi/2)*(-1))  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2>2 )||( i1=3 && i2<3 )||( i1=4 && i2<4 )) then 	0 
else	if (( i1=3 && i2=3 )||( i1=4 && i2=4 ) ) then 								1 
else	if ( i1=1 && i2=4 ) then 				-1*Aw 	 				 
else	if ( i1=3 && i2=4 ) then 										0 
; 
param TF1_2{i1 in 1..4, i2 in 1..4} :=   
if ((i1=1&&i2=1)||(i1=3&&i2=2)) then 	cos(joint_fingers[2]+phi_2)  
else 	if (i1=1&&i2=2)					then   -sin(joint_fingers[2]+phi_2)  
else 	if (i1=3&&i2=1)					then    sin(joint_fingers[2]+phi_2)  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=4 && i2<4 )||( i1=2 && i2=4 )) then 	0 
else	if ( i1=4 && i2=4 )  then 								1 
else	if ( i1=2 && i2=3 )  then 								-1 
else	if ( i1=1 && i2=4 ) then 								A1 
; 
param TF1_3{i1 in 1..4, i2 in 1..4} :=   
if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos((joint_fingers[2])/3+phi_3) 
else 	if (i1=1&&i2=2)					then   -sin((joint_fingers[2])/3+phi_3) 
else 	if (i1=2&&i2=1)					then    sin((joint_fingers[2])/3+phi_3) 
else 	if (( i1=1 && i2=3 )||( i1=3 && i2<3 )||( i1=2 && i2>2 )||( i1=4 && i2<4 )||( i1=3 && i2=4 )) then 	0 
else	if (( i1=4 && i2=4 )||( i1=3 && i2=3 ))  then 														1 
else	if ( i1=1 && i2=4 ) then 								A2 
; 
param TF1_4{i1 in 1..4, i2 in 1..4} :=   
if ((i1=1&&i2=1)||(i1=2&&i2=3)||(i1=4&&i2=4)) then 	  1
else 	if (i1=3&&i2=2)								  then   -1 
else 	if (i1=1&&i2=4)					              then    A3 
else 	if (i1=2&&i2=4)					              then    D3 
else 	if (( i1=1 && i2=2 )||( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=3 && i2=1 )||( i1=4 && i2<4 )) then 	0 
;

var F1_0   {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4} T_W_H[i1,j]*TF1_1[j,i2]; 
var F1_1   {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}  F1_0[i1,j]*TF1_2[j,i2]; 
var F1_2   {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}  F1_1[i1,j]*TF1_3[j,i2]; 
var F1_tip {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}  F1_2[i1,j]*TF1_4[j,i2]; 

var Finger1_0   {i1 in 1..4} =  if i1<4 then F1_0[i1,4] 	else 25.00; 
var Finger1_1   {i1 in 1..4} =  if i1<4 then F1_1[i1,4] 	else 25.00; 
var Finger1_2   {i1 in 1..4} =  if i1<4 then F1_2[i1,4] 	else 20.00; 
var Finger1_tip {i1 in 1..4} =  if i1<4 then F1_tip[i1,4] else 15.00; 

# Finger 2 

param TF2_1{i1 in 1..4, i2 in 1..4} :=   
 if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos(1*joint_fingers[1]-(pi/2)*(1)) 
else 	if (i1=1&&i2=2)					then   -sin(1*joint_fingers[1]-(pi/2)*(1)) 
else 	if (i1=2&&i2=1)					then 	sin(1*joint_fingers[1]-(pi/2)*(1))  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2>2 )||( i1=3 && i2<3 )||( i1=4 && i2<4 )) then 	0 
else	if (( i1=3 && i2=3 )||( i1=4 && i2=4 ) ) then 								1 
else	if ( i1=1 && i2=4 ) then 				1*Aw 	 				 
else	if ( i1=3 && i2=4 ) then 										0 
; 
param TF2_2{i1 in 1..4, i2 in 1..4} :=   
if ((i1=1&&i2=1)||(i1=3&&i2=2)) then 	cos(joint_fingers[3]+phi_2)  
else 	if (i1=1&&i2=2)					then   -sin(joint_fingers[3]+phi_2)  
else 	if (i1=3&&i2=1)					then    sin(joint_fingers[3]+phi_2)  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=4 && i2<4 )||( i1=2 && i2=4 )) then 	0 
else	if ( i1=4 && i2=4 )  then 								1 
else	if ( i1=2 && i2=3 )  then 								-1 
else	if ( i1=1 && i2=4 ) then 								A1 
; 
param TF2_3{i1 in 1..4, i2 in 1..4} :=   
if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos((joint_fingers[3])/3+phi_3) 
else 	if (i1=1&&i2=2)					then   -sin((joint_fingers[3])/3+phi_3) 
else 	if (i1=2&&i2=1)					then    sin((joint_fingers[3])/3+phi_3) 
else 	if (( i1=1 && i2=3 )||( i1=3 && i2<3 )||( i1=2 && i2>2 )||( i1=4 && i2<4 )||( i1=3 && i2=4 )) then 	0 
else	if (( i1=4 && i2=4 )||( i1=3 && i2=3 ))  then 														1 
else	if ( i1=1 && i2=4 ) then 								A2 
; 
param TF2_4{i1 in 1..4, i2 in 1..4} :=   
if ((i1=1&&i2=1)||(i1=2&&i2=3)||(i1=4&&i2=4)) then 	  1
else 	if (i1=3&&i2=2)								  then   -1 
else 	if (i1=1&&i2=4)					              then    A3 
else 	if (i1=2&&i2=4)					              then    D3 
else 	if (( i1=1 && i2=2 )||( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=3 && i2=1 )||( i1=4 && i2<4 )) then 	0 
;

var F2_0   {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4} T_W_H[i1,j]*TF2_1[j,i2]; 
var F2_1   {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}  F2_0[i1,j]*TF2_2[j,i2]; 
var F2_2   {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}  F2_1[i1,j]*TF2_3[j,i2]; 
var F2_tip {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}  F2_2[i1,j]*TF2_4[j,i2]; 

var Finger2_0   {i1 in 1..4} =  if i1<4 then F2_0[i1,4] 	else 25.00; 
var Finger2_1   {i1 in 1..4} =  if i1<4 then F2_1[i1,4] 	else 25.00; 
var Finger2_2   {i1 in 1..4} =  if i1<4 then F2_2[i1,4] 	else 20.00; 
var Finger2_tip {i1 in 1..4} =  if i1<4 then F2_tip[i1,4] else 15.00; 

# Finger 3 

param TF3_1{i1 in 1..4, i2 in 1..4} :=   
 if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos(0*joint_fingers[1]-(pi/2)*(0)) 
else 	if (i1=1&&i2=2)					then   -sin(0*joint_fingers[1]-(pi/2)*(0)) 
else 	if (i1=2&&i2=1)					then 	sin(0*joint_fingers[1]-(pi/2)*(0))  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2>2 )||( i1=3 && i2<3 )||( i1=4 && i2<4 )) then 	0 
else	if (( i1=3 && i2=3 )||( i1=4 && i2=4 ) ) then 								1 
else	if ( i1=1 && i2=4 ) then 				0*Aw 	 				 
else	if ( i1=3 && i2=4 ) then 										0 
; 
param TF3_2{i1 in 1..4, i2 in 1..4} :=   
if ((i1=1&&i2=1)||(i1=3&&i2=2)) then 	cos(joint_fingers[4]+phi_2)  
else 	if (i1=1&&i2=2)					then   -sin(joint_fingers[4]+phi_2)  
else 	if (i1=3&&i2=1)					then    sin(joint_fingers[4]+phi_2)  
else 	if (( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=4 && i2<4 )||( i1=2 && i2=4 )) then 	0 
else	if ( i1=4 && i2=4 )  then 								1 
else	if ( i1=2 && i2=3 )  then 								-1 
else	if ( i1=1 && i2=4 ) then 								A1 
; 
param TF3_3{i1 in 1..4, i2 in 1..4} :=   
if ((i1=1&&i2=1)||(i1=2&&i2=2)) then 	cos((joint_fingers[4])/3+phi_3) 
else 	if (i1=1&&i2=2)					then   -sin((joint_fingers[4])/3+phi_3) 
else 	if (i1=2&&i2=1)					then    sin((joint_fingers[4])/3+phi_3) 
else 	if (( i1=1 && i2=3 )||( i1=3 && i2<3 )||( i1=2 && i2>2 )||( i1=4 && i2<4 )||( i1=3 && i2=4 )) then 	0 
else	if (( i1=4 && i2=4 )||( i1=3 && i2=3 ))  then 														1 
else	if ( i1=1 && i2=4 ) then 								A2 
; 
param TF3_4{i1 in 1..4, i2 in 1..4} :=   
if ((i1=1&&i2=1)||(i1=2&&i2=3)||(i1=4&&i2=4)) then 	  1
else 	if (i1=3&&i2=2)								  then   -1 
else 	if (i1=1&&i2=4)					              then    A3 
else 	if (i1=2&&i2=4)					              then    D3 
else 	if (( i1=1 && i2=2 )||( i1=1 && i2=3 )||( i1=2 && i2<3 )||( i1=3 && i2>2 )||( i1=3 && i2=1 )||( i1=4 && i2<4 )) then 	0 
;

var F3_0   {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4} T_W_H[i1,j]*TF3_1[j,i2]; 
var F3_1   {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}  F3_0[i1,j]*TF3_2[j,i2]; 
var F3_2   {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}  F3_1[i1,j]*TF3_3[j,i2]; 
var F3_tip {i1 in 1..4, i2 in 1..4} =  sum {j in 1..4}  F3_2[i1,j]*TF3_4[j,i2]; 

var Finger3_0   {i1 in 1..4} =  if i1<4 then F3_0[i1,4] 	else 25.00; 
var Finger3_1   {i1 in 1..4} =  if i1<4 then F3_1[i1,4] 	else 25.00; 
var Finger3_2   {i1 in 1..4} =  if i1<4 then F3_2[i1,4] 	else 20.00; 
var Finger3_tip {i1 in 1..4} =  if i1<4 then F3_tip[i1,4] else 15.00; 

var Points_Arm {j in 1..15, i in 1..4} = 
if ( j=1 ) then 	(Shoulder[i]+Elbow[i])/2  
else	if ( j=2 ) then 	Elbow[i] 
else    if ( j=3 ) then 	(Wrist[i]+Elbow[i])/2  
else	if ( j=4 ) then 	Wrist[i] 
else	if ( j=5 ) then 	Wrist[i]+0.45*(Hand[i]-Wrist[i]) 
else	if ( j=6 ) then 	Wrist[i]+0.75*(Hand[i]-Wrist[i]) 
else	if ( j=7 ) then 	Finger1_1[i] 
else	if ( j=8 ) then 	Finger2_1[i] 
else	if ( j=9 ) then 	Finger3_1[i]
else	if ( j=10 ) then 	 Finger1_2[i] 
else	if ( j=11 ) then 	 Finger2_2[i] 
else	if ( j=12 ) then 	 Finger3_2[i] 
else	if ( j=13 ) then 	Finger1_tip[i]
else	if ( j=14 ) then 	Finger2_tip[i] 
else	if ( j=15 ) then 	Finger3_tip[i] 
; 

# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
#  
#		       Objective function          # 
#  
minimize z: sum {j in nJoints} (lambda[j]*(thet_init[j]-theta[j])^2); 
# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 
#  
#		      Constraints                  # 
#  
# Hand position 
# subject to constr_hand_pos  {i in 1..3}: Hand[i] - Tar_pos[i] = 0; 
subject to constr_hand_pos := dual_in[1] : (sum{i in 1..3} (Hand[i] - Tar_pos[i])^2) <= 1.00; 

# Hand orientation
subject to constr_hand_orient := dual_in[2] : (sum{i in 1..3} (x_H[i] - x_t[i])^2 + sum{i in 1..3} (z_H[i] - z_t[i])^2 )<= 0.0010; #  x_H = x_t and z_H = x_t 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# 
subject to obst_Arm{j in 1..15, i in 1..n_Obstacles} := dual_in[(j-1)*n_Obstacles + i +2] :  
(((Rot[1,1,i]*Points_Arm[j,1]+Rot[2,1,i]*Points_Arm[j,2]+Rot[3,1,i]*Points_Arm[j,3]
-Obstacles[i,1]*Rot[1,1,i]-Obstacles[i,2]*Rot[2,1,i]-Obstacles[i,3]*Rot[3,1,i])
/(Obstacles[i,4]+Points_Arm[j,4]+10.00))^2
+
((Rot[1,2,i]*Points_Arm[j,1]+Rot[2,2,i]*Points_Arm[j,2]+Rot[3,2,i]*Points_Arm[j,3]
-Obstacles[i,1]*Rot[1,2,i]-Obstacles[i,2]*Rot[2,2,i]-Obstacles[i,3]*Rot[3,2,i])
/(Obstacles[i,5]+Points_Arm[j,4]+10.00))^2
+
((Rot[1,3,i]*Points_Arm[j,1]+Rot[2,3,i]*Points_Arm[j,2]+Rot[3,3,i]*Points_Arm[j,3]
-Obstacles[i,1]*Rot[1,3,i]-Obstacles[i,2]*Rot[2,3,i]-Obstacles[i,3]*Rot[3,3,i])
/(Obstacles[i,6]+Points_Arm[j,4]+150.00))^2)>= 1;
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#  
# Constraints with the body: the body is modeled as a cylinder 
subject to BodyArm_Elbow := dual_in[18] : (Elbow[1]/(body[1]+Elbow[4]))^2 + (Elbow[2]/(body[2]+Elbow[4]))^2 >= 1; 
subject to BodyArm_Wrist := dual_in[19] : (Wrist[1]/(body[1]+Wrist[4]))^2 + (Wrist[2]/(body[2]+Wrist[4]))^2 >= 1; 
subject to BodyArm_Hand  := dual_in[20] :  (Hand[1]/(body[1]+Hand[4]))^2  + (Hand[2]/(body[2]+Hand[4]))^2  >= 1; 

# *+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*+*# 


