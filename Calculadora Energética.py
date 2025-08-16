# Librerías
import math
import time as sleep
import matplotlib.pyplot as plt

# Variables
ing = 0 # Ingresos, cambiar para tener una inversión inicial
potenciaCentral = 500 # Potencia de la central en MW
t = 0 # Tiempo inicial

# Clase FuenteEnergia con atributos

class FuenteEnergia:
    def __init__(self, nombre, tconst, toperativo, emisiones, cconst, beneficio):
        self.nombre = nombre
        self.tconst = tconst 
        self.toperativo = toperativo
        self.emisiones = emisiones
        self.cconst = cconst
        self.beneficio = beneficio
        self.ling = [] # Lista de valores de ingreso
        self.lt = [] # Lista de valores de tiempo

nuclear = FuenteEnergia(
    nombre='Nuclear',
    tconst = 15,  # años de construcción
    cconst = -6,  # Euro/MWh
    beneficio = 10,  # Euro/MWh
    toperativo= 40,  # años de operación
    emisiones = 1  # g de CO2 por MWh
)

solar = FuenteEnergia(
    nombre='Solar',
    tconst = 5,
    cconst = -4,
    beneficio = 2,
    toperativo = 25,
    emisiones = 0.1 # g de CO2 por MWh
)

# LCOE 

# Ploteando gráficos

for t in range(0, nuclear.tconst + nuclear.toperativo): # 0 a tiempo final       
    if t < nuclear.tconst:
        ing = ing + nuclear.cconst * potenciaCentral
    elif t >= nuclear.tconst:
        ing = ing + nuclear.beneficio * potenciaCentral
    nuclear.ling.append(ing)
    nuclear.lt.append(t)

plt.plot(nuclear.lt, nuclear.ling, 'bo-')
plt.xlabel('Años')
plt.ylabel('Ingresos acumulados (Euro)')
plt.title('Ingresos acumulados de la central nuclear')
plt.show()

# Interfaz

    # Título

    # Gráfico

    # Texto