import parametros
import random


def cargar_partida():
    with open(parametros.RUTA_MAPA_CSV, "r", encoding="UTF-8") as file:
        datos = file.readlines()
        datos = [dato.strip().split(",") for dato in datos]
    return datos


def revisar_creacion(datos, forma, pos):
    condicion = True
    lista_puntos = [[pos[0], pos[1]], [pos[0] + forma[0], pos[1]], [pos[0], pos[1] + forma[1]],
                    [pos[0] + forma[0], pos[1] + forma[1]],
                    [pos[0] + forma[0] / 2, pos[1] + forma[1] / 2],
                    [pos[0] + forma[0] / 2, pos[1]], [pos[0], pos[1] + forma[1] / 2],
                    [pos[0] + forma[0], pos[1] + forma[1] / 2],
                    [pos[0] + forma[0] / 2, pos[1] + forma[1]]]
    for dato in datos:
        if dato[0] == "mesa":
            forma_chequeo = parametros.FORMA_MESA
        elif dato[0] == "chef":
            forma_chequeo = parametros.FORMA_CHEF
        else:
            forma_chequeo = parametros.FORMA_MESERO
        for punto in lista_puntos:
            if int(dato[1]) <= int(punto[0]) <= int(dato[1]) + forma_chequeo[0]:
                if int(dato[2]) <= int(punto[1]) <= int(dato[2]) + forma_chequeo[1]:
                    condicion = False
    return condicion


def crear_partida():
    forma_mesa = parametros.FORMA_MESA
    forma_chef = parametros.FORMA_CHEF
    forma_mesero = parametros.FORMA_MESERO
    mapa_x = parametros.LIMITE_MAPA_X
    mapa_y = parametros.LIMITE_MAPA_Y
    datos = list()
    pos_x_i = str(random.randint(mapa_x[0], mapa_x[1] - forma_mesero[0]))
    pos_y_i = str(random.randint(mapa_y[0], mapa_y[1] - forma_mesero[1]))
    mesero = ["mesero", pos_x_i, pos_y_i]
    datos.append(mesero)
    contador = 0
    while contador < parametros.MESAS_INICIALES:
        pos = [random.randint(mapa_x[0], mapa_x[1] - forma_mesa[0]),
               random.randint(mapa_y[0], mapa_y[1] - forma_mesa[1])]
        if revisar_creacion(datos, forma_mesa, pos):
            datos.append(["mesa", str(pos[0]), str(pos[1])])
            contador += 1
    contador = 0
    while contador < parametros.CHEFS_INICIALES:
        pos = [random.randint(mapa_x[0], mapa_x[1] - forma_chef[0]),
               random.randint(mapa_y[0], mapa_y[1] - forma_chef[1])]
        if revisar_creacion(datos, forma_chef, pos):
            datos.append(["chef", str(pos[0]), str(pos[1])])
            contador += 1
    with open(parametros.RUTA_MAPA_CSV, "w", encoding="UTF-8") as file:
        for dato in datos:
            file.write(",".join(dato))
            file.write("\n")
    with open(parametros.RUTA_DATOS_CSV, "w", encoding="UTF-8") as file:
        iniciales = [str(parametros.DINERO_INICIAL), str(parametros.REPUTACION_INICIAL), str(0)]
        file.write(",".join(iniciales))
        file.write("\n")
        platos = list()
        for dato in datos:
            if dato[0] == "chef":
                platos.append("0")
        file.write(",".join(platos))
        file.write("\n")
    return datos


def cargar_dccafe():
    with open(parametros.RUTA_DATOS_CSV, "r", encoding="UTF-8") as file:
        datos = file.readlines()
        datos = [dato.strip().split(",") for dato in datos]
        return datos


def aceptar_drop(mesas, chefs, mesero, pos, text):
    mapa_x = parametros.LIMITE_MAPA_X
    mapa_y = parametros.LIMITE_MAPA_Y
    if text == "mesa":
        forma = parametros.FORMA_MESA
    else:
        forma = parametros.FORMA_CHEF
    lista_datos = [[pos[0], pos[1]], [pos[0] + forma[0], pos[1]], [pos[0], pos[1] + forma[1]],
                   [pos[0] + forma[0], pos[1] + forma[1]],
                   [pos[0] + forma[0] / 2, pos[1] + forma[1] / 2],
                   [pos[0] + forma[0] / 2, pos[1]], [pos[0], pos[1] + forma[1] / 2],
                   [pos[0] + forma[0], pos[1] + forma[1] / 2],
                   [pos[0] + forma[0] / 2, pos[1] + forma[1]]]
    for mesa in mesas:
        for dato in lista_datos:
            if mesa.x() <= int(dato[0]) <= mesa.x() + parametros.FORMA_MESA[0]:
                if mesa.y() <= int(dato[1]) <= mesa.y() + parametros.FORMA_MESA[1]:
                    return False
    for chef in chefs:
        for dato in lista_datos:
            if chef.x() <= int(dato[0]) <= chef.x() + parametros.FORMA_CHEF[0]:
                if chef.y() <= int(dato[1]) <= chef.y() + parametros.FORMA_CHEF[1]:
                    return False
    for dato in lista_datos:
        if mesero.x() <= int(dato[0]) <= mesero.x() + parametros.FORMA_MESERO[0]:
            if mesero.y() <= int(dato[1]) <= mesero.y() + parametros.FORMA_MESERO[1]:
                return False
        if not (mapa_x[0] <= int(dato[0]) <= mapa_x[1]):
            return False
        if not (mapa_y[0] <= int(dato[1]) <= mapa_y[1]):
            return False
    return True
