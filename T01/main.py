import criaturas
import zoologos
import DCC
import parametros
import funciones
from random import randint


condicion_general = True
condicion_menu_inicio = True
condicion_elegir_criatura = False
condicion_crear_magizoologo = False
condicion_menu_acciones = False
condicion_menu_dccriaturas = False
condicion_menu_dcc = False
dcc = DCC.Dcc()
print("Bienvenido a DCCriaturas Fantasticas")
while condicion_general:
    while condicion_menu_inicio:
        print("[1] Crear magizoologo")
        print("[2] Cargar magizoologo")
        print("[0] Salir")
        opcion_seleccionada = input("Seleccione una opcion (1, 2 o 0):")
        if opcion_seleccionada == "1":
            condicion_crear = True
            while condicion_crear:
                nombre = input("Seleccione un nombre para su magizoologo")
                if funciones.validar_usuario(nombre):
                    condicion_crear_magizoologo = True
                    while condicion_crear_magizoologo:
                        print("[1] Docencio")
                        print("[2] Tareo")
                        print("[3] Hibrido")
                        tipo_seleccionado = input("Seleccione un tipo de magizoologo (1, 2 o 3):")
                        if tipo_seleccionado == "1":
                            magizoologo = zoologos.Docencio(nombre, *funciones.generar_datos(opcion_seleccionada))
                            condicion_crear_magizoologo = False
                        elif tipo_seleccionado == "2":
                            magizoologo = zoologos.Tareo(nombre, *funciones.generar_datos(opcion_seleccionada))
                            condicion_crear_magizoologo = False
                        elif tipo_seleccionado == "3":
                            magizoologo = zoologos.Hibrido(nombre, *funciones.generar_datos(opcion_seleccionada))
                            condicion_crear_magizoologo = False
                        else:
                            print("Error: La opcion seleccionada no existe")
                    condicion_elegir_criatura = True
                    while condicion_elegir_criatura:
                        nombre = input("Indique el nombre que desea para su DCCriatura:")
                        if funciones.validar_criatura(nombre):
                            print("[1] Augurey")
                            print("[2] Niffler")
                            print("[3] Erkling")
                            criatura_seleccionada = input("Seleccione una DCCriatura (1, 2 o 3):")
                            if criatura_seleccionada == "1":
                                criatura = criaturas.Augurey(nombre, *funciones.generar_criatura(criatura_seleccionada,
                                                                                                 0))
                                magizoologo.dccriaturas = [criatura]
                                funciones.guardar_magizoologo(magizoologo)
                                funciones.guardar_criatura(criatura)
                                condicion_elegir_criatura = False
                                condicion_menu_inicio = False
                                condicion_menu_acciones = True
                                condicion_crear = False
                            elif criatura_seleccionada == "2":
                                cleptomania = randint(*parametros.CLEPTOMANIA_NIFFLER)
                                criatura = criaturas.Niffler(nombre, *funciones.generar_criatura(criatura_seleccionada,
                                                                                                 cleptomania))
                                magizoologo.dccriaturas = [criatura]
                                funciones.guardar_magizoologo(magizoologo)
                                funciones.guardar_criatura(criatura)
                                condicion_elegir_criatura = False
                                condicion_menu_inicio = False
                                condicion_menu_acciones = True
                                condicion_crear = False
                            elif criatura_seleccionada == "3":
                                criatura = criaturas.Erkling(nombre, *funciones.generar_criatura(criatura_seleccionada,
                                                                                                 0))
                                magizoologo.dccriaturas = [criatura]
                                funciones.guardar_magizoologo(magizoologo)
                                funciones.guardar_criatura(criatura)
                                condicion_elegir_criatura = False
                                condicion_menu_inicio = False
                                condicion_menu_acciones = True
                                condicion_crear = False
                            else:
                                print("Error: La opcion seleccionada no existe")
                else:
                    print("Error: Dicho magizoologo ya existe")
                    print("[1] Volver a intentar")
                    print("[2] Volver atras")
                    print("[0] Salir")
                    opcion = input("Seleccione una DCCriatura (1, 2 o 0):")
                    if opcion == "1":
                        condicion_crear = True
                    if opcion == "2":
                        condicion_crear = False
                    if opcion == "0":
                        condicion_crear = False
                        condicion_general = False
                        condicion_menu_inicio = False
        elif opcion_seleccionada == "2":
            condicion_abrir = True
            while condicion_abrir:
                nombre = input("Indique el nombre de su Magizoologo")
                if len(funciones.abrir_magizoologo(nombre)) != 0:
                    datos_zoologo = funciones.abrir_magizoologo(nombre)
                    if datos_zoologo[1] == "Docencio":
                        magizoologo = zoologos.Docencio(datos_zoologo[0], *datos_zoologo[2: len(datos_zoologo)])
                        condicion_menu_acciones = True
                        condicion_menu_inicio = False
                        condicion_abrir = False
                    elif datos_zoologo[1] == "Tareo":
                        magizoologo = zoologos.Tareo(datos_zoologo[0], *datos_zoologo[2: len(datos_zoologo)])
                        condicion_menu_acciones = True
                        condicion_menu_inicio = False
                        condicion_abrir = False
                    elif datos_zoologo[1] == "Hibrido":
                        magizoologo = zoologos.Hibrido(datos_zoologo[0], *datos_zoologo[2: len(datos_zoologo)])
                        condicion_menu_acciones = True
                        condicion_menu_inicio = False
                        condicion_abrir = False
                else:
                    print("Error: Dicho usuario no existe")
                    print("[1] Volver a intentar")
                    print("[2] Volver atras")
                    print("[0] Salir")
                    opcion = input("Seleccione una DCCriatura (1, 2 o 0):")
                    if opcion == "1":
                        condicion_abrir = True
                    if opcion == "2":
                        condicion_abrir = False
                    if opcion == "0":
                        condicion_abrir = False
                        condicion_general = False
                        condicion_menu_inicio = False
        elif opcion_seleccionada == "0":
            condicion_elegir_criatura = False
            condicion_menu_inicio = False
            condicion_crear_magizoologo = False
            condicion_general = False
        else:
            print("Error: Dicha opcion no existe")
    while condicion_menu_acciones:
        print("[1] Menu DCCriaturas")
        print("[2] Menu DCC")
        print("[3] Pasar al dia siguiente")
        print("[4] Volver atras")
        print("[0] Salir")
        opcion_seleccionada = input("Seleccione una opcion (1, 2, 3, 4 o 0):")
        if opcion_seleccionada == "1":
            condicion_menu_dccriaturas = True
            condicion_menu_acciones = False
        elif opcion_seleccionada == "2":
            condicion_menu_dcc = True
            condicion_menu_acciones = False
        elif opcion_seleccionada == "3":
            dcc.pasar_dia(magizoologo)
        elif opcion_seleccionada == "4":
            condicion_menu_inicio = True
            condicion_menu_acciones = False
        elif opcion_seleccionada == "0":
            condicion_menu_inicio = False
            condicion_general = False
            condicion_menu_acciones = False
        else:
            print("Error: Dicha opcion no existe")
    while condicion_menu_dccriaturas:
        print("[1] Alimentar DCCriaturas")
        print("[2] Sanar DCCriatura")
        print("[3] Recuperar DCCriatura")
        print("[4] Usar habilidad especial")
        print("[5] Volver atras")
        print("[0] Salir")
        opcion_seleccionada = input("Seleccione una opcion (1, 2, 3, 4, 5 o 0):")
        if opcion_seleccionada == "1":
            if len(magizoologo.alimentos) == 0:
                print("No tienes alimentos que darle a tus DCCriaturas")
            elif magizoologo.energia < parametros.COSTO_ALIMENTAR:
                print("No tienes suficiente energia para alimentar a tu DCCriatura")
            else:
                alimento = funciones.obtener_alimento(magizoologo)
                dccriatura = funciones.obtener_criatura(magizoologo)
                magizoologo.alimentar(dccriatura, alimento)
                funciones.cambiar_criatura(dccriatura)
                funciones.cambiar_magizoologo(magizoologo)
        elif opcion_seleccionada == "2":
            dccriatura = funciones.obtener_criatura(magizoologo)
            magizoologo.sanar(dccriatura)
            funciones.cambiar_criatura(dccriatura)
            funciones.cambiar_magizoologo(magizoologo)
        elif opcion_seleccionada == "3":
            dccriatura = funciones.obtener_criatura(magizoologo)
            magizoologo.recuperar(dccriatura)
            funciones.cambiar_criatura(dccriatura)
            funciones.cambiar_magizoologo(magizoologo)
        elif opcion_seleccionada == "4":
            if magizoologo.especial:
                magizoologo.hab_especial()
                funciones.cambiar_magizoologo(magizoologo)
            else:
                print("Ya has ocupado tu habilidad especial")
        elif opcion_seleccionada == "5":
            condicion_menu_dccriaturas = False
            condicion_menu_dcc = False
            condicion_menu_inicio = False
            condicion_menu_acciones = True
        elif opcion_seleccionada == "0":
            condicion_menu_dccriaturas = False
            condicion_menu_dcc = False
            condicion_menu_inicio = False
            condicion_menu_acciones = False
            condicion_general = False
        else:
            print("Error: Dicha opcion no existe")
    while condicion_menu_dcc:
        print("[1] Adoptar DCCriaturas")
        print("[2] Comprar alimentos")
        print("[3] Revisar estado")
        print("[4] Volver atras")
        print("[0] Salir")
        opcion_seleccionada = input("Seleccione una opcion (1, 2, 3, 4 o 0):")
        if opcion_seleccionada == "1":
            dcc.adoptar(magizoologo)
            funciones.cambiar_magizoologo(magizoologo)
        elif opcion_seleccionada == "2":
            dcc.comprar(magizoologo)
            funciones.cambiar_magizoologo(magizoologo)
        elif opcion_seleccionada == "3":
            dcc.revisar(magizoologo)
            funciones.cambiar_magizoologo(magizoologo)
        elif opcion_seleccionada == "4":
            condicion_menu_dccriaturas = False
            condicion_menu_dcc = False
            condicion_menu_inicio = False
            condicion_menu_acciones = True
        elif opcion_seleccionada == "0":
            condicion_menu_dccriaturas = False
            condicion_menu_dcc = False
            condicion_menu_inicio = False
            condicion_menu_acciones = False
            condicion_general = False
        else:
            print("Error: No existe dicha opcion")





