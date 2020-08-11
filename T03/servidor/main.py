import socket
import threading
import funciones
from generador_de_mazos import sacar_cartas
import pickle
import json


class Server:
    def __init__(self, port):
        self.lista_usuarios = list()
        self.socket_clientes = list()
        with open("parametros.json", "r") as file:
            self.parametros = json.load(file)

        self.host = self.parametros["HOST"]
        self.port = port
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_and_listen()
        self.accept_connections()
        self.__turno = 0
        self.cantidad_robar = 0
        self.dccuatro = list()
        self.condicion_resetear = True
        self.lista_activos = list()
        print("Inicio servidor")
        print("Formato de informacion: accion(usuario): detalles")

    @property
    def turno(self):
        return self.__turno

    @turno.setter
    def turno(self, valor):
        if valor >= len(self.lista_usuarios):
            self.__turno = 0
        else:
            self.__turno = valor

    def bind_and_listen(self):
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()

    def accept_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
         while True:
            client_socket, _ = self.socket_server.accept()
            listening_client_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket, ),
                daemon=True)
            listening_client_thread.start()

    @staticmethod
    def send(value, sock):
        stringified_value = str(value)
        msg_bytes = stringified_value.encode()
        msg_length = len(msg_bytes).to_bytes(4, byteorder='big')
        sock.send(msg_length + msg_bytes)

    def listen_client_thread(self, client_socket):
        while True:
            try:
                response_bytes_length = client_socket.recv(4)
                response_length = int.from_bytes(
                    response_bytes_length, byteorder='big')
                response = bytearray()

                while len(response) < response_length:
                    read_length = min(4096, response_length - len(response))
                    response.extend(client_socket.recv(read_length))

                if response[0: len("cartas 4".encode())].decode() == "cartas 4":
                    received = ["jugar", response[len("cartas 4".encode()): len(response)]]
                else:
                    received = response.decode()
                if type(received) is str:
                    vacio = ""
                elif type(received) is list:
                    vacio = []
                if received != vacio:
                    response = self.handle_command(received, client_socket)
                    if response != "solicitud denegada":
                        if response == "error con el nombre":
                            self.send("error con el nombre", client_socket)
                        else:
                            self.enviar_a_todos(response)
                    else:
                        self.send("solicitud denegada", client_socket)
                        client_socket.close()
                        break
            except ConnectionResetError:
                if client_socket in self.socket_clientes:
                    cliente = self.lista_activos[self.socket_clientes.index(client_socket)]
                    self.lista_activos.remove(cliente)
                    if cliente in self.lista_usuarios:
                        self.lista_usuarios.remove(cliente)
                    self.socket_clientes.remove(client_socket)
                    if cliente in self.lista_usuarios:
                        self.lista_usuarios.remove(cliente)
                        if len(self.lista_activos) != 0:
                            if self.turno >= len(self.lista_usuarios):
                                self.turno += 1
                            self.enviar_a_todos(
                                "cambio de turno," + str(self.lista_usuarios[self.turno]))
                        self.enviar_a_todos("desconeccion," + str(cliente))
                    print(f"Desconeccion ({cliente}): {cliente} se ha desconectado")
                    if len(self.lista_activos) == 1:
                        self.condicion_resetear = True
                        print(f"Ganador ({self.lista_activos[0]}): {self.lista_activos[0]} "
                              f"ha ganado el juego")
                        self.enviar_a_todos("ganador," + str(self.lista_activos[0]))
                client_socket.close()
                break

    def handle_command(self, received, client_socket):
        if type(received) is str:
            datos = received.split(",")
        elif type(received) is list:
            datos = received
        if datos[0] == "solicitud de entrada":
            print(f"Solicitud de entrada ({datos[1]}): {datos[1]} Esta tratando de entrar al juego")
            if len(self.lista_usuarios) <= self.parametros["NUM_USUARIOS"] - 1:
                if datos[1] in self.lista_usuarios or not datos[1].isalnum():
                    print(f"Error nombre ({datos[1]}): {datos[1]} Ya esta ocupado")
                    return "error con el nombre"
                self.lista_usuarios.append(datos[1])
                self.socket_clientes.append(client_socket)
                self.lista_activos.append(datos[1])
                if len(self.lista_usuarios) == self.parametros["NUM_USUARIOS"]:
                    info = list()
                    lista = ["entrar sala de juego"] + self.lista_usuarios
                    for usuario in self.lista_usuarios:
                        print(f"Jugar ({usuario}): {usuario} Entro a la sala de juego")
                        cartas = sacar_cartas(4)
                        cartas = funciones.generar_byte_imagen(cartas)
                        info.append([usuario, cartas])
                    while True:
                        carta = sacar_cartas(1)
                        if carta[0][0] != "color" and carta[0][0] != "+2" and \
                                carta[0][0] != "sentido":
                            info.append(funciones.generar_byte_imagen(carta))
                            info.append([self.lista_usuarios, self.turno])
                            break
                    for sock in self.socket_clientes:
                        mensaje = "cartas 1"
                        mensaje = bytearray(mensaje.encode())
                        mensaje.extend(pickle.dumps(info))
                        largo = len(mensaje).to_bytes(4, byteorder='big')
                        sock.send(largo + mensaje)
                else:
                    print(f"Espera ({datos[1]}): {datos[1]} Entro a la sala de espera")
                    lista = ["entrar sala de espera"] + self.lista_usuarios
                return ",".join(lista)
            else:
                print(f"Solicitud denegada ({datos[1]}): El servidor esta lleno")
                return "solicitud denegada"
        if datos[0] == "robar":
            cartas = [datos[1]]
            if self.cantidad_robar == 0:
                self.cantidad_robar += 1
            print(f"Robar Carta ({datos[1]}): {datos[1]} ha robado {self.cantidad_robar} cartas")
            cartas.append(funciones.generar_byte_imagen(sacar_cartas(self.cantidad_robar)))
            msg = bytearray("cartas 2".encode()) + pickle.dumps(cartas)
            for sock in self.socket_clientes:
                largo = len(msg).to_bytes(4, byteorder='big')
                sock.send(largo + msg)
            self.cantidad_robar = 0
            self.turno += 1
            siguiente = self.lista_usuarios[self.turno]
            print(f"Turno ({siguiente}): es el turno de {siguiente}")
            self.enviar_a_todos("cambio de turno," + str(self.lista_usuarios[self.turno]))
        if datos[0] == "jugar":
            dato_carta = pickle.loads(datos[1])
            carta = funciones.generar_imagen([dato_carta[1]])[0]
            print(f"Carta ({dato_carta[0]}): {dato_carta[0]} jugo la carta {carta[1]}_{carta[0]}")
            if carta[1] == "+2":
                self.cantidad_robar += 2
                self.enviar_a_todos("salio un +2")
            if carta[1] == "sentido":
                self.lista_usuarios.reverse()
                self.socket_clientes.reverse()
                self.turno = self.lista_usuarios.index(dato_carta[0])
            entrega = funciones.generar_byte_imagen([(carta[1], carta[0])])
            msg = "cartas 3".encode() + pickle.dumps([dato_carta[0], entrega])
            for sock in self.socket_clientes:
                largo = len(msg).to_bytes(4, byteorder='big')
                sock.send(largo + msg)
            self.turno += 1
            siguiente = self.lista_usuarios[self.turno]
            print(f"Turno ({siguiente}): es el turno de {siguiente}")
            self.enviar_a_todos("cambio de turno," + str(self.lista_usuarios[self.turno]))
        if datos[0] == "perdio":
            self.perder(datos)
            self.turno += 1
            siguiente = self.lista_usuarios[self.turno]
            print(f"Turno ({siguiente}): es el turno de {siguiente}")
            self.enviar_a_todos("cambio de turno," + str(self.lista_usuarios[self.turno]))
        if datos[0] == "gritar":
            if len(self.dccuatro) != 0:
                if datos[1] in self.dccuatro:
                    print(f"DCCuatro ({datos[1]}): {datos[1]} se ha salvado de robar 4 cartas")
                    self.dccuatro.remove(datos[1])
                else:
                    for parte in self.dccuatro:
                        print(f"DCCuatro ({parte}): {parte} Roba 4 cartas")
                        cartas = [parte]
                        cartas.append(funciones.generar_byte_imagen(sacar_cartas(4)))
                        msg = bytearray("cartas 2".encode()) + pickle.dumps(cartas)
                        for sock in self.socket_clientes:
                            largo = len(msg).to_bytes(4, byteorder='big')
                            sock.send(largo + msg)
            else:
                print(f"DCCuatro ({datos[1]}): {datos[1]} Debe robar 4 cartas por equivocarse")
                cartas = [datos[1]]
                cartas.append(funciones.generar_byte_imagen(sacar_cartas(4)))
                msg = bytearray("cartas 2".encode()) + pickle.dumps(cartas)
                for sock in self.socket_clientes:
                    largo = len(msg).to_bytes(4, byteorder='big')
                    sock.send(largo + msg)
        if datos[0] == "queda una":
            print(f"Uno ({datos[1]}): a {datos[1]} le queda una carta")
            self.dccuatro.append(datos[1])
        if datos[0] == "ganador":
            self.coondicion_resetear = True
            print(f"Ganador ({datos[1]}): {datos[1]} ha ganado el juego")
            self.enviar_a_todos("ganador," + str(datos[1]))
        if datos[0] == "resetear":
            if self.condicion_resetear:
                self.lista_activos = list()
                self.lista_usuarios = list()
                self.socket_clientes = list()
                self.dccuatro = list()
                self.condicion_resetear = False
        if datos[0] == "perder_dccuatro":
            self.perder(datos)

    def enviar_a_todos(self, mensaje):
        for socket in self.socket_clientes:
            self.send(mensaje, socket)

    def perder(self, datos):
        if datos[1] in self.lista_usuarios:
            print(f"Perdio ({datos[1]}): {datos[1]} ha perdido")
            self.enviar_a_todos("perdio," + str(datos[1]))
            self.lista_usuarios.remove(datos[1])
            if len(self.lista_usuarios) == 1:
                print(f"Ganador ({datos[1]}): {datos[1]} ha ganado el juego")
                self.enviar_a_todos("ganador," + str(datos[1]))


if __name__ == "__main__":
    port = 8080
    server = Server(port)


