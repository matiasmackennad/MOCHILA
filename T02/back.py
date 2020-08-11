from PyQt5.QtCore import pyqtSignal, QObject, QThread
import time
import parametros
import random


class Tiempo(QThread):

    def __init__(self, evento, pausa):
        super().__init__()
        self.pausa = pausa
        self. evento = evento
        self.condicion = True

    def run(self):
        while self.condicion:
            self.pausa.wait()
            time.sleep(parametros.VEL_TIEMPO)
            self.pausa.wait()
            self.evento.set()
            self.evento.clear()

    def setear_pausa(self):
        if self.pausa.isSet():
            self.pausa.clear()
        else:
            self.pausa.set()


class Chef(QThread):

    def __init__(self, platos, senal_tiempo, dccafe, pos_x, pos_y):
        super().__init__()
        self.platos = platos
        self.cocinando = False
        self.listo = False
        self.nivel = 0
        self.calcular_nivel()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.bocadillo = list()
        self.senal_tiempo = senal_tiempo
        self.dccafe = dccafe

    def calcular_nivel(self):
        if self.platos >= parametros.PLATOS_EXPERTO:
            self.nivel = 3
        elif self.platos >= parametros.PLATOS_INTERMEDIO:
            self.nivel = 2
        else:
            self.nivel = 1

    def run(self):
        contador = 0
        self.dccafe.senal_chef_partir.emit(["chef", self.pos_x, self.pos_y])
        self.cocinando = True
        while self.cocinando:
            self.senal_tiempo.wait()
            contador += 1
            if contador == max(0, 15 - self.dccafe.reputacion - self.nivel):
                self.cocinando = False
        if random.random() <= 0.3 / (self.nivel + 1):
            self.dccafe.senal_chef_fallar.emit(["chef", self.pos_x, self.pos_y])
            self.listo = False
        else:
            self.dccafe.senal_chef_listo.emit(["chef", self.pos_x, self.pos_y])
            self.listo = True
            self.platos += 1
            self.bocadillo.append(Bocadillo(self.senal_tiempo, self.nivel))
            self.calcular_nivel()


