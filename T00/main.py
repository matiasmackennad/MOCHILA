import funciones
import clases

condicion_menu_inicio = True
condicion_general = True
print("Bienvenido a DCCahuin!!")
while condicion_general:
    while condicion_menu_inicio:
        condicion_menu1 = True
        print("Seleccione una opción:")
        print("[1] Iniciar sesión")
        print("[2] Registrar usuario")
        print("[0] Salir")
        opcion_seleccionada = input("Indique su opción (0, 1 o 2):")
        if opcion_seleccionada == "1":
            nombre = input("Indique su nombre de usuario:")
            if funciones.seleccionar_usuario(nombre):
                print("Has iniciado sesion como", nombre)
                usuario = clases.Usuario(nombre)
                condicion_menu_inicio = False
            else:
                print("Error: Nombre de usuario no existe")
        elif opcion_seleccionada == "2":
            nombre = input("Indique el nombre de usuario que desea crear:")
            if funciones.validar_usuario(nombre):
                if funciones.crear_usuario(nombre):
                    print("Has elegido", nombre, "como tu nombre de usuario")
                    usuario = clases.Usuario(nombre)
                    condicion_menu_inicio = False
                else:
                    print("Error: Nombre de usuario ya existe")
        elif opcion_seleccionada == "0":
            print("Has salido de DCCahuin")
            condicion_general = False
            condicion_menu_inicio = False
            condicion_menu_prograposts = False
            condicion_menu1 = False
            condicion_menu_usuarios = False
        else:
            print("Error: no existe dicha opcion")
    while condicion_menu1:
        condicion_menu_usuarios = False
        condicion_menu_prograposts = False
        print("Seleccione una opción:")
        print("[1] Ir al menu de prograposts")
        print("[2] Ir al menu de seguidores")
        print("[3] Volver al menu de inicio")
        print("[0] Salir")
        opcion_seleccionada = input("Indique su opción (0, 1, 2 o 3):")
        if opcion_seleccionada == "1":
            condicion_menu_prograposts = True
            condicion_menu1 = False
        elif opcion_seleccionada == "2":
            condicion_menu_usuarios = True
            condicion_menu1 = False
        elif opcion_seleccionada == "3":
            condicion_menu1 = False
            condicion_menu_inicio = True
        elif opcion_seleccionada == "0":
            print("Has salido de DCCahuin")
            condicion_general = False
            condicion_menu_inicio = False
            condicion_menu_prograposts = False
            condicion_menu1 = False
            condicion_menu_usuarios = False
        else:
            print("Error: no existe dicha opcion")
    while condicion_menu_usuarios:
        print("Seleccione una opción:")
        print("[1] Seguir a un usuario")
        print("[2] Dejar de seguir a un usuario")
        print("[3] Volver al menu anterior")
        print("[4] Volver al menu de inicio")
        print("[0] Salir")
        opcion_seleccionada = input("Indique su opción (0, 1, 2, 3 o 4):")
        if opcion_seleccionada == "1":
            seguido = input("Indique el usuario que desea seguir:")
            if seguido == usuario.nombre:
                print("Error: No puedes seguirte a ti mismo")
            elif seguido in usuario.seguidos:
                print("Error: Ya sigues a dicho usuario")
            elif not funciones.seleccionar_usuario(seguido):
                print("Error: Dicho usuario no existe")
            else:
                print("Has comenzado a seguir a", usuario.seguir(seguido))
        elif opcion_seleccionada == "2":
            seguido = input("Indique el usuario que desea dejar de seguir:")
            if seguido == usuario.nombre:
                print("Error: No puedes dejar de seguirte a ti mismo")
            elif seguido not in usuario.seguidos:
                print("Error: No sigues a dicho usuario")
            elif not funciones.seleccionar_usuario(seguido):
                print("Error: Dicho usuario no existe")
            else:
                print("Has dejado de seguir a", usuario.dejar_seguir(seguido))
        elif opcion_seleccionada == "3":
            condicion_menu_usuarios = False
            condicion_menu1 = True
        elif opcion_seleccionada == "4":
            condicion_menu_usuarios = False
            condicion_menu_inicio = True
        elif opcion_seleccionada == "0":
            print("Has salido de DCCahuin")
            condicion_general = False
            condicion_menu_inicio = False
            condicion_menu_prograposts = False
            condicion_menu1 = False
            condicion_menu_usuarios = False
        else:
            print("Error: no existe dicha opcion")
    while condicion_menu_prograposts:
        print("Seleccione una opción:")
        print("[1] Crear un prograpost")
        print("[2] Eliminar un prograpost")
        print("[3] Ver tus prograposts")
        print("[4] Ver prograposts de los usuarios que sigues")
        print("[5] Volver al menu anterior")
        print("[6] Volver al menu de inicio")
        print("[0] Salir")
        opcion_seleccionada = input("Indique su opción (0, 1, 2, 3 o 4):")
        if opcion_seleccionada == "1":
            texto = input("Indique el texto que quiere escribir en su prograpost:")
            if len(texto) > 140:
                print("No se puede escribir un prograpost con más de 140 caracteres")
            elif len(texto) < 1:
                print("No se puede escribir un prograpost con menos de 1 caracter")
            else:
                usuario.crear_post(texto)
                print("Has creado un prograpost que dice", texto)
        elif opcion_seleccionada == "2":
            if usuario.eliminar_post():
                print("Se ha eliminado el prograpost seleccionado")
        elif opcion_seleccionada == "3":
            print("Seleccione el orden en que quiere que se muestren sus prograposts:")
            print("[0] Creciente")
            print("[1] Decreciente")
            orden = input("Elija el orden que quiera (0 o 1):")
            usuario.mostrar_posts_propios(orden)
        elif opcion_seleccionada == "4":
            print("Seleccione el orden en que quiere que se muestren los prograposts de los usuarios que sigues:")
            print("[0] Creciente")
            print("[1] Decreciente")
            orden = input("Elija el orden que quiera (0 o 1):")
            usuario.mostrar_posts_seguidos(orden)
        elif opcion_seleccionada == "5":
            condicion_menu_prograposts = False
            condicion_menu1 = True
        elif opcion_seleccionada == "6":
            condicion_menu_prograposts = False
            condicion_menu_inicio = True
        elif opcion_seleccionada == "0":
            print("Has salido de DCCahuin")
            condicion_general = False
            condicion_menu_inicio = False
            condicion_menu_prograposts = False
            condicion_menu1 = False
            condicion_menu_usuarios = False
        else:
            print("Error: no existe dicha opcion")













