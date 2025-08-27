# Librerías
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as VistaGrafico
from matplotlib.figure import Figure

# PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout
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

# Funciones de la clase FuenteEnergia.

    # Función LCOE 

    def lcoe(self):
        lcoe = (self.cconst * self.tconst + self.beneficio * self.toperativo) / (self.tconst + self.toperativo)                               
                            # Ingreso neto (ingresos menos gastos)                      # Tiempo total

        return round(lcoe, 3)

    # Función de ploteo de gráficos

    def ingresos(self):
        ing = 0  # Inicializar la variable de ingresos

        for t in range(1, self.tconst + self.toperativo):
            if t < self.tconst:
                ing += self.cconst * self.potenciaCentral # Pérdida de construcción.
            elif t == self.tconst:
                ing += self.cconst * self.potenciaCentral
                plt.text(t, ing, str(ing) + " €", va = "bottom", ha = "center", fontstyle = "italic") # Texto de pérdida máxima
            else:
                ing += self.beneficio * self.potenciaCentral # !!!!!!!""menos costos!!!!!!! # Beneficio operativo.
            self.ling.append(ing)
            self.lt.append(t)

        plt.xlabel('Años')
        plt.ylabel('Ingresos acumulados (Euro)')
        plt.title('Ingresos acumulados de las centrales')
        plt.grid()
        plt.xlim(0, max(nuclear.tconst + nuclear.toperativo, solar.tconst + solar.toperativo, termica.tconst + termica.toperativo, hidro.tconst + hidro.toperativo) + 1)
        plt.legend()

        return plt.plot(self.lt, self.ling, label=self.nombre)
    
    # Función de cálculo de emisiones totales.

    def emisiones(self):
        return str(self.emisiones * self.potenciaCentral * 0.001 * self.toperativo) + " kg CO2"
    


# Funciones de ploteo comparativo.

    # Función de emisiones.
def plotemisiones():
    for fuente in listafuentes:
        plt.bar(fuente.nombre, fuente.emisiones, label=fuente.nombre)
        # Formato
        plt.text(
        fuente.nombre,
        (fuente.emisiones/2) - fuente.emisiones * 0.5,
        str(fuente.emisiones), 
        ha="center", va="bottom",
        fontweight = "bold",
        color = "white"
            )
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
        plt.xlabel('Fuente de energía')
        plt.ylabel('Emisiones de CO2 por año (g/MWh)')
        plt.title('CO2 emitido por las fuentes de energía')
        plt.legend()
    return plt.figure("Emisiones de CO2 de las fuentes energéticas")

    # Función de ploteo de LCOE.

def plotlcoe():
    for fuente in listafuentes:
        plt.bar(fuente.nombre, fuente.lcoe(), label=fuente.nombre)
        plt.text(
            fuente.nombre,  # x
            fuente.lcoe(),   # y
            str(fuente.lcoe()),  # texto
            ha="center", va="bottom",
            fontweight = "bold"
        )
    plt.xlabel('Fuente de energía')
    plt.ylabel('LCOE (Euro/MWh)')
    plt.title('LCOE de las fuentes de energía')
    plt.legend()
    
    return plt.figure("LCOE calculado de fuentes energéticas")

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

listafuentes = [nuclear, solar, termica, hidro, eolica]

#-----------------------------------------------------------------INTERFAZ-------------------------------------------------------------#

class Ventana(QMainWindow): #Ventana principal

    def __init__(self):
        super().__init__() # La ventana se inicializa llamando a la clase padre (QMainWindow, la ventana principal)
        self.setWindowTitle("Calculadora Energética | El pasado, presente y futuro de la energía nuclear. Hecho por Franco Baldassarre.") 
        # self.setWindowIcon(QtGui.QIcon()) !!ICONO!!
        self.interfaz()
        self.showMaximized()

    def interfaz(self):  # Contenedor
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        layout = QGridLayout()
        contenedor.setLayout(layout)

        ploteo = plt.figure(figsize=(8, 4))

# Gráfico mostrado en la interfaz

        for fuente in listafuentes:
            fuente.ingresos()
        grafico = VistaGrafico(ploteo)

# Texto

        label1 = QLabel("Calculadora energética")
        label1.setGeometry(200, 100, 200, 100)

#Añadir gráfico al layout

        layout.addWidget(label1, 0, 0) # Izquierda
        layout.addWidget(grafico, 0, 1, 100, 200) # Derecha


def inicio():
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    inicio() # Ejecutar la interfaz cuando el nombre es el principal
