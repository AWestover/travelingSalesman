# Alek Westover
# full ai for salesman problem
# WARNING SOMETHING IS WRONG WITH THIS PROGRAM :( it should do a lot better than it does, use greedySwitcher until this is fixed
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import random
import numpy as np
import time
import pygame
import sys


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


def combiner(first: list, after: list) -> list:
    # For the perm thing, combiner takes a list and then puts every possible combination of the next 2 things after it
    if len(after) == 0:
        return first
    out = []
    for i in range(0, len(after)):
        out.append(first+[after[i]])
    return out


def missing(total: list, already: list) -> list:
    missed = []
    for element in total:
        if total.count(element) > already.count(element) + missed.count(element):
            missed.append(element)
    return missed


def permutations(array:  list) -> list:
    arrayed_array = [[array[i]] for i in range(0, len(array))]
    print(arrayed_array)
    out_perms = arrayed_array
    for i in range(0, len(array)-1):
        j_len = len(out_perms)
        for j in range(0, j_len):
            combined = combiner(out_perms[0], missing(array, out_perms[0]))
            for k in range(0, len(combined)):
                out_perms.append(combined[k])
            out_perms.pop(0)
    return out_perms


def cyclic_permutations(array: list) -> list:
    out_perms = [[array[0]]]
    for i in range(0, len(array)-1):
        j_len = len(out_perms)
        for j in range(0, j_len):
            combined = combiner(out_perms[0], missing(array, out_perms[0]))
            for k in range(0, len(combined)):
                out_perms.append(combined[k])
            out_perms.pop(0)
    return out_perms


def pt_dist(pt1, pt2):
    return np.linalg.norm([pt1[i] - pt2[i] for i in range(0, len(pt1))], axis="0")


def path_dist(path: list, pt_dists: list) -> float or int:
    total_dist = 0
    for i in range(0, len(path)-1):
        total_dist += pt_dists[path[i]][path[i+1]]
    total_dist += pt_dists[path[-1]][path[0]]
    return total_dist


def remove_indices(array: list, indices_to_remove: list) -> list:
    out_array = []
    for i in range(0, len(array)):
        if i not in indices_to_remove:
            out_array.append(array[i])
    return out_array


def smallest_positive_index(array: list, used: list) -> int:  # used lists indices that are not allowed
    usable = remove_indices(array, used)
    min_val = np.inf
    for element in usable:
        if min_val > element > 0:
            min_val = element
    if min_val in array:
        return array.index(min_val)
    else:
        print("AGH ERROR")
        return None


def update_plot(i, pts, figure):
    if i == 0:
        time.sleep(0.5)
    plt.cla()
    figure.set_title("Towns and  Routes")
    figure.set_ylabel("y")
    figure.set_xlabel("x")
    plt.tight_layout()
    display_pts(pts, figure)
    figure.plot([pts[j][0] for j in range(0, i)], [pts[k][1] for k in range(0, i)])


def index_switcher(path, i, j):
    out_path = path[:]
    out_path[i] = path[j]
    out_path[j] = path[i]
    return out_path


def switcher(path, num_towns, pt_dists):
    for i in range(0, num_towns-1):
        for j in range(0, num_towns-1):
            seg1 = [path[i], path[i+1]]
            seg2 = [path[j], path[j+1]]
            if seg1[0] != seg2[0] and seg1[0] != seg2[1] and seg2[0] != seg1[1]:
                # no mods necessary because must go back to start, ie len(path) = num_towns + 1
                # find more efficient distance calculations (below is wrong, but close i think...)
                # original_dist = pt_dists[seg1[0]][seg1[1]] + pt_dists[seg2[0]][seg2[1]]
                # new_dist = pt_dists[seg1[0]][seg2[1]] + pt_dists[seg2[0]][seg1[1]]
                original_dist_stupid = path_dist(path, pt_dists)
                proposed_path = index_switcher(path, i+1, j+1)
                new_dist_stupid = path_dist(proposed_path, pt_dists)
                if original_dist_stupid > new_dist_stupid:
                    path = proposed_path
    return path


