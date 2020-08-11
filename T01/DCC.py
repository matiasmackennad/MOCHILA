import parametros
import random
import criaturas
import funciones
from abc import ABC
from random import randint


class Dcc:
    def __init__(self):
        self.tipo = parametros.DCC

    def aprobacion(self, magizoologo):
        sanas = 0
        retenidas = 0
        for dccriatura in magizoologo.dccriaturas:
            if not dccriatura.enfermo:
                sanas += 1
            if not dccriatura.escape:
                retenidas += 1
        aprobacion = min(100, max(0, int((100 * (sanas + retenidas)) / (2 * len(magizoologo.dccriaturas)))))
        return aprobacion

    def comprar(self, magizoologo):
        condicion_elegir_alimento = True
        while condicion_elegir_alimento:
            print("[1] Comprar", parametros.MALEZA)
            print("[2] Comprar", parametros.DRAGON)
            print("[3] Comprar", parametros.GUSARAJO)
            print("[0] No Comprar")
            alimento_seleccionada = input("Seleccione una opcion (1, 2, 3 o 0):")
            if alimento_seleccionada == "1":
                if magizoologo.sickles < parametros.PRECIO_MALEZA:
                    print("No puedes comprar este alimento porque no cuentas con suficientes sickles")
                else:
                    if len(magizoologo.alimentos) == 0:
                        magizoologo.alimentos = [TartaMaleza()]
                    else:
                        magizoologo.alimentos.append(TartaMaleza())
                    magizoologo.sickles += -parametros.PRECIO_MALEZA
                    print("Compraste un:", parametros.MALEZA)
                    return True
            elif alimento_seleccionada == "2":
                if magizoologo.sickles < parametros.PRECIO_DRAGON:
                    print("No puedes comprar este alimento porque no cuentas con suficientes sickles")
                else:
                    if len(magizoologo.alimentos) == 0:
                        magizoologo.alimentos = [HigadoDragon()]
                    else:
                        magizoologo.alimentos.append(HigadoDragon())
                    magizoologo.sickles += -parametros.PRECIO_DRAGON
                    print("Compraste un:", parametros.DRAGON)
                    return True
            elif alimento_seleccionada == "3":
                if magizoologo.sickles < parametros.PRECIO_GUSARAJO:
                    print("No puedes comprar este alimento porque no cuentas con suficientes sickles")
                else:
                    if len(magizoologo.alimentos) == 0:
                        magizoologo.alimentos = [BuñueloGusarajo()]
                    else:
                        magizoologo.alimentos.append(BuñueloGusarajo())
                    magizoologo.sickles += -parametros.PRECIO_GUSARAJO
                    print("Compraste un:", parametros.GUSARAJO)
                    return True
            elif alimento_seleccionada == "0":
                print("Decidiste no comprar ningun alimento")
                return False
            else:
                print("Error: Dicha opcion no existe")

    def adoptar(self, magizoologo):
        condicion_elegir_criatura = True
        while condicion_elegir_criatura:
            nombre = input("Indique el nombre que desea para su DCCriatura:")
            if funciones.validar_criatura(nombre):
                print("[1] Adoptar Augurey")
                print("[2] Adoptar Niffler")
                print("[3] Adoptar Erkling")
                print("[0] No adoptar")
                criatura_seleccionada = input("Seleccione una opcion (1, 2, 3 o 0):")
                if criatura_seleccionada == "1":
                    if magizoologo.sickles < parametros.PRECIO_AUGUREY:
                        print("No tienes suficientes sickles para adoptar un Augurey")
                    elif not magizoologo.licencia:
                        print("No puedes adoptar porque no tienes licencia")
                    else:
                        criatura = criaturas.Augurey(nombre, *funciones.generar_criatura(criatura_seleccionada, 0))
                        magizoologo.dccriaturas.append(criatura)
                        funciones.guardar_criatura(criatura)
                        magizoologo.sickles += -parametros.PRECIO_AUGUREY
                        funciones.cambiar_magizoologo(magizoologo)
                        print("Adoptaste la criatura de tipo", criatura.tipo, "con el nombre", criatura.nombre)
                        return True
                elif criatura_seleccionada == "2":
                    if magizoologo.sickles < parametros.PRECIO_NIFFLER:
                        print("No tienes suficientes sickles para adoptar un Niffler")
                    elif not magizoologo.licencia:
                        print("No puedes adoptar porque no tienes licencia")
                    else:
                        cleptomania = randint(*parametros.CLEPTOMANIA_NIFFLER)
                        criatura = criaturas.Niffler(nombre, *funciones.generar_criatura(criatura_seleccionada,
                                                                                         cleptomania))
                        magizoologo.dccriaturas.append(criatura)
                        funciones.guardar_criatura(criatura)
                        magizoologo.sickles += -parametros.PRECIO_NIFFLER
                        funciones.cambiar_magizoologo(magizoologo)
                        print("Adoptaste la criatura de tipo", criatura.tipo, "con el nombre", criatura.nombre)
                        return True
                elif criatura_seleccionada == "3":
                    if magizoologo.sickles < parametros.PRECIO_ERKLING:
                        print("No tienes suficientes sickles para adoptar un Augurey")
                    elif not magizoologo.licencia:
                        print("No puedes adoptar porque no tienes licencia")
                    else:
                        criatura = criaturas.Erkling(nombre, *funciones.generar_criatura(criatura_seleccionada, 0))
                        magizoologo.dccriaturas.append(criatura)
                        funciones.guardar_criatura(criatura)
                        magizoologo.sickles += -parametros.PRECIO_ERKLING
                        funciones.cambiar_magizoologo(magizoologo)
                        print("Adoptaste la criatura de tipo", criatura.tipo, "con el nombre", criatura.nombre)
                        return True
                elif criatura_seleccionada == "0":
                    print("Has decidido no adoptar a una DCCriatura")
                    return False
                else:
                    print("Error: La opcion seleccionada no existe")

    def revisar(self, magizoologo):
        print("Datos del magizoologo:", magizoologo.nombre)
        print("Sickles:", magizoologo.sickles, "\nEnergia actual:", magizoologo.energia)
        aprobacion = self.aprobacion(magizoologo)
        if magizoologo.licencia:
            print("Usted SI cuenta con su licencia, y su nivel de aprobacion es", aprobacion)
        else:
            print("Usted NO cuenta con su licencia, y su nivel de aprobacion es", aprobacion)
        print("Nivel magico:", magizoologo.magia, "\nDestreza:", magizoologo.destreza, "\nResponsabilidad:",
              magizoologo.responsabilidad)
        if len(magizoologo.alimentos) == 0:
            print("No tienes alimentos restantes")
        else:
            print("Tus alimentos restantes son:")
        for alimento in magizoologo.alimentos:
            if alimento.efecto_salud == parametros.SALUD_MALEZA:
                print(parametros.MALEZA, "\n", "Efecto de salud:", parametros.SALUD_MALEZA)
            elif alimento.efecto_salud == parametros.SALUD_DRAGON:
                print(parametros.DRAGON, "\n", "Efecto de salud:", parametros.SALUD_DRAGON)
            elif alimento.efecto_salud == parametros.SALUD_GUSARAJO:
                print(parametros.GUSARAJO, "\n", "Efecto de salud:", parametros.SALUD_GUSARAJO)
        print("Tus dccriaturas adoptadas son:")
        for dccriatura in magizoologo.dccriaturas:
            if dccriatura.enfermo:
                print(dccriatura.nombre, "\n", "Salud:", dccriatura.salud, "\n", "La criatura esta enferma", "\n",
                      "La criatura esta", dccriatura.estado_hambre, "\n", "La criatura es", dccriatura.agresividad)
            else:
                print(dccriatura.nombre, "\n", "Salud:", dccriatura.salud, "\n", "La criatura esta sana", "\n",
                      "La criatura esta", dccriatura.estado_hambre, "\n", "La criatura es", dccriatura.agresividad)

    def pasar_dia(self, zoologo):
        pago = 4 * self.aprobacion(zoologo) + 15 * len(zoologo.alimentos) + 3 * zoologo.magia
        zoologo.sickles += pago
        print("Se te ha pagado", pago, "sickles")
        licencia = True
        escapadas = list()
        vida_minima = list()
        enfermas = list()
        for dccriatura in zoologo.dccriaturas:
            if dccriatura.pasar_dia():
                vida_minima.append(dccriatura.nombre)
            if dccriatura.escaparse(zoologo):
                escapadas.append(dccriatura.nombre)
            if dccriatura.enfermarse(zoologo):
                enfermas.append(dccriatura.nombre)
            funciones.cambiar_criatura(dccriatura)
        if len(enfermas) == 0:
            print("Ninguna dccriatura se enfermo")
        else:
            print("Se enfermaron:", ", ".join(enfermas))
        if len(escapadas) == 0:
            print("Ninuna dccriatura se escapo")
        else:
            print("Se escaparon:", ", ".join(escapadas))
        if len(vida_minima) == 0:
            print("Ninuna dccriatura quedo con salud aminima")
        else:
            print("Quedaron con salud minima:", ", ".join(vida_minima))
        for enferma in enfermas:
            if randint(1, 100) <= parametros.PROB_ENFERMAS:
                if zoologo.sickles < parametros.COBRO_ENFERMAS:
                    if licencia:
                        print("Se te ha quitado la licencia por no poder pagar la multa por enfermedad de", enferma)
                    licencia = False
                    break
                else:
                    print("Se te cobro", parametros.COBRO_ENFERMAS, "por la enfermedad de", enferma)
                    zoologo.sickles += -parametros.COBRO_ENFERMAS
        for escapada in escapadas:
            if randint(1, 100) <= parametros.PROB_ESCAPADAS:
                if zoologo.sickles < parametros.COBRO_ESCAPADAS:
                    if licencia:
                        print("Se te ha quitado la licencia por no poder pagar la multa por el escape de", escapada)
                    licencia = False
                    break
                else:
                    print("Se te cobro", parametros.COBRO_ESCAPADAS, "por el escape de", escapada)
                    zoologo.sickles += -parametros.COBRO_ESCAPADAS
        for muriendose in vida_minima:
            if zoologo.sickles < parametros.COBRO_VIDA_MINIMA:
                if licencia:
                    print("Se te ha quitado la licencia por no poder pagar la multa por el estado de vida minima de",
                          muriendose)
                licencia = False
                break
            else:
                print("Se te cobro", parametros.COBRO_VIDA_MINIMA, "por el estado de vida minima de", muriendose)
                zoologo.sickles += -parametros.COBRO_VIDA_MINIMA
        for dccriatura in zoologo.dccriaturas:
            dccriatura.hab_especial(zoologo)
            funciones.cambiar_criatura(dccriatura)
        if licencia and self.aprobacion(zoologo) < parametros.MINIMO_APROBACION:
            print("Usted no mantuvo su licencia y obtuvo una aprobacion de", self.aprobacion(zoologo))
            zoologo.licencia = False
        else:
            print("Usted mantuvo su licencia con una aprobacion de", self.aprobacion(zoologo))
            zoologo.licencia = True
        funciones.cambiar_magizoologo(zoologo)


class Alimento(ABC):
    def __init__(self):
        self.efecto_salud = 0

    def rechazo(self):
        return False

    def sanada_especial(self):
        return False

    def anti_agresivo(self):
        return False


class TartaMaleza(Alimento):
    def __init__(self):
        Alimento.__init__(self)
        self.efecto_salud = parametros.SALUD_MALEZA

    def __str__(self):
        return parametros.MALEZA

    def anti_agresivo(self):
        if random.randint(1, 100) <= parametros.ANTI_AGRESIVO:
            return True
        else:
            return False


class HigadoDragon(Alimento):
    def __init__(self):
        Alimento.__init__(self)
        self.efecto_salud = parametros.SALUD_DRAGON

    def __str__(self):
        return parametros.DRAGON

    def sanada_especial(self):
        return True


class BuñueloGusarajo(Alimento):
    def __init__(self):
        Alimento.__init__(self)
        self.efecto_salud = parametros.SALUD_GUSARAJO

    def __str__(self):
        return parametros.GUSARAJO

    def rechazo(self):
        if random.randint(1, 100) <= parametros.RECHAZO:
            return False
        else:
            return True



