import numpy as np
import matplotlib.pyplot as plt
import random
import math


plane_height = 100.0
plane_count = 100.0
plane_separation = 10.0
smearing_dist = 0.015

mean_residuals = []
max_err = []
min_err = []
stdev = []
irresolvable_prop = []


plane_rotations = np.linspace(-0.09, 0.09, 50)

gradients = []
track_angles = []

for i in plane_rotations:

    rotation_residuals = []
    irresolvable_count = 0

    for j in xrange(10000):

        gradient = ((random.random() - 0.5) * plane_height) / ((plane_count - 1.0) * plane_separation)
        y_intercept = (0.5 * plane_height) + (0.1 * plane_height * (random.random() - 0.5))

        gradients.append(gradient)
        
        track_angle = 0.0
        if (gradient > 0.0):
            track_angle = math.atan(gradient)
        else:
            track_angle = -math.atan(-gradient)
        
        track_angles.append(track_angle)

        y_true = y_intercept + (gradient * 0.0 * plane_separation)
        y_rotated = 0.0

        if (i < 0.0):
            y_rotated = y_true * (math.sin((math.pi / 2.0) - track_angle) / math.sin(i + track_angle + (math.pi / 2.0)))
        else:
            y_rotated = y_true * (math.sin((math.pi / 2.0) + track_angle) / math.sin((math.pi / 2.0) - i - track_angle))
        

        if ((((y_rotated - y_true) / smearing_dist) < 3.0) and (((y_rotated - y_true) / smearing_dist) > -3.0)):
            irresolvable_count += 1.0
            

        rotation_residuals.append(y_rotated - y_true)

    irresolvable_prop.append(irresolvable_count / 10000.0)
    print np.mean(rotation_residuals), min(rotation_residuals), max(rotation_residuals)

    mean_residuals.append(np.mean(rotation_residuals))
    max_err.append(max(rotation_residuals) - np.mean(rotation_residuals))
    min_err.append(np.mean(rotation_residuals) - min(rotation_residuals))
    stdev.append(np.std(rotation_residuals))

plt.errorbar(plane_rotations, mean_residuals, xerr=0.0, yerr=[min_err, max_err], color='b', fmt='.')
plt.errorbar(plane_rotations, mean_residuals, xerr=0.0, yerr=stdev, color='b', fmt='.', elinewidth=3)
plt.title("Residual Distributions Produced by Plane Rotations of Given Angles")
plt.xlabel("Plane Rotation / radians")
plt.ylabel("Hit Position Residual")
plt.grid()
plt.show()

plt.plot(plane_rotations, irresolvable_prop, 'b.')
plt.title("Proportion of Tracks with a Residual Produced by \n Rotation Within $3\sigma_{smear}$ of Zero")
plt.xlabel("Plane Rotation / radians")
plt.ylabel("Proportion of Residuals Within $3\sigma$ of Zero")
plt.ylim(0, 1.05)
plt.grid()
plt.show()

plt.hist(gradients, 50)
plt.title("Gradients")
plt.show()

plt.hist(track_angles, 50)
plt.title("Track Angles")
plt.show()
