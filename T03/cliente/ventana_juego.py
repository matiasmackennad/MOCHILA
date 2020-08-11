from PyQt5.QtWidgets import QLabel, QWidget, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QTransform
import funciones
import json


class VentanaJuego(QWidget):
    senal_robar_carta = pyqtSignal(list)
    senal_jugar_carta = pyqtSignal(list)
    senal_gritar = pyqtSignal(list)
    senal_elegir_color = pyqtSignal(list)
    senal_perder_dccuatro = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 60, 1000, 640)
        self.setWindowTitle("Ventana de juego DCCuatro")
        self.cartas_1 = list()
        self.cartas_2 = list()
        self.cartas_3 = list()
        self.cartas_propias = list()
        self.datos_cartas = list()
        self.nombre_jugador = ""
        self.carta_jugada = None
        self.imagen_carta_jugada = QLabel(self)
        self.vivo = True
        self.cantidad_robar = 0
        self.condicion_masdos = True
        with open("parametros.json", "r") as file:
            self.parametros = json.load(file)

        self.mostrar_cartas_oponentes()

        self.dccuatro = QPushButton("&¡Dccuatro!", self)
        self.dccuatro.clicked.connect(self.gritar)
        self.turno = QLabel("Turno de: ", self)
        self.color = QLabel("Color: ", self)
        self.robar = QLabel("Robar 1 carta", self)
        self.imagen_robar = QLabel(self)
        self.imagen_robar.setPixmap(QPixmap(self.parametros["PATH_REVERSO"]).scaled(200, 280))

        self.dccuatro.move(790, 550)
        self.imagen_robar.move(725, 150)
        self.robar.move(790, 440)
        self.turno.move(750, 50)
        self.color.move(750, 100)

    def mostrar_cartas_oponentes(self):
        self.movedor_1 = 70
        for i in range(0, 4):
            carta = QLabel(self)
            pixmap = QPixmap(self.parametros["PATH_REVERSO"]).scaled(50, 70)
            transform = QTransform().rotate(90)
            pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
            carta.setPixmap(pixmap)
            carta.move(0, self.movedor_1)
            self.movedor_1 += 50
            self.cartas_1.append(carta)
        self.movedor_2 = 70
        for i in range(0, 4):
            carta = QLabel(self)
            pixmap = QPixmap(self.parametros["PATH_REVERSO"]).scaled(50, 70)
            transform = QTransform().rotate(180)
            pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
            carta.setPixmap(pixmap)
            carta.move(self.movedor_2, 0)
            self.movedor_2 += 50
            self.cartas_2.append(carta)
        self.movedor_3 = 70
        for i in range(0, 4):
            carta = QLabel(self)
            pixmap = QPixmap(self.parametros["PATH_REVERSO"]).scaled(50, 70)
            transform = QTransform().rotate(270)
            pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
            carta.setPixmap(pixmap)
            carta.move(570, self.movedor_3)
            self.movedor_3 += 50
            self.cartas_3.append(carta)

    def ajustar_cartas(self):
        self.movedor_1 = 70
        self.movedor_2 = 70
        self.movedor_3 = 70
        for parte in self.cartas_1:
            parte.move(0, self.movedor_1)
            self.movedor_1 += 50
        for parte in self.cartas_2:
            parte.move(self.movedor_2, 0)
            self.movedor_2 += 50
        for parte in self.cartas_3:
            parte.move(570, self.movedor_3)
            self.movedor_3 += 50
        mover_propias = 70
        for parte in self.cartas_propias:
            parte[3].move(mover_propias, 570)
            mover_propias += 50
        mover_1 = (500 - 50 * len(self.cartas_1)) / 2
        for parte in self.cartas_1:
            parte.move(0, parte.y() + mover_1)
        mover_2 = (500 - 50 * len(self.cartas_2)) / 2
        for parte in self.cartas_2:
            parte.move(parte.x() + mover_2, 0)
        mover_3 = (500 - 50 * len(self.cartas_3)) / 2
        for parte in self.cartas_3:
            parte.move(570, parte.y() + mover_3)
        mover_propias = (500 - 50 * len(self.cartas_propias)) / 2
        for parte in self.cartas_propias:
            parte[3].move(parte[3].x() + mover_propias, 570)

    def abrir(self, nombre):
        self.nombre_jugador = nombre
        self.poner_nombres(self.nombre_jugador)
        for dato in self.datos_cartas:
            if dato[0] == self.nombre_jugador:
                self.cartas_propias = funciones.generar_imagen(dato[1])
                movedor = 70
                for carta in self.cartas_propias:
                    imagen = QLabel(self)
                    pix = QPixmap()
                    pix.loadFromData(carta[2])
                    imagen.setPixmap(pix.scaled(50, 70))
                    imagen.move(movedor, 570)
                    carta.append(imagen)
                    movedor += 50
        self.ajustar_cartas()
        self.show()

    def gritar(self):
        if self.vivo:
            self.senal_gritar.emit([self.nombre_jugador, len(self.cartas_propias)])

    def actualizar(self, datos):
        self.datos_cartas = datos[0: len(datos) - 2]
        self.carta_jugada = funciones.generar_imagen(datos[len(datos) - 2])[0]
        self.dato_jugador = datos[len(datos) - 1][0][datos[len(datos) - 1][1]]
        self.lista_usuarios = datos[len(datos) - 1][0]
        self.turno.setText("Turno: " + str(self.dato_jugador))
        self.turno.adjustSize()
        pixmap = QPixmap()
        pixmap.loadFromData(self.carta_jugada[2])
        self.dato_color = self.carta_jugada[0]
        self.dato_tipo = self.carta_jugada[1]
        self.color.setText("Color: " + str(self.dato_color))
        self.color.adjustSize()
        self.imagen_carta_jugada.setPixmap(pixmap.scaled(200, 280))
        self.imagen_carta_jugada.move(220, 180)

    def poner_nombres(self, nombre):
        self.lista_usuarios.remove(nombre)
        self.imagen_nombre = QLabel(nombre, self)
        self.imagen_nombre.move(320, 550)
        self.imagenes_usuarios = list()
        imagen1 = QLabel(self.lista_usuarios[0], self)
        self.imagenes_usuarios.append(imagen1)
        imagen1.move(80, 320)
        if len(self.lista_usuarios) >= 2:
            imagen2 = QLabel(self.lista_usuarios[1], self)
            self.imagenes_usuarios.append(imagen2)
            imagen2.move(320, 80)
        if len(self.lista_usuarios) == 3:
            imagen3 = QLabel(self.lista_usuarios[2], self)
            self.imagenes_usuarios.append(imagen3)
            imagen3.adjustSize()
            imagen3.move(560 - imagen3.width(), 320)

    def mousePressEvent(self, evento):
        if self.dato_jugador == self.nombre_jugador and self.vivo is True and \
                evento.button() == Qt.LeftButton:
            if 725 <= evento.pos().x() <= 925:
                if 150 <= evento.pos().y() <= 430:
                    self.senal_robar_carta.emit([self.nombre_jugador, self.cantidad_robar,
                                                 len(self.cartas_propias)])
            for carta in self.cartas_propias:
                if carta[3].x() <= evento.pos().x() <= carta[3].x() + 50:
                    if carta[3].y() <= evento.pos().y() <= carta[3].y() + 70:
                        if self.dato_color == carta[0] or self.dato_tipo == carta[1] or \
                                carta[1] == "color":
                            if self.condicion_masdos or carta[1] == "+2":
                                if carta[1] != "color":
                                    carta_enviar = funciones.generar_bytes(carta)
                                    self.senal_jugar_carta.emit([self.nombre_jugador, carta_enviar,
                                                                 len(self.cartas_propias)])
                                    carta[3].hide()
                                    self.cartas_propias.remove(carta)
                                if carta[1] == "color":
                                    self.senal_elegir_color.emit(carta)

    def actualizar_robo(self, datos):
        if datos[0] == self.nombre_jugador:
            if len(datos[1]) + len(self.cartas_propias) > self.parametros["CARTAS_MAX"]:
                self.senal_perder_dccuatro.emit()
                self.perder(datos[0])
                return
            movedor = 70
            for carta in self.cartas_propias:
                carta[3].move(movedor, 570)
                movedor += 50
            cartas = funciones.generar_imagen(datos[1])
            for carta in cartas:
                imagen = QLabel(self)
                pix = QPixmap()
                pix.loadFromData(carta[2])
                imagen.setPixmap(pix.scaled(50, 70))
                imagen.show()
                imagen.move(self.cartas_propias[len(self.cartas_propias) - 1][3].x() + 50, 570)
                carta.append(imagen)
                self.cartas_propias.append(carta)
            self.ajustar_cartas()
        else:
            for i in range(0, len(datos[1])):
                carta = QLabel(self)
                pixmap = QPixmap(self.parametros["PATH_REVERSO"]).scaled(50, 70)
                if self.lista_usuarios.index(datos[0]) == 0:
                    if len(self.cartas_1) + len(datos[1]) > 10:
                        self.cantidad_robar = 0
                        self.condicion_masdos = True
                        self.robar.setText("Robar 1 carta")
                        self.robar.adjustSize()
                        carta.hide()
                        return
                    lista = self.cartas_1
                    transform = QTransform().rotate(90)
                elif self.lista_usuarios.index(datos[0]) == 1:
                    if len(self.cartas_2) + len(datos[1]) > 10:
                        self.perder(datos[0])
                        self.cantidad_robar = 0
                        self.condicion_masdos = True
                        self.robar.setText("Robar 1 carta")
                        self.robar.adjustSize()
                        carta.hide()
                        return
                    lista = self.cartas_2
                    transform = QTransform().rotate(180)
                elif self.lista_usuarios.index(datos[0]) == 2:
                    if len(self.cartas_3) + len(datos[1]) > 10:
                        self.perder(datos[0])
                        self.cantidad_robar = 0
                        self.condicion_masdos = True
                        self.robar.setText("Robar 1 carta")
                        self.robar.adjustSize()
                        carta.hide()
                        return
                    lista = self.cartas_3
                    transform = QTransform().rotate(270)
                pixmap = pixmap.transformed(transform, Qt.SmoothTransformation)
                carta.setPixmap(pixmap)
                carta.show()
                lista.append(carta)
            self.ajustar_cartas()
        self.cantidad_robar = 0
        self.condicion_masdos = True
        self.robar.setText("Robar 1 carta")
        self.robar.adjustSize()

    def cambiar_carta(self, datos):
        self.carta_jugada = funciones.generar_imagen(datos[1])[0]
        pix = QPixmap()
        pix.loadFromData(self.carta_jugada[2])
        self.imagen_carta_jugada.setPixmap(pix.scaled(200, 280))
        self.dato_color = self.carta_jugada[0]
        self.color.setText("Color: " + str(self.dato_color))
        self.color.adjustSize()
        self.dato_tipo = self.carta_jugada[1]
        if datos[0] != self.nombre_jugador:
            if self.lista_usuarios.index(datos[0]) == 0:
                self.cartas_1[0].hide()
                self.cartas_1.remove(self.cartas_1[0])
            elif self.lista_usuarios.index(datos[0]) == 1:
                self.cartas_2[0].hide()
                self.cartas_2.remove(self.cartas_2[0])
            elif self.lista_usuarios.index(datos[0]) == 2:
                self.cartas_3[0].hide()
                self.cartas_3.remove(self.cartas_3[0])
        self.ajustar_cartas()

    def color_elegido(self, datos):
        carta = datos[1]
        carta[3].hide()
        self.cartas_propias.remove(carta)
        carta[0] = datos[0]
        carta_enviar = funciones.generar_bytes(carta)
        self.senal_jugar_carta.emit([self.nombre_jugador, carta_enviar, len(self.cartas_propias)])

    def masdos(self):
        self.cantidad_robar += 2
        self.robar.setText(f"Robar {self.cantidad_robar} cartas")
        self.condicion_masdos = False
        self.robar.adjustSize()

    def cambio_turno(self, nombre):
        self.dato_jugador = nombre
        self.turno.setText("Turno: " + str(nombre))
        self.turno.adjustSize()

    def desconectado(self, nombre):
        for parte in self.imagenes_usuarios:
            if parte.text() == nombre:
                parte.setText("[Desconectado]")
                parte.adjustSize()
                if self.imagenes_usuarios.index(parte) == 2:
                    parte.move(560 - parte.width(), 320)

    def perder(self, nombre):
        if nombre == self.nombre_jugador:
            imagen = QLabel("¡Perdiste!", self)
            imagen.move(self.imagen_nombre.x(), self.imagen_nombre.y() - 10)
            self.vivo = False
            imagen.show()
        else:
            mover = 0
            indice = self.lista_usuarios.index(nombre)
            if indice == 2:
                mover = -5
            usuario = self.imagenes_usuarios[indice]
            imagen = QLabel("¡Perdio!", self)
            imagen.move(usuario.x() + mover, usuario.y() + 10)
            imagen.show()

    def resetear(self):
        for parte in self.cartas_1:
            parte.hide()
        for parte in self.cartas_2:
            parte.hide()
        for parte in self.cartas_3:
            parte.hide()
        for parte in self.cartas_propias:
            parte[3].hide()
        for parte in self.imagenes_usuarios:
            parte.hide()
        self.imagen_nombre.hide()
        self.imagenes_usuarios = list()
        self.cartas_1 = list()
        self.cartas_2 = list()
        self.cartas_3 = list()
        self.cartas_propias = list()
        self.datos_cartas = list()
        self.nombre_jugador = ""
        self.carta_jugada = None
        self.imagen_carta_jugada = QLabel(self)
        self.vivo = True
        self.cantidad_robar = 0
        self.condicion_masdos = True
        self.mostrar_cartas_oponentes()