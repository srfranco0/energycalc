# Librerías
import math
import matplotlib.pyplot as plt
# PyQt5

# --------------------------- Clase FuenteEnergia con atributos -----------------------------------#

class FuenteEnergia:
    def __init__(self, nombre, tconst, toperativo, emisiones, cconst, beneficio): #cmant, ccomb):

        # Atributos

        self.nombre = nombre
        self.tconst = tconst # años de construcción
        self.toperativo = toperativo # años de operación

        self.cconst = cconst # Euros por año de construcción por MWh (negativo, ya que es pérdida)
        #self.cmant = cmant # Costo de mantenimiento por año
        #self.ccomb = ccomb # Costo de combustible por año

        self.beneficio = beneficio # Euro/MWh por año en operación

        self.emisiones = emisiones # g de CO2 por MWh
        # Listas vacías para almacenar y graficar

        self.ling = [] # Lista de valores de ingreso
        self.lt = [] # Lista de valores de tiempo


#---------------------------------- FUENTE ENERGÍA: VARIABLES. El usuario puede modificar los valores. ----------------------------------#

# Variables universales: 

ingorigen = 0 # Ingresos, cambiar para tener una inversión inicial
potenciaCentral = 500 # Potencia de la central en MW
potenciaTermica = 1000 # Potencia solar en MW/m^2
c = 2.99792*(10**8) # Velocidad de la luz

# Variables de cálculo
areaFoto = potenciaCentral / potenciaTermica
resnucleares = potenciaCentral * c ** -2
# Dimensiones embalse !!!CALCULAR!!!

# Variables específicas de cada fuente de energía:

nuclear = FuenteEnergia(
    nombre='Nuclear',
    tconst = 15, 
    cconst = -6,  
    beneficio = 10,
    toperativo= 40, 
    emisiones = 1,
)

solar = FuenteEnergia(
    nombre='Solar',
    tconst = 10,
    cconst = -2,
    beneficio = 5,
    toperativo = 40,
    emisiones = 2,
)

termica = FuenteEnergia(
    nombre='Térmica',
    tconst = 5,
    cconst = -10,
    beneficio = 5,
    toperativo = 10,
    emisiones = 10,
)

hidro = FuenteEnergia(
    nombre='Hidráulica',
    tconst = 15,
    cconst = -3,
    beneficio = 1,
    toperativo = 60,
    emisiones = 1,
)

#-----------------------------------------------------------------FUNCIONES-------------------------------------------------------------#

# Función LCOE 
def lcoe(self):
    lcoe = (self.cconst * self.tconst + self.beneficio * self.toperativo) / (self.tconst + self.toperativo)                               
                        # Ingreso neto (ingresos menos gastos)                      # Tiempo total
    return round(lcoe, 3)

# Función de cálculo de variables concretas

def recalcular():
    areaFoto == potenciaCentral / potenciaTermica # Área en m^2
    resnucleares == potenciaCentral * c **-2 # Residuos en kg

# Función de ploteo de gráficos

def plotall(): 

    plt.figure("Comparación de ingresos", figsize=(15, 8)) # Tamaño y título

    for fuente in [nuclear, solar, termica, hidro]:  # !!!ACTUALIZAR!!!

        # Reset de variables
        t = 0
        ing = ingorigen
        fuente.ling = []    
        fuente.lt = []
        fuente.ling.append(t)
        fuente.lt.append(ing)

        # Tiempo 0 a final.
        for t in range(1, fuente.tconst + fuente.toperativo):
            if t < fuente.tconst:
                ing += fuente.cconst * potenciaCentral # Pérdida de construcción.

            elif t == fuente.tconst:
                ing += fuente.cconst * potenciaCentral
                plt.text(t, 
                ing, str(ing) + " €", va = "bottom", ha = "center", fontstyle = "italic") # Texto de pérdida máxima

            else:
                ing += fuente.beneficio * potenciaCentral # menos costos!!!!!!! # Beneficio operativo.
                
            fuente.ling.append(ing)
            fuente.lt.append(t)

        # Formato
        plt.xlabel('Años')
        plt.ylabel('Ingresos acumulados (Euro)')
        plt.title('Ingresos acumulados de las centrales')
        plt.grid()
        plt.plot(fuente.lt, fuente.ling, label=fuente.nombre)
        plt.xlim(0, max(nuclear.tconst + nuclear.toperativo, solar.tconst + solar.toperativo, termica.tconst + termica.toperativo, hidro.tconst + hidro.toperativo) + 1)
        plt.legend()
    plt.show()

def plotlcoe():
    plt.figure("LCOE calculado de fuentes energéticas", figsize=(15, 8)) # Tamaño y título

    for fuente in [nuclear, solar, termica, hidro]:  # !!!ACTUALIZAR!!!
        plt.bar(fuente.nombre, lcoe(fuente), label=fuente.nombre)
        
        plt.text(
            fuente.nombre,  # x
            lcoe(fuente),   # y
            str(lcoe(fuente)),  # texto
            ha="center", va="bottom",
            fontweight = "bold"
        )
    
    plt.xlabel('Fuente de energía')
    plt.ylabel('LCOE (Euro/MWh)')
    plt.title('LCOE de las fuentes de energía')
    plt.legend()
    plt.show()

def plotemisiones():    
    plt.figure("Emisiones de CO2 de las fuentes de energía", figsize=(15, 8)) # Tamaño y título

    for fuente in [nuclear, solar, termica, hidro]:  # !!!ACTUALIZAR!!!
        plt.bar(fuente.nombre, fuente.emisiones, label=fuente.nombre)
        
        plt.text(
            fuente.nombre,  # x
            fuente.emisiones,   # y
            str(fuente.emisiones),  # texto
            ha="center", va="bottom",
            fontweight = "bold"            
        )
    
        plt.text(
            fuente.nombre,
            fuente.emisiones/2,
            "Emisiones totales", 
            ha="center", va="bottom",
        )

        plt.text(
            fuente.nombre,
            (fuente.emisiones/2) - fuente.emisiones * 0.5,
            str(fuente.emisiones * potenciaCentral * 0.001 * fuente.toperativo) + " kg CO2", 
            ha="center", va="bottom",
            fontweight = "bold",
            color = "white"
        )

    plt.xlabel('Fuente de energía')
    plt.ylabel('Emisiones de CO2 por año (g/MWh)')
    plt.title('CO2 emitido por las fuentes de energía')
    plt.legend()
    plt.show()


plotall()
plotemisiones()
plotlcoe()

#-----------------------------------------------------------------INTERFAZ-------------------------------------------------------------#

    # Título

    # Gráfico

    # Texto