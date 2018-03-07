import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
fig.canvas.set_window_title('Dynamic Plot')
su = fig.add_subplot(111)
su.axis([-1, 1, -1, 1])
plt.ion()

for i in range(1000):
    y = 2*np.random.random()-1
    su.scatter(y, 0.5-y**2)
    plt.pause(0.4)

while True:
    plt.pause(0.05)
