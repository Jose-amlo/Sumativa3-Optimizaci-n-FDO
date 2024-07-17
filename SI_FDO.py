# --------- SUMATIVA 3 + TAREA : FORMULACION Y RESOLUCION  --------- #
# --------- DE UN LP CON FITNESS DEPENDENT OPTIMIZER (FDA) --------- #
# ------------------------------------------------------------------ #
# -----------------------   Jose Molina     ------------------------ #
# ----------------------- Ricardo Valencia  ------------------------ #

import random as rnd
import numpy as np
import math
import csv
import os

class Problem:
  def __init__(self):
    # Inicializacion de valores referentes al problema y sus restricciones
    self.dimension = 5
    self.maxPres_tv = 380
    self.maxPres_diar_rev = 280
    self.maxPres_diar_rad = 350
    self.max_anuncios = [15,10,25,4,30]

  def eval(self, x):
    # Inicializacion de las mejores soluciones encontradas en la maximizacion y minimizacion de las funciones objetivos (utilizando Simplex y B&B)
    mejorSol_max = 3922
    mejorSol_min = 0

    # De manera predeterminada las ponderaciones de la maximizacion y minimizacion son 0.5, se puede ajustar bajo propio criterio siempre que su suma iguale a 1  
    pondValor = 0.5
    pondCosto = 0.5

    # Almacenamiento del resultado de la funcion objetivo escalarizada (scalarizing)
    resultado = ((75*x[0]+94*x[1]+55*x[2]+60*x[3]+30*x[4])/mejorSol_max)*pondValor+((1500-(18*x[0]+34*x[1]+7*x[2]+10*x[3]+2*x[4]))/1500-mejorSol_min)*pondCosto
    return resultado

  def check(self, x):
    # Revision del cumplimiento de las restricciones del problema
    costo_tv = 18*x[0] + 34*x[1]
    costo_diar_rev = 7*x[2] + 10*x[3]
    costo_diar_rad = 7*x[2] + 2*x[4]
    # Confirmar que no se exceda la cantidad maxima de anuncios
    if any(x[i] > self.max_anuncios[i] for i in range(self.dimension)):
      return False
    # Confirmar que la cantidad de anuncios no sea un valor negativo
    if any(x[i] < 0 for i in range(self.dimension)):
      return False
    # Confirmar que no se exceda el presupuesto establecido para anuncios de TV
    if costo_tv > self.maxPres_tv:
      return False
    # Confirmar que no se exceda el presupuesto establecido para anuncios en diarios o revistas
    if costo_diar_rev > self.maxPres_diar_rev:
      return False
    # Confirmar que no se exceda el presupuesto establecido para anuncios en diarios y radio
    if costo_diar_rad > self.maxPres_diar_rad:
      return False
    # Correcto cumplimiento de todas las restricciones
    else:
      return True

