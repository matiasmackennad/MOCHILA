import parametros
from PyQt5.QtCore import pyqtSignal, QObject
from random import randint, random


class Juego(QObject):
    senal_nombre_malo = pyqtSignal()
    senal_partir = pyqtSignal(list)
    senal_dados = pyqtSignal(list)
    senal_vaso_terminado = pyqtSignal(str)
    senal_turno = pyqtSignal(list)
    senal_dado_1 = pyqtSignal(str)
    senal_jugador_extra = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.jugadores = list()
        self.tragos = list()
        self.vasos = list()
        self.__turno = 0
        self.dado1 = 0

    @property
    def turno(self):
        return self.__turno

    @turno.setter
    def turno(self, valor):
        if valor >= len(self.jugadores):
            self.__turno = 0
        else:
            self.__turno = valor

    def agregar(self, nombre):
        if nombre not in self.jugadores:
            self.jugadores.append(nombre)
            self.tragos.append(parametros.TRAGOS_VASO)
            self.vasos.append(0)
        else:
            self.senal_nombre_malo.emit()

    def comenzar(self):
        self.senal_partir.emit([self.jugadores[0], self.vasos[0], self.tragos[0]])

    def tirar_dados(self):
        dado_1 = self.dado1
        dado_2 = randint(1, 6)
        numero = 2
        if random() <= parametros.PROB_BOTAR_DADO * self.vasos[self.turno] * self.vasos[self.turno]:
            dato = "dado caido"
            dado_1 = "vacio"
            dado_2 = "vacio"
            self.senal_vaso_terminado.emit(self.jugadores[self.turno])
            numero = parametros.TRAGOS_VASO
        else:
            if dado_1 < dado_2:
                dato = "regalar"
            elif dado_1 > dado_2:
                dato = "tomar"
            elif dado_1 == 1 and dado_2 == 1:
                dato = "tomar"
                numero = parametros.TRAGOS_VASO
            elif dado_2 == 6 and dado_1 == 6:
                dato = "regalar"
                numero = parametros.TRAGOS_VASO
            elif dado_1 == dado_2:
                dato = "chancho"
                numero = parametros.TRAGOS_VASO
        self.senal_dados.emit([dato, dado_1, dado_2, numero, self.jugadores])

    def tomar(self, datos):
        nombre = datos[0]
        numero = datos[1]
        if nombre in self.jugadores:
            self.tomando(nombre, numero)

    def tomando(self, nombre, numero):
        indice = self.jugadores.index(nombre)
        if self.tragos[indice] - numero <= 0:
            self.tragos[indice] = parametros.TRAGOS_VASO
            self.vasos[indice] += 1
            self.senal_vaso_terminado.emit(nombre)
        else:
            self.tragos[indice] -= numero
        self.pasar_turno()

    def pasar_turno(self):
        self.turno += 1
        self.senal_turno.emit([self.jugadores[self.turno], self.vasos[self.turno],
                               self.tragos[self.turno]])

    def primero(self):
        self.dado1 = randint(1, 6)
        self.senal_dado_1.emit(str(self.dado1))

    def jugador_extra(self):
        self.senal_jugador_extra.emit(self.jugadores)

    def agregar_extra(self, nombre):
        self.jugadores.append(nombre)
        self.tragos.append(parametros.TRAGOS_VASO)
        self.vasos.append(0)
