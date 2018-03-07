# Alek Westover
# The traveling salesman problem
# Greedy : shortest distance is always chosen
import travelingSalesmanSetup as tsSetup
import matplotlib.pyplot as plt
import matplotlib.animation as animation

num_towns = 17
towns = [i for i in range(0, num_towns)]
points = tsSetup.gen_pts(num_towns, 30.0)
pt_dists = tsSetup.gen_distances(points)
path = towns + [0]
points_order = [points[path[i]] for i in range(0, num_towns)] + [points[path[0]]]

fig = plt.figure()
picture = fig.add_subplot(1, 1, 1)
anim = animation.FuncAnimation(fig, tsSetup.update_plot, fargs=(points_order, picture), frames=num_towns + 2, interval=20)
plt.show()
