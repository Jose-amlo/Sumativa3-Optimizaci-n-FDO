import matplotlib.pyplot as plt
import numpy as np

maxPres_tv = 380
maxPres_diar_rev = 280
maxPres_diar_rad = 350

def satisfies_constraints(combination):
    # Restricción 1: combinación[0]*18 + combinación[1]*34 <= 380
    if combination[0] is not None and combination[1] is not None:
        if combination[0]*18 + combination[1]*34 > maxPres_tv:
            return False
    
    # Restricción 2: combinación[2]*7 + combinación[3]*10 <= 280
    if combination[2] is not None and combination[3] is not None:
        if combination[2]*7 + combination[3]*10 > maxPres_diar_rev:
            return False
    
    # Restricción 3: combinación[2]*7 + combinación[4]*2 <= 350
    if combination[2] is not None and combination[4] is not None:
        if combination[2]*7 + combination[4]*2 > maxPres_diar_rad:
            return False
    
    return True  # Si todas las restricciones se cumplen, retorna True

def backtrack(lists, combination, index, valid_combinations):
    if index == len(lists):
        if satisfies_constraints(combination):
            valid_combinations.append(combination.copy())
        return

    for element in lists[index]:
        combination[index] = element
        backtrack(lists, combination, index + 1, valid_combinations)
        combination[index] = None  # Backtrack

def find_combinations(lists):
    combination = [None] * len(lists)
    valid_combinations = []
    backtrack(lists, combination, 0, valid_combinations)
    return valid_combinations

# Define las dos funciones que usarán los valores de las combinaciones
def maximizar(combination):
    max_val = 75 * combination[0] + 94 * combination[1] + 55 * combination[2] + 60 * combination[3] + 30 * combination[4]
    return max_val  # Ejemplo: suma de los valores de la combinación

def minimizar(combination):
    min_val = 18 * combination[0] + 34 * combination[1] + 7 * combination[2] + 10 * combination[3] + 2 * combination[4]
    return min_val  # Ejemplo: valor máximo de la combinación

# Ejemplo de listas con las restricciones dadas
lists = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
]

# Encuentra las combinaciones válidas
valid_combinations = find_combinations(lists)

# Calcula los puntos para cada combinación usando las dos funciones
points = [(maximizar(comb), minimizar(comb)) for comb in valid_combinations]

# Convierte los puntos a un array numpy para facilitar la manipulación
points_np = np.array(points)

# Encuentra la frontera de Pareto
def pareto_frontier(points):
    # Ordena los puntos por la función de maximización (mayor a menor)
    sort_index = np.argsort(-points[:, 0])
    sorted_points = points[sort_index]

    frontier = [sorted_points[0]]  # El primer punto siempre es parte de la frontera

    # Itera sobre los puntos restantes para encontrar la frontera de Pareto
    for point in sorted_points[1:]:
        if point[1] <= frontier[-1][1]:  # Si el punto minimizado es menor o igual al último punto en la frontera
            frontier.append(point)

    return np.array(frontier)

pareto_front = pareto_frontier(points_np)

# Desempaqueta los puntos para graficar
x_vals, y_vals = zip(*points)
x_pareto, y_pareto = zip(*pareto_front)

# Grafica todos los puntos en azul
plt.scatter(x_vals, y_vals, color='blue', label='Posibles soluciones')

# Grafica la frontera de Pareto en rojo
plt.plot(x_pareto, y_pareto, color='red', label='Frontera de Pareto', linewidth=2)

plt.xlabel('Max Z1 = 75*x1 + 94*x2 + 55*x3 + 60*x4 + 30*x5')  # Función 1 en el eje x
plt.ylabel('Min Z2 = 18*x1 + 34*x2 + 7*x3 + 10*x4 + 2*x5')  # Función 2 en el eje y
plt.title('Grafico de resultado de las funciones y Frontera de Pareto')
plt.legend()
plt.show()