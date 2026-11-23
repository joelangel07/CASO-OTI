
from datetime import datetime


class MovimientoInventario:

    def __init__(
        self,
        numero_lote,
        tipo,
        cantidad,
        motivo,
        fecha=None
    ):

        if not numero_lote.strip():
            raise ValueError("El lote es obligatorio")

        if tipo not in ("ENTRADA", "SALIDA"):
            raise ValueError("Tipo de movimiento inválido")

        if type(cantidad) is not int or cantidad <= 0:
            raise ValueError("Cantidad inválida")

        if not motivo.strip():
            raise ValueError("El motivo es obligatorio")

        self.__numero_lote = numero_lote
        self.__tipo = tipo
        self.__cantidad = cantidad
        self.__motivo = motivo
        self.__fecha = fecha or datetime.now()

    @property
    def numero_lote(self):
        return self.__numero_lote

    @property
    def tipo(self):
        return self.__tipo

    @property
    def cantidad(self):
        return self.__cantidad

    @property
    def motivo(self):
        return self.__motivo

    @property
    def fecha(self):
        return self.__fecha
