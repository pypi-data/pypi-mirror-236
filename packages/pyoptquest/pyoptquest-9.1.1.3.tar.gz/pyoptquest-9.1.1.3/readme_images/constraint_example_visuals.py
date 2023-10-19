import numpy as np

from matplotlib import pyplot as plt

x = np.linspace(-2, 2)
objective_y = x**2
constraint = 0.1 * x + 1

# graph results
fig, ax = plt.subplots()
ax.set_title('Constraint Demo')
ax.set_xlabel('x')
ax.plot(x, objective_y, color='green')
ax.plot(x, constraint, color='blue')
ax.fill_between(x, constraint, 4, color='lightblue')
ax.scatter(-0.9573366917472107, 0.9164935413654939, marker='X', color='green', s=150)
ax.legend(['objective_y', 'constraint boundary', 'feasible region', 'optimal solution'])
plt.show()
