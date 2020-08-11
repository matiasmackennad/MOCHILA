from PyQt5.QtWidgets import QLabel, QWidget, QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from DragDrop import DropLabel, DraggableLabel
from front import Mesa, Chef
import parametros
import random


class VentanaPrincipal(QWidget):
    senal_pausar = pyqtSignal()
    senal_mover_mesero = pyqtSignal(str)
    senal_setear_mesero = pyqtSignal(list)
    senal_setear_dccafe = pyqtSignal(list)
    senal_agregar_imagen = pyqtSignal(list)
    senal_eliminar = pyqtSignal(list)
    senal_comenzar_ronda = pyqtSignal()
    senal_actualizar_clientes_mesa = pyqtSignal(list)
    senal_actualizar_datos = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.mesas = list()
        self.chefs = list()
        self.cliente_mesa = list()
        self.bocadillos = list()
        self.string = ""
        self.ganancias = 0

        self.setWindowTitle("Ventana Principal DCCafe")
        self.setGeometry(200, 100, 564, 372)
        self.mapa = DropLabel(self, self)
        self.mapa.setPixmap(QPixmap(parametros.RUTA_MAPA).scaled(414, 312))
        self.mapa.move(0, 60)

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap(parametros.RUTA_LOGO_NEGRO).scaled(130.4, 50))

        self.reputacion = QLabel("Reputacion:", self)
        self.reputacion.move(150, 0)
        self.dinero = QLabel("Dinero:", self)
        self.dinero.move(150, 20)
        self.ronda = QLabel("Ronda:", self)
        self.ronda.move(150, 40)
        self.atendidos = QLabel("Atendidos:", self)
        self.atendidos.move(300, 0)
        self.perdidos = QLabel("Perdidos:", self)
        self.perdidos.move(300, 20)
        self.proximos = QLabel("Proximos:", self)
        self.proximos.move(300, 40)

        self.boton_pausar = QPushButton("&Pausar", self)
        self.boton_pausar.clicked.connect(self.pausar)
        self.boton_pausar.move(470, 10)
        self.boton_salir = QPushButton("&Salir", self)
        self.boton_salir.clicked.connect(self.salir)
        self.boton_salir.move(470, 30)
        self.boton_comenzar = QPushButton("&Comenzar", self)
        self.boton_comenzar.hide()
        self.boton_comenzar.clicked.connect(self.comenzar_ronda)
        self.boton_comenzar.move(220, 35)

        self.tienda = QLabel("Tienda:", self)
        self.tienda.move(470, 80)
        self.tienda_chef = DraggableLabel(self, "chef", self)
        self.tienda_chef.setPixmap(QPixmap(parametros.RUTA_CHEF).scaled(*parametros.FORMA_CHEF))
        self.tienda_chef.move(460, 120)
        self.precio_chef = QLabel("$" + str(parametros.PRECIO_CHEF), self)
        self.precio_chef.move(480, 180)
        self.tienda_mesa = DraggableLabel(self, "mesa", self)
        self.tienda_mesa.setPixmap(QPixmap(parametros.RUTA_MESA).scaled(*parametros.FORMA_MESA))
        self.tienda_mesa.move(480, 240)
        self.precio_mesa = QLabel("$" + str(parametros.PRECIO_MESA), self)
        self.precio_mesa.move(480, 285)

    def pausar(self):
        if self.estado == "ronda":
            if self.boton_pausar.text() == "&Pausar":
                self.boton_pausar.setText("&Seguir")
            else:
                self.boton_pausar.setText("&Pausar")
            self.senal_pausar.emit()

    def cargar_partida(self, datos):
        self.show()
        if not len(self.chefs) == 0:
            for chef in self.chefs:
                chef.clear()
            self.chefs = list()
        if not len(self.mesas) == 0:
            for mesa in self.mesas:
                mesa.clear()
            self.mesas = list()
            self.mesero.clear()
        for parte in datos[0]:
            if parte[0] == "mesero":
                self.mesero = QLabel(self)
                self.mesero.setPixmap(QPixmap(parametros.RUTA_MESERO_ABAJO[1]).scaled(*parametros.
                                                                                      FORMA_MESERO))
                self.mesero.move(int(parte[1]), int(parte[2]))
                self.senal_setear_mesero.emit([int(parte[1]), int(parte[2])])
                self.mesero.show()
            elif parte[0] == "mesa":
                imagen = Mesa(self)
                imagen.move(int(parte[1]), int(parte[2]))
                self.mesas.append(imagen)
                imagen.show()
                imagen.raise_()
            elif parte[0] == "chef":
                imagen = Chef(self)
                imagen.move(int(parte[1]), int(parte[2]))
                self.chefs.append(imagen)
                imagen.show()
                imagen.raise_()
        self.estado = datos[1]
        if self.estado == "pre-ronda":
            self.boton_comenzar.show()
        self.senal_setear_dccafe.emit(datos)

    def salir(self):
        self.close()

    def keyPressEvent(self, event):
        self.string += event.text()
        largo = len(self.string)
        if self.string[largo - 3: largo] == "mon":
            self.dato_dinero += parametros.DINERO_TRAMPA
            self.dinero.setText("Dinero: " + str(self.dato_dinero))
            self.dinero.adjustSize()
            self.senal_mover_mesero.emit("mon")
            self.string = ""
        if self.string[largo - 3: largo] == "rtg":
            if self.dato_reputacion + parametros.REPUTACION_TRAMPA > 5:
                self.dato_reputacion = 5
            else:
                self.dato_reputacion += parametros.REPUTACION_TRAMPA
            self.reputacion.setText("Reputacion: " + str(self.dato_reputacion))
            self.reputacion.adjustSize()
            self.senal_mover_mesero.emit("rtg")
            self.string = ""
        if self.string[largo - 3: largo] == "fin":
            if self.estado == "ronda":
                self.dato_clientes_perdidos = self.totales - self.dato_clientes_atendidos
                self.dato_clientes_proximos = 0
                self.proximos.setText("Proximos: " + str(self.dato_clientes_proximos))
                self.perdidos.setText("Perdidos: " + str(self.dato_clientes_perdidos))
                self.perdidos.adjustSize()
                self.proximos.adjustSize()
                self.senal_mover_mesero.emit("fin")
        if self.estado == "ronda":
            if event.text() == "w":
                self.senal_mover_mesero.emit('w')
            if event.text() == "s":
                self.senal_mover_mesero.emit('s')
            if event.text() == "d":
                self.senal_mover_mesero.emit('d')
            if event.text() == "a":
                self.senal_mover_mesero.emit('a')

    def update_position(self, event):
        char = self.mesero
        pixmap = QPixmap(str(event["sprite"][event["frame"]]))
        char.setPixmap(pixmap)
        char.adjustSize()
        char.move(event['x'], event['y'])
        self.update()

    def agregar(self, datos):
        if datos[1] == "mesa":
            imagen = Mesa(self)
            self.mesas.append(imagen)
            precio = parametros.PRECIO_MESA
        elif datos[1] == "chef":
            imagen = Chef(self)
            self.chefs.append(imagen)
            precio = parametros.PRECIO_CHEF
        if precio <= self.dato_dinero:
            self.dato_dinero -= precio
            self.dinero.setText("Dinero: " + str(self.dato_dinero))
            self.dinero.adjustSize()
            imagen.move(int(datos[0][0]), int(datos[0][1]))
            pos_x = str(imagen.x())
            pos_y = str(imagen.y())
            self.senal_agregar_imagen.emit([datos[1], pos_x, pos_y])
            imagen.show()

    def mousePressEvent(self, evento):
        if self.estado == "pre-ronda":
            if evento.button() == Qt.LeftButton:
                pos_evento_x = evento.pos().x()
                pos_evento_y = evento.pos().y()
                for mesa in self.mesas:
                    pos_mesa_x = mesa.x()
                    pos_mesa_y = mesa.y()
                    if pos_mesa_x <= pos_evento_x <= pos_mesa_x + parametros.FORMA_MESA[0]:
                        if pos_mesa_y <= pos_evento_y <= pos_mesa_y + parametros.FORMA_MESA[1]:
                            if len(self.mesas) > 1:
                                mesa.hide()
                                self.mesas.remove(mesa)
                                self.senal_eliminar.emit(["mesa", str(pos_mesa_x), str(pos_mesa_y)])
                for chef in self.chefs:
                    pos_chef_x = chef.x()
                    pos_chef_y = chef.y()
                    if pos_chef_x <= pos_evento_x <= pos_chef_x + parametros.FORMA_CHEF[0]:
                        if pos_chef_y <= pos_evento_y <= pos_chef_y + parametros.FORMA_CHEF[1]:
                            if len(self.chefs) > 1:
                                chef.hide()
                                self.chefs.remove(chef)
                                self.senal_eliminar.emit(["chef", str(pos_chef_x), str(pos_chef_y)])

    def comenzar_ronda(self):
        if self.estado == "pre-ronda":
            self.boton_comenzar.hide()
            self.ganancias = 0
            self.estado = "ronda"
            self.senal_comenzar_ronda.emit()

    def completar_datos(self, datos):
        self.dato_clientes_proximos = datos[3]
        self.totales = datos[3]
        self.dato_ronda = datos[0]
        self.dato_reputacion = datos[1]
        self.dato_dinero = datos[2]
        self.dato_clientes_atendidos = 0
        self.dato_clientes_perdidos = 0
        self.reputacion.setText("Reputacion: " + str(self.dato_reputacion) + "/5")
        self.reputacion.adjustSize()
        self.ronda.setText("Ronda: " + str(self.dato_ronda))
        self.ronda.adjustSize()
        self.proximos.setText("Proximos: " + str(self.dato_clientes_proximos))
        self.proximos.adjustSize()
        self.dinero.setText("Dinero: " + str(self.dato_dinero))
        self.dinero.adjustSize()
        self.atendidos.setText("Atendidos: " + str(self.dato_clientes_atendidos))
        self.atendidos.adjustSize()
        self.perdidos.setText("Perdidos: " + str(self.dato_clientes_perdidos))
        self.perdidos.adjustSize()

    def agregar_cliente(self, cliente):
        condicion = True
        for mesa in self.mesas:
            if not mesa.ocupada and condicion:
                imagen_cliente = QLabel(self)
                if cliente[1] == "apurado":
                    imagen_cliente.setPixmap(QPixmap(parametros.RUTA_CLIENTE_APURADO).scaled(23.2,
                                                                                             27.4))
                    imagen_cliente.move(mesa.x(), mesa.y() - 10)
                else:
                    imagen_cliente.setPixmap(QPixmap(parametros.RUTA_CLIENTE_RELAJADO).scaled(18.6,
                                                                                              25.3))
                    imagen_cliente.move(mesa.x() + 2, mesa.y() - 9)
                imagen_cliente.show()
                imagen_cliente.raise_()
                mesa.ocupada = True
                self.senal_actualizar_clientes_mesa.emit([cliente, mesa, "agregar"])
                self.cliente_mesa.append([cliente, mesa, imagen_cliente])
                self.dato_clientes_proximos -= 1
                self.proximos.setText("Proximos: " + str(self.dato_clientes_proximos))
                self.proximos.adjustSize()
                condicion = False

    def cliente_enojado(self, id_cliente):
        for cliente in self.cliente_mesa:
            if cliente[0][0] == id_cliente:
                if cliente[0][1] == "apurado":
                    ruta = parametros.RUTA_CLIENTE_APURADO_ENOJADO
                    pos_x = cliente[1].x() - 14
                    pos_y = cliente[1].y() - 30
                else:
                    ruta = parametros.RUTA_CLIENTE_RELAJADO_ENOJADO
                    pos_x = cliente[1].x() - 15
                    pos_y = cliente[1].y() - 25
                cliente[2].setPixmap(QPixmap(ruta).scaled(50, 50))
                cliente[2].adjustSize()
                cliente[2].move(pos_x, pos_y)

    def cliente_llendose(self, datos):
        id_cliente = datos[0]
        prob_propina = datos[1]
        for cliente in self.cliente_mesa:
            if cliente[0][0] == id_cliente:
                cliente[1].ocupada = False
                cliente[2].hide()
                eliminar_cliente = cliente[0:2] + ["eliminar"]
                self.senal_actualizar_clientes_mesa.emit(eliminar_cliente)
                self.cliente_mesa.remove(cliente)
        condicion = False
        for parte in self.bocadillos:
            if parte[0] == id_cliente:
                condicion = True
                bocadillo = parte[1]
                break
        if condicion:
            bocadillo.hide()
            self.bocadillos.remove([id_cliente, bocadillo])
            self.dato_dinero += parametros.PRECIO_BOCADILLOS
            self.ganancias += parametros.PRECIO_BOCADILLOS
            if random.random() <= prob_propina:
                self.dato_dinero += parametros.PROPINA
                self.ganancias += parametros.PROPINA
            self.dinero.setText("Dinero: " + str(self.dato_dinero))
            self.dinero.adjustSize()
        else:
            self.dato_clientes_perdidos += 1
            self.perdidos.setText("Perdidos: " + str(self.dato_clientes_perdidos))
            self.perdidos.adjustSize()

    def chef_partir(self, datos):
        for chef in self.chefs:
            if int(datos[1]) == chef.x() and int(datos[2]) == chef.y():
                pixmap = QPixmap(parametros.RUTA_CHEF_COCINANDO).scaled(*parametros.FORMA_CHEF)
                chef.setPixmap(pixmap)

    def chef_listo(self, datos):
        for chef in self.chefs:
            if int(datos[1]) == chef.x() and int(datos[2]) == chef.y():
                chef.setPixmap(QPixmap(parametros.RUTA_CHEF_LISTO).scaled(*parametros.FORMA_CHEF))

    def resetear_chef(self, datos):
        for chef in self.chefs:
            if int(datos[1]) == chef.x() and int(datos[2]) == chef.y():
                chef.setPixmap(QPixmap(parametros.RUTA_CHEF).scaled(*parametros.FORMA_CHEF))

    def cliente_atendido(self, id_cliente):
        numero = random.randint(1, 68)
        if numero // 10 == 0:
            numero = "0" + str(numero)
        else:
            numero = str(numero)
        for parte in self.cliente_mesa:
            if parte[0][0] == id_cliente:
                pos_x = parte[1].x()
                pos_y = parte[1].y()
        pixmap = QPixmap(parametros.RUTA_BOCADILLOS + numero)
        bocadillo = QLabel(self)
        bocadillo.setPixmap(pixmap)
        bocadillo.adjustSize()
        bocadillo.move(pos_x + 2.5, pos_y + 15)
        bocadillo.show()
        self.dato_clientes_atendidos += 1
        self.atendidos.setText("Atendidos: " + str(self.dato_clientes_atendidos))
        self.bocadillos.append([id_cliente, bocadillo])
        self.atendidos.adjustSize()

    def ronda_acabada(self):
        self.estado = "post-ronda"
        self.senal_actualizar_datos.emit([self.ganancias, self.dato_clientes_atendidos,
                                          self.dato_clientes_perdidos])

    def continuar(self, datos):
        self.estado = "pre-ronda"
        self.ganancias = 0
        self.boton_comenzar.show()
        self.cliente_mesa = list()
        self.bocadillos = list()
        self.completar_datos(datos)
