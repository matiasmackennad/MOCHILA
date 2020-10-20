import front
import back
from PyQt5.QtWidgets import QApplication
import sys


qapp = QApplication([])

juego = back.Juego()
ventana_inicio = front.VentanaInicio()
ventana_juego = front.VentanaJuego()
ventana_penitencia = front.VentanaPenitencia()
ventana_vaso = front.VasoTerminado()
ventana_agregar = front.VentanaAgregar()

ventana_inicio.senal_agregar.connect(juego.agregar)
ventana_inicio.senal_comenzar.connect(juego.comenzar)

juego.senal_nombre_malo.connect(ventana_inicio.error_nombre)
juego.senal_partir.connect(ventana_juego.comenzar)
juego.senal_dados.connect(ventana_juego.jugada)
juego.senal_vaso_terminado.connect(ventana_vaso.mostrar)
juego.senal_turno.connect(ventana_juego.pasar_turno)
juego.senal_dado_1.connect(ventana_juego.primer_dado)
juego.senal_jugador_extra.connect(ventana_agregar.mostrar)

ventana_juego.senal_jugar.connect(juego.tirar_dados)
ventana_juego.senal_penitencia.connect(ventana_penitencia.mostrar)
ventana_juego.senal_primero.connect(juego.primero)
ventana_juego.senal_saltar.connect(juego.pasar_turno)
ventana_juego.senal_agregar.connect(juego.jugador_extra)

ventana_penitencia.senal_tomar.connect(juego.tomar)

ventana_agregar.senal_agregar_extra.connect(juego.agregar_extra)

ventana_inicio.show()
sys.exit(qapp.exec())