def best_next_two(all_towns, cur_path, all_pt_dists):
    out_dists = []  # Also gives the path that achieves the distance
    for a_town in all_towns:
        if a_town not in cur_path:
            new_first_dist = all_pt_dists[a_town][cur_path[-1]]
            out_dists.append([new_first_dist, [a_town]])
    min_cum_dist = np.inf
    optimal_sequence = []
    for town_dist_pair in out_dists:
        prev_town = town_dist_pair[1][0]
        next_best_town = smallest_positive_index(all_pt_dists[prev_town], cur_path + [prev_town])
        town_dist_pair[1] = [prev_town, next_best_town]
        town_dist_pair[0] += all_pt_dists[next_best_town][prev_town]  # += later
        if town_dist_pair[0] < min_cum_dist:
            min_cum_dist = town_dist_pair[0]
            optimal_sequence = town_dist_pair[1]
    for out_disti in out_dists:
        for not_allowed in cur_path:
            if not_allowed in out_disti[1]:
                print("PROBLEM")
    return optimal_sequence


def validInput(question, condition):
    if type(condition) == type:
        uin=None
        while type(uin) != condition:
            uin = input(question)
            try:
                uin = condition(uin)
            except:
                pass
    elif type(condition) == list:
        uin = None
        for i in range(0, len(condition)):
            if type(condition[i])==int or type(condition[i])==float or type(condition[i])==bool:
                condition[i]=str(condition[i])
        while uin not in condition:
            uin = input(question)
    else:
        print("Please carefully input your answer to comply with the following condition : "+condition)
        uin = input(question)
    return uin


def arrayProd(array):
    result=1  # Rerturns 1 for null set convinentially enough
    for i in range(0,len(array)):
        result *= array[i]
    return result


def pFactorization(x):
    primeFactors=[]
    for i in range(2,x+1):
        if(x%i==0):
            primeFactors.append(i)
            xperifactors=pFactorization(int(x/i))
            for j in range(0,len(xperifactors)):
                primeFactors.append(xperifactors[j])
            break
        elif(i==x):
            primeFactors.append(i)
    return(primeFactors)


def nthPlace(x,n):
    return(int(np.floor((x%10**n)/10**(n-1))))


def factorial(n):
    if(n>1):
        result=n*factorial(n-1)
    if(n<=1):
        result=1
    return result


def ncr(n,r):
    rReal=r
    if r<n/2:
        rReal=n-r
    ncr=1
    for m in range(1,n-rReal+1):
        ncr=ncr*(n-m+1)/(n-m-rReal+1)
    return ncr


def primeChecker(n):   # sketchy
    x=int(n)
    lastVal=int(np.ceil(np.linalg.norm(x)))
    if(x==2 or x==3):
        return 1
    elif(x==4):
        return 0
    elif(x<=1):
        return 0
    elif(x>4):
        for i in range(2,lastVal+1):
            if((x/i).is_integer()):
                return 0
                break
            if(i+1==lastVal):
                return 1


def dydx(f,x,h):
    return (f(x+h)-f(x))/h


def hi(name):
    print("Hello "+str(name)+".\nThe program is now running.")


def degToRad(th,pi):
    return th*pi/180


def radToDeg(th,pi):
    return th*180/pi


# Actual program
num_towns = int(validInput("How many cities will you be visiting today?\n", int))  # parity doesn't matter
if num_towns < 2:
    num_towns = 3  # Ya know what, Im not in the mood...
towns = [i for i in range(0, num_towns)]
points = gen_pts(num_towns, 30.0)
pt_dists = gen_distances(points)
path = [0]
for i in range(0, int(num_towns/2) - 1):
    path += best_next_two(towns, path, pt_dists)
time.sleep(1)
for town in towns:
    if town not in path:
        path.append(smallest_positive_index(pt_dists[path[-1]], path))   # doesn't make sense, but works since values of towns are the same a s the indices of towns
path.append(0)
path = switcher(path, num_towns, pt_dists)
greedy_points_order = [points[path[i]] for i in range(0, num_towns)] + [points[path[0]]]
print("This is the path I would advise you take between the " + str(num_towns) + " semi random points I chose.\n")
print(greedy_points_order)
print("It is not necessarily the best path if you have a long trip, but I think it is pretty good.\n")
print("With units of cool-Aleks the distance it will take to travel this is about " + str(path_dist(path, pt_dists)))

fig = plt.figure()
picture = fig.add_subplot(1, 1, 1)
anim = animation.FuncAnimation(fig, update_plot, fargs=(greedy_points_order, picture), frames=num_towns + 2, interval=20)
plt.show()

pygame.init()
window = pygame.display.set_mode((640, 600))
pygame.mixer.music.load("C:/Users/alekw/Dropbox/Python/PythonImagesAndVideos/AlekDuDuDu.mp3")
pygame.mixer.music.play(-1, 0.0)
circle = pygame.draw.circle(window, (50, 30, 90), (90, 30), 16, 5)
window.blit(window, circle)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()

