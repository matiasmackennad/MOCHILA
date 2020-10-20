from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
import parametros


class VentanaInicio(QWidget):
    senal_agregar = pyqtSignal(str)
    senal_comenzar = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chumingo!")
        self.setGeometry(100, 100, 480, 200)
        self.ingresar = QLineEdit("")
        self.ingresar.setPlaceholderText("Ingrese un nombre")
        self.boton_ingresar = QPushButton("&Agregar")
        self.boton_ingresar.clicked.connect(self.agregar)
        self.jugadores = 0
        self.mensaje_jugadores = QLabel("Numero de jugadores: " + str(self.jugadores))
        self.boton_comenzar = QPushButton("&Comenzar")
        self.boton_comenzar.clicked.connect(self.comenzar)
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("sprites/logo_chumingo.jpg").scaled(480, 200))

        contenedor_v = QVBoxLayout()
        contenedor_h1 = QHBoxLayout()
        contenedor_h2 = QHBoxLayout()

        contenedor_h1.addWidget(self.ingresar)
        contenedor_h1.addWidget(self.boton_ingresar)
        contenedor_h2.addWidget(self.mensaje_jugadores)
        contenedor_h2.addWidget(self.boton_comenzar)

        contenedor_v.addWidget(self.logo)
        contenedor_v.addLayout(contenedor_h1)
        contenedor_v.addLayout(contenedor_h2)
        self.setLayout(contenedor_v)

    def agregar(self):
        if self.ingresar.text() != "":
            self.ingresar.setPlaceholderText("Ingrese un nombre")
            self.senal_agregar.emit(self.ingresar.text())
            self.jugadores += 1
            self.mensaje_jugadores.setText("Numero de jugadores: " + str(self.jugadores))
            self.ingresar.setText("")

    def comenzar(self):
        if self.jugadores != 0:
            self.senal_comenzar.emit()
            self.hide()

    def error_nombre(self):
        self.ingresar.setPlaceholderText("Trate otro nombre")
        self.jugadores -= 1
        self.mensaje_jugadores.setText("Numero de jugadores: " + str(self.jugadores))


class VentanaJuego(QWidget):
    senal_jugar = pyqtSignal()
    senal_penitencia = pyqtSignal(list)
    senal_primero = pyqtSignal()
    senal_saltar = pyqtSignal()
    senal_agregar = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chumingo!")
        self.setGeometry(100, 100, 800, 400)
        self.jugador = QLabel("Jugando: ")
        self.vasos = QLabel("Vasos: ")
        self.tragos = QLabel("Tragos restantes: " + str(parametros.TRAGOS_VASO))
        self.nombre = ""
        self.condicion = True
        self.primero = True
        self.boton_jugar = QPushButton("&Tirar dado")
        self.boton_jugar.clicked.connect(self.jugar)
        self.dado_1 = QLabel(self)
        self.dado_1.setPixmap(QPixmap("sprites/vacio.png").scaled(250, 250))
        self.dado_2 = QLabel(self)
        self.dado_2.setPixmap(QPixmap("sprites/vacio.png").scaled(250, 250))
        self.boton_saltar = QPushButton("&Saltar")
        self.boton_saltar.clicked.connect(self.senal_saltar.emit)
        self.boton_agregar = QPushButton("&Agregar")
        self.boton_agregar.clicked.connect(self.senal_agregar.emit)

        contenedor_v = QVBoxLayout()
        contenedor_h1 = QHBoxLayout()
        contenedor_h2 = QHBoxLayout()
        contenedor_h3 = QHBoxLayout()

        contenedor_h1.addWidget(self.jugador)
        contenedor_h1.addWidget(self.vasos)
        contenedor_h1.addWidget(self.tragos)

        contenedor_h2.addWidget(self.dado_1)
        contenedor_h2.addWidget(self.dado_2)

        contenedor_h3.addWidget(self.boton_agregar)
        contenedor_h3.addWidget(self.boton_saltar)
        contenedor_h3.addWidget(self.boton_jugar)

        contenedor_v.addLayout(contenedor_h1)
        contenedor_v.addLayout(contenedor_h2)
        contenedor_v.addLayout(contenedor_h3)
        self.setLayout(contenedor_v)

    def comenzar(self, datos):
        self.show()
        self.pasar_turno(datos)

    def pasar_turno(self, datos):
        self.condicion = True
        self.primero = True
        self.nombre = str(datos[0])
        self.jugador.setText("Jugando: " + str(datos[0]))
        self.jugador.adjustSize()
        self.vasos.setText("Vasos: " + str(datos[1]))
        self.vasos.adjustSize()
        self.tragos.setText("Tragos restantes: " + str(datos[2]))
        self.dado_1.setPixmap(QPixmap("sprites/vacio.png").scaled(250, 250))
        self.dado_2.setPixmap(QPixmap("sprites/vacio.png").scaled(250, 250))

    def jugar(self):
        if self.condicion:
            if self.primero:
                self.senal_primero.emit()
                self.primero = False
            else:
                self.senal_jugar.emit()
                self.condicion = False

    def jugada(self, dados):
        self.dado_1.setPixmap(QPixmap("sprites/" + str(dados[1]) + ".png").scaled(250, 250))
        self.dado_1.show()
        self.dado_2.setPixmap(QPixmap("sprites/" + str(dados[2]) + ".png").scaled(250, 250))
        self.dado_2.show()
        self.senal_penitencia.emit([dados[0], self.nombre, dados[3], dados[4]])

    def primer_dado(self, numero):
        self.dado_1.setPixmap(QPixmap("sprites/" + numero + ".png").scaled(250, 250))
        self.dado_1.show()


