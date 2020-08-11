import front
import back
import ventana_principal as vp
import dccafe as dc
from PyQt5.QtWidgets import QApplication
from threading import Event
import sys

qapp = QApplication([])
pausa = Event()
senal_tiempo = Event()

ventana_inicio = front.VentanaInicio()
ventana_principal = vp.VentanaPrincipal()
reloj = back.Tiempo(senal_tiempo, pausa)
dccafe = dc.Dccafe(senal_tiempo, pausa)
ventana_post_ronda = front.VentanaFinal()

pausa.set()
reloj.start()

ventana_inicio.senal_partir.connect(ventana_principal.cargar_partida)

ventana_principal.senal_mover_mesero.connect(dccafe.mesero.move)
ventana_principal.senal_setear_mesero.connect(dccafe.mesero.setear_posicion)
ventana_principal.senal_setear_dccafe.connect(dccafe.setear_datos)
ventana_principal.senal_agregar_imagen.connect(dccafe.agregar_elemento)
ventana_principal.senal_eliminar.connect(dccafe.eliminar_elemento)
ventana_principal.senal_comenzar_ronda.connect(dccafe.comenzar_ronda)
ventana_principal.senal_pausar.connect(reloj.setear_pausa)
ventana_principal.senal_actualizar_clientes_mesa.connect(dccafe.modificar_clientes_mesa)
ventana_principal.senal_actualizar_datos.connect(dccafe.ronda_acabada)

dccafe.senal_enviar_datos.connect(ventana_principal.completar_datos)
dccafe.senal_ronda_acabada.connect(ventana_principal.ronda_acabada)
dccafe.senal_abrir_ventana_final.connect(ventana_post_ronda.abrir)
dccafe.senal_ronda_nueva.connect(ventana_principal.continuar)
dccafe.senal_reinicio.connect(ventana_principal.cargar_partida)

dccafe.senal_cliente_nuevo.connect(ventana_principal.agregar_cliente)
dccafe.senal_cliente_enojado.connect(ventana_principal.cliente_enojado)
dccafe.senal_cliente_llendose.connect(ventana_principal.cliente_llendose)
dccafe.senal_cliente_atendido.connect(ventana_principal.cliente_atendido)

dccafe.mesero.senal_actualizar_mesero.connect(ventana_principal.update_position)

dccafe.senal_chef_partir.connect(ventana_principal.chef_partir)
dccafe.senal_chef_listo.connect(ventana_principal.chef_listo)
dccafe.senal_resetear_chef.connect(ventana_principal.resetear_chef)
dccafe.senal_chef_fallar.connect(ventana_principal.resetear_chef)

ventana_post_ronda.senal_salir.connect(ventana_principal.salir)
ventana_post_ronda.senal_guardar.connect(dccafe.guardar)
ventana_post_ronda.senal_continuar.connect(dccafe.continuar)

ventana_inicio.show()
sys.exit(qapp.exec())

