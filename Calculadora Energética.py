# Librerías
import math
import time as sleep
import matplotlib.pyplot as plt
plt.figure("Comparación de ingresos", figsize=(15, 8))

# Clase FuenteEnergia con atributos

class FuenteEnergia:
    def __init__(self, nombre, tconst, toperativo, emisiones, cconst, beneficio):

        # Atributos

        self.nombre = nombre
        self.tconst = tconst # años de construcción
        self.toperativo = toperativo # años de operación
        self.emisiones = emisiones # g de CO2 por MWh
        self.cconst = cconst # Euro/MWh en construcción
        self.beneficio = beneficio # Euro/MWh en operación

        # Listas vacías para almacenar y graficar

        self.ling = [] # Lista de valores de ingreso
        self.lt = [] # Lista de valores de tiempo

        # Función LCOE 

        self.lcoe = float(self.cconst * self.tconst + self.beneficio * self.toperativo) / (self.tconst + self.toperativo)                                   
                                    # Ingreso neto (ingresos menos gastos)                   # Tiempo total


# FUENTE ENERGÍA: VARIABLES. El usuario puede modificar los valores.

# Variables universales: 

ingorigen = 0 # Ingresos, cambiar para tener una inversión inicial
potenciaCentral = 500 # Potencia de la central en MW

# Variables generales:

nuclear = FuenteEnergia(
    nombre='Nuclear',
    tconst = 15, 
    cconst = -6,  
    beneficio = 10,
    toperativo= 40, 
    emisiones = 1
)

solar = FuenteEnergia(
    nombre='Solar',
    tconst = 5,
    cconst = -4,
    beneficio = 2,
    toperativo = 25,
    emisiones = 0.1
)

# Ploteando gráficos

def plot(ingorigen, potenciaCentral): 

    for fuente in [nuclear, solar]:  # Lista de fuentes de energía. Es necesario actualizarla.

        # Reset de variables

        t = 0
        ing = ingorigen
        fuente.ling = []
        fuente.lt = []
        
        # Tiempo 0 a final.

        for t in range(0, fuente.tconst + fuente.toperativo):
            if t < fuente.tconst:
                ing += fuente.cconst * potenciaCentral # Pérdida de construcción.
            else:
                ing += fuente.beneficio * potenciaCentral # Beneficio operativo.
                
            fuente.ling.append(ing)
            fuente.lt.append(t)

    plt.plot(fuente.lt, fuente.ling, label=fuente.nombre)
    plt.xlabel('Años')
    plt.ylabel('Ingresos acumulados (Euro)')
    plt.title('Ingresos acumulados de las centrales')
    plt.grid()
    plt.legend()
    plt.show()

# Interfaz

    # Título

    # Gráfico

    # Texto