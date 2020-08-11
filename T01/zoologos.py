from abc import ABC, abstractmethod
from random import randint
import funciones
import parametros


class Magizoologo(ABC):
    def __init__(self, nombre, sickles, dccriaturas,  alimentos, licencia, magia, destreza, energia_max,
                 responsabilidad, hab_especial):
        self.nombre = nombre
        self.energia_max = energia_max
        self.sickles = sickles
        self.__energia = energia_max
        self.licencia = licencia
        self.dccriaturas = dccriaturas
        self.alimentos = alimentos
        self.magia = magia
        self.destreza = destreza
        self.responsabilidad = responsabilidad
        self.especial = hab_especial

    @property
    def energia(self):
        return self.__energia

    @energia.setter
    def energia(self, cambio):
        if self.__energia + cambio < 0:
            self.__energia = 0
        elif self.__energia + cambio > self.energia_max:
            self.__energia = self.energia_max
        else:
            self.__energia += cambio

    @abstractmethod
    def alimentar(self, criatura, alimento):
        print("alimentaste a tu criatura")

    @abstractmethod
    def recuperar(self, criatura):
        print("Has recuperado tu criatura")

    @abstractmethod
    def hab_especial(self):
        print("Has ocupado tu habilidad especial")

    def sanar(self, criatura):
        if criatura.escape:
            print("No puedes sanar a una dccriatura que esta escapada")
            return False
        if criatura.enfermo:
            if self.energia < parametros.COBRO_SANAR:
                print("No puedes realizar esta accion")
                return False
            else:
                self.energia += -parametros.COBRO_SANAR
        else:
            print("No puedes sanar una criatura sana")
            return False
        prob_sanar = min(1, max(0, (self.magia - criatura.salud) / (self.magia + criatura.salud)))
        if randint(1, 100) <= prob_sanar * 100:
            criatura.enfermo = False
            print("Has sanado la DCCriatura")
            return True
        else:
            print("no pudiste sanar a la DCCriatura")
            return False


class Docencio(Magizoologo):
    def __init__(self, nombre, sickles, dccriaturas,  alimentos, licencia, magia, destreza, energia_max,
                 responsabilidad, hab_especial):
        Magizoologo.__init__(self, nombre, sickles, dccriaturas,  alimentos, licencia, magia, destreza, energia_max,
                             responsabilidad, hab_especial)
        self.tipo = parametros.DOCENCIO

    def alimentar(self, criatura, alimento):
        if criatura.escape:
            print("No puedes sanar a una dccriatura que esta escapada")
            return False
        if len(self.alimentos) == 0:
            print("No tienes alimentos")
            return False
        self.energia += -parametros.COSTO_ALIMENTAR
        if criatura.alimentarse(self):
            print("La criatura te ha atcado")
        if alimento.rechazo():
            self.alimentos.remove(alimento)
            print("La DCCriatura rechazo el alimento que le diste")
            return False
        else:
            if criatura.tipo == parametros.NIFFLER and alimento.anti_agresivo():
                criatura.agresividad = parametros.INOFENSIVA
                print("La DCCriatura se ha vuelto inofensiva")
            if criatura.enfermo and alimento.sanada_especial():
                criatura.enfermo = False
                print("La DCCriatura se ha mejorado de su enfermedad")
            criatura.salud += parametros.EXTRA_ALIMENTAR
            criatura.salud += alimento.efecto_salud
            criatura.dias_hambre = 0
            criatura.estado_hambre = parametros.SATISFECHA
            self.alimentos.remove(alimento)
            print("Alimentaste a", criatura.nombre)
            return True

    def hab_especial(self):
        for dccriatura in self.dccriaturas:
            dccriatura.estado_hambre = parametros.SATISFECHA
            dccriatura.dias_hambre = 0
            funciones.cambiar_criatura(dccriatura)
        self.especial = False
        print("Alimentaste todas tus dccriaturas")

    def recuperar(self, criatura):
        if criatura.escape:
            prob_escape = min(1, max(0, (self.destreza + self.magia - criatura.magia) / (self.destreza + self.magia
                                                                                         + criatura.magia)))
            if randint(1, 100) <= prob_escape * 100:
                print("Has recuperado a tu dccriatura")
                criatura.escape = False
                self.energia += -parametros.COSTO_RECUPERAR
                criatura.salud += -parametros.EXTRA_RECUPERAR
                return True
            else:
                print("No lograste recuperar la dccriatura seleccionada")
                return False
        else:
            print("Dicha criatura no se ha escapado")
            return False


