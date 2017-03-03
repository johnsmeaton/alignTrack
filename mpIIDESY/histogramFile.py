import numpy as np
import matplotlib.pyplot as plt


rotation_residuals = []
plane_num = 0
rotation_angle = 0

with open("rotations.txt") as rotation_file:
    for line in rotation_file.readlines():

        items = line.split()

        if (len(items) == 0):
            continue

        try:
            plane_num = int(items[0])
            rotation_angle = float(items[1])
            rotation_residuals.append(float(items[2]))
        except Exception:
            continue


plt.hist(np.array(rotation_residuals), 20)
plt.title("Hit Distance Residuals Arising from Rotation of Plane " + str(plane_num) + " by " + str(rotation_angle) + " rad.")
plt.ylabel("Number of Tracks with Hit Residual")
plt.xlabel("Hit Distance Residual")
plt.show()
