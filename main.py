# Librerías
import sys
import matplotlib.pyplot as plt
import pygame
import numpy as np
pygame.init()
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as VistaGrafico

# PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QPlainTextEdit, QInputDialog, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# --------------------------- Clase FuenteEnergia con atributos -----------------------------------#
# Variables universales: 

ingorigen = 0 # Ingresos, cambiar para tener una inversión inicial
potenciaCentral = 500 # Potencia de la central en MW
potenciaTermica = 1000 # Potencia solar en MW/m^2
c = 2.99792*(10**8) # Velocidad de la luz

class FuenteEnergia:
    def __init__(self, nombre, tconst, toperativo, emisiones, cconst, beneficio): #cmant, ccomb):
        # Atributos

        self.nombre = nombre
        self.tconst = tconst # años de construcción
        self.toperativo = toperativo # años de operación

        self.cconst = cconst # Euros por año de construcción por MWh (negativo, ya que es pérdida)

        self.beneficio = beneficio # Euro/MWh por año en operación

        self.emisiones = emisiones # g de CO2 por MWh

        # Listas vacías para almacenar y graficar
        self.ling = [] # Lista de valores de ingreso
        self.lt = [] # Lista de valores de tiempo

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
        ing = ingorigen  # Inicializar la variable de ingresos
        self.ling = []  # Limpiar lista de ingresos
        self.lt = []    # Limpiar lista de tiempos

        for t in range(0, self.tconst + self.toperativo):
            if t < self.tconst:
                ing += self.cconst * potenciaCentral # Pérdida de construcción.
            elif t == self.tconst:
                ing += self.cconst * potenciaCentral
                plt.text(t, ing, str(ing) + " €", va = "bottom", ha = "center", fontstyle = "italic") # Texto de pérdida máxima
            else: 
                ing += self.beneficio * potenciaCentral
            self.ling.append(ing)
            self.lt.append(t)

        plt.text(self.lt[-1], self.ling[-1], f"{self.ling[-1]} €", va="bottom", ha="center", fontstyle="italic") # Texto de beneficio máximo
        plt.xlabel('Años')
        plt.ylabel('Ingresos acumulados (Euro)')
        plt.title('Ingresos acumulados de las centrales')
        plt.grid()
        plt.xlim(0, max(f.tconst + f.toperativo for f in listafuentes) + 1)

        return plt.plot(self.lt, self.ling, label=self.nombre)
    
    # Función de cálculo de emisiones totales.

    def emisionestotales(self):
        return str(self.emisiones * potenciaCentral * 0.001 * self.toperativo) + " kg CO2"
    
# Funciones de ploteo comparativo.
    # Emisiones

