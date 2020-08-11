import parametros
from random import randint
import DCC
import criaturas


def validar_usuario(nombre):
    with open(parametros.MAGIZOOLOGOS, "r", encoding="UTF-8") as file:
        usuarios = list()
        for line in file:
            magizoologos = line.split(",")
            usuarios.append(magizoologos[0])
        for usuario in usuarios:
            if usuario.upper() == nombre.upper():
                print("Error: Este usuario ya existe")
                return False
        if len(nombre) < 8:
            print("El nombre de su magizoologo debe tener al menos 8 caracteres")
            return False
        if not nombre.isalnum():
            print("Error: El nombre seleccionado no es alfanumerico")
            return False
        else:
            print("Se a aceptado", nombre, "como tu nombre de magizoologo")
            return True


def generar_datos(tipo):
    if tipo == "1":
        energia = randint(*parametros.ENERGIA_DOCENCIO)
        destreza = randint(*parametros.DESTREZA_DOCENCIO)
        magia = randint(*parametros.MAGIA_DOCENCIO)
        responsabilidad = randint(*parametros.RESPONSABILIDAD_DOCENCIO)
    elif tipo == "2":
        energia = randint(*parametros.ENERGIA_TAREO)
        destreza = randint(*parametros.DESTREZA_TAREO)
        magia = randint(*parametros.MAGIA_TAREO)
        responsabilidad = randint(*parametros.RESPONSABILIDAD_TAREO)
    elif tipo == "3":
        energia = randint(*parametros.ENERGIA_HIBRIDO)
        destreza = randint(*parametros.DESTREZA_HIBRIDO)
        magia = randint(*parametros.MAGIA_HIBRIDO)
        responsabilidad = randint(*parametros.RESPONSABILIDAD_HIBRIDO)
    datos = (parametros.SICKLES_INICIALES, [], [], True, magia, destreza, energia, responsabilidad, True)
    return datos


def generar_criatura(tipo, cleptomania):
    if tipo == "1":
        salud = randint(*parametros.SALUD_AUGUREY)
        magia = randint(*parametros.MAGIA_AUGUREY)
        prob_escape = parametros.PROB_ESCAPE_AUGUREY
        prob_enfermarse = parametros.PROB_ENFERMARSE_AUGUREY
        agresividad = parametros.INOFENSIVA
    elif tipo == "2":
        salud = randint(*parametros.SALUD_NIFFLER)
        magia = randint(*parametros.MAGIA_NIFFLER)
        prob_escape = parametros.PROB_ESCAPE_NIFFLER
        prob_enfermarse = parametros.PROB_ENFERMARSE_NIFFLER
        agresividad = parametros.ARISCA
    elif tipo == "3":
        salud = randint(*parametros.SALUD_ERKLING)
        magia = randint(*parametros.MAGIA_ERKLING)
        prob_escape = parametros.PROB_ESCAPE_ERKLING
        prob_enfermarse = parametros.PROB_ENFERMARSE_ERKLING
        agresividad = parametros.PELIGROSA
    datos = (magia, prob_escape, prob_enfermarse, False, False, salud, salud, parametros.SATISFECHA, agresividad, 0,
             cleptomania)
    return datos


def guardar_magizoologo(magizoologo):
    lista_guardado = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    lista_guardado[0] = magizoologo.nombre
    lista_guardado[1] = magizoologo.tipo
    lista_guardado[2] = str(magizoologo.sickles)
    lista_dccriaturas = [criatura.nombre for criatura in magizoologo.dccriaturas]
    lista_guardado[3] = ";".join(lista_dccriaturas)
    lista_guardado[4] = ";".join(magizoologo.alimentos)
    lista_guardado[5] = str(magizoologo.licencia)
    lista_guardado[6] = str(magizoologo.magia)
    lista_guardado[7] = str(magizoologo.destreza)
    lista_guardado[8] = str(magizoologo.energia_max)
    lista_guardado[9] = str(magizoologo.responsabilidad)
    lista_guardado[10] = str(magizoologo.especial)
    string_guardado = ",".join(lista_guardado)
    with open(parametros.MAGIZOOLOGOS, "a", encoding="UTF-8") as file:
        file.write(string_guardado)
        file.write("\n")