class Tareo(Magizoologo):
    def __init__(self, nombre, sickles, dccriaturas,  alimentos, licencia, magia, destreza, energia_max,
                 responsabilidad, hab_especial):
        Magizoologo.__init__(self, nombre, sickles, dccriaturas,  alimentos, licencia, magia, destreza, energia_max,
                             responsabilidad, hab_especial)
        self.tipo = parametros.TAREO

    def alimentar(self, criatura, alimento):
        if criatura.escape:
            print("No puedes sanar a una dccriatura que esta escapada")
            return False
        if len(self.alimentos) == 0:
            print("No tienes alimentos")
            return False
        self.energia += -parametros.COSTO_ALIMENTAR
        if criatura.alimentarse(self):
            print("La criatura te ha atcado")
        if alimento.rechazo():
            self.alimentos.remove(alimento)
            print("La DCCriatura rechazo el alimento que le diste")
            return False
        else:
            if criatura.tipo == parametros.NIFFLER and alimento.anti_agresivo():
                criatura.agresividad = parametros.INOFENSIVA
                print("La DCCriatura se ha vuelto inofensiva")
            if criatura.enfermo and alimento.sanada_especial():
                criatura.enfermo = False
                print("La DCCriatura se ha mejorado de su enfermedad")
            if randint(1, 100) <= parametros.PROB_RECUPERADO_ESPECIAL:
                print("La DCCriatura ha recuperado toda su salud")
                criatura.salud = criatura.salud_max
            criatura.salud += alimento.efecto_salud
            criatura.dias_hambre = 0
            criatura.estado_hambre = parametros.SATISFECHA
            self.alimentos.remove(alimento)
            print("Alimentaste a", criatura.nombre)
            return True

    def recuperar(self, criatura):
        if criatura.escape:
            prob_escape = min(1, max(0, (self.destreza + self.magia - criatura.magia) / (self.destreza + self.magia
                                                                                         + criatura.magia)))
            if randint(1, 100) <= prob_escape * 100:
                print("Has recuperado a tu dccriatura")
                criatura.escape = False
                self.energia += -parametros.COSTO_RECUPERAR
                return True
            else:
                print("No lograste recuperar la dccriatura seleccionada")
                return False
        else:
            print("Dicha criatura no se ha escapado")
            return False

    def hab_especial(self):
        for dccriatura in self.dccriaturas:
            dccriatura.escape = False
            funciones.cambiar_criatura(dccriatura)
        self.especial = False
        print("Recuperaste todas tus dccriaturas")


class Hibrido(Magizoologo):
    def __init__(self, nombre, sickles, dccriaturas,  alimentos, licencia, magia, destreza, energia_max,
                 responsabilidad, hab_especial):
        Magizoologo.__init__(self, nombre, sickles, dccriaturas,  alimentos, licencia, magia, destreza, energia_max,
                             responsabilidad, hab_especial)
        self.tipo = parametros.HIBRIDO

    def alimentar(self, criatura, alimento):
        if criatura.escape:
            print("No puedes sanar a una dccriatura que esta escapada")
            return False
        if len(self.alimentos) == 0:
            print("No tienes alimentos")
        self.energia += -parametros.COSTO_ALIMENTAR
        if criatura.alimentarse(self):
            print("La criatura te ha atcado")
            return False
        if alimento.rechazo():
            self.alimentos.remove(alimento)
            print("La DCCriatura rechazo el alimento que le diste")
            return False
        else:
            if criatura.tipo == parametros.NIFFLER and alimento.anti_agresivo():
                criatura.agresividad = parametros.INOFENSIVA
                print("La DCCriatura se ha vuelto inofensiva")
            if criatura.enfermo and alimento.sanada_especial():
                criatura.enfermo = False
                print("La DCCriatura se ha mejorado de su enfermedad")
            criatura.salud += parametros.EXTRA_ALIMENTAR_HIBRIDO
            criatura.salud += alimento.efecto_salud
            criatura.dias_hambre = 0
            criatura.estado_hambre = parametros.SATISFECHA
            self.alimentos.remove(alimento)
            print("Alimentaste a", criatura.nombre)
            return True

    def recuperar(self, criatura):
        if criatura.escape:
            prob_escape = min(1, max(0, (self.destreza + self.magia - criatura.magia) / (self.destreza + self.magia
                                                                                         + criatura.magia)))
            if randint(1, 100) <= prob_escape * 100:
                print("Has recuperado a tu dccriatura")
                criatura.escape = False
                self.energia += -parametros.COSTO_RECUPERAR
                return True
            else:
                print("No lograste recuperar la dccriatura seleccionada")
                return False
        else:
            print("Dicha criatura no se ha escapado")
            return False

    def hab_especial(self):
        for dccriatura in self.dccriaturas:
            dccriatura.enfermo = False
            funciones.cambiar_criatura(dccriatura)
        self.especial = False
        print("Sanaste todas tus dccriaturas")
