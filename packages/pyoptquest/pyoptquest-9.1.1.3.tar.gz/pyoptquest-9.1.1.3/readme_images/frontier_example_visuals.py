import numpy as np

from matplotlib import pyplot as plt

x = np.linspace(-2, 2)
obj1 = pow(x + 1, 2)
obj2 = pow(x - 1, 2)

# graph results
fig, ax = plt.subplots()
ax.set_title('Pareto Efficient Set Demo')
ax.set_xlabel('x')
ax.set_ylabel('objectives')
ax.plot(x, obj1, color='red')
ax.plot(x, obj2, color='blue')
ax.scatter(-1, 0, color='red', marker='X', s=150)
ax.scatter(1, 0, color='blue', marker='X', s=150)
ax.scatter(np.linspace(-1, 1, num=10), np.zeros(10), marker='+', color='green')
ax.legend(['objective_1', 'objective_2', 'objective_1 optimal solution', 'objective_2 optimal solution', 'Pareto Efficient Set'])
plt.show()
