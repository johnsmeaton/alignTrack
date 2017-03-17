import numpy as np
import matplotlib.pyplot as plt
import random
import math

# Detector geometry
plane_height = 100.0
plane_count = 100.0
plane_separation = 10.0
plane_x_start = 10.0

# Intrinsic resolution for planes
smearing_dist = 0.015

# For plotting
mean_residuals = []
max_err = []
min_err = []
stdev = []
irresolvable_prop = []

# Array of plane rotation angles to examine
plane_rotations = np.linspace(-0.09, 0.09, 50)

# For sanity plotting
gradients = []
track_angles = []

# Iterate over plane rotations
for i in plane_rotations:

    # List of calculated residuals, and the number of residuals within smearing distance
    rotation_residuals = []
    irresolvable_count = 0

    # Generate 10,000 tracks
    for j in xrange(10000):

        # Calculate random gradient and intercept for track 
        gradient = ((random.random() - 0.5) * plane_height) / ((plane_count - 1.0) * plane_separation)
        y_intercept = (0.5 * plane_height) + (0.1 * plane_height * (random.random() - 0.5))

        # Calculate angle of elevation for track
        track_angle = math.atan(gradient)

        # Calculate x-position at centre of detector, and y-position of track at this point
        x = plane_x_start + ((plane_count / 2.) + 0.5) * plane_separation
        y_true = y_intercept + (gradient * x)

        # Calculate recorded y-position from rotation of plane
        y_rotated = y_true * (math.sin((math.pi / 2.0) + track_angle) / math.sin(i + track_angle + (math.pi / 2.0)))
                
        # Check if residual within smearing bounds, and increment number of irresolvable hits if so
        if ((((y_rotated - y_true) / smearing_dist) < 1.0) and (((y_rotated - y_true) / smearing_dist) > -1.0)):
            irresolvable_count += 1.0
            
        # Append residual distance to list
        rotation_residuals.append(y_rotated - y_true)

    # Calculate proportion of irresolvable hits, and normalise this
    irresolvable_prop.append(irresolvable_count / 10000.0)
    
    # Add various stats of residual distribution to list
    mean_residuals.append(np.mean(rotation_residuals))
    max_err.append(max(rotation_residuals) - np.mean(rotation_residuals))
    min_err.append(np.mean(rotation_residuals) - min(rotation_residuals))
    stdev.append(np.std(rotation_residuals))

# Plot hit position residual distributions at different plane rotation angles
plt.errorbar(plane_rotations, mean_residuals, xerr=0.0, yerr=[min_err, max_err], color='b', fmt='.')
plt.errorbar(plane_rotations, mean_residuals, xerr=0.0, yerr=stdev, color='b', fmt='.', elinewidth=3)
plt.title("Residual Distributions Produced by Plane Rotations of Given Angles")
plt.xlabel("Plane Rotation / radians")
plt.ylabel("Hit Position Residual")
plt.grid()
plt.show()

# Plot proportion of irresolvable hits 
plt.plot(plane_rotations, irresolvable_prop, 'b.')
plt.title("Proportion of Tracks with a Residual Produced by \n Rotation Within $3\sigma_{smear}$ of Zero")
plt.xlabel("Plane Rotation / radians")
plt.ylabel("Proportion of Residuals Within $3\sigma$ of Zero")
plt.ylim(0, 1.05)
plt.grid()
plt.show()
