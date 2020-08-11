from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
import json


class VentanaInicio(QWidget):
    senal_comenzar = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana de Inicio DCCuatro")
        self.setGeometry(200, 200, 200, 200)
        self.indicacion = QLabel("Usuario:")
        self.nombre = QLineEdit()
        self.nombre.setPlaceholderText("Debe ser alfanumerico")
        self.boton_comenzar = QPushButton("&Comenzar")
        contenedor_h = QHBoxLayout()
        contenedor_v = QVBoxLayout()
        contenedor_h.addWidget(self.indicacion)
        contenedor_h.addWidget(self.nombre)
        contenedor_h.addWidget(self.boton_comenzar)
        self.imagen = QLabel()
        self.imagen.setPixmap(QPixmap("../sprites/logo_2").scaled(300, 200))
        contenedor_v.addWidget(self.imagen)
        contenedor_v.addLayout(contenedor_h)
        self.setLayout(contenedor_v)
        self.boton_comenzar.clicked.connect(self.comenzar)
        self.show()

    def comenzar(self):
        if not self.nombre.text() == "":
            self.senal_comenzar.emit(self.nombre.text())
            self.hide()

    def error_nombre(self):
        self.showNormal()
        self.nombre.setText("")
        self.nombre.setPlaceholderText("Intente con otro nombre")

    def resetear(self):
        self.nombre.setText("")
        self.nombre.setPlaceholderText("Debe ser alfanumerico")
        self.show()


class VentanaEspera(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sala de espera")
        self.setGeometry(200, 200, 200, 200)
        self.lista_jugadores = list()
        with open("parametros.json", "r") as file:
            self.parametros = json.load(file)

        contenedor_h1 = QHBoxLayout()
        contenedor_h2 = QHBoxLayout()
        contenedor_h3 = QHBoxLayout()
        contenedor_v = QVBoxLayout()
        self.imagen = QLabel()
        self.imagen.setPixmap(QPixmap(self.parametros["PATH_LOGO"]).scaled(300, 200))
        contenedor_v.addWidget(self.imagen)
        contenedor_h1.addWidget(QLabel("Jugadores conectados:"))
        contenedor_v.addLayout(contenedor_h1)

        contador = 0
        while contador < self.parametros["NUM_USUARIOS"]:
            jugador = QLabel("[Esperando]")
            jugador.move(100, 100)
            self.lista_jugadores.append(jugador)
            if contador <= 1:
                contenedor_h2.addWidget(jugador)
            else:
                contenedor_h3.addWidget(jugador)
            contador += 1

        contenedor_v.addLayout(contenedor_h2)
        contenedor_v.addLayout(contenedor_h3)
        self.setLayout(contenedor_v)

    def setear_datos(self, lista):
        contador = 0
        self.nombres = lista
        while contador < len(lista):
            self.lista_jugadores[contador].setText(lista[contador])
            self.lista_jugadores[contador].adjustSize()
            contador += 1
        self.show()

    def actualizar(self, nombre):
        if nombre in self.nombres:
            self.nombres.remove(nombre)
        for parte in self.lista_jugadores:
            parte.setText("[Esperando]")
        contador = 0
        while contador < len(self.nombres):
            self.lista_jugadores[contador].setText(self.nombres[contador])
            self.lista_jugadores[contador].adjustSize()
            contador += 1

    def resetear(self):
        for parte in self.lista_jugadores:
            parte.setText("[Esperando]")


class VentanaColor(QWidget):
    senal_color_elegido = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Carta Color DCCuatro")
        self.setGeometry(300, 300, 200, 150)
        contenedor_h1 = QHBoxLayout()
        contenedor_h2 = QHBoxLayout()
        contenedor_v = QVBoxLayout()
        self.rojo = QPushButton("&Rojo")
        self.rojo.clicked.connect(self.senal_rojo)
        self.amarillo = QPushButton("&Amarillo")
        self.amarillo.clicked.connect(self.senal_amarillo)
        self.azul = QPushButton("&Azul")
        self.azul.clicked.connect(self.senal_azul)
        self.verde = QPushButton("&Verde")
        self.verde.clicked.connect(self.senal_verde)
        contenedor_h1.addWidget(self.rojo)
        contenedor_h1.addWidget(self.amarillo)
        contenedor_h2.addWidget(self.verde)
        contenedor_h2.addWidget(self.azul)
        self.mensaje = QLabel("Elija un color:", self)
        contenedor_v.addWidget(self.mensaje)
        contenedor_v.addLayout(contenedor_h1)
        contenedor_v.addLayout(contenedor_h2)
        self.setLayout(contenedor_v)

    def senal_rojo(self):
        self.senal_color_elegido.emit(["rojo", self.carta])
        self.hide()

    def senal_amarillo(self):
        self.senal_color_elegido.emit(["amarillo", self.carta])
        self.hide()

    def senal_azul(self):
        self.senal_color_elegido.emit(["azul", self.carta])
        self.hide()

    def senal_verde(self):
        self.senal_color_elegido.emit(["verde", self.carta])
        self.hide()

    def abrir(self, carta):
        print("hola")
        self.carta = carta
        self.show()


class VentanaTermino(QWidget):
    senal_comenzar_nuevo = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana de Termino DCCuatro")
        self.setGeometry(200, 200, 100, 100)
        contenedor = QVBoxLayout()
        self.texto = QLabel(self)
        self.boton = QPushButton("&Continuar", self)
        self.boton.clicked.connect(self.nuevo)
        contenedor.addWidget(self.texto)
        contenedor.addWidget(self.boton)
        self.setLayout(contenedor)

    def nuevo(self):
        self.senal_comenzar_nuevo.emit()
        self.hide()

    def mensaje(self, texto):
        self.texto.setText(texto)
        self.texto.adjustSize()
        self.show()