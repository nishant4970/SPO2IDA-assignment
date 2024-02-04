This assignment file contains the	Python code to create a %50 fractile of the IDA responses of the extended SPO2IDA model for a 6-storey strong infilled frame which is based on the extension provided in the study by Nafeh, A. M. B. et al. (2020).

The code is explained here:

Assumptions: 

I have assumed the value of T* to be equal to the first mode period of vibration which is 0.41 seconds for a 6-story strong infilled frame.

The values of ductility are assumed based on Figure 17 provided in the paper being reviewed which are 1, 2.35, 2.6, 3.35, and 7 corresponding to points A, B, C, D, and E of Fig. 10 in the paper.

The rest of the data and analytical formulas used in this code are obtained from the information given in the paper.
(Note: The analytical formula in the paper used to calculate α1 and β1 is different from the formula used in the GitHub files. The formula provided in the paper gives inappropriate values for the parameters.)

Explanation: 

It is easier to understand the code by dividing it into three steps:

Step 1: Calculation of parameters and strength ratio using the analytical equations given in the paper
The Numpy library is used to create an array containing 10 equally spaced values of ductility within the given range of each branch.

The values of coefficients obtained from the paper are defined in the form of lists for each branch. Using the for loop that iterates until the value of i is equal to one less than the length of the list containing values of aα1, the value of α1 and β1 is calculated. By employing formula 12, the strength ratio for each value of ductility is calculated using a for loop. Each value of the strength ratio is added to the list strength_ratio using the append() method.

This process is repeated for all the branches. The values of the strength ratios for hardening, softening, plateau and strength degradation branches are added to the lists strength_ratio_h, strength_ratio_s, strength_ratio_p, and strength_ratio_d respectively.

Step 2: Fitting of the branches so that the continuous curve is obtained when plotting
First, the difference in the first value of the subsequent branch and the last value of the preceding branch is calculated. To correctly fit the branches, utmost care should be taken whether the last value of the preceding branch is the old value or the updated value. Here updated value refers to the value which has been fitted.

For example, for hardening branch:
First, the correction value defined by variable ‘value1’ is calculated by subtracting 1 from the first value of the strength ratio in the hardening branch. If this value is negative, it means that the first value of the strength ratio is less than 1 and hence the correction is added to it. Accordingly, all the values of the strength ratio in this branch are updated by adding the correction. These updated values are added to the variable ‘strength_ratio_R’.

Now, to calculate the correction value for the softening branch, the last value of the list ‘strength_ratio_R’ is subtracted from the first value of the strength ratio in the softening branch. In this way, a continuous curve is formed. This process is repeated until the strength degradation branch and all the updated values of the strength ratio are added to the variable ‘strength_ratio_R’.

Finally, the variable list ‘strength_ratio_R’ is copied to another variable ‘strength_ratio_r’ where the flat-line points are added. Similarly, all the values of ductility along with flat-line points are added to the list ‘duct’.

Step 3: Plotting the values of strength ratios vs ductility to obtain the required curve.
Matplotlib library is used to plot the graph between strength ratios and ductility.
