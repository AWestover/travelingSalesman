# Alek Westover
# The traveling salesman problem
# Brute force : check sum of each perms distance and take smallest
# Convention : towns are point 0, point 1, ect as represented in my nice little array
import travelingSalesmanSetup as tsSetup
import matplotlib.pyplot as plt
import matplotlib.animation as animation

num_towns = 7
towns = [i for i in range(0, num_towns)]
points = tsSetup.gen_pts(num_towns, 30.0)
paths = tsSetup.cyclic_permutations(towns)
dists = [tsSetup.not_fast_path_dist(paths[i], points) for i in range(0, len(paths))]
best_path = paths[dists.index(min(dists))]
best_points_order = [points[best_path[i]] for i in range(0, num_towns)] + [points[best_path[0]]]
print("The minimum path distance is " + str(min(dists)))
print("That path is " + str(best_path))
print("Which is achieved  via these points in the following order")
print(best_points_order)

fig = plt.figure()
picture = fig.add_subplot(1, 1, 1)
anim = animation.FuncAnimation(fig, tsSetup.update_plot, fargs=(best_points_order, picture), frames=num_towns + 2, interval=100)
plt.show()

