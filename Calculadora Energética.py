# Librerías
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as VistaGrafico
from matplotlib.figure import Figure

# PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

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
            
# Variables universales: 

    ingorigen = 0 # Ingresos, cambiar para tener una inversión inicial
    potenciaCentral = 500 # Potencia de la central en MW
    potenciaTermica = 1000 # Potencia solar en MW/m^2
    c = 2.99792*(10**8) # Velocidad de la luz

# Variables de cálculo
    areaFoto = potenciaCentral / potenciaTermica
    resnucleares = potenciaCentral * c ** -2
# Dimensiones embalse !!!CALCULAR!!!


#-----------------------------------------------------------------FUNCIONES-------------------------------------------------------------#

# Función LCOE 

    def lcoe(self):
        lcoe = (self.cconst * self.tconst + self.beneficio * self.toperativo) / (self.tconst + self.toperativo)                               
                            # Ingreso neto (ingresos menos gastos)                      # Tiempo total
        return round(lcoe, 3)

    # Función de ploteo de gráficos

    def plot(self):
        for t in range(1, self.tconst + self.toperativo):
            if t < self.tconst:
                ing += self.cconst * self.potenciaCentral # Pérdida de construcción.
            elif t == self.tconst:
                ing += self.cconst * self.potenciaCentral
                plt.text(t, 
                ing, str(ing) + " €", va = "bottom", ha = "center", fontstyle = "italic") # Texto de pérdida máxima
            else:
                ing += self.beneficio * self.potenciaCentral # menos costos!!!!!!! # Beneficio operativo.
            self.ling.append(ing)
            self.lt.append(t)

        plt.plot(self.lt, self.ling, label=self.nombre)
        plt.xlabel('Años')
        plt.ylabel('Ingresos acumulados (Euro)')
        plt.title('Ingresos acumulados de las centrales')
        plt.grid()
        plt.xlim(0, max(nuclear.tconst + nuclear.toperativo, solar.tconst + solar.toperativo, termica.tconst + termica.toperativo, hidro.tconst + hidro.toperativo) + 1)
        plt.legend()
        return plt


    def plotlcoe(self):
        plt.figure("LCOE calculado de fuentes energéticas", figsize=(15, 8)) # Tamaño y título

        for fuente in [nuclear, solar, termica, hidro]:  # !!!ACTUALIZAR!!!
            plt.bar(fuente.nombre, self.lcoe, label=fuente.nombre)

            plt.text(
                fuente.nombre,  # x
                self.lcoe,   # y
                str(self.lcoe),  # texto
                ha="center", va="bottom",
                fontweight = "bold"
            )

        plt.xlabel('Fuente de energía')
        plt.ylabel('LCOE (Euro/MWh)')
        plt.title('LCOE de las fuentes de energía')
        plt.legend()
        plt.show()

    def emisiones(self):
        plt.bar(self.nombre, self.emisiones, label=self.nombre)

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

#---------------------------------- FUENTE ENERGÍA: VARIABLES. El usuario puede modificar los valores. ----------------------------------#

# Variables específicas de cada fuente de energía:

nuclear = FuenteEnergia(
    nombre='Nuclear',
    tconst = 10, 
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
    toperativo = 15,
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
eolica = FuenteEnergia(
    nombre='Eólica',
    tconst = 5,
    cconst = -4,
    beneficio = 3,
    toperativo = 25,
    emisiones = 3,
)

#-----------------------------------------------------------------INTERFAZ-------------------------------------------------------------#

class Ventana(QMainWindow): #Ventana principal

    def __init__(self):
        super().__init__() # La ventana se inicializa llamando a la clase padre (QMainWindow)

        self.setWindowTitle("Calculadora Energética | El pasado, presente y futuro de la energía nuclear. Hecho por Franco Baldassarre.") 
        # self.setWindowIcon(QtGui.QIcon()) !!ICONO!!
        self.showMaximized()

    def interfaz(self): # Contenedor
        contenedor = QWidget()
        self.setCentralWidget(contenedor)

        contenedorizquierdo = QVBoxLayout()
        contenedorizquierdo.setGeometry(0,0, QMainWindow.width/2, QMainWindow.height)

        #contenedorsubgrafico = QHBoxLayout()
        #contenedorsubgrafico.setGeometry()
        
        #contenedorgrafico = QVBoxLayout()
        #grafico = Figure(nuclear.plot())
        #contenedorgrafico.addWidget(grafico)

def inicio():
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    inicio() # Ejecutar la interfaz cuando el nombre es el principal
