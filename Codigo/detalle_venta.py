class DetalleVenta:
    def __init__(self, lote, cantidad):
        if type(cantidad) is not int or cantidad <= 0:
            raise ValueError("La cantidad debe ser un entero positivo")
        self.__lote = lote
        self.__cantidad = cantidad
        self.__precio_unitario = lote.medicamento.precio

    @property
    def lote(self):
        return self.__lote

    @property
    def cantidad(self):
        return self.__cantidad

    @property
    def precio_unitario(self):
        return self.__precio_unitario

    def calcular_subtotal(self):
        return self.__cantidad * self.__precio_unitario

    def mostrar_info(self):
        print(
            f"{self.__lote.medicamento.nombre} | "
            f"{self.__cantidad} x "
            f"S/ {self.__precio_unitario:.2f} = "
            f"S/ {self.calcular_subtotal():.2f}"
        )