def validar_criatura(nombre):
    with open(parametros.CRIATURAS, "r", encoding="UTF-8") as file:
        dccriaturas = list()
        lista_file = file.readlines()
        for line in lista_file:
            lista_criaturas = line.split(",")
            dccriaturas.append(lista_criaturas[0])
        for criatura in dccriaturas:
            if criatura.upper() == nombre.upper():
                print("Error: Ese nombre ya esta ocupado")
                return False
        if len(nombre) == 0:
            print("La criatura debe tener nombre")
            return False
        if not nombre.isalnum():
            print("Error: El nombre debe ser alfanumerico")
            return False
        else:
            print("Has escogido", nombre, "como el nombre de tu DCCriatura")
            return True


def guardar_criatura(criatura):
    lista_guardado = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    lista_guardado[0] = criatura.nombre
    lista_guardado[1] = criatura.tipo
    lista_guardado[2] = str(criatura.magia)
    lista_guardado[3] = str(criatura.prob_escape)
    lista_guardado[4] = str(criatura.prob_enfermarse)
    lista_guardado[5] = str(criatura.enfermo)
    lista_guardado[6] = str(criatura.escape)
    lista_guardado[7] = str(criatura.salud_max)
    lista_guardado[8] = str(criatura.salud)
    lista_guardado[9] = criatura.estado_hambre
    lista_guardado[10] = criatura.agresividad
    lista_guardado[11] = str(criatura.dias_hambre)
    lista_guardado[12] = str(criatura.cleptomania)
    string_guardado = ",".join(lista_guardado)
    with open(parametros.CRIATURAS, "a", encoding="UTF-8") as file:
        file.write(string_guardado)
        file.write("\n")


def cambiar_criatura(criatura):
    lista_guardado = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    lista_guardado[0] = criatura.nombre
    lista_guardado[1] = criatura.tipo
    lista_guardado[2] = str(criatura.magia)
    lista_guardado[3] = str(criatura.prob_escape)
    lista_guardado[4] = str(criatura.prob_enfermarse)
    lista_guardado[5] = str(criatura.enfermo)
    lista_guardado[6] = str(criatura.escape)
    lista_guardado[7] = str(criatura.salud_max)
    lista_guardado[8] = str(criatura.salud)
    lista_guardado[9] = criatura.estado_hambre
    lista_guardado[10] = criatura.agresividad
    lista_guardado[11] = str(criatura.dias_hambre)
    lista_guardado[12] = str(criatura.cleptomania)
    string_guardado = ",".join(lista_guardado)
    with open(parametros.CRIATURAS, "r", encoding="UTF-8") as file:
        lista = file.readlines()
        contador = 0
        while contador < len(lista):
            lista_split = lista[contador].split(",")
            if lista_split[0] == criatura.nombre:
                lista[contador] = string_guardado + "\n"
            contador += 1
        with open(parametros.CRIATURAS, "w", encoding="UTF-8") as archivo:
            for line in lista:
                archivo.write(line)


def abrir_magizoologo(nombre):
    with open(parametros.MAGIZOOLOGOS, "r", encoding="UTF-8") as file:
        for line in file:
            lista = line.split(",")
            if lista[0].upper() == nombre.upper():
                lista[2] = int(lista[2])
                lista[3] = lista[3].split(";")
                lista_dccriaturas = list()
                for nombre in lista[3]:
                    criatura = abrir_criatura(nombre)
                    if criatura[1] == parametros.AUGUREY:
                        dccriatura = criaturas.Augurey(criatura[0], *criatura[2: len(criatura)])
                    elif criatura[1] == parametros.NIFFLER:
                        dccriatura = criaturas.Niffler(criatura[0], *criatura[2: len(criatura)])
                    elif criatura[1] == parametros.ERKLING:
                        dccriatura = criaturas.Erkling(criatura[0], *criatura[2: len(criatura)])
                    lista_dccriaturas.append(dccriatura)
                lista[3] = lista_dccriaturas
                lista[4] = lista[4].split(";")
                lista_alimentos = list()
                for alimento in lista[4]:
                    if alimento == parametros.MALEZA:
                        lista_alimentos.append(DCC.TartaMaleza())
                    elif alimento == parametros.DRAGON:
                        lista_alimentos.append(DCC.HigadoDragon())
                    elif alimento == parametros.GUSARAJO:
                        lista_alimentos.append(DCC.BuñueloGusarajo())
                lista[4] = lista_alimentos
                lista[5] = bool(lista[5] == "True")
                lista[6] = int(lista[6])
                lista[7] = int(lista[7])
                lista[8] = int(lista[8])
                lista[9] = int(lista[9])
                lista[10] = bool(lista[10] == "True")
                return lista
        return []


