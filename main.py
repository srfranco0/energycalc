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

# Conversión
conversion_segundos_por_año = 365.25 * 24 * 3600
conversion_kwh_por_mj = 3.6 
conversion_kg_por_tonelada = 1000

class FuenteEnergia:
    def __init__(self, nombre, tconst, toperativo, emisiones, cconst, beneficio, rendimiento, factor):
        # Atributos
        self.nombre = nombre
        self.tconst = tconst # años de construcción
        self.toperativo = toperativo # años de operación
        self.cconst = cconst # Euros por año de construcción por MW (negativo, ya que es pérdida)

        self.potencia = potenciaCentral # Potencia de la central en MW
        self.beneficio = beneficio # Euro/MWh por año en operación
        self.emisiones = emisiones # kg de CO2 por MJ
        self.rendimiento = rendimiento # Rendimiento de la fuente (0-1)
        self.factor = factor # Factor de carga (0-1)

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
        return str(self.emisiones * potenciaCentral * self.toperativo * conversion_segundos_por_año * conversion_kg_por_tonelada**-1 * 1000**-1) + " mil T CO2"
     
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
            fuente.emisiones + 0.1,
            f"Total: {str(fuente.emisionestotales())}" ,
            ha="center", va="bottom",
            fontweight = "bold",
            color = "black",
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
    tconst = 7, 
    cconst = -2,  
    beneficio = 0.4,
    toperativo= 70, 
    emisiones = 0.025,
    rendimiento=0.35,
    factor=0.9
)

fotovoltaica = FuenteEnergia(
    nombre='Fotovoltaica',
    tconst = 2,
    cconst = -0.8,
    beneficio = 0.065,
    toperativo = 45,
    emisiones = 0.18,
    rendimiento= 0.2,
    factor=0.2
)

termica = FuenteEnergia(
    nombre='Térmica',
    tconst = 3,
    cconst = -0.7,
    beneficio = 0.078,
    toperativo = 30,
    emisiones = 3.24,
    rendimiento= 0.4,
    factor=0.5
)

hidro = FuenteEnergia(
    nombre='Hidroeléctrica',
    tconst = 7,
    cconst = -1,
    beneficio = 0.0064,
    toperativo = 27,
    emisiones = 0.022,
    rendimiento=0.9,
    factor=0.5
)
eolica = FuenteEnergia(
    nombre='Eólica',
    tconst = 9,
    cconst = -0.95,
    beneficio = 0.0057,
    toperativo = 30,
    emisiones = 0.054,
    rendimiento=0.45,
    factor=0.3
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
                            "Factor de carga": fuente.factor
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

# ------------------------------CONSOLA---------------------------------- #

class ConsolaRedirector:
    def __init__(self, widget_output):
        self.output = widget_output

    def write(self, mensaje):
        self.output.moveCursor(QTextCursor.End)
        self.output.insertPlainText(str(mensaje))
        self.output.moveCursor(QTextCursor.End)

    def flush(self):
        pass
    
# ------------------------------VENTANA---------------------------------- #

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

        # FUNCIÓN NUEVAFUENTE

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
                
                # Factor de carga
                factor_text, ok7 = QInputDialog.getText(self, "Nueva fuente", "Inserte factor de carga (0–1):")
                if not ok7 or not factor_text:
                    return
                factor = float(factor_text)
                if factor >= 1:
                    print("El factor de carga debe ser menor que 1.")
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
                rendimiento=rendimiento,
                factor=factor
            )

            nueva_fuente.diccionarioprop = {
                "Nombre de la fuente": nueva_fuente.nombre,
                "Tiempo de construcción (años)": nueva_fuente.tconst,
                "Tiempo operativo (años)": nueva_fuente.toperativo,
                "Costo de construcción (Euros, en negativo)": nueva_fuente.cconst,
                "Beneficio anual (Mill. Euros)": nueva_fuente.beneficio,
                "Emisiones anuales (kg CO2)": nueva_fuente.emisiones,
                "Rendimiento (0-1)": nueva_fuente.rendimiento,
                "Factor de carga": nueva_fuente.factor
            }
            # Botones nueva fuente

            boton_creador = BotonInteractivo(self)
            listafuentes.append(nueva_fuente)
            desplegableizq.addItem(nueva_fuente.nombre, userData=nueva_fuente)
            for boton in boton_creador.botones([nueva_fuente]):
                laypropiedades.addWidget(boton)
            desplegableder.setCurrentIndex(1 if desplegableder.count() > 1 else 0)
            cambiargrafico()
            
        # Conectar función a boton enviar
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
        
        # FUNCIÓN CAMBIOBOTONES
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

    # FUNCIÓN ENVIAR
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

        if etiqueta != "Rendimiento" or "Factor de carga" and abs(valor) < 1:
            print("Seleccione un valor mayor a 1.")
            return
            
        if etiqueta == "Rendimiento" or "Factor de carga" and not (0 < valor < 1):
            print("El valor debe estar entre 0 y 1.")
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
            elif etiqueta == "Factor de carga":
                fuente.factor = valor

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


# ------------------------------BOTONINTERACTIVO---------------------------------- #

class BotonInteractivo: # Clase para crear botones
    def __init__(self, ventana):
        self.ventana = ventana
        self.id_counter = 0 # id de los botones

    def botones(self, fuentes):
        listabotones = []
        for fuente in fuentes:
            for nombre, valor in fuente.diccionarioprop.items():

                if nombre == "Nombre de la fuente": # Título de nombre de fuente
                    boton_widget = QLabel(valor)
                    boton_widget.setAlignment(Qt.AlignCenter)
                    boton_widget.setFont(titulo)

                elif valor is None: # Para creador de nuevas fuentes
                    boton_widget = QPushButton(f"{nombre}: ")
                    boton_widget.setFont(negrita)
                    boton_id = self.id_counter
                    self.ventana.botones_dict[boton_id] = (boton_widget, fuente, nombre)
                    self.id_counter += 1
                    boton_widget.clicked.connect(
                        lambda _, bid=boton_id: self.interactuar(bid)
                    )
                else: # Botones interactivos con propiedades de la fuente
                    boton_widget = QPushButton(f"{nombre}: {valor}") 
                    boton_widget.setFont(negrita)
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

# ------------------------------EJECUTAR---------------------------------- #

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
