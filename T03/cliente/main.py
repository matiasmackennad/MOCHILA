from PyQt5.QtWidgets import QApplication
import sys
from back import Client
import front
import ventana_juego as vj


qapp = QApplication([])

port = 8080
client = Client(port)

ventana_inicio = front.VentanaInicio()
ventana_espera = front.VentanaEspera()
ventana_juego = vj.VentanaJuego()
ventana_color = front.VentanaColor()
ventana_final = front.VentanaTermino()

ventana_inicio.senal_comenzar.connect(client.comenzar)

client.senal_sala_entrar_espera.connect(ventana_espera.setear_datos)
client.senal_error_nombre.connect(ventana_inicio.error_nombre)
client.senal_sala_entrar_juego.connect(ventana_juego.abrir)
client.senal_cartas.connect(ventana_juego.actualizar)
client.senal_cerrar_ventana_espera.connect(ventana_espera.hide)
client.senal_cartas_robadas.connect(ventana_juego.actualizar_robo)
client.senal_carta_jugada.connect(ventana_juego.cambiar_carta)
client.senal_masdos.connect(ventana_juego.masdos)
client.senal_cambio_turno.connect(ventana_juego.cambio_turno)
client.senal_desconectado.connect(ventana_juego.desconectado)
client.senal_actualizar_espera.connect(ventana_espera.actualizar)
client.senal_perder.connect(ventana_juego.perder)
client.senal_cerrar.connect(ventana_inicio.hide)
client.senal_cerrar.connect(ventana_juego.hide)
client.senal_cerrar.connect(ventana_color.hide)
client.senal_cerrar.connect(ventana_espera.hide)
client.senal_juego_acabado.connect(ventana_final.mensaje)

ventana_juego.senal_jugar_carta.connect(client.jugar_carta)
ventana_juego.senal_robar_carta.connect(client.robar_carta)
ventana_juego.senal_gritar.connect(client.gritar)
ventana_juego.senal_elegir_color.connect(ventana_color.abrir)
ventana_juego.senal_perder_dccuatro.connect(client.perder_dccuatro)

ventana_color.senal_color_elegido.connect(ventana_juego.color_elegido)

ventana_final.senal_comenzar_nuevo.connect(ventana_juego.resetear)
ventana_final.senal_comenzar_nuevo.connect(ventana_espera.resetear)
ventana_final.senal_comenzar_nuevo.connect(ventana_inicio.resetear)
ventana_final.senal_comenzar_nuevo.connect(client.resetear)

sys.exit(qapp.exec())

