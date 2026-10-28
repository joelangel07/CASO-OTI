# ==========================================
# CASO 02 - OTI UNSCH - SISTEMA DE MATRÍCULA
# ==========================================

# 1. ENCAPSULAMIENTO
# Se utiliza el prefijo de doble guion bajo (__costo_base, __modificadores) 
# para proteger los atributos, impidiendo que se modifiquen directamente 
# desde fuera de la clase.

class MatriculaGeneral:
    def __init__(self, estudiante):
        # Atributo protegido/privado (Encapsulamiento)
        self.__costo_base = 60.00
        self.estudiante = estudiante

    def calcular_costo(self):
        return self.__costo_base

# 2. HERENCIA SIMPLE
# Las especializaciones heredan directamente de una sola clase padre (MatriculaGeneral).

class MatriculaExtemporanea(MatriculaGeneral):
    def calcular_costo(self):
        return super().calcular_costo() + 15.00

class MatriculaDesaprobado(MatriculaGeneral):
    def calcular_costo(self):
        return super().calcular_costo() + 15.00

class MatriculaBeca(MatriculaGeneral):
    def calcular_costo(self):
        return super().calcular_costo() / 2.0

# 3. HERENCIA MÚLTIPLE (Implementación original problemática de los programadores)
# Estas clases heredan de MÁS DE UNA CLASE a la vez, creando una cadena MRO 
# (Method Resolution Order) que define el orden de ejecución.

class MatriculaCombinada1(MatriculaBeca, MatriculaDesaprobado, MatriculaExtemporanea):
    def calcular_costo(self):
        return super().calcular_costo()

class MatriculaCombinada2(MatriculaDesaprobado, MatriculaExtemporanea, MatriculaBeca):
    def calcular_costo(self):
        return super().calcular_costo()

# ==========================================
# REDISEÑO PROPUESTO (Solución a implementar)
# Evita la herencia múltiple usando Composición. 
# Esto permite elegir el orden de cobros por estudiante.
# ==========================================

class Modificador:
    def aplicar(self, monto):
        pass

# Herencia simple en los objetos modificadores
class RecargoExtemporaneo(Modificador):
    def aplicar(self, monto):
        return monto + 15.00

class RecargoDesaprobado(Modificador):
    def aplicar(self, monto):
        return monto + 15.00

class DescuentoBeca(Modificador):
    def aplicar(self, monto):
        return monto / 2.0

class MatriculaRedisenada:
    def __init__(self, estudiante):
        self.__costo_base = 60.00  # Encapsulamiento
        self.estudiante = estudiante
        self.__modificadores = []  # Encapsulamiento (lista privada)

    def agregar_modificador(self, modificador):
        # Se permite decidir el orden en que se añaden dinámicamente
        self.__modificadores.append(modificador)

    def calcular_costo_final(self):
        monto = self.__costo_base
        for mod in self.__modificadores:
            monto = mod.aplicar(monto)
        return monto

# ==========================================
# PRUEBAS Y RESULTADOS DEL CASO OTI
# ==========================================
if __name__ == "__main__":
    print("--- RESULTADOS HERENCIA MÚLTIPLE (EL PROBLEMA) ---")
    comb1 = MatriculaCombinada1("Luis")
    comb2 = MatriculaCombinada2("Rosa")
    
    print(f"Versión 1 (Pago de Luis): S/ {comb1.calcular_costo()}")
    print(f"Versión 2 (Pago de Rosa): S/ {comb2.calcular_costo()}")

    print("\n--- RESULTADO DEL REDISEÑO ---")
    matricula_correcta = MatriculaRedisenada("Nuevo Estudiante")
    
    # El rediseño permite aplicar recargos primero y luego la beca al final:
    matricula_correcta.agregar_modificador(RecargoExtemporaneo())
    matricula_correcta.agregar_modificador(RecargoDesaprobado())
    matricula_correcta.agregar_modificador(DescuentoBeca())
    
    print(f"Costo con Rediseño (Suma primero, divide al final): S/ {matricula_correcta.calcular_costo_final()}")
