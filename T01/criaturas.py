import parametros
from abc import ABC, abstractmethod
from random import randint
import DCC


class DCCriatura(ABC):
    def __init__(self, nombre, magia, prob_escape, prob_enfermarse, enfermo, escape, salud_max, salud, estado_hambre,
                 agresividad, dias_hambre, cleptomania):
        self.nombre = nombre
        self.salud_max = salud_max
        self.__salud = salud
        self.magia = magia
        self.enfermo = enfermo
        self.escape = escape
        self.estado_hambre = estado_hambre
        self.dias_hambre = dias_hambre
        self.prob_escape = prob_escape
        self.prob_enfermarse = prob_enfermarse
        self.agresividad = agresividad
        self.cleptomania = cleptomania
        self.max_dias_sin_comer = 0

    @property
    def salud(self):
        return self.__salud

    @salud.setter
    def salud(self, cambio):
        if self.__salud + cambio <= self.salud_max:
            self.__salud += cambio
        else:
            self.__salud = self.salud_max

    def alimentarse(self, magizoologo):
        if self.agresividad == parametros.INOFENSIVA:
            efecto_agresividad = parametros.EFECTO_INOFENSIVA
        elif self.agresividad == parametros.ARISCA:
            efecto_agresividad = parametros.EFECTO_ARISCA
        elif self.agresividad == parametros.PELIGROSA:
            efecto_agresividad = parametros.EFECTO_PELIGROSA
        if self.estado_hambre == parametros.SATISFECHA:
            efecto_hambre = parametros.EFECTO_SATISFECHA
        elif self.estado_hambre == parametros.HAMBRIENTA:
            efecto_hambre = parametros.EFECTO_HAMBRIENTA
        prob_ataque = min(1, ((efecto_agresividad + efecto_hambre) / 100))
        if randint(1, 100) <= 100 * prob_ataque:
            magizoologo.energia += -max(10, magizoologo.magia - self.magia)
            return True
        else:
            return False

    def pasar_dia(self):
        if self.estado_hambre == parametros.HAMBRIENTA:
            self.salud += -parametros.PERDIDA_HAMBRE
            print(self.nombre, "perdio salud por estar hambriento")
        if self.enfermo:
            self.salud += -parametros.PERDIDA_ENFERMO
            print(self.nombre, "perdio salud por estar enfermo")
        self.dias_hambre += 1
        if self.dias_hambre >= self.max_dias_sin_comer:
            self.estado_hambre = parametros.HAMBRIENTA
            print(self.nombre, "paso a estar hambriento")
        if self.salud == 1:
            return True
        else:
            return False

    def escaparse(self, magizoologo):
        if self.escape:
            return False
        if self.estado_hambre == parametros.HAMBRIENTA:
            hambre = parametros.EFECTO_HAMBRE
        else:
            hambre = parametros.EFECTO_SATISFECHA
        escaparse = min(1, self.prob_escape + max(0, (hambre - magizoologo.responsabilidad) / 100))
        if randint(1, 100) <= escaparse * 100:
            self.escape = True
            print(self.nombre, "se ha escapado")
            return True
        else:
            return False

    def enfermarse(self, magizoologo):
        if self.enfermo:
            return False
        enfermarse = min(1, self.prob_enfermarse + max(0, ((self.salud_max - self.salud) / self.salud_max) -
                                                       (magizoologo.responsabilidad / 100)))
        if randint(1, 100) <= enfermarse * 100:
            print(self.nombre, "se ha enfermado")
            self.enfermo = True
            return True
        else:
            return False

    @abstractmethod
    def hab_especial(self, zoologo):
        print("Esta es tu habilidad especial")


class Augurey(DCCriatura):
    def __init__(self, nombre, magia, prob_escape, prob_enfermarse, enfermo, escape, salud_max, salud, estado_hambre,
                 agresividad, dias_hambre, cleptomania):
        DCCriatura.__init__(self, nombre, magia, prob_escape, prob_enfermarse, enfermo, escape, salud_max, salud,
                            estado_hambre, agresividad, dias_hambre, cleptomania)
        self.tipo = parametros.AUGUREY
        self.max_dias_sin_comer = parametros.MAX_DIAS_SIN_COMER_AUGUREY

    def hab_especial(self, zoologo):
        if self.estado_hambre == parametros.SATISFECHA and self.salud == self.salud_max:
            lista_alimentos = [DCC.TartaMaleza(), DCC.HigadoDragon(), DCC.BuñueloGusarajo()]
            alimento = lista_alimentos[randint(0, 2)]
            zoologo.alimentos.append(alimento)
            print(self.nombre, "te ha traido de regalo:", alimento)


class Niffler(DCCriatura):
    def __init__(self, nombre, magia, prob_escape, prob_enfermarse, enfermo, escape, salud_max, salud, estado_hambre,
                 agresividad, dias_hambre, cleptomania):
        DCCriatura.__init__(self, nombre, magia, prob_escape, prob_enfermarse, enfermo, escape, salud_max, salud,
                            estado_hambre, agresividad, dias_hambre, cleptomania)
        self.tipo = parametros.NIFFLER
        self.max_dias_sin_comer = parametros.MAX_DIAS_SIN_COMER_NIFFLER

    def hab_especial(self, zoologo):
        if self.estado_hambre == parametros.HAMBRIENTA:
            if zoologo.sickles < self.cleptomania * 2:
                zoologo.sickles = 0
                print(self.nombre, "te ha robado", zoologo.sickles, "sickles")
            else:
                zoologo.sickles += -self.cleptomania * 2
        else:
            zoologo.sickles += self.cleptomania * 2


class Erkling(DCCriatura):
    def __init__(self, nombre, magia, prob_escape, prob_enfermarse, enfermo, escape, salud_max, salud, estado_hambre,
                 agresividad, dias_hambre, cleptomania):
        DCCriatura.__init__(self, nombre, magia, prob_escape, prob_enfermarse, enfermo, escape, salud_max, salud,
                            estado_hambre, agresividad, dias_hambre, cleptomania)
        self.tipo = parametros.ERKLING
        self.max_dias_sin_comer = parametros.MAX_DIAS_SIN_COMER_ERKLING

    def hab_especial(self, zoologo):
        if len(zoologo.alimentos) != 0 and self.estado_hambre == parametros.HAMBRIENTA:
            zoologo.alimentos.remove(zoologo.alimentos[randint(0, len(zoologo.alimentos) - 1)])
            self.estado_hambre = parametros.SATISFECHA