class VentanaPenitencia(QWidget):
    senal_tomar = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Penitencia")
        self.setGeometry(900, 100, 300, 200)
        self.mensaje = QLabel("2 tragos")
        self.toma = QLineEdit("")
        self.toma.setPlaceholderText("Quien Toma?")
        self.boton = QPushButton("&Aceptar")
        self.boton.clicked.connect(self.aceptar)
        self.numero = 0
        self.jugadores = list()
        contenedor_h = QHBoxLayout()
        contenedor_v = QVBoxLayout()

        contenedor_h.addWidget(self.toma)
        contenedor_h.addWidget(self.boton)

        contenedor_v.addWidget(self.mensaje)
        contenedor_v.addLayout(contenedor_h)
        self.setLayout(contenedor_v)

    def aceptar(self):
        if self.toma.text() in self.jugadores:
            self.senal_tomar.emit([self.toma.text(), self.numero])
            self.toma.setPlaceholderText("Quien Toma?")
            self.hide()
        else:
            self.error_nombre()

    def mostrar(self, datos):
        self.numero = datos[2]
        self.jugadores = datos[3]
        if datos[0] == "tomar":
            self.toma.hide()
            self.toma.setText(datos[1])
            if self.numero != parametros.TRAGOS_VASO:
                self.mensaje.setText(str(datos[1]) + " debe tomar " + str(self.numero) + " tragos")
            else:
                self.mensaje.setText(str(datos[1]) + " debe matarla")
        elif datos[0] == "regalar":
            self.toma.setText("")
            self.toma.show()
            if self.numero != parametros.TRAGOS_VASO:
                self.mensaje.setText(str(datos[1]) + " regala " + str(self.numero) + " tragos")
            else:
                self.mensaje.setText(str(datos[1]) + " regala matada")
        elif datos[0] == "chancho":
            self.toma.setText("")
            self.toma.show()
            self.mensaje.setText("El ultimo en poner ese numero en la frente la mata")
        elif datos[0] == "dado caido":
            self.mensaje.setText("Se te ha caido el dado, la debes matar")
            self.toma.setText(datos[1])
            self.toma.hide()
        self.show()

    def error_nombre(self):
        self.toma.setText("")
        self.toma.setPlaceholderText("Trate otro nombre")


class VasoTerminado(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vaso Terminado")
        self.setGeometry(900, 300, 300, 200)
        self.mensaje = QLabel("2 tragos")
        self.boton = QPushButton("&Aceptar")
        self.boton.clicked.connect(self.aceptar)
        contenedor_v = QVBoxLayout()
        contenedor_v.addWidget(self.mensaje)
        contenedor_v.addWidget(self.boton)
        self.setLayout(contenedor_v)

    def aceptar(self):
        self.hide()

    def mostrar(self, nombre):
        self.mensaje.setText(f"a {nombre} se le acabo el vaso, debe matar lo que le queda")
        self.show()


class VentanaAgregar(QWidget):
    senal_agregar_extra = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Usuario")
        self.setGeometry(300, 300, 300, 100)
        self.boton = QPushButton("&Agregar")
        self.boton.clicked.connect(self.agregar)
        self.linea = QLineEdit("")
        self.linea.setPlaceholderText("Ingresa un usuario")
        self.usuarios = list()

        contenedor_h = QHBoxLayout()
        contenedor_h.addWidget(self.linea)
        contenedor_h.addWidget(self.boton)
        self.setLayout(contenedor_h)

    def agregar(self):
        if self.linea.text() not in self.usuarios and self.linea.text() != "":
            self.senal_agregar_extra.emit(self.linea.text())
            self.hide()
        else:
            self.linea.setPlaceholderText("Intente otro nombre")
            self.linea.setText("")

    def mostrar(self, usuarios):
        self.usuarios = usuarios
        self.linea.setPlaceholderText("Ingresa un usuario")
        self.linea.setText("")
        self.show()
