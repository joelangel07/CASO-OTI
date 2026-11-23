
from datetime import date

class Lote:
    def __init__(self, numero_lote, medicamento, cantidad, fecha_vencimiento):
        if type(cantidad) is not int or cantidad < 0:
            raise ValueError("La cantidad debe ser un entero no negativo")
        self.numero_lote = numero_lote
        self.medicamento = medicamento
        self.__cantidad = cantidad
        self.fecha_vencimiento = fecha_vencimiento

    @property
    def cantidad(self):
        return self.__cantidad

    def esta_vencido(self):
        return self.fecha_vencimiento < date.today()

    def agregar_stock(self, cantidad):

        if type(cantidad) is not int or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo")

        self.__cantidad += cantidad

    def descontar_stock(self, cantidad):

        if type(cantidad) is not int or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo")

        if self.esta_vencido():
            raise ValueError("No se puede vender un lote vencido")

        if cantidad > self.__cantidad:
            raise ValueError("Stock insuficiente")

        self.__cantidad -= cantidad

    def mostrar_info(self):

        print(f"Lote: {self.numero_lote}")
        print(f"Medicamento: {self.medicamento.nombre}")
        print(f"Stock: {self.__cantidad}")
        print(f"Vencimiento: {self.fecha_vencimiento}")