class Mesero(QObject):
    senal_actualizar_mesero = pyqtSignal(dict)

    def __init__(self, dccafe):
        super().__init__()
        self.__x = parametros.LIMITE_MAPA_X[0]
        self.__y = parametros.LIMITE_MAPA_Y[0]
        self.__frame = 1
        self.dccafe = dccafe
        self.atendiendo = False
        self.bocadillo = list()

    @property
    def frame(self):
        return self.__frame

    @frame.setter
    def frame(self, value):
        if 2 < value:
            self.__frame = 0
        else:
            self.__frame = value

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, value):
        if self.atendiendo:
            if value > self.x:
                sprite = parametros.RUTA_MESERO_ATENDIENDO_DERECHA
            if value < self.x:
                sprite = parametros.RUTA_MESERO_ATENDIENDO_IZQUIERDA
        else:
            if value > self.x:
                sprite = parametros.RUTA_MESERO_DERECHA
            if value < self.x:
                sprite = parametros.RUTA_MESERO_IZQUIERDA
        extra_x = parametros.FORMA_MESERO[0] / 2
        extra_y = parametros.FORMA_MESERO[1] / 2
        condicion_colision = True
        contador = 0
        for parte in self.dccafe.mesas:
            if int(parte[1]) <= value + extra_x <= int(parte[1]) + parametros.FORMA_MESA[0]:
                if int(parte[2]) <= self.y + extra_y <= int(parte[2]) + parametros.FORMA_MESA[1]:
                    condicion_colision = False
                    self.dccafe.colision([parte, contador])
            contador += 1
        contador = 0
        for parte in self.dccafe.chefs:
            if int(parte[1]) <= value + extra_x <= int(parte[1]) + parametros.FORMA_CHEF[0]:
                if int(parte[2]) <= self.y + extra_y <= int(parte[2]) + parametros.FORMA_CHEF[1]:
                    condicion_colision = False
                    self.dccafe.colision([parte, contador])
            contador += 1
        if parametros.LIMITE_MAPA_X[0] < value < parametros.LIMITE_MAPA_X[1] and condicion_colision:
            self.__x = value
        self.senal_actualizar_mesero.emit(
            {'char': 'mesero',
            'x': self.x,
            'y': self.y,
            "frame": self.frame,
            "sprite": sprite
            })

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, value):
        if self.atendiendo:
            if value > self.y:
                sprite = parametros.RUTA_MESERO_ATENDIENDO_ABAJO
            if value < self.y:
                sprite = parametros.RUTA_MESERO_ATENDIENDO_ARRIBA
        else:
            if value > self.y:
                sprite = parametros.RUTA_MESERO_ABAJO
            if value < self.y:
                sprite = parametros.RUTA_MESERO_ARRIBA
        extra_x = parametros.FORMA_MESERO[0] / 2
        extra_y = parametros.FORMA_MESERO[1] / 2
        condicion_colision = True
        contador = 0
        for parte in self.dccafe.mesas:
            if int(parte[2]) <= value + extra_y <= int(parte[2]) + parametros.FORMA_MESA[1]:
                if int(parte[1]) <= self.x + extra_x <= int(parte[1]) + parametros.FORMA_MESA[0]:
                    condicion_colision = False
                    self.dccafe.colision([parte, contador])
            contador += 1
        contador = 0
        for parte in self.dccafe.chefs:
            if int(parte[2]) <= value + extra_y <= int(parte[2]) + parametros.FORMA_CHEF[1]:
                if int(parte[1]) <= self.x + extra_x <= int(parte[1]) + parametros.FORMA_CHEF[0]:
                    condicion_colision = False
                    self.dccafe.colision([parte, contador])
            contador += 1
        if parametros.LIMITE_MAPA_Y[0] < value < parametros.LIMITE_MAPA_Y[1] and condicion_colision:
            self.__y = value
        self.senal_actualizar_mesero.emit(
            {'char': 'mesero',
            'x': self.x,
            'y': self.y,
            "frame": self.frame,
            "sprite": sprite
            })

    def move(self, event):
        if self.dccafe.estado == "ronda" and self.dccafe.pausa.isSet():
            self.frame += 1
            if event == 'd':
                self.x += parametros.VEL_MOV
            if event == 'a':
                self.x -= parametros.VEL_MOV
            if event == 'w':
                self.y -= parametros.VEL_MOV
            if event == 's':
                self.y += parametros.VEL_MOV
        if event == "mon":
            self.dccafe.dinero += parametros.DINERO_TRAMPA
        if event == "rtg":
            self.dccafe.reputacion += parametros.REPUTACION_TRAMPA
        if event == "fin":
            self.dccafe.clientes_atendidos = self.dccafe.totales
            for cliente in self.dccafe.clientes:
                self.dccafe.senal_cliente_llendose.emit([cliente.id_cliente, 0])

    def setear_posicion(self, posicion):
        self.x = posicion[0]
        self.y = posicion[1]


class Cliente(QThread):
    def __init__(self, tipo, tiempo, dccafe, id_cliente):
        super().__init__()
        self.tipo = tipo
        self.tiempo = tiempo
        self.dccafe = dccafe
        self.bocadillo = None
        self.id_cliente = id_cliente
        self.condicion = True
        if self.tipo == "apurado":
            self.espera = parametros.TIEMPO_ESPERA_APURADO
        else:
            self.espera = parametros.TIEMPO_ESPERA_RELAJADO

    def run(self):
        contador = 0
        condicion_enojado = True
        while contador <= self.espera and self.condicion:
            self.tiempo.wait()
            contador += 1
            if contador >= self.espera / 2 and condicion_enojado:
                self.dccafe.senal_cliente_enojado.emit(self.id_cliente)
                condicion_enojado = False
        if not self.condicion:
            time.sleep(parametros.TIEMPO_COMER)
            self.dccafe.senal_cliente_llendose.emit([self.id_cliente, self.bocadillo.calidad])
        else:
            self.dccafe.senal_cliente_llendose.emit([self.id_cliente, 0])
        self.dccafe.clientes_atendidos += 1
        self.dccafe.mesas_disponibles += 1


class Bocadillo(QThread):
    def __init__(self, senal_tiempo, nivel):
        super().__init__()
        self.tiempo = 0
        self.senal_tiempo = senal_tiempo
        self.entregado = False
        self.calidad = 0
        self.nivel = nivel

    def run(self):
        while self.entregado is False:
            self.senal_tiempo.wait()
            self.tiempo += 1
        self.calidad = max(0, (self.nivel * (1 - self.tiempo * 0.05)) / 3)
