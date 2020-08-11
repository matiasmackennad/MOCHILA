import socket
import threading
from PyQt5.QtCore import QObject, pyqtSignal
import pickle
import json


class Client(QObject):
    senal_sala_entrar_espera = pyqtSignal(list)
    senal_sala_entrar_juego = pyqtSignal(str)
    senal_error_nombre = pyqtSignal()
    senal_cartas = pyqtSignal(list)
    senal_cerrar_ventana_espera = pyqtSignal()
    senal_cartas_robadas = pyqtSignal(list)
    senal_carta_jugada = pyqtSignal(list)
    senal_masdos = pyqtSignal()
    senal_cambio_turno = pyqtSignal(str)
    senal_actualizar_espera = pyqtSignal(str)
    senal_desconectado = pyqtSignal(str)
    senal_perder = pyqtSignal(str)
    senal_juego_acabado = pyqtSignal(str)
    senal_cerrar = pyqtSignal()

    def __init__(self, port):
        super().__init__()
        with open("parametros.json", "r") as file:
            self.parametros = json.load(file)
        self.host = self.parametros["HOST"]
        self.port = port
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.nombre = ""
        self.espera = True

        try:
            self.connect_to_server()
            self.listen()
        except ConnectionError:
            self.socket_client.close()
            exit()

    def connect_to_server(self):
        self.socket_client.connect((self.host, self.port))

    def listen(self):
        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

    def send(self, msg):
        msg_bytes = msg.encode()
        msg_length = len(msg_bytes).to_bytes(4, byteorder='big')
        self.socket_client.sendall(msg_length + msg_bytes)

    def comenzar(self, msg):
        self.nombre = msg
        msg = "solicitud de entrada," + msg
        self.send(msg)

    def listen_thread(self):
        self.escuchando = True
        while self.escuchando:
            response_bytes_length = self.socket_client.recv(4)
            response_length = int.from_bytes(
                response_bytes_length, byteorder='big')
            response = bytearray()
            while len(response) < response_length:
                read_length = min(4096, response_length - len(response))
                response.extend(self.socket_client.recv(read_length))
            if response[0: len("cartas 1".encode())].decode() == "cartas 1":
                datos = response[len("cartas 1".encode()): len(response)]
                datos = pickle.loads(datos)
                self.senal_cartas.emit(datos)
            elif response[0: len("cartas 2".encode())].decode() == "cartas 2":
                datos = response[len("cartas 2".encode()): len(response)]
                datos = pickle.loads(datos)
                self.senal_cartas_robadas.emit(datos)
            elif response[0: len("cartas 3".encode())].decode() == "cartas 3":
                datos = response[len("cartas 3".encode()): len(response)]
                datos = pickle.loads(datos)
                self.senal_carta_jugada.emit(datos)
            else:
                datos = response.decode()
                datos = datos.split(",")
            if datos[0] == "entrar sala de espera":
                self.espera = True
                self.senal_sala_entrar_espera.emit(datos[1: len(datos)])
            if datos[0] == "solicitud denegada":
                self.senal_cerrar.emit()
            if datos[0] == "error con el nombre":
                self.nombre = ""
                self.senal_error_nombre.emit()
            if datos[0] == "entrar sala de juego":
                self.espera = False
                self.senal_sala_entrar_juego.emit(self.nombre)
                self.senal_cerrar_ventana_espera.emit()
            if datos[0] == "salio un +2":
                self.senal_masdos.emit()
            if datos[0] == "cambio de turno":
                self.senal_cambio_turno.emit(datos[1])
            if datos[0] == "desconeccion":
                if self.espera:
                    self.senal_actualizar_espera.emit(datos[1])
                else:
                    self.senal_desconectado.emit(datos[1])
            if datos[0] == "perdio":
                self.senal_perder.emit(datos[1])
            if datos[0] == "ganador":
                if datos[1] == self.nombre:
                    self.senal_juego_acabado.emit("Se acabo el juego: ¡Ganaste!")
                else:
                    self.senal_juego_acabado.emit("Se acabo el juego, el ganador fue: " +
                                                  str(datos[1]))
                self.senal_cerrar.emit()

    def robar_carta(self, datos):
        msg = "robar," + str(datos[0])
        self.send(msg)

    def jugar_carta(self, datos):
        if datos[2] - 1 == 1:
            self.send("queda una," + str(self.nombre))
        if datos[2] - 1 == 0:
            self.send("ganador," + str(self.nombre))
        msg = "cartas 4".encode() + pickle.dumps([datos[0], datos[1]])
        largo = len(msg).to_bytes(4, byteorder='big')
        self.socket_client.sendall(largo + msg)

    def gritar(self, datos):
        self.send(f"gritar,{datos[0]},{datos[1]}")

    def resetear(self):
        self.send("resetear")
        self.nombre = ""
        self.espera = True

    def perder_dccuatro(self):
        self.send("perder_dccuatro," + str(self.nombre))