def abrir_criatura(nombre):
    with open(parametros.CRIATURAS, "r", encoding="UTF-8") as file:
        file1 = file.readlines()
        for line in file1:
            lista = line.split(",")
            if lista[0].upper() == nombre.upper():
                lista[2] = int(lista[2])
                lista[3] = float(lista[3])
                lista[4] = float(lista[4])
                lista[5] = bool(lista[5] == "True")
                lista[6] = bool(lista[6] == "True")
                lista[7] = int(lista[7])
                lista[8] = int(lista[8])
                lista[11] = int(lista[11])
                lista[12] = int(lista[12])
                return lista
        return []


def obtener_alimento(magizoologo):
    print("estos son tus alimentos:")
    contador = 0
    while contador < len(magizoologo.alimentos):
        if magizoologo.alimentos[contador].efecto_salud == parametros.SALUD_MALEZA:
            print("[" + str(contador) + "]", parametros.MALEZA)
        elif magizoologo.alimentos[contador].efecto_salud == parametros.SALUD_DRAGON:
            print("[" + str(contador) + "]", parametros.DRAGON)
        elif magizoologo.alimentos[contador].efecto_salud == parametros.SALUD_GUSARAJO:
            print("[" + str(contador) + "]", parametros.GUSARAJO)
        contador += 1
    condicion_alimento = True
    while condicion_alimento:
        opcion = input("Seleccione una opcion:")
        if 0 <= int(opcion) < len(magizoologo.alimentos):
            condicion_alimento = False
        else:
            print("Dicha opcion no existe")
    return magizoologo.alimentos[int(opcion)]


def obtener_criatura(magizoologo):
    print("estos son tus dccriaturas:")
    contador = 0
    while contador < len(magizoologo.dccriaturas):
        print("[" + str(contador) + "]", magizoologo.dccriaturas[contador].nombre)
        contador += 1
    condicion_criatura = True
    while condicion_criatura:
        opcion = input("Seleccione una opcion:")
        if 0 <= int(opcion) < len(magizoologo.dccriaturas):
            criatura = magizoologo.dccriaturas[int(opcion)]
            condicion_criatura = False
        else:
            print("No existe dicha opcion")
    return criatura


def cambiar_magizoologo(magizoologo):
    lista_guardado = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    lista_guardado[0] = magizoologo.nombre
    lista_guardado[1] = magizoologo.tipo
    lista_guardado[2] = str(magizoologo.sickles)
    lista_dccriaturas = [criatura.nombre for criatura in magizoologo.dccriaturas]
    lista_guardado[3] = ";".join(lista_dccriaturas)
    lista_alimentos = list()
    for alimento in magizoologo.alimentos:
        if alimento.efecto_salud == parametros.SALUD_MALEZA:
            lista_alimentos.append(parametros.MALEZA)
        if alimento.efecto_salud == parametros.SALUD_DRAGON:
            lista_alimentos.append(parametros.DRAGON)
        elif alimento.efecto_salud == parametros.SALUD_GUSARAJO:
            lista_alimentos.append(parametros.GUSARAJO)
    lista_guardado[4] = ";".join(lista_alimentos)
    lista_guardado[5] = str(magizoologo.licencia)
    lista_guardado[6] = str(magizoologo.magia)
    lista_guardado[7] = str(magizoologo.destreza)
    lista_guardado[8] = str(magizoologo.energia_max)
    lista_guardado[9] = str(magizoologo.responsabilidad)
    lista_guardado[10] = str(magizoologo.especial)
    string_guardado = ",".join(lista_guardado)
    with open(parametros.MAGIZOOLOGOS, "r", encoding="UTF-8") as file:
        lista = file.readlines()
        contador = 0
        while contador < len(lista):
            lista_split = lista[contador].split(",")
            if lista_split[0] == magizoologo.nombre:
                lista[contador] = string_guardado + "\n"
            contador += 1
        with open(parametros.MAGIZOOLOGOS, "w", encoding="UTF-8") as archivo:
            for line in lista:
                archivo.write(line)






