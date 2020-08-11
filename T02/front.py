from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
import parametros
import funciones


class VentanaInicio(QWidget):
    senal_partir = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana Inicial DCCafe")
        self.setGeometry(200, 100, 300, 200)
        contenedor_h = QHBoxLayout()
        contenedor_v = QVBoxLayout()
        pixeles = QPixmap(parametros.RUTA_LOGO_BLANCO).scaled(260.8, 100)
        self.foto = QLabel()
        self.foto.setPixmap(pixeles)
        self.mensaje = QLabel("¡Bienvenido al mejor cafe virtual del DCC!")
        self.boton_cargar = QPushButton("Seguir jugando")
        self.boton_comenzar = QPushButton("Comenzar de nuevo")
        contenedor_h.addWidget(self.boton_cargar)
        contenedor_h.addWidget(self.boton_comenzar)
        contenedor_v.addWidget(self.foto)
        contenedor_v.addWidget(self.mensaje)
        contenedor_v.addLayout(contenedor_h)
        self.setLayout(contenedor_h)
        self.setLayout(contenedor_v)
        self.boton_cargar.clicked.connect(self.cargar_partida)
        self.boton_comenzar.clicked.connect(self.comenzar_partida)

    def cargar_partida(self):
        lista = funciones.cargar_partida()
        self.senal_partir.emit([lista, "pre-ronda"])
        self.hide()

    def comenzar_partida(self):
        lista = funciones.crear_partida()
        self.senal_partir.emit([lista, "ronda"])
        self.hide()


class Mesa(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPixmap(QPixmap(parametros.RUTA_MESA).scaled(*parametros.FORMA_MESA))
        self.tipo = "mesa"
        self.ocupada = False


class Chef(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setPixmap(QPixmap(parametros.RUTA_CHEF).scaled(*parametros.FORMA_CHEF))
        self.tipo = "chef"


class VentanaFinal(QWidget):
    senal_guardar = pyqtSignal()
    senal_continuar = pyqtSignal()
    senal_salir = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana de post-ronda")
        self.setGeometry(200, 200, 400, 200)
        self.ronda = QLabel(self)
        self.dinero = QLabel(self)
        self.perdidos = QLabel(self)
        self.atendidos = QLabel(self)
        self.reputacion = QLabel(self)
        self.boton_guardar = QPushButton("&Guardar", self)
        self.boton_salir = QPushButton("&Salir", self)
        self.boton_continuar = QPushButton("&Continuar", self)
        cont_v = QVBoxLayout()
        cont_h = QHBoxLayout()
        cont_h.addWidget(self.boton_guardar)
        cont_h.addWidget(self.boton_salir)
        cont_h.addWidget(self.boton_continuar)
        cont_v.addWidget(self.ronda)
        cont_v.addWidget(self.atendidos)
        cont_v.addWidget(self.perdidos)
        cont_v.addWidget(self.dinero)
        cont_v.addWidget(self.reputacion)
        cont_v.addLayout(cont_h)
        self.setLayout(cont_h)
        self.setLayout(cont_v)
        self.boton_continuar.clicked.connect(self.continuar)
        self.boton_salir.clicked.connect(self.salir)
        self.boton_guardar.clicked.connect(self.guardar)

    def abrir(self, datos):
        self.ronda.setText("Resumen Ronda Numero: " + str(datos[2]))
        self.ronda.adjustSize()
        self.dinero.setText("Dinero Acomulado: " + str(datos[0]))
        self.dinero.adjustSize()
        self.perdidos.setText("Clientes Perdidos: " + str(datos[3]))
        self.perdidos.adjustSize()
        self.atendidos.setText("Clientes Atendidos: " + str(datos[1]))
        self.atendidos.adjustSize()
        if datos[4] == 0:
            self.reputacion.setText("Reputacion: " + str(datos[4]) + "/5 ¡Perdiste!")
        else:
            self.reputacion.setText("Reputacion: " + str(datos[4]) + "/5")
        self.reputacion.adjustSize()
        self.show()

    def guardar(self):
        self.senal_guardar.emit()

    def continuar(self):
        self.senal_continuar.emit()
        self.hide()

    def salir(self):
        self.senal_salir.emit()
        self.close()
