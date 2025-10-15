# Librerías
import sys
import traceback
import matplotlib.pyplot as plt
import pygame
import numpy as np
pygame.init()
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as VistaGrafico

# PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QPlainTextEdit, QInputDialog, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor

# --------------------------- Clase FuenteEnergia con atributos -----------------------------------#
# Variables universales: 

ingorigen = 0 # Ingresos, cambiar para tener una inversión inicial
amortizacion = 20 # Años de amortización de la central
potenciaCentral = 500 # Potencia ÚTIL de la central en MW
potenciaTermica = 1000 # Potencia solar en W/m^2
caudalagua = 100 # Caudal de agua en m^3/s
densidadagua = 997 # kg/m^3
c = 2.99792*(10**8) # Velocidad de la luz

class FuenteEnergia:
    def __init__(self, nombre, tconst, toperativo, emisiones, cconst, beneficio, rendimiento):
        # Atributos
        self.nombre = nombre
        self.tconst = tconst # años de construcción
        self.toperativo = toperativo # años de operación
        self.cconst = cconst # Euros por año de construcción por MW (negativo, ya que es pérdida)

        self.potencia = potenciaCentral # Potencia de la central en MW
        self.beneficio = beneficio # Euro/MWh por año en operación
        self.emisiones = emisiones # kg de CO2 por MJ
        self.rendimiento = rendimiento # Rendimiento de la fuente (0-1)

        # Listas vacías para almacenar y graficar
        self.ling = [] # Lista de valores de ingreso
        self.lt = [] # Lista de valores de tiempo

#-----------------------------------------------------------------FUNCIONES-------------------------------------------------------------#

# Funciones de la clase FuenteEnergia.

    # Función LCOE 
    def lcoe(self):
        lcoe = (self.cconst * self.tconst + self.beneficio * self.toperativo) / (self.tconst + self.toperativo)                               
                            # Ingreso neto (ingresos menos gastos)                      # Tiempo total

        return round(lcoe, 5)
    
    # Función de ploteo de gráficos
    def ingresos(self):
        ing = ingorigen  # Inicializar la variable de ingresos
        self.ling = []  # Limpiar lista de ingresos
        self.lt = []    # Limpiar lista de tiempos

        for t in range(0, self.tconst + self.toperativo):
            if t < self.tconst:
                ing += self.cconst * self.potencia * self.rendimiento**-1 # Pérdida de construcción (dividir por el rendimiento porque es consumida)
            elif t == self.tconst:
                ing += self.cconst * self.potencia * self.rendimiento**-1
                plt.text(t, ing, str("%.2f" % ing) + " €", va = "bottom", ha = "center", fontstyle = "italic") # Texto de pérdida máxima
            else: 
                ing += self.beneficio * self.potencia
            self.ling.append(ing)
            self.lt.append(t)

        plt.text(self.lt[-1], self.ling[-1], f"{self.ling[-1]} €", va="bottom", ha="center", fontstyle="italic") # Texto de beneficio máximo
        plt.xlabel('Años')
        plt.ylabel('Ingresos acumulados (Mill. Euro)')
        plt.title('Ingresos acumulados de las centrales')
        plt.grid()
        plt.xlim(0, max(f.tconst + f.toperativo for f in listafuentes) + 1)

        return plt.plot(self.lt, self.ling, label=self.nombre)
    
    # Función de cálculo de emisiones totales.

    def emisionestotales(self):
        return str(self.emisiones * potenciaCentral * self.toperativo * 365.25 * 24 * 3600* 1000**-1) + " T CO2"
     
# Funciones de ploteo comparativo.

    # Emisiones
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
    plt.ylabel('Emisiones de CO2 por año (kg/MJ)')
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
    rendimiento=1
)

fotovoltaica = FuenteEnergia(
    nombre='Fotovoltaica',
    tconst = 10,
    cconst = -2,
    beneficio = 5,
    toperativo = 40,
    emisiones = 2,
    rendimiento=1
)

termica = FuenteEnergia(
    nombre='Térmica',
    tconst = 5,
    cconst = -10,
    beneficio = 5,
    toperativo = 15,
    emisiones = 10,
    rendimiento=1
)

hidro = FuenteEnergia(
    nombre='Hidráulica',
    tconst = 15,
    cconst = -3,
    beneficio = 1,
    toperativo = 60,
    emisiones = 1,
    rendimiento=1
)
eolica = FuenteEnergia(
    nombre='Eólica',
    tconst = 5,
    cconst = -4,
    beneficio = 3,
    toperativo = 25,
    emisiones = 3,
    rendimiento=1
)

listafuentes = [nuclear, fotovoltaica, termica, hidro, eolica]
listagraficos = {"Ingresos": plotingresos, "LCOE": plotlcoe, "Emisiones": plotemisiones}