#substitute in the "for attr in", the "nombre" for fuente.nombre, "tconst" for fuente.tconst and so on
def plotemisiones():
    plt.clf()
    for fuente in listafuentes:

        if all(
            getattr(fuente, attr) is not None
            for attr in ["nombre", "tconst", "toperativo", "cconst", "beneficio", "emisiones"]
        ):

            plt.bar(fuente.nombre, fuente.emisiones, label=fuente.nombre)
            # Formato
            plt.text(
            fuente.nombre,
            0,
            str(fuente.emisionestotales()), 
            ha="center", va="bottom",
            fontweight = "bold",
            color = "white",
            size = 10
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
    return

    # LCOE
def plotlcoe():
    
    plt.clf()
    for fuente in listafuentes:
        if all(
            getattr(fuente, attr) is not None
            for attr in ["nombre", "tconst", "toperativo", "cconst", "beneficio", "emisiones"]
        ):
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

    return
 
    # Ingresos
def plotingresos():
    plt.clf()
    for fuente in listafuentes:
        fuente.ingresos()
    plt.legend()
    plt.grid(True)
    return

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
listagraficos = {"Ingresos": plotingresos, "LCOE": plotlcoe, "Emisiones": plotemisiones}

for fuente in listafuentes:
    fuente.diccionarioprop = {
                            "Nombre": fuente.nombre, 
                            "Tiempo de construcción": fuente.tconst,
                            "Tiempo operativo": fuente.toperativo, 
                            "Costo de construcción": fuente.cconst,
                            "Beneficio anual":fuente.beneficio,
                            "Emisiones anuales":fuente.emisiones}

listavariables = {
    "Ingresos": ingorigen,
    "Potencia de las centrales": potenciaCentral,
    "Potencia térmica del sol": potenciaTermica,
}


#-----------------------------------------------------------------INTERFAZ-------------------------------------------------------------#

# Fuente
titulo = QFont()
titulo.setBold(True)
titulo.setCapitalization(True)
titulo.setFamily("Cambria Math")
titulo.setPointSize(20)

textonormal = QFont()
textonormal.setBold(False)
textonormal.setCapitalization(False)
textonormal.setFamily("Arial")
textonormal.setPointSize(10)

negrita = QFont()
negrita == textonormal
negrita.setBold(True)

# Resolución
res = pygame.display.Info()
resw = res.current_w
resh = res.current_h

class ConsolaRedirector:
    def __init__(self, widget_output):
        self.output = widget_output

    def write(self, mensaje):
        self.output.moveCursor(self.output.textCursor().End)
        self.output.insertPlainText(mensaje)
        self.output.moveCursor(self.output.textCursor().End)

    def flush(self):
        pass
    
class Ventana(QMainWindow): #Ventana principal

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora Energética | El pasado, presente y futuro de la energía nuclear. Hecho por Franco Baldassarre.") 
        # self.setWindowIcon(QtGui.QIcon()) !!ICONO!!
        self.boton_seleccionado_id = None
        self.botones_dict = {} # Diccionario botones
        self.interfaz()
        self.showMaximized()


    def interfaz(self):  
        # Contenedor genérico
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        layout = QGridLayout()
        contenedor.setLayout(layout)

# Gráfico mostrado en la interfaz
        self.ploteo = plt.figure(figsize=(12, 8))
        self.grafico = VistaGrafico(self.ploteo)
    
# CONTENEDOR DERECHO
        contder = QWidget()
        contder.setFixedWidth(int(7/8*resw))
        layder = QVBoxLayout()

        # Grafico
        layder.addWidget(self.grafico)

        desplegableder = QComboBox()
        desplegableder.addItem("Seleccione tipo de gráfico.")
        for item, plot in listagraficos.items():
            desplegableder.addItem(item, userData = plot)
        desplegableder.setFont(textonormal)
        layder.addWidget(desplegableder)
        
        # Funciones grafico

        def canviargrafico():
            if desplegableder.currentIndex() == 0:
                return
            self.ploteo.clf()
            graficofuncion = desplegableder.currentData()
            if graficofuncion is None:
                return
            graficofuncion()
            self.grafico.draw()
            print(f"Se ha cambiado el gráfico a {desplegableder.currentText()}.")
        
        def actualizargrafico():
            graficofuncion = desplegableder.currentData()
            if graficofuncion is None:
                return
            graficofuncion()
            self.grafico.draw()
            print(f"Se ha actualizado el gráfico {desplegableder.currentText()}.") 

        desplegableder.currentIndexChanged.connect(canviargrafico)

        # Consola
        self.consola = QPlainTextEdit()
        self.consola.backgroundRole()
        self.consola.setReadOnly(True)
        layder.addWidget(self.consola)
        sys.stdout = ConsolaRedirector(self.consola)
        sys.stderr = ConsolaRedirector(self.consola)
        self.consola.setStyleSheet("""
        QPlainTextEdit {
        background-color: #000000;
        color: #00FF00;
        font-family: Courier    ;
        font-size: 14px;
        }
        """)

# CONTENEDOR IZQUIERDO
        contizq = QWidget()
        layizq = QVBoxLayout()

    # Desplegable
        contdespizq = QWidget()
        laydesplegableizq = QHBoxLayout()

        desplegableizq = QComboBox()
        desplegableizq.addItem("Seleccione o cree fuente.")
        for fuente in listafuentes:
            desplegableizq.addItem(fuente.nombre, userData = fuente)
        botoncrear = QPushButton("+")
        botoncrear.setFont(negrita)
        botoncrear.setFixedWidth(25)

        def nuevafuente():
            texto, ok = QInputDialog.getText(self, "Nueva fuente", "Inserte nombre de la fuente:")
            if ok and texto: # se escribió y dio a ok
                limpiar()
                nombrefuente = FuenteEnergia(
                    nombre=texto,
                    tconst=5,
                    cconst=-2,
                    beneficio=5,
                    toperativo=10,
                    emisiones=1,
                )

                nombrefuente.diccionarioprop = {
                    "Nombre": nombrefuente.nombre,
                    "Tiempo de construcción": nombrefuente.tconst,
                    "Tiempo operativo": nombrefuente.toperativo,
                    "Costo de construcción": nombrefuente.cconst,
                    "Beneficio anual": nombrefuente.beneficio,
                    "Emisiones anuales": nombrefuente.emisiones
                }
            else:
                return
            
            boton_creador = BotonInteractivo(self)
            listafuentes.append(nombrefuente)
            desplegableizq.addItem(nombrefuente.nombre, userData=nombrefuente)
            for boton in boton_creador.botones([nombrefuente]):
                laypropiedades.addWidget(boton)

        botoncrear.clicked.connect(nuevafuente)

        laydesplegableizq.addWidget(desplegableizq)
        laydesplegableizq.addWidget(botoncrear)
        contdespizq.setLayout(laydesplegableizq)

        laypropiedades = QVBoxLayout()
        listapropiedades = QWidget()
        listapropiedades.setLayout(laypropiedades)

        # caja de texto
        continput = QWidget() 
        layinput = QHBoxLayout()
        continput.setLayout(layinput)
        self.textinput = QLineEdit()
        self.botoninput = QPushButton("Enviar", self) 
        self.botoninput.setFixedWidth(100)
        layinput.addWidget(self.textinput)
        layinput.addWidget(self.botoninput)
        self.botoninput.clicked.connect(self.enviar) # Conectar el boton a la función enviar
        self.botoninput.clicked.connect(actualizargrafico)

        layizq.addWidget(contdespizq, alignment= Qt.AlignTop)
        layizq.addWidget(listapropiedades)
        layizq.addWidget(continput, alignment= Qt.AlignBottom)
        

        def cambiobotones():
            try:
                boton_creador = BotonInteractivo(self)
                fuentes = desplegableizq.currentData()
                for boton in boton_creador.botones([fuentes]):
                    laypropiedades.addWidget(boton)
                print("Cambiada interfaz a mostrar datos de", fuentes.nombre)
            except:
                print("Seleccione una fuente correcta.")
                for boton in boton_creador.botones([nuclear]):
                    laypropiedades.addWidget(boton)
            return 

        def limpiar():
            while laypropiedades.count():
                item = laypropiedades.takeAt(0)
                laypropiedades.removeWidget(item.widget())

        desplegableizq.currentIndexChanged.connect(limpiar)
        desplegableizq.currentIndexChanged.connect(cambiobotones)
        contder.setLayout(layder)
        contizq.setLayout(layizq)

        layout.addWidget(contizq, 0, 0)
        layout.addWidget(contder, 0, 1)

    def enviar(self):
        global ingorigen, potenciaCentral, potenciaTermica
        if self.boton_seleccionado_id is None:
            print("Seleccione primero un atributo pulsando su botón.")
            return

        boton, fuente, etiqueta = self.botones_dict[self.boton_seleccionado_id]
        valor_texto = self.textinput.text()

        if valor_texto == "":
            print("Introduzca un valor antes de enviar.")
            return

        try:
            if fuente is not None and etiqueta in ["Tiempo de construcción", "Tiempo operativo", "Emisiones anuales"]:
                valor = int(float(valor_texto))
            else:
                valor = float(valor_texto)
        except ValueError:
            print("Introduzca un valor numérico válido.")
            return
        if valor < 1:
            print("Seleccione un valor mayor a 1.")
            return

        if fuente is not None:
            fuente.diccionarioprop[etiqueta] = valor

            if etiqueta == "Tiempo de construcción":
                fuente.tconst = int(valor)
            elif etiqueta == "Tiempo operativo":
                fuente.toperativo = int(valor)
            elif etiqueta == "Costo de construcción":
                fuente.cconst = float(valor)
            elif etiqueta == "Beneficio anual":
                fuente.beneficio = float(valor)
            elif etiqueta == "Emisiones anuales":
                fuente.emisiones = int(valor)
            else:
                print(f"Etiqueta {etiqueta} no reconocida, no se actualizó ningún atributo de la fuente.")
        else:
            listavariables[etiqueta] = valor

            if etiqueta == "Ingresos":
                ingorigen = float(valor)
            elif etiqueta == "Potencia de las centrales":
                potenciaCentral = float(valor)
            elif etiqueta == "Potencia térmica del sol":
                potenciaTermica = float(valor)
            else:
                print(f"Etiqueta {etiqueta} no reconocida, no se actualizó ninguna variable global.")

        boton.setText(f"{etiqueta}: {valor}") 
        if fuente is not None:
            print(f"Se actualizó {etiqueta} de {fuente.nombre} a {valor}")
        else:
            print(f"Se actualizó valor de la variable universal a {valor}.")

class BotonInteractivo: # Clase para crear botones
    def __init__(self, ventana):
        self.ventana = ventana
        self.id_counter = 0 # id de los botones
    def botones(self, fuentes):
        listabotones = []
        for fuente in fuentes:
            for nombre, valor in fuente.diccionarioprop.items():

                if nombre == "Nombre": # Título de nombre de fuente
                    boton_widget = QLabel(valor)
                    boton_widget.setAlignment(Qt.AlignCenter)
                    boton_widget.setFont(titulo)

                elif valor is None: # Para creador de nuevas fuentes
                    boton_widget = QPushButton(f"{nombre}: ")
                    boton_widget.setFont(textonormal)
                    boton_id = self.id_counter
                    self.ventana.botones_dict[boton_id] = (boton_widget, fuente, nombre)
                    self.id_counter += 1
                    boton_widget.clicked.connect(
                        lambda _, bid=boton_id: self.interactuar(bid)
                    )

                else: # Botones interactivos con propiedades de la fuente
                    boton_widget = QPushButton(f"{nombre}: {valor}") 
                    boton_widget.setFont(textonormal)
                    boton_id = self.id_counter
                    self.ventana.botones_dict[boton_id] = (boton_widget, fuente, nombre)
                    self.id_counter += 1
                    boton_widget.clicked.connect(
                        lambda _, bid=boton_id: self.interactuar(bid)
                    )
                listabotones.append(boton_widget)

        for nombre, valor in listavariables.items(): # Botones de variables universales
            boton_id = self.id_counter
            boton_widget = QPushButton(f"{nombre}: {valor}")
            boton_widget.setFont(textonormal)
            listabotones.append(boton_widget)
            self.ventana.botones_dict[boton_id] = (boton_widget, None, nombre)
            self.id_counter += 1
            boton_widget.clicked.connect(
            lambda _, bid=boton_id: self.interactuar(bid)
            )

    # Texto específico de las fuentes !!!!!!!!!!!!!!ACTUALIZAR!!!!!!!!!!!!!!!!
        texto = QLabel(f"Área de placas fotovoltaicas: {FuenteEnergia.areaFoto}")
        texto.setFont(textonormal)
        listabotones.append(texto)
        texto = QLabel(f"Cantidad de residuos nucleares: {FuenteEnergia.resnucleares}")
        texto.setFont(textonormal)
        listabotones.append(texto)

        return listabotones

    def interactuar(self, boton_id):
        if self.ventana.boton_seleccionado_id is not None: # Poner en negrita el color del botón seleccionado
            boton_anterior, _, _ = self.ventana.botones_dict[self.ventana.boton_seleccionado_id]
            boton_anterior.setFont(textonormal)

        self.ventana.boton_seleccionado_id = boton_id
        boton, fuente, atributo = self.ventana.botones_dict[boton_id]
        boton.setFont(negrita)
            
        if boton_id < 5:
            print(f"Seleccionado botón {boton_id}, {atributo} de {fuente.nombre}")
        else:
            print(f"Seleccionado boton {boton_id}, variable universal.")


def inicio():
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    print("Resolución actual:", resw, "por", resh)
    print("Aplicación inicializada con datos predeterminados de fuentes:")
    for fuente in listafuentes:
        print(f"{fuente.nombre}, con tiempo de construcción {fuente.tconst}, tiempo operativo {fuente.toperativo}, costo de construcción {fuente.cconst}, beneficio de {fuente.beneficio} y emisiones de {fuente.emisiones}.")
    sys.exit(app.exec_())

if __name__ == "__main__":
    inicio() # Ejecutar la interfaz cuando el nombre es el principal

# Diagrama de flujo
# Datos programa