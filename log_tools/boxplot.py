from matplotlib import pyplot

figure = pyplot.figure()
ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])

ax.set_title("Urgency of Codelets Run")
ax.set_xlabel("Run")
ax.set_ylabel("Urgency")

bp = ax.boxplot([1, 2, 3, 4, 5], 0, "")

pyplot.savefig(f"boxplot.png")
