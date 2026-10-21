"""
Caso OTI - POO .
"""
from abc import ABC, abstractmethod
from enum import Enum
import datetime

#### Funciones de validación (apoyan la Actividad 2.1) ####
def validar_texto(valor, campo, maximo=None):
    """El texto no puede quedar vacío ni pasar del máximo de caracteres."""
    if not isinstance(valor, str):
        raise TypeError(f"{campo}: debe ser texto")
    valor = valor.strip()
    if valor == "":
        raise ValueError(f"{campo}: no puede quedar vacío")
    if maximo is not None and len(valor) > maximo:
        raise ValueError(f"{campo}: no puede pasar de {maximo} caracteres")
    return valor


def validar_entero(valor, campo, minimo, maximo=None):
    """Número entero dentro de un rango (el mínimo y el máximo se permiten)."""
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"{campo}: debe ser un número entero")
    if valor < minimo:
        raise ValueError(f"{campo}: no puede ser menor que {minimo}")
    if maximo is not None and valor > maximo:
        raise ValueError(f"{campo}: no puede pasar de {maximo}")
    return valor


def validar_numero(valor, campo, minimo, maximo=None,
                   incluir_minimo=True, max_decimales=None):
    """Número con decimales (int o float) dentro de un rango."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError(f"{campo}: debe ser un número")
    if incluir_minimo and valor < minimo:
        raise ValueError(f"{campo}: no puede ser menor que {minimo}")
    if not incluir_minimo and valor <= minimo:
        raise ValueError(f"{campo}: debe ser mayor que {minimo}")
    if maximo is not None and valor > maximo:
        raise ValueError(f"{campo}: no puede pasar de {maximo}")
    if max_decimales is not None and round(valor, max_decimales) != valor:
        raise ValueError(f"{campo}: admite como máximo {max_decimales} decimales")
    return valor


#### Actividad 3.3: Enum del estado del periodo ####

class EstadoPeriodo(Enum):
    PLANIFICADO = 1
    EN_CURSO = 2
    MATRICULA_CERRADA = 3
    FINALIZADO = 4
# Ejemplos:  EstadoPeriodo(2) -> EN_CURSO      EstadoPeriodo(7) -> ValueError

#### Actividad 3.1 y 3.2: clase abstracta RegistroConNombre ####
class RegistroConNombre(ABC):

    def __init__(self, nombre):
        self._nombre = None       # ACTIVIDAD 2.1: dato protegido 
        self.nombre = nombre      # usa el setter, por eso se valida

    # Actividad 2.1: dato protegido con regla de validación
    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "El nombre", self.limite_nombre())

    # Actividad 3.2: método abstracto
    @abstractmethod
    def limite_nombre(self):
        """Cantidad máxima de caracteres que admite el nombre."""

    @abstractmethod
    def resumen(self):
        """Texto corto que describe al registro."""


#### Actividad 3.1 y 3.2: clase abstracta Persona ####

class Persona(ABC):

    def __init__(self, dni, nombres, apellidos):
        # Actividad 2.1: dato protegido con regla de validación
        self._dni = None
        self._nombres = None
        self._apellidos = None
        self.dni = dni
        self.nombres = nombres
        self.apellidos = apellidos

    # Actividad 2.1: dato protegido con regla de validación
    @property
    def dni(self):
        return self._dni

    @dni.setter
    def dni(self, valor):
        self._dni = validar_texto(valor, "El DNI")

    @property
    def nombres(self):
        return self._nombres

    @nombres.setter
    def nombres(self, valor):
        self._nombres = validar_texto(valor, "Los nombres")

    @property
    def apellidos(self):
        return self._apellidos

    @apellidos.setter
    def apellidos(self, valor):
        self._apellidos = validar_texto(valor, "Los apellidos")

    # Actividad 2.2: dato calculado (no se guarda)
    @property
    def nombre_completo(self):
        return f"{self._nombres} {self._apellidos}"

    # Actividad 3.2: método abstracto
    @abstractmethod
    def rol(self):
        """Rol que cumple la persona en la universidad."""

    def resumen(self):
        return f"{self.rol()}: {self.nombre_completo} (DNI {self._dni})"

    def __str__(self):
        return self.resumen()

#### Actividad 1 y 4: Curso es un RegistroConNombre ###
# Hereda el nombre; agrega id, créditos y horas; redefine limite_nombre y resumen
class Curso(RegistroConNombre):
    _contador_id = 0

    def __init__(self, codigo, nombre, creditos, horas_teoricas=0,
                 horas_practicas=0, horas_seminario=0, horas_virtuales=0):
        super().__init__(nombre)            # el nombre lo valida la clase padre
        Curso._contador_id += 1
        self._id = Curso._contador_id       # lo genera el sistema, nadie lo cambia
        self._codigo = None
        self._creditos = None
        self._horas_teoricas = None
        self._horas_practicas = None
        self._horas_seminario = None
        self._horas_virtuales = None
        self.codigo = codigo
        self.creditos = creditos
        self.horas_teoricas = horas_teoricas
        self.horas_practicas = horas_practicas
        self.horas_seminario = horas_seminario
        self.horas_virtuales = horas_virtuales

    # Actividad 2.3: sin modificación directa
    @property
    def id(self):
        return self._id

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = validar_texto(valor, "El código")

    # Actividad 2.1: dato protegido con regla de validación
    @property
    def creditos(self):
        return self._creditos

    @creditos.setter
    def creditos(self, valor):
        self._creditos = validar_numero(valor, "Los créditos", 0,
                                        incluir_minimo=False, max_decimales=2)

    # Actividad 2.1: dato protegido con regla de validación
    @property
    def horas_teoricas(self):
        return self._horas_teoricas

    @horas_teoricas.setter
    def horas_teoricas(self, valor):
        self._horas_teoricas = validar_entero(valor, "Las horas teóricas", 0, 255)

    @property
    def horas_practicas(self):
        return self._horas_practicas

    @horas_practicas.setter
    def horas_practicas(self, valor):
        self._horas_practicas = validar_entero(valor, "Las horas prácticas", 0, 255)

    @property
    def horas_seminario(self):
        return self._horas_seminario

    @horas_seminario.setter
    def horas_seminario(self, valor):
        self._horas_seminario = validar_entero(valor, "Las horas de seminario", 0, 255)

    @property
    def horas_virtuales(self):
        return self._horas_virtuales

    @horas_virtuales.setter
    def horas_virtuales(self, valor):
        self._horas_virtuales = validar_entero(valor, "Las horas virtuales", 0, 255)

    # Actividad 2.2: dato calculado (no se guarda)
    @property
    def horas_totales(self):
        return (self._horas_teoricas + self._horas_practicas
                + self._horas_seminario + self._horas_virtuales)

    # Actividad 4.2: redefine el método de la clase padre
    def limite_nombre(self):
        return 200

    def resumen(self):
        return (f"Curso {self._codigo} - {self._nombre} | "
                f"{self._creditos} créditos | {self.horas_totales} horas")


# --- Actividad 1: Seccion (no hereda de nadie) ---
class Seccion:

    def __init__(self, codigo, codigo_curso, codigo_periodo, vacantes):
        # Actividad 2.3: sin modificación directa
        self._codigo = validar_texto(codigo, "El código de la sección")
        self._codigo_curso = validar_texto(codigo_curso, "El código del curso")
        self._codigo_periodo = validar_texto(codigo_periodo, "El código del periodo")
        # Actividad 2.1: dato protegido con regla de validación
        self._vacantes = validar_entero(vacantes, "Las vacantes", 1)
        self._matriculados = 0            # empieza en 0 y NO tiene setter

    @property
    def codigo(self):
        return self._codigo

    @property
    def codigo_curso(self):
        return self._codigo_curso

    @property
    def codigo_periodo(self):
        return self._codigo_periodo

    # Actividad 2.1: dato protegido con regla de validación
    @property
    def vacantes(self):
        return self._vacantes

    @vacantes.setter
    def vacantes(self, valor):
        valor = validar_entero(valor, "Las vacantes", 1)
        if valor < self._matriculados:
            raise ValueError("No se pueden reducir las vacantes por debajo "
                             f"de los matriculados ({self._matriculados})")
        self._vacantes = valor

    # Actividad 2.3: sin modificación directa
    @property
    def matriculados(self):
        return self._matriculados

    # Actividad 2.2: dato calculado (no se guarda)
    @property
    def vacantes_disponibles(self):
        return self._vacantes - self._matriculados

    # Actividad 2.3: sin modificación directa
    def matricular(self):
        """Aumenta en 1 los matriculados. Si la sección está llena, se rechaza."""
        if self._matriculados >= self._vacantes:
            raise ValueError("La sección está llena, no se puede matricular")
        self._matriculados += 1

    def retirar(self):
        """Disminuye en 1 los matriculados (un estudiante se retira)."""
        if self._matriculados == 0:
            raise ValueError("No hay estudiantes matriculados que retirar")
        self._matriculados -= 1

    def __str__(self):
        return (f"Sección {self._codigo} | curso {self._codigo_curso} | "
                f"periodo {self._codigo_periodo} | "
                f"{self._matriculados}/{self._vacantes} matriculados")


#### Actividad 1 y 4: PlanEstudio es un RegistroConNombre ####
# Hereda el nombre; agrega créditos y vigente; redefine limite_nombre y resumen

class PlanEstudio(RegistroConNombre):

    def __init__(self, nombre, anio_aprobacion, creditos_obligatorios,
                 creditos_electivos, creditos_extracurriculares, vigente=True):
        super().__init__(nombre)
        # Actividad 2.3: sin modificación directa
        self._anio_aprobacion = validar_entero(anio_aprobacion,
                                               "El año de aprobación", 1900,
                                               datetime.date.today().year)
        self._creditos_obligatorios = None
        self._creditos_electivos = None
        self._creditos_extracurriculares = None
        self._vigente = 0                 # se guarda como 0 o 1
        self.creditos_obligatorios = creditos_obligatorios
        self.creditos_electivos = creditos_electivos
        self.creditos_extracurriculares = creditos_extracurriculares
        self.vigente = vigente

    @property
    def anio_aprobacion(self):            # solo lectura
        return self._anio_aprobacion

    # Actividad 2.1: dato protegido con regla de validación
    @property
    def creditos_obligatorios(self):
        return self._creditos_obligatorios

    @creditos_obligatorios.setter
    def creditos_obligatorios(self, valor):
        self._creditos_obligatorios = validar_entero(valor, "Los créditos obligatorios", 0)

    @property
    def creditos_electivos(self):
        return self._creditos_electivos

    @creditos_electivos.setter
    def creditos_electivos(self, valor):
        self._creditos_electivos = validar_entero(valor, "Los créditos electivos", 0)

    @property
    def creditos_extracurriculares(self):
        return self._creditos_extracurriculares

    @creditos_extracurriculares.setter
    def creditos_extracurriculares(self, valor):
        self._creditos_extracurriculares = validar_entero(valor, "Los créditos extracurriculares", 0)

    # Actividad 2.2: dato calculado (no se guarda)
    @property
    def creditos_totales(self):
        return (self._creditos_obligatorios + self._creditos_electivos
                + self._creditos_extracurriculares)

    # Actividad 2.4: se guarda 0/1 y se entrega True/False
    @property
    def vigente(self):
        return self._vigente == 1         # entrega True o False

    @vigente.setter
    def vigente(self, valor):
        if not isinstance(valor, bool):
            raise TypeError("vigente debe ser True o False")
        self._vigente = 1 if valor else 0  # guarda 0 o 1

    def limite_nombre(self):
        return 36

    def resumen(self):
        estado = "vigente" if self.vigente else "no vigente"
        return (f"Plan {self._nombre} ({self._anio_aprobacion}) | "
                f"{self.creditos_totales} créditos | {estado}")


#### Actividad 1 y 4: EscuelaProfesional es un RegistroConNombre ####
# Hereda el nombre; agrega códigos y datos de la escuela; redefine limite_nombre y resumen

class EscuelaProfesional(RegistroConNombre):

    def __init__(self, codigo, nombre, informacion_general, perfil_egresado,
                 codigo_director, codigo_secretario):
        super().__init__(nombre)
        self._codigo = None
        self._informacion_general = None
        self._perfil_egresado = None
        self._codigo_director = None
        self._codigo_secretario = None
        self.codigo = codigo
        self.informacion_general = informacion_general
        self.perfil_egresado = perfil_egresado
        self.codigo_director = codigo_director
        self.codigo_secretario = codigo_secretario

    # Actividad 2.1: dato protegido con regla de validación
    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = validar_texto(valor, "El código")

    @property
    def informacion_general(self):
        return self._informacion_general

    @informacion_general.setter
    def informacion_general(self, valor):
        self._informacion_general = validar_texto(valor, "La información general")

    @property
    def perfil_egresado(self):
        return self._perfil_egresado

    @perfil_egresado.setter
    def perfil_egresado(self, valor):
        self._perfil_egresado = validar_texto(valor, "El perfil del egresado")

    @property
    def codigo_director(self):
        return self._codigo_director

    @codigo_director.setter
    def codigo_director(self, valor):
        self._codigo_director = validar_texto(valor, "El código del director")

    @property
    def codigo_secretario(self):
        return self._codigo_secretario

    @codigo_secretario.setter
    def codigo_secretario(self, valor):
        self._codigo_secretario = validar_texto(valor, "El código del secretario académico")

    def limite_nombre(self):
        return 100

    def resumen(self):
        return (f"Escuela {self._codigo} - {self._nombre} | "
                f"Director: {self._codigo_director} | "
                f"Secretario académico: {self._codigo_secretario}")


#### Actividad 1 y 4: PeriodoAcademico es un RegistroConNombre ####
# Hereda el nombre; agrega fechas, nota y estado; redefine limite_nombre y resumen
class PeriodoAcademico(RegistroConNombre):

    def __init__(self, nombre, numero, anio, fecha_inicio, fecha_fin,
                 matricula_inicio, matricula_fin, es_verano=False,
                 nota_minima=11, estado=EstadoPeriodo.PLANIFICADO):
        super().__init__(nombre)
        self._numero = None
        self._anio = None
        self._fecha_inicio = None
        self._fecha_fin = None
        self._matricula_inicio = None
        self._matricula_fin = None
        self._es_verano = 0               # se guarda como 0 o 1
        self._nota_minima = None
        self._estado = None
        self.numero = numero
        self.anio = anio
        self.cambiar_fechas(fecha_inicio, fecha_fin)
        self.cambiar_intervalo_matricula(matricula_inicio, matricula_fin)
        self.es_verano = es_verano
        self.nota_minima = nota_minima
        self.estado = estado

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, valor):
        self._numero = validar_entero(valor, "El número del periodo", 1)

    @property
    def anio(self):
        return self._anio

    @anio.setter
    def anio(self, valor):
        self._anio = validar_entero(valor, "El año del periodo", 1)

    # Actividad 2.3: sin modificación directa
    @property
    def fecha_inicio(self):
        return self._fecha_inicio

    @property
    def fecha_fin(self):
        return self._fecha_fin

    @property
    def matricula_inicio(self):
        return self._matricula_inicio

    @property
    def matricula_fin(self):
        return self._matricula_fin

    # Actividad 2.1: dato protegido con regla de validación
    @staticmethod
    def _validar_intervalo(inicio, fin, campo):
        if not isinstance(inicio, datetime.date) or not isinstance(fin, datetime.date):
            raise TypeError(f"Las fechas de {campo} deben ser de tipo date")
        if fin < inicio:
            raise ValueError(f"En {campo}, la fecha de fin no puede ser anterior a la de inicio")

    def cambiar_fechas(self, inicio, fin):
        """Cambia fecha_inicio y fecha_fin JUNTAS."""
        self._validar_intervalo(inicio, fin, "el periodo")
        self._fecha_inicio = inicio
        self._fecha_fin = fin

    def cambiar_intervalo_matricula(self, inicio, fin):
        """Cambia el inicio y el fin de la matrícula JUNTOS."""
        self._validar_intervalo(inicio, fin, "la matrícula")
        self._matricula_inicio = inicio
        self._matricula_fin = fin

    # Actividad 2.4: se guarda 0/1 y se entrega True/False
    @property
    def es_verano(self):
        return self._es_verano == 1

    @es_verano.setter
    def es_verano(self, valor):
        if not isinstance(valor, bool):
            raise TypeError("es_verano debe ser True o False")
        self._es_verano = 1 if valor else 0

    # Actividad 2.1: dato protegido con regla de validación
    @property
    def nota_minima(self):
        return self._nota_minima

    @nota_minima.setter
    def nota_minima(self, valor):
        self._nota_minima = validar_numero(valor, "La nota mínima", 0, 20)

    # Actividad 3.3: estado con Enum
    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        if isinstance(valor, EstadoPeriodo):
            self._estado = valor
        elif isinstance(valor, int) and not isinstance(valor, bool):
            self._estado = EstadoPeriodo(valor)   # con 7 lanza ValueError
        else:
            raise TypeError("El estado debe ser un EstadoPeriodo o un número")

    def limite_nombre(self):
        return 45

    def resumen(self):
        tipo = "verano" if self.es_verano else "regular"
        return (f"Periodo {self._nombre} ({self._anio}-{self._numero}) | "
                f"{tipo} | estado: {self._estado.name}")


#### Actividad 1 y 4: Estudiante es una Persona ####
# Hereda dni y nombres; agrega códigos; redefine rol y resumen
class Estudiante(Persona):

    def __init__(self, dni, nombres, apellidos, codigo_estudiante, codigo_escuela):
        super().__init__(dni, nombres, apellidos)   # reutiliza lo de Persona
        self._codigo_estudiante = None
        self._codigo_escuela = None
        self.codigo_estudiante = codigo_estudiante
        self.codigo_escuela = codigo_escuela

    @property
    def codigo_estudiante(self):
        return self._codigo_estudiante

    @codigo_estudiante.setter
    def codigo_estudiante(self, valor):
        self._codigo_estudiante = validar_texto(valor, "El código de estudiante")

    @property
    def codigo_escuela(self):
        return self._codigo_escuela

    @codigo_escuela.setter
    def codigo_escuela(self, valor):
        self._codigo_escuela = validar_texto(valor, "El código de la escuela")

    def rol(self):                     # redefine el método abstracto de Persona
        return "Estudiante"

    def resumen(self):                 # redefine resumen() para agregar datos
        return (f"{super().resumen()} | código {self._codigo_estudiante} "
                f"| escuela {self._codigo_escuela}")


#### Actividad 1 y 4: Docente es una Persona ####
# Hereda dni y nombres; agrega código de docente; redefine rol y resumen
class Docente(Persona):

    def __init__(self, dni, nombres, apellidos, codigo_docente):
        super().__init__(dni, nombres, apellidos)
        self._codigo_docente = None
        self.codigo_docente = codigo_docente

    @property
    def codigo_docente(self):
        return self._codigo_docente

    @codigo_docente.setter
    def codigo_docente(self, valor):
        self._codigo_docente = validar_texto(valor, "El código de docente")

    def rol(self):                     # redefine el método abstracto de Persona
        return "Docente"

    def resumen(self):
        return f"{super().resumen()} | código {self._codigo_docente}"

#### Actividad 5: pruebas (dato válido aceptado, dato inválido rechazado) ####
# La sección 7 es la Actividad 4.3 (polimorfismo)
def probar(descripcion, accion):
    """Ejecuta 'accion'. Si funciona dice ACEPTADO; si lanza error, RECHAZADO."""
    try:
        accion()
        print(f"  [ACEPTADO]  {descripcion}")
    except (ValueError, TypeError, AttributeError) as error:
        print(f"  [RECHAZADO] {descripcion} -> {error}")


def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)


def ejecutar_pruebas():
    # Objetos válidos que usaremos en las pruebas
    curso = Curso("IS-282", "Programación Orientada a Objetos", 4.5, 2, 4, 0, 1)
    plan = PlanEstudio("Plan Ingenieria de Sistemas", 2020, 150, 20, 10)
    periodo = PeriodoAcademico("Periodo 2026-II", 2, 2026,
                               datetime.date(2026, 8, 17), datetime.date(2026, 12, 18),
                               datetime.date(2026, 8, 1), datetime.date(2026, 8, 14))

    # ----------------------------------------------------------------------
    # Reglas del curso (Actividad 2)
    titulo("1. CURSO")
    probar("Curso válido", lambda: Curso("IS-100", "Algoritmos", 3, 2, 2, 0, 0))
    probar("Nombre vacío", lambda: Curso("IS-101", "   ", 3))
    probar("Nombre de más de 200 caracteres", lambda: Curso("IS-102", "A" * 201, 3))
    probar("Nombre de exactamente 200 caracteres", lambda: Curso("IS-103", "A" * 200, 3))
    probar("Créditos 0 (debe ser mayor que 0)", lambda: Curso("IS-104", "Redes", 0))
    probar("Créditos negativos", lambda: Curso("IS-105", "Redes", -2))
    probar("Créditos con 2 decimales (3.25)", lambda: Curso("IS-106", "Redes", 3.25))
    probar("Créditos con 3 decimales (3.255)", lambda: Curso("IS-107", "Redes", 3.255))
    probar("Horas teóricas 255 (límite)", lambda: Curso("IS-108", "Redes", 3, 255))
    probar("Horas teóricas 256 (pasa de 255)", lambda: Curso("IS-109", "Redes", 3, 256))
    probar("Horas prácticas negativas", lambda: Curso("IS-110", "Redes", 3, 0, -1))
    probar("Horas de seminario 300", lambda: Curso("IS-111", "Redes", 3, 0, 0, 300))
    probar("Horas virtuales -5", lambda: Curso("IS-112", "Redes", 3, 0, 0, 0, -5))
    print(f"  Horas totales (calculadas) de {curso.codigo}: {curso.horas_totales}")
    curso.horas_practicas = 6
    print(f"  Si cambio las horas prácticas a 6, el total se recalcula solo: {curso.horas_totales}")
    probar("Intentar cambiar las horas totales", lambda: setattr(curso, "horas_totales", 99))
    probar("Intentar cambiar el id del curso", lambda: setattr(curso, "id", 99))
    print(f"  Los ids los genera el sistema: {Curso('A-1', 'X', 1).id} y {Curso('A-2', 'Y', 1).id}")

    # ----------------------------------------------------------------------
    # Reglas de la sección (Actividad 2)
    titulo("2. SECCIÓN (vacantes y matriculados)")
    seccion = Seccion("SEC-01", "IS-282", "2026-II", 2)
    probar("Sección con vacantes 2", lambda: Seccion("SEC-02", "IS-282", "2026-II", 2))
    probar("Sección con 0 vacantes", lambda: Seccion("SEC-03", "IS-282", "2026-II", 0))
    probar("Matricular estudiante 1", seccion.matricular)
    probar("Matricular estudiante 2", seccion.matricular)
    print(f"  Vacantes disponibles: {seccion.vacantes_disponibles}")
    probar("Matricular estudiante 3 (sección llena)", seccion.matricular)
    probar("Escribir matriculados directamente", lambda: setattr(seccion, "matriculados", 0))
    probar("Retirar a un estudiante", seccion.retirar)
    print(f"  Vacantes disponibles: {seccion.vacantes_disponibles}")


    def aumentar_vacantes_valido():
        seccion.vacantes = 5


    # Sección nueva con 5 vacantes y 3 matriculados
    otra = Seccion("SEC-05", "IS-282", "2026-II", 5)
    otra.matricular()
    otra.matricular()
    otra.matricular()
    probar("Reducir vacantes de 5 a 4 (hay 3 matriculados)", lambda: setattr(otra, "vacantes", 4))
    probar("Reducir vacantes de 4 a 2 (hay 3 matriculados)", lambda: setattr(otra, "vacantes", 2))
    probar("Aumentar vacantes a 5", aumentar_vacantes_valido)
    probar("Retirar de una sección vacía",
           lambda: Seccion("SEC-04", "IS-282", "2026-II", 3).retirar())

    # ----------------------------------------------------------------------
    # Reglas del plan de estudio (Actividad 2)
    titulo("3. PLAN DE ESTUDIO")
    probar("Plan válido", lambda: PlanEstudio("Plan 2021", 2021, 140, 20, 5))
    probar("Nombre de más de 36 caracteres", lambda: PlanEstudio("P" * 37, 2021, 140, 20, 5))
    probar("Créditos obligatorios negativos", lambda: PlanEstudio("Plan X", 2021, -1, 20, 5))
    probar("Créditos electivos negativos", lambda: PlanEstudio("Plan X", 2021, 140, -1, 5))
    probar("Créditos extracurriculares negativos", lambda: PlanEstudio("Plan X", 2021, 140, 20, -1))
    print(f"  Créditos totales (calculado) = {plan.creditos_totales}")
    plan.creditos_electivos = 30
    print(f"  Si cambio electivos a 30, el total pasa a {plan.creditos_totales}")
    probar("Intentar editar créditos totales", lambda: setattr(plan, "creditos_totales", 500))
    probar("Intentar cambiar el año de aprobación", lambda: setattr(plan, "anio_aprobacion", 1999))
    print(f"  Guardado internamente: {plan._vigente} | Entregado al consultar: {plan.vigente} ({type(plan.vigente).__name__})")
    plan.vigente = False
    print(f"  Después de cambiar a False -> guardado: {plan._vigente} | entregado: {plan.vigente}")
    probar("Asignar vigente = 5 (no es booleano)", lambda: setattr(plan, "vigente", 5))

    # ----------------------------------------------------------------------
    # Reglas de la escuela (Actividad 2)
    titulo("4. ESCUELA PROFESIONAL")
    probar("Escuela válida", lambda: EscuelaProfesional(
        "EP-01", "Ingeniería de Sistemas", "Forma ingenieros...", "Egresado capaz de...", "DOC-001", "DOC-002"))
    probar("Escuela con nombre vacío", lambda: EscuelaProfesional(
        "EP-02", "", "Info", "Perfil", "DOC-001", "DOC-002"))
    probar("Escuela sin código de director", lambda: EscuelaProfesional(
        "EP-03", "Derecho", "Info", "Perfil", "", "DOC-002"))

    # ----------------------------------------------------------------------
    # Reglas del periodo (Actividad 2 y 3.3)
    titulo("5. PERIODO ACADÉMICO")
    fecha = datetime.date
    probar("Periodo válido", lambda: PeriodoAcademico(
        "Periodo 2027-I", 1, 2027, fecha(2027, 3, 1), fecha(2027, 7, 1), fecha(2027, 2, 1), fecha(2027, 2, 20)))
    probar("Nombre de más de 45 caracteres", lambda: PeriodoAcademico(
        "P" * 46, 1, 2027, fecha(2027, 3, 1), fecha(2027, 7, 1), fecha(2027, 2, 1), fecha(2027, 2, 20)))
    probar("Fecha de fin anterior a la de inicio", lambda: PeriodoAcademico(
        "Periodo malo", 1, 2027, fecha(2027, 7, 1), fecha(2027, 3, 1), fecha(2027, 2, 1), fecha(2027, 2, 20)))
    probar("Matrícula con fin anterior al inicio", lambda: PeriodoAcademico(
        "Periodo malo", 1, 2027, fecha(2027, 3, 1), fecha(2027, 7, 1), fecha(2027, 2, 20), fecha(2027, 2, 1)))
    probar("Cambiar las fechas juntas (válido)",
           lambda: periodo.cambiar_fechas(fecha(2026, 9, 1), fecha(2027, 1, 10)))
    probar("Cambiar las fechas juntas (fin < inicio)",
           lambda: periodo.cambiar_fechas(fecha(2027, 1, 10), fecha(2026, 9, 1)))
    probar("Cambiar intervalo de matrícula (válido)",
           lambda: periodo.cambiar_intervalo_matricula(fecha(2026, 8, 5), fecha(2026, 8, 20)))
    probar("Cambiar solo fecha_fin directamente", lambda: setattr(periodo, "fecha_fin", fecha(2030, 1, 1)))
    print(f"  Guardado internamente es_verano: {periodo._es_verano} | entregado: {periodo.es_verano}")
    probar("es_verano = 3 (no es booleano)", lambda: setattr(periodo, "es_verano", 3))
    periodo.es_verano = True
    print(f"  Después de cambiar a True -> guardado: {periodo._es_verano} | entregado: {periodo.es_verano}")
    probar("Nota mínima 11.5 (con decimales)", lambda: setattr(periodo, "nota_minima", 11.5))
    probar("Nota mínima 0 (límite)", lambda: setattr(periodo, "nota_minima", 0))
    probar("Nota mínima 20 (límite)", lambda: setattr(periodo, "nota_minima", 20))
    probar("Nota mínima 21", lambda: setattr(periodo, "nota_minima", 21))
    probar("Nota mínima -1", lambda: setattr(periodo, "nota_minima", -1))
    probar("Estado EN_CURSO (Enum)", lambda: setattr(periodo, "estado", EstadoPeriodo.EN_CURSO))
    probar("Estado 3 (número válido)", lambda: setattr(periodo, "estado", 3))
    print(f"  Estado actual: {periodo.estado.name} (valor {periodo.estado.value})")
    probar("Estado 7 (inválido)", lambda: setattr(periodo, "estado", 7))

    # ----------------------------------------------------------------------
    # Personas y clases abstractas (Actividad 3.1)
    titulo("6. PERSONAS (Estudiante y Docente)")
    probar("Estudiante válido", lambda: Estudiante("12345678", "Ana María", "Quispe Rojas", "20260001", "EP-01"))
    probar("Docente válido", lambda: Docente("87654321", "Luis", "Huamán Díaz", "DOC-001"))
    probar("Estudiante con DNI vacío", lambda: Estudiante("", "Ana", "Quispe", "20260002", "EP-01"))
    probar("Docente con apellidos vacíos", lambda: Docente("11111111", "Luis", "  ", "DOC-002"))
    probar("Persona sola (clase abstracta)", lambda: Persona("12345678", "Ana", "Quispe"))
    probar("RegistroConNombre solo (clase abstracta)", lambda: RegistroConNombre("Algo"))
    estudiante = Estudiante("12345678", "Ana María", "Quispe Rojas", "20260001", "EP-01")
    docente = Docente("87654321", "Luis", "Huamán Díaz", "DOC-001")
    print(f"  Nombre completo (calculado): {estudiante.nombre_completo}")
    print(f"  Rol del estudiante: {estudiante.rol()} | Rol del docente: {docente.rol()}")

    # ----------------------------------------------------------------------
    # Polimorfismo (Actividad 4.3)
    titulo("7. POLIMORFISMO: lista mixta pidiendo resumen() sin usar isinstance")
    escuela = EscuelaProfesional("EP-01", "Ingeniería de Sistemas", "Info general",
                                 "Perfil del egresado", "DOC-001", "DOC-002")
    registros = [curso, plan, escuela, periodo, estudiante, docente]
    for registro in registros:
        print("  -", registro.resumen())


if __name__ == "__main__":
    ejecutar_pruebas()
