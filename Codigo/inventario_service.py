
from datetime import date


class InventarioService:

    def __init__(self, stock_minimo=5):

        if type(stock_minimo) is not int or stock_minimo < 0:
            raise ValueError("Stock mínimo inválido")

        self.stock_minimo = stock_minimo

    def obtener_estado(self, cantidad, fecha_vencimiento):

        if fecha_vencimiento < date.today():
            return "Vencido"

        if cantidad == 0:
            return "Sin stock"

        if cantidad <= self.stock_minimo:
            return "Stock bajo"

        return "Disponible"
