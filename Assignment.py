
# This code explains the backbone curve of a 6 storey strong-infilled frame
duct_points = [1, 2.35, 2.6, 3.35, 7] #this list contains the values of ductility at points where the SPO backbone curve changes its direction

# 1. For Hardening branch:
import numpy as np
import math
duct1 = np.linspace(1, 2.35, 10)
#assume 
time_T = 0.41 #sec

# a. Calculation of parameters 'alpha1' and 'beta1'
a_alpha1 = [0.8628, 0.9235, 0.9195, 0.9632, 0.4745, 0.0654, 0.04461]
b_alpha1 = [0.7624, 0.5041, 0.1785, 1.0220, 0.3253, 0.4064, 0.4479]
c_alpha1 = [0.1643, 0.1701, 0.1147, 0.1694, 0.0940, 0.0205, 0.0158]
a_beta1 = [-0.1334, 0.3312, 0.7985, 0.000, 0.1543, 0.9252, 0.2809]
b_beta1 = [0.7771, 0.7647, 0.0428, 0.5721, 0.4788, 0.8165, 0.3003]
c_beta1 = [0.04907, 0.00098, 0.09365, 0.0001, 0.1050, 0.5100, 0.1216]

alpha = []
beta = []
for i in range(len(a_alpha1)):
    pow_term = pow(((time_T-b_alpha1[i])/c_alpha1[i]), 2)
    alpha_i = a_alpha1[i]*(math.exp(-pow_term))
    alpha.append(alpha_i)

    pow_term = pow(((time_T-b_beta1[i])/c_beta1[i]), 2)
    beta_i = a_beta1[i]*(math.exp(-pow_term))
    beta.append(beta_i)
    
alpha1 = sum(alpha) 
beta1 = sum(beta)

# b. Calculation of strength ratio R for hardening branch

strength_ratio_h = []
for i in range(len(duct1)):
    x = duct1[i]
    R = alpha1 * pow(x, beta1)
    strength_ratio_h.append(R)
print(strength_ratio_h)

# 2. For Softening branch
# a. Calculation of parameters 'alpha2', 'beta2', and 'gamma2'

a_coeffs = [0.0183, 0.8237, -0.7208] #alpha, beta, and gamma parameters respectively
b_coeffs = [-0.0148, 0.0408, 1.2790] #alpha, beta, and gamma parameters respectively
alpha2 = a_coeffs[0]*time_T + b_coeffs[0]
beta2 = a_coeffs[1]*time_T + b_coeffs[1]
gamma2 = a_coeffs[2]*time_T + b_coeffs[2]
duct2 = np.linspace(2.35, 2.6, 10)

# b. Calculation of strength_ratio Rdyn for softening branch

strength_ratio_s = []
for i in range(len(duct2)):
    R = (alpha2*pow(duct2[i], 2)) + (beta2*duct2[i]) + gamma2
    strength_ratio_s.append(R)

# 3. For Residual Plateau Branch
# a. Calculation of parameters 'alpha3', and 'beta3'

alpha_coeffs = [-2.099, 3.182, -0.6989, 0.0481] 
beta_coeffs = [8.417, -14.51, 6.750, 0.9061] 
alpha3 = alpha_coeffs[0]*pow(time_T, 3) + alpha_coeffs[1]*pow(time_T, 2) + alpha_coeffs[2]*time_T + alpha_coeffs[3]
beta3 = beta_coeffs[0]*pow(time_T, 3) + beta_coeffs[1]*pow(time_T, 2) + beta_coeffs[2]*time_T + beta_coeffs[3]
duct3 = np.linspace(2.6, 3.35, 10)

# b. Calculation of strength_ratio Rdyn for softening branch

strength_ratio_p = []

for i in range(len(duct3)):
    R = alpha3*duct3[i] + beta3
    strength_ratio_p.append(R)

# 4. For Strength Degradation Branch
# a. Calculation of parameters 'alpha', and 'beta'

alpha_coeffs = [-0.5954, 0.8170, -0.0919, 0.00182]
beta_coeffs = [0.7315, -3.7030, 4.3910, 1.1160]
alpha4 = alpha_coeffs[0]*pow(time_T, 3) + alpha_coeffs[1]*pow(time_T, 2) + alpha_coeffs[2]*time_T + alpha_coeffs[3]
beta4 = beta_coeffs[0]*pow(time_T, 3) + beta_coeffs[1]*pow(time_T, 2) + beta_coeffs[2]*time_T + beta_coeffs[3]
duct4 = np.linspace(3.35, 7, 10)

# b. Calculation of strength ratio 'Rdyn' for strength degradation branch

strength_ratio_d = []

for i in range(len(duct4)):
    R = alpha4*duct4[i] + beta4
    strength_ratio_d.append(R)


# 5. Fitting of branches

strength_ratio_R = []
fit_value = []
value1 = strength_ratio_h[0] - 1
fit_value.append(value1)
for i in range(len(strength_ratio_h)):
    if fit_value[0] < 0:
        strength_ratio = strength_ratio_h[i] + abs(fit_value[0])
    else:
        strength_ratio = strength_ratio_h[i] - abs(fit_value[0])
    strength_ratio_R.append(strength_ratio)
value2 = strength_ratio_s[0] - strength_ratio_R[-1]
fit_value.append(value2)
for i in range(len(strength_ratio_s)):
    if fit_value[1] < 0:
        strength_ratio = strength_ratio_s[i] + abs(fit_value[1])
    else:
        strength_ratio = strength_ratio_s[i] - abs(fit_value[1])
    strength_ratio_R.append(strength_ratio)
value3 = strength_ratio_p[0] - strength_ratio_R[-1]
fit_value.append(value3)
for i in range(len(strength_ratio_p)):
    if fit_value[2] < 0:
        strength_ratio = strength_ratio_p[i] + abs(fit_value[2])
    else:
        strength_ratio = strength_ratio_p[i] - abs(fit_value[2])
    strength_ratio_R.append(strength_ratio)
value4 = strength_ratio_d[0] - strength_ratio_R[-1]
fit_value.append(value4)
for i in range(len(strength_ratio_d)):
    if fit_value[3] < 0:
        strength_ratio = strength_ratio_d[i] + abs(fit_value[3])
    else:
        strength_ratio = strength_ratio_d[i] - abs(fit_value[3])
    strength_ratio_R.append(strength_ratio)
strength_ratio_R.insert(0, 0)

# Adding flat-line values to the list of strength ratios

i = 41
strength_ratio_r = strength_ratio_R.copy()
while i < 47:
    x = strength_ratio_R[-1]
    strength_ratio_r.append(x)
    i += 1


# 6. Making a list of all values of ductility to plot in a graph
duct = []
def arrlist(array):
    for x in array:
        duct.append(x)
arrlist(duct1)
arrlist(duct2)
arrlist(duct3)
arrlist(duct4)
duct.insert(0, 0)

# Adding the flat_line values to the list of ductility values

i = 41
x = duct[-1]
while i < 47:
    x += 1
    duct.append(x)
    x = x
    i +=1

# Plotting the points on graph

import matplotlib.pyplot as plt
plt.title('6 Storey Strong Infilled Frame')
plt.xlabel('Ductility, μ')
plt.ylabel('Strength Ratio, R')
plt.ylim(0, 5)
plt.plot(duct, strength_ratio_r, color = 'r')
plt.show()

