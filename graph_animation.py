# Alek Westover
# Mat plot lib animations

import matplotlib.pyplot as plt
import matplotlib.animation as animation
# If you wanna read the csv like a cool kid import pandas as pd

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    pullData = open('C:/Users/alekw/Dropbox/Python/PythonDocuments/dynamic_data.csv').read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for line in dataArray:
        if len(line) > 1:
            x, y = line.split(',')
            xar.append(int(x))
            yar.append(int(y))
    ax1.clear()
    ax1.plot(xar, yar)

# ani = animation.FuncAnimation(fig, animate, interval=1000)
# plt.show()


print("Animation 2 starting up")


def update_plot(i, fig, scat):
    scat.set_offsets(([0, 1*i], [50, 1], [100, 1]))
    print("Frames: %d" %i)
    return scat


fig = plt.figure()
x = [0, 50, 100]
y = [0, 0, 0]

ax = fig.add_subplot(111)
ax.grid(True, linestyle='-', color='0.75')
ax.set_xlim([-50, 200])
ax.set_ylim([-50, 200])

scat = plt.scatter(x, y, c=x)
scat.set_alpha(0.8)

anim = animation.FuncAnimation(fig, update_plot, fargs=(fig, scat), frames=100, interval=100)

plt.show()


print("Animation 3 starting up")


def update_plot(i, pts, fig):
    fig.clear()
    return fig.plot([pts[0][i % 5], pts[1][0]], [pts[1][0], pts[1][1]])

fig = plt.figure()
x = [0, 50, 100, 1000, 10]
y = [0, 0, 0, 3, 4]

ax = fig.add_subplot(1, 1, 1)
ax.set_xlim([-50, 200])
ax.set_ylim([-50, 200])

anim = animation.FuncAnimation(fig, update_plot, fargs=([x, y], ax), frames=10, interval=100)

plt.show()

'''
data_file_path = 'C:/Users/alekw/Dropbox/Python/PythonDocuments/dynamic_data.csv'
df = pd.DataFrame({
    "x": [],
    "y": []
}, index=[])

df.to_csv(data_file_path)
time.sleep(100)
'''




fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
    data_file_path = 'C:/Users/alekw/Dropbox/Python/PythonDocuments/dynamic_data.csv'
    df = pd.DataFrame({
        "x": [best_points_order[j][0] for j in range(0, (i+1) % num_towns)],
        "y": [best_points_order[j][1] for j in range(0, (i+1) % num_towns)]
    }, index=towns)
    print(df, i)
    df.to_csv(data_file_path)
    data = pd.read_csv(data_file_path)
    ax1.clear()
    ax1.plot(data["x"], data["y"])

anim = animation.FuncAnimation(fig, animate, fargs=(fig, scat), frames=100, interval=100)
plt.show()
