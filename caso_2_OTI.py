from abc import ABC, abstractmethod

# CLASE ESTUDIANTE: ENCAPSULAMIENTO
class Estudiante:
    def __init__(self, nombre, becado, desaprobado, extemporaneo):
        self.__nombre = nombre
        self.__becado = becado
        self.__desaprobado = desaprobado
        self.__extemporaneo = extemporaneo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def becado(self):
        return self.__becado

    @property
    def desaprobado(self):
        return self.__desaprobado

    @property
    def extemporaneo(self):
        return self.__extemporaneo

# CLASE ABSTRACTA: HERENCIA Y POLIMORFISMO
class ReglaCobro(ABC):
    @abstractmethod
    def aplicar(self, monto):
        pass

# CLASES HIJAS
class ReglaBeca(ReglaCobro):
    def aplicar(self, monto):
        return monto * 0.5

class ReglaIndice(ReglaCobro):
    def aplicar(self, monto):
        return monto + 15

class ReglaExtemporanea(ReglaCobro):
    def aplicar(self, monto):
        return monto + 15

# CLASE MATRICULA: COMPOSICION
class Matricula:
    def __init__(self, estudiante, reglas):
        self.__estudiante = estudiante
        self.__reglas = tuple(reglas)
        self.__monto_base = 60

    def calcular_costo(self):
        monto = self.__monto_base
        for regla in self.__reglas:
            monto = regla.aplicar(monto)
        return monto

    def mostrar_reporte(self):
        print("Estudiante:", self.__estudiante.nombre)
        print("Total: S/", self.calcular_costo())

# FUNCION PARA ELEGIR EL ORDEN
def crear_reglas(estudiante, beca_primero):
    reglas = []

    if beca_primero and estudiante.becado:
        reglas.append(ReglaBeca())

    if estudiante.desaprobado:
        reglas.append(ReglaIndice())

    if estudiante.extemporaneo:
        reglas.append(ReglaExtemporanea())

    if not beca_primero and estudiante.becado:
        reglas.append(ReglaBeca())

    return reglas

# CREAMOS LOS ESTUDIANTES
luis = Estudiante("Luis Huamani Cardenas", True, True, True)
rosa = Estudiante("Rosa Ccahuana Prado", True, True, True)

# MISMA POLITICA PARA AMBOS
reglas_luis = crear_reglas(luis, beca_primero=False)
reglas_rosa = crear_reglas(rosa, beca_primero=False)

matricula_luis = Matricula(luis, reglas_luis)
matricula_rosa = Matricula(rosa, reglas_rosa)

matricula_luis.mostrar_reporte()
matricula_rosa.mostrar_reporte()