class Abeja(Problem):
  def __init__(self):
    self.p = Problem()
    self.x = []
    # Inicializacion del parametro "pace" de cada variable de Abeja  
    self.pace = [0] * self.p.dimension

    # Inicializacion de los valores de las variables (Bees - Abejas)
    for j in range(self.p.dimension):
      self.x.append(rnd.randint(0,self.p.max_anuncios[j]))

  def isFeasible(self):
    return self.p.check(self.x)

  def isBetterThan(self, g):
    return self.fit() > g.fit() # En este caso se busca maximizar la funcion

  def fit(self):
    return self.p.eval(self.x)

  def move(self, g, fw):
    for j in range(self.p.dimension):
      r = np.random.uniform(-1,1) # Determinacion del valor aleatorio entre -1 y 1 "r" presente en las formulas (3), (4) y (5) de FDO
      if (fw < 1) and (fw > 0):
        # Calculo de pace en base a la formula (5) de FDO
        if r >= 0:
          pace = (self.x[j]-g.x[j]) * fw
        # Calculo de pace en base a la formula (4) de FDO
        else:
          pace = (self.x[j]-g.x[j])* -fw
      # Calculo de pace en base a la formula (3) de FDO
      else:
        pace = self.x[j] * r
      
      self.pace[j] = pace # Almacenamiento de pace de la posicion de la abeja

      pos_nueva = self.x[j] + pace # Calculo de la nueva posicion de la abeja en base al pace calculado
      self.x[j] = self.convSigmoide(pos_nueva, j) # Ajuste de la posicion con la funcion sigmoide

  def move_pace_anterior(self, ant):
    # Movimiento de la abeja con el "pace" anterior
    for j in range(self.p.dimension):
      pos_nueva = self.x[j] + ant.pace[j]
      self.x[j] = self.convSigmoide(pos_nueva, j)

  def convSigmoide(self, x, j):
    rango_valores = self.p.max_anuncios[j] + 1  # Cantidad de posibles valores que puede tomar la variable
    min_valor = self.p.max_anuncios[j]*-1       # Valor minimo que puede tomar la nueva posicion
    max_valor = self.p.max_anuncios[j]*2        # Valor maximo que puede tomar la nueva posicion
    punto_medio = (min_valor+max_valor)/2       # Valor medio entre min_valor y max_valor (para posterior ajuste de sigmoide)

    k = math.log(99)/(max_valor-min_valor)              # Constante para ajuste de sigmoide
    div_partes = np.linspace(0,1,rango_valores+1)[1:]   # División de distancia entre 0 y 1 (corte) en la cantidad de valores que puede tomar la variable

    posiciones_sigmoide = {indice: valor for indice, valor in enumerate(div_partes)}  # Asignacion del valor de las posiciones en base a los cortes realizados
                                                                                      # Ej. (4: 0,456) el corte 0,456 representa la posicion "4"
    
    sigmoide = 1 / (1 + math.pow(math.e, -k*(x-punto_medio))) # Calculo de la sigmoide ajustada con valores desde min_valor a max_valor

    # Comparacion del valor entregado por la sigmoide con los cortes realizados
    for posConvert, valor in posiciones_sigmoide.items():
      if sigmoide < valor:
        return posConvert # si el valor es menor al corte, la posicion toma su valor representativo
  
  def __str__(self) -> str:
    return f"fit:{self.fit()} x:{self.x}"

  def copy(self, a):
    self.x = a.x.copy()

class FDO:
  def __init__(self):
    self.maxIter = 30
    self.nAbejas = 50
    self.abejas = []
    self.g = Abeja()

  def solve(self):
    self.initRand()
    self.evolve()

  def initRand(self):
    for i in range(self.nAbejas):
      while True:
        a = Abeja()
        if a.isFeasible():
          if i == 0:
            self.g.copy(a)
          else:
            if a.isBetterThan(self.g):
              self.g.copy(a)
          break
      self.abejas.append(a)

    self.toConsole()

  def evolve(self):
    t = 1
    if os.path.exists('resultados.csv'):
      os.remove('resultados.csv')
  
    while t <= self.maxIter:
      for i in range(self.nAbejas):
        a = Abeja()     # Inicializacion de la abeja "despues" de cambiar de posicion
        a_ant = Abeja() # Inicialización de la abeja "antes" de cambiar de posicion
        while True:
          a.copy(self.abejas[i])
          a_ant.copy(self.abejas[i])
          wf = np.random.random()           # Determinacion del factor de peso (weight factor) para la formula (2) de FDO (valor entre 0 y 1)
          
          fw = (a.fit()/self.g.fit()) - wf  # Calculo de fitness weight de la formula (2) de FDO
                                            # Como es un problema de maximizacion, el fitness de la posicion actual es dividido por el fitness de la mejor solucion
          a.move(self.g, fw)
          if a.isFeasible():
            # Identificacion de si la nueva posicion de la abeja es mejor que la mejor solucion hasta el momento
            if a.isBetterThan(self.g):
              self.g.copy(a)
            # Calculo de nueva posicion de la abeja con los valores "pace" pasadas
            else:
              a.move_pace_anterior(a_ant)
              # Identificacion de si la nueva posicion de la abeja es mejor que la mejor solucion hasta el momento
              if a.isFeasible():
                if a.isBetterThan(self.g):
                  self.g.copy(a)
                # En caso de no serlo, la abeja no se mueve
                else:
                  a = a_ant
            break
        self.abejas[i].copy(a)

      self.toConsole()
      self.paso_csv(t)
      t = t + 1

  def paso_csv(self, t):
    with open('resultados.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([t, self.g.x, self.g.fit()])
  
  def toConsole(self):
    print(f"{self.g}")

try:
  FDO().solve()
except Exception as e:
  print(f"{e} \nCaused by {e.__cause__}")