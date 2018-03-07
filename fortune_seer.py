# Not quite working....
# Alek Westover
import random
import numpy as np


def gen_pts(quantity: int, std_deviation: float or int, env_size: list = [250, 250]) -> object:
    #  Two-d visualization uses and graphs these points,
    # the algorithm should work with any valid list of distances like the one generated with genDistances
    pts = []
    for i in range(0, quantity):
        pts.append([random.gauss(env_size[0] / 2, std_deviation), random.gauss(env_size[1] / 2, std_deviation)])
    return pts


def display_pts(pts, picture):
    #  Must have fig = plt.figure \ picture=fig.add_subplot(1,1,1) before this in real code
    #  Also must have plt.tight_layout() \ plt.show() Afterwords in real code
    picture.scatter([pt[0] for pt in pts], [pt[1] for pt in pts], color='red')


def gen_distances(points: list) -> list:  # kinda like an adjacency matrix, really redundant
    return [[np.linalg.norm(np.subtract(pt1, pt2)) for pt2 in points] for pt1 in points]


def remove_indices(total, marked_indices):
    out_array = []
    for i in range(0, len(total)):
        if i not in marked_indices:
            out_array.append(total[i])
    return out_array


def smallest_positive_index(array):
    the_min = np.inf
    the_index = 0
    for i in range(0, len(array)):
        if the_min > array[i] > 0:
            the_min = array[i]
            the_index = i
    return the_index


def next_best_two(usable, point_dists, cur_path):
    out_pairs = []
    for town in usable:
        out_pairs.append([pt_dists[cur_path[-1]][town], town])
    print(out_pairs)
    min_tot_dist = np.inf
    how_min = []
    for i in range(0, len(out_pairs)):
        prev_town = out_pairs[i][1]
        best_next_town = smallest_positive_index(point_dists[prev_town])  # should work b/c towns vals = towns indices
        out_pairs[i][0] += point_dists[prev_town][best_next_town]
        out_pairs[i][1] = [prev_town, best_next_town]
        if out_pairs[i][0] < min_tot_dist:
            how_min = out_pairs[i][1]
            min_tot_dist = out_pairs[i][0]
    return how_min


num_towns = 3
towns = [i for i in range(0, num_towns)]
points = gen_pts(num_towns, 30.0)
pt_dists = gen_distances(points)
path = [0]
for i in range(0, int(np.floor((num_towns-1)/2))):
    usable = remove_indices(towns, path)
    print(usable)
    next_two = next_best_two(usable, pt_dists, path)
    print(next_two)
    for j in range(0, 2):
        path.append(next_two[j])
path.append(0)

print(path)

