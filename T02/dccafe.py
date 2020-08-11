from PyQt5.QtCore import pyqtSignal, QThread
import time
import parametros
import random
from math import floor
import funciones
from back import Mesero, Cliente, Chef
from threading import Lock


class Dccafe(QThread):
    senal_cliente_enojado = pyqtSignal(int)
    senal_cliente_llendose = pyqtSignal(list)
    senal_enviar_datos = pyqtSignal(list)
    senal_cliente_nuevo = pyqtSignal(list)
    senal_ronda_acabada = pyqtSignal()
    senal_chef_listo = pyqtSignal(list)
    senal_chef_partir = pyqtSignal(list)
    senal_chef_fallar = pyqtSignal(list)
    senal_resetear_chef = pyqtSignal(list)
    senal_cliente_atendido = pyqtSignal(int)
    senal_abrir_ventana_final = pyqtSignal(list)
    senal_ronda_nueva = pyqtSignal(list)
    senal_reinicio = pyqtSignal(list)

    def __init__(self, tiempo, pausa):
        super().__init__()
        self.mesero = Mesero(self)
        self.mesas = list()
        self.chefs = list()
        self.lock = Lock()
        self.dinero = parametros.DINERO_INICIAL
        self.estado = "pre-ronda"
        self.ronda = 1
        self.exitosos = 0
        self.totales = 0
        self.__reputacion = parametros.REPUTACION_INICIAL
        self.disponibilidad = True
        self.chefs_clases = list()
        self.evento_tiempo = tiempo
        self.pausa = pausa
        self.andando = True
        self.start()

    @property
    def reputacion(self):
        return self.__reputacion

    @reputacion.setter
    def reputacion(self, valor):
        if valor <= 0:
            self.__reputacion = 0
        elif valor > 5:
            self.__reputacion = 5
        else:
            self.__reputacion = valor

    def setear_datos(self, datos):
        atributos = funciones.cargar_dccafe()
        for parte in datos[0]:
            if parte[0] == "mesa":
                self.mesas.append(parte)
            elif parte[0] == "chef":
                self.chefs.append(parte)
                for atributo in atributos[1]:
                    chef = Chef(int(atributo), self.evento_tiempo, self, parte[1], parte[2])
                    self.chefs_clases.append(chef)
        self.dinero = int(atributos[0][0])
        self.reputacion = int(atributos[0][1])
        self.ronda = int(atributos[0][2]) + 1
        self.estado = datos[1]
        self.calcular_clientes_ronda()
        self.lista_datos = [self.ronda, self.reputacion, self.dinero, self.totales]
        self.senal_enviar_datos.emit(self.lista_datos)

    def agregar_elemento(self, datos):
        if datos[0] == "mesa":
            self.mesas.append(datos)
            self.dinero -= parametros.PRECIO_MESA
        if datos[0] == "chef":
            self.dinero -= parametros.PRECIO_CHEF
            self.chefs.append(datos)
            chef = Chef(0, self.evento_tiempo, self, datos[1], datos[2])
            self.chefs_clases.append(chef)

    def eliminar_elemento(self, datos):
        if datos[0] == "mesa":
            self.mesas.remove(datos)
        if datos[0] == "chef":
            self.chefs.remove(datos)
            for parte in self.chefs_clases:
                if datos[1] == parte.pos_x and datos[2] == parte.pos_y:
                    self.chefs_clases.remove(parte)

    def calcular_reputacion(self):
        dato = max(0, min(5, (self.reputacion + floor(4 * (self.exitosos / self.totales) - 2))))
        self.reputacion = dato

    def calcular_clientes_ronda(self):
        self.totales = 5 * (1 + self.ronda)

    def run(self):
        while self.andando:
            if self.estado == "ronda":
                self.clientes = list()
                self.clientes_atendidos = 0
                self.mesas_disponibles = len(self.mesas)
                self.clientes_mesas = list()
                contador = 0
                while self.clientes_atendidos < self.totales:
                    self.evento_tiempo.wait()
                    if self.mesas_disponibles != 0 and self.pausa.isSet() and \
                            contador < self.totales:
                        time.sleep(parametros.TIEMPO_LLEGADA_CLIENTES)
                        if random.randint(0, 100) <= parametros.PROB_APURADO:
                            cliente = Cliente("apurado", self.evento_tiempo, self, contador)
                        else:
                            cliente = Cliente("relajado", self.evento_tiempo, self, contador)
                        contador += 1
                        self.evento_tiempo.wait()
                        cliente.start()
                        self.clientes.append(cliente)
                        self.senal_cliente_nuevo.emit([cliente.id_cliente, cliente.tipo])
                        self.mesas_disponibles -= 1
                self.senal_ronda_acabada.emit()
                for chef in self.chefs_clases:
                    chef.dccafe.senal_resetear_chef.emit(["chef", chef.pos_x, chef.pos_y])
                self.mesero.atendiendo = False
                self.estado = "post-ronda"

    def comenzar_ronda(self):
        self.calcular_clientes_ronda()
        self.estado = "ronda"

    def colision(self, datos):
        if datos[0][0] == "chef":
            for parte in self.chefs_clases:
                if datos[0][1] == parte.pos_x and datos[0][2] == parte.pos_y:
                    if parte.cocinando is False and parte.listo is False and \
                            self.mesero.atendiendo is False:
                        parte.start()
                    if parte.listo is True:
                        self.mesero.atendiendo = True
                        self.mesero.bocadillo.append(parte.bocadillo[0])
                        parte.bocadillo[0].start()
                        parte.bocadillo.remove(parte.bocadillo[0])
                        self.senal_resetear_chef.emit(["chef", parte.pos_x, parte.pos_y])
                        parte.listo = False
        elif datos[0][0] == "mesa":
            for parte in self.clientes_mesas:
                if parte[1].x() == int(datos[0][1]) and parte[1].y() == int(datos[0][2]):
                    if self.mesero.atendiendo:
                        self.mesero.atendiendo = False
                        self.mesero.bocadillo[0].entregado = True
                        cliente = self.clientes[parte[0][0]]
                        cliente.bocadillo = self.mesero.bocadillo[0]
                        self.mesero.bocadillo.remove(self.mesero.bocadillo[0])
                        cliente.condicion = False
                        self.senal_cliente_atendido.emit(parte[0][0])

    def modificar_clientes_mesa(self, datos):
        if datos[2] == "agregar":
            self.clientes_mesas.append(datos[0:2])
        else:
            self.clientes_mesas.remove(datos[0:2])

    def ronda_acabada(self, datos):
        self.dinero += datos[0]
        self.ronda += 1
        self.exitosos = datos[1]
        self.totales = datos[1] + datos[2]
        self.calcular_reputacion()
        self.senal_abrir_ventana_final.emit([self.dinero, datos[1], self.ronda - 1,
                                             datos[2], self.reputacion])

    def guardar(self):
        with open(parametros.RUTA_MAPA_CSV, "w", encoding="UTF-8") as file:
            for mesa in self.mesas:
                file.write(",".join(mesa))
                file.write("\n")
            for chef in self.chefs:
                file.write(",".join(chef))
                file.write("\n")
            datos_mesero = ["mesero", str(self.mesero.x), str(self.mesero.y)]
            file.write(",".join(datos_mesero))
            file.write("\n")
        with open(parametros.RUTA_DATOS_CSV, "w", encoding="UTF-8") as file:
            datos_dccafe = [str(self.dinero), str(self.reputacion), str(self.ronda - 1)]
            file.write(",".join(datos_dccafe))
            file.write("\n")
            datos_chefs = list()
            for chef in self.chefs_clases:
                datos_chefs.append(str(chef.platos))
            file.write(",".join(datos_chefs))
            file.write("\n")

    def continuar(self):
        self.estado = "pre-ronda"
        self.exitosos = 0
        self.calcular_clientes_ronda()
        if self.reputacion == 0:
            lista = funciones.crear_partida()
            self.senal_reinicio.emit([lista, "ronda"])
        self.senal_ronda_nueva.emit([self.ronda, self.reputacion, self.dinero, self.totales])
