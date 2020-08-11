def crear_usuario(nombre):
    with open("usuarios.csv", "r", encoding="utf-8", errors="ignore") as usuarios:
        lista_usuarios = usuarios.readlines()
        lista_usuarios = [usuario.strip() for usuario in lista_usuarios]
    with open("usuarios.csv", "a") as usuarios:
        if nombre not in lista_usuarios:
            lista_usuarios.append(nombre)
            usuarios.write(nombre)
            usuarios.write("\n")
            with open("seguidores.csv", "a") as seguidores:
                seguidores.write(nombre)
                seguidores.write("\n")
            return True
        else:
            return False


def seleccionar_usuario(nombre):
    with open('usuarios.csv', "r", encoding="utf-8", errors="ignore") as usuarios:
        lista_usuarios = usuarios.readlines()
        lista_usuarios = [usuario.strip() for usuario in lista_usuarios]
        if nombre in lista_usuarios:
            return True
        else:
            return False


def obtener_seguidos(nombre):
    vacio = list()
    with open("seguidores.csv", "r", encoding="utf-8", errors="ignore") as seguidos:
        lista_seguidos = seguidos.readlines()
        lista_seguidos = [seguido.strip() for seguido in lista_seguidos]
        for parte in lista_seguidos:
            lista = parte.split(",")
            if lista[0] == nombre:
                seguidos_ususario = lista[1:len(parte)]
                return seguidos_ususario
        return vacio


def validar_usuario(nombre):
    una_letra = False
    un_numero = False
    for letra in nombre:
        if letra.isalpha():
            una_letra = True
        if letra.isdigit():
            un_numero = True
    if not nombre.isalnum():
        print("Error: Tu nombre de usuario no es alfanumerico")
        return False
    elif not una_letra:
        print("Error: Tu nombre de usuario debe tener al menos una letra")
        return False
    elif not un_numero:
        print("Error: Tu nombre de usuario debe tener al menos un numero")
        return False
    elif len(nombre) < 8:
        print("Error: Tu nombre de usuario debe tener minimo 8 caracteres")
        return False
    else:
        return True
# Parte de esta funcion fue obtenida de:
# https://www.tutorialspoint.com/How-to-check-if-a-string-has-at-least-one-letter-and-one-number-in-Python


def ordenar_fechas(lista):
    lista = lista.split(",")
    fecha = lista[1].split("/")
    fecha_numero = 10000*fecha[0] + 100*fecha[1] + fecha[2]
    return fecha_numero







