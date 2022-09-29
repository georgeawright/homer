import math

from matplotlib import pyplot

x = [i / 100 for i in range(101)]
y = [1 / (1 + math.e ** -(10 * x - 5)) for x in x]

figure = pyplot.figure()
ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(x, y)
ax.set_title("sigmoid")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_xticks([i / 10 for i in range(11)])
ax.set_yticks([i / 10 for i in range(11)])

for i in range(len(x)):
    if x[i] in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
        print(f"{x[i]}: {y[i]}")

pyplot.savefig(f"sigmoid.png")
