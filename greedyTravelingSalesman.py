# Alek Westover
# The traveling salesman problem
# Greedy : shortest distance is always chosen
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import travelingSalesmanSetup as tsSetup

num_towns = 30
towns = [i for i in range(0, num_towns)]
points = tsSetup.gen_pts(num_towns, 30.0)
pt_dists = tsSetup.gen_distances(points)
path = [0]
for i in range(0, num_towns-1):
    path.append(tsSetup.smallest_positive(pt_dists[path[-1]], path))
path.append(0)
best_points_order = [points[path[i]] for i in range(0, num_towns)] + [points[path[0]]]

fig = plt.figure()
picture = fig.add_subplot(1, 1, 1)
anim = animation.FuncAnimation(fig, tsSetup.update_plot, fargs=(best_points_order, picture), frames=num_towns + 2, interval=20)
plt.show()
