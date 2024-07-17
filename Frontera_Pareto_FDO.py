import matplotlib.pyplot as plt
import numpy as np

maxPres_tv = 380
maxPres_diar_rev = 280
maxPres_diar_rad = 350

def satisfaccion_restricciones(combinacion):
    # Restricción 1: combinación[0]*18 + combinación[1]*34 <= 380
    if combinacion[0] is not None and combinacion[1] is not None:
        if combinacion[0]*18 + combinacion[1]*34 > maxPres_tv:
            return False
    
    # Restricción 2: combinación[2]*7 + combinación[3]*10 <= 280
    if combinacion[2] is not None and combinacion[3] is not None:
        if combinacion[2]*7 + combinacion[3]*10 > maxPres_diar_rev:
            return False
    
    # Restricción 3: combinación[2]*7 + combinación[4]*2 <= 350
    if combinacion[2] is not None and combinacion[4] is not None:
        if combinacion[2]*7 + combinacion[4]*2 > maxPres_diar_rad:
            return False
    
    return True  # Si todas las restricciones se cumplen, retorna True

def backtrack(listas, combinacion, index, combinaciones_factibles):
    if index == len(listas):
        if satisfaccion_restricciones(combinacion):
            combinaciones_factibles.append(combinacion.copy())
        return

    for e in listas[index]:
        combinacion[index] = e
        backtrack(listas, combinacion, index + 1, combinaciones_factibles)
        combinacion[index] = None  # Backtrack

def buscar_combinaciones(listas):
    combinacion = [None] * len(listas)
    combinaciones_factibles = []
    backtrack(listas, combinacion, 0, combinaciones_factibles)
    return combinaciones_factibles

# Define las dos funciones que usarán los valores de las combinaciones
def maximizar(combinacion):
    max_val = 75 * combinacion[0] + 94 * combinacion[1] + 55 * combinacion[2] + 60 * combinacion[3] + 30 * combinacion[4]
    return max_val  # Ejemplo: suma de los valores de la combinación

def minimizar(combinacion):
    min_val = 18 * combinacion[0] + 34 * combinacion[1] + 7 * combinacion[2] + 10 * combinacion[3] + 2 * combinacion[4]
    return min_val  # Ejemplo: valor máximo de la combinación

# Ejemplo de listas con las restricciones dadas
listas = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25],
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
]

# Encuentra las combinaciones válidas
combinaciones_factibles = buscar_combinaciones(listas)

# Calcula los puntos para cada combinación usando las dos funciones
puntos = [(maximizar(comb), minimizar(comb)) for comb in combinaciones_factibles]

# Convierte los puntos a un array numpy para facilitar la manipulación
puntos_np = np.array(puntos)

# Encuentra la frontera de Pareto
def frontera_pareto(puntos):
    # Ordena los puntos por la función de maximización (mayor a menor)
    ord_index = np.argsort(-puntos[:, 0])
    puntos_ord = puntos[ord_index]

    frontera = [puntos_ord[0]]  # El primer punto siempre es parte de la frontera

    # Itera sobre los puntos restantes para encontrar la frontera de Pareto
    for p in puntos_ord[1:]:
        if p[1] <= frontera[-1][1]:  # Si el punto minimizado es menor o igual al último punto en la frontera
            frontera.append(p)

    return np.array(frontera)

pareto_front = frontera_pareto(puntos_np)

# Desempaqueta los puntos para graficar
x_vals, y_vals = zip(*puntos)
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