for fuente in listafuentes:
    fuente.diccionarioprop = {
                            "Nombre de la fuente": fuente.nombre, 
                            "Tiempo de construcción (años)": fuente.tconst,
                            "Tiempo operativo (años)": fuente.toperativo, 
                            "Costo de construcción (Euros, en negativo)": fuente.cconst,
                            "Beneficio anual (Mill. Euros)":fuente.beneficio,
                            "Emisiones anuales (kg CO2)":fuente.emisiones,
                            "Rendimiento (0-1)": fuente.rendimiento,
                            "Potencia útil (MW)": fuente.potencia,
                            }
    
# Variables de cálculo
areaFoto = potenciaCentral*(10**6)/ potenciaTermica
resnucleares = round((potenciaCentral * 10**6 * 365.25 * 24 * 3600)/(nuclear.rendimiento * c ** 2), 5) # E = mc^2 -> m = E/c^2 (la energía es la consumida). kg por año de residuos
resnuctot = round(resnucleares * nuclear.toperativo, 5)
altembalse = (potenciaCentral/10**6)/(9.81*hidro.rendimiento*caudalagua) # P = rendimiento * densidadagua * g * h * caudal -> altura = P / (rendimiento * densidadagua * g * caudal)

listavariables = {
    "Ingresos iniciales (Mill. Euro)": ingorigen,
    "Potencia de las centrales (MW)": potenciaCentral,
    "Potencia térmica del sol (W)": potenciaTermica,
    "Caudal de agua (m^3/s)": caudalagua,
    "Densidad del agua (kg/m^3)": densidadagua,
    "Residuos nucleares anuales (kg)": resnucleares,
    "Residuos nucleares totales (kg)": resnuctot,
    "Área de placas fotovoltaicas (m^2)": areaFoto,
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

negrita = QFont(textonormal)
negrita.setBold(True)

# Resolución
res = pygame.display.Info()
resw = res.current_w
resh = res.current_h

class ConsolaRedirector:
    def __init__(self, widget_output):
        self.output = widget_output

    def write(self, mensaje):
        self.output.moveCursor(QTextCursor.End)
        self.output.insertPlainText(str(mensaje))
        self.output.moveCursor(QTextCursor.End)

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

        def cambiargrafico():
            if desplegableder.currentIndex() == 0:
                return
            self.ploteo.clf()  # Always clear
            graficofuncion = desplegableder.currentData()
            if graficofuncion is None:
                return

            for fuente in listafuentes:
                for k, v in fuente.diccionarioprop.items():
                    if isinstance(v, str):
                        try:
                            fuente.diccionarioprop[k] = float(v)
                        except:
                            pass
                        
            graficofuncion()  # plot
            self.grafico.draw()
            print(f"Se ha cambiado el gráfico a {desplegableder.currentText()}.")

        desplegableder.currentIndexChanged.connect(cambiargrafico)

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
        def limpiar():
            while laypropiedades.count():
                item = laypropiedades.takeAt(0)
                laypropiedades.removeWidget(item.widget())
                widget = item.widget()
                if widget:
                    widget.setParent(None)

        def nuevafuente():
            try:
                # Nombre
                texto, ok = QInputDialog.getText(self, "Nueva fuente", "Inserte nombre de la fuente:")
                if not ok or not texto:
                    return

                # Tiempo de construcción
                tconst_text, ok1 = QInputDialog.getText(self, "Nueva fuente", "Inserte tiempo de construcción de la fuente (años):")
                if not ok1 or not tconst_text:
                    return
                tconst = int(tconst_text)

                # Costo de construcción
                cconst_text, ok2 = QInputDialog.getText(self, "Nueva fuente", "Inserte costo de construcción de la fuente (Euro/MW, en negativo):")
                if not ok2 or not cconst_text:
                    return
                cconst = float(cconst_text)

                # Beneficio anual
                beneficio_text, ok3 = QInputDialog.getText(self, "Nueva fuente", "Inserte beneficio anual (Euro/MW):")
                if not ok3 or not beneficio_text:
                    return
                beneficio = float(beneficio_text)

                # Tiempo operativo
                toperativo_text, ok4 = QInputDialog.getText(self, "Nueva fuente", "Inserte tiempo operativo (años):")
                if not ok4 or not toperativo_text:
                    return
                toperativo = int(toperativo_text)

                # Emisiones
                emisiones_text, ok5 = QInputDialog.getText(self, "Nueva fuente", "Inserte emisiones anuales (kg CO2):")
                if not ok5 or not emisiones_text:
                    return
                emisiones = float(emisiones_text)

                # Rendimiento
                rendimiento_text, ok6 = QInputDialog.getText(self, "Nueva fuente", "Inserte rendimiento (0–1):")
                if not ok6 or not rendimiento_text:
                    return
                rendimiento = float(rendimiento_text)
                if rendimiento >= 1:
                    print("El rendimiento debe ser menor que 1.")
                    return

            except ValueError:
                print("Introduzca valores numéricos válidos.")
                return

            # Crear nueva fuente
            limpiar()

            nueva_fuente = FuenteEnergia(
                nombre=texto,
                tconst=tconst,
                cconst=cconst,
                beneficio=beneficio,
                toperativo=toperativo,
                emisiones=emisiones,
                rendimiento=rendimiento
            )

            nueva_fuente.diccionarioprop = {
                "Nombre": nueva_fuente.nombre,
                "Tiempo de construcción": nueva_fuente.tconst,
                "Tiempo operativo": nueva_fuente.toperativo,
                "Costo de construcción": nueva_fuente.cconst,
                "Beneficio anual": nueva_fuente.beneficio,
                "Emisiones anuales": nueva_fuente.emisiones,
                "Rendimiento": nueva_fuente.rendimiento
            }

            boton_creador = BotonInteractivo(self)
            listafuentes.append(nueva_fuente)
            desplegableizq.addItem(nueva_fuente.nombre, userData=nueva_fuente)

            for boton in boton_creador.botones([nueva_fuente]):
                laypropiedades.addWidget(boton)

            desplegableder.setCurrentIndex(1 if desplegableder.count() > 1 else 0)
            cambiargrafico()
        
            boton_creador = BotonInteractivo(self)
            listafuentes.append(nueva_fuente)
            desplegableizq.addItem(nueva_fuente.nombre, userData=nueva_fuente)
            for boton in boton_creador.botones([nueva_fuente]):
                laypropiedades.addWidget(boton)
            desplegableder.setCurrentIndex(1 if desplegableder.count() > 1 else 0)
            cambiargrafico()

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
        self.botoninput.clicked.connect(cambiargrafico)
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

        desplegableizq.currentIndexChanged.connect(limpiar)
        desplegableizq.currentIndexChanged.connect(cambiobotones)
        contder.setLayout(layder)
        contizq.setLayout(layizq)

        layout.addWidget(contizq, 0, 0)
        layout.addWidget(contder, 0, 1)

    def enviar(self):
        global ingorigen, potenciaCentral, potenciaTermica, caudalagua, densidadagua, resnucleares, resnuctot, areaFoto

        if self.boton_seleccionado_id is None:
            print("Seleccione primero un atributo pulsando su botón.")
            return

        boton, fuente, etiqueta = self.botones_dict[self.boton_seleccionado_id]
        valor_texto = self.textinput.text().strip()

        if not valor_texto:
            print("Introduzca un valor antes de enviar.")
            return

        try:
            if etiqueta in ["Tiempo de construcción (años)", "Tiempo operativo (años)"]:
                valor = int(valor_texto)
            else:
                valor = int(valor_texto)
        except ValueError:
            print("Introduzca un valor numérico válido.")
            return

        if etiqueta != "Rendimiento" and abs(valor) < 1:
            print("Seleccione un valor mayor a 1.")
            return
            
        if etiqueta == "Rendimiento" and not (0 < valor < 1):
            print("El rendimiento debe ser entre 0 y 1.")
            return

        if fuente is not None:
            fuente.diccionarioprop.update({
                etiqueta: valor
            })
            print(f"Se actualizó {etiqueta} de {fuente.nombre} a {valor}")
            print(valor, etiqueta, fuente.diccionarioprop)
            if etiqueta == "Costo de construcción (Euros, en negativo)":
                fuente.cconst = valor
            elif etiqueta == "Beneficio anual (Mill. Euros)":
                fuente.beneficio = valor
            elif etiqueta == "Emisiones anuales (kg CO2)":
                fuente.emisiones = valor
            elif etiqueta == "Rendimiento (0-1)":
                fuente.rendimiento = valor
            elif etiqueta == "Tiempo de construcción (años)":
                fuente.tconst = int(valor)
            elif etiqueta == "Tiempo operativo (años)":
                fuente.toperativo = int(valor)
            elif etiqueta == "Potencia útil (MW)":
                fuente.potencia = valor

        else:
            if etiqueta == "Ingresos iniciales (Mill. Euros)":
                ingorigen = valor
            elif etiqueta == "Potencia de las centrales (MW)":
                potenciaCentral = valor
            elif etiqueta == "Potencia térmica del sol (W)":
                potenciaTermica = valor
            elif etiqueta == "Caudal de agua (m^3/s)":
                caudalagua = valor
            elif etiqueta == "Densidad del agua (kg/m^3)":
                densidadagua = valor
            elif etiqueta == "Residuos nucleares anuales (kg)":
                resnucleares = valor
            elif etiqueta == "Residuos nucleares totales (kg)":
                resnuctot = valor
            elif etiqueta == "Área de placas fotovoltaicas (m^2)":
                areaFoto = valor
            else:
                print(f"Etiqueta {etiqueta} no reconocida, no se actualizó ninguna variable global.")
                return

            print(f"Se actualizó valor de la variable universal {etiqueta} a {valor}.")

        self.textinput.clear()
        boton.setText(f"{etiqueta}: {valor}")

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

def excepthook(exc_type, exc_value, exc_tb): # Error en la consola
    traceback.print_exception(exc_type, exc_value, exc_tb)
    sys.__excepthook__(exc_type, exc_value, exc_tb)

sys.excepthook = excepthook

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
    inicio() # Ejecutar la interfaz
