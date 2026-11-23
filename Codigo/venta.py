from datetime import datetime
from detalle_venta import DetalleVenta

class Venta:
    def __init__(self, numero_venta, cliente):
        self.__numero_venta = numero_venta
        self.__cliente = cliente
        self.__fecha = datetime.now()
        self.__detalles = []
        self.__confirmada = False
        
    @property
    def numero_venta(self):
        return self.__numero_venta

    @property
    def confirmada(self):
        return self.__confirmada

    def agregar_detalle(self, lote, cantidad):

        if self.__confirmada:
            raise ValueError("La venta ya está confirmada")

        if lote.esta_vencido():
            raise ValueError("El lote está vencido")

        cantidad_acumulada = cantidad

        for detalle in self.__detalles:
            if detalle.lote is lote:
                cantidad_acumulada += detalle.cantidad

        if cantidad_acumulada > lote.cantidad:
            raise ValueError("Stock insuficiente")

        detalle = DetalleVenta(lote, cantidad)
        self.__detalles.append(detalle)

    def calcular_total(self):
        return sum(
            detalle.calcular_subtotal()
            for detalle in self.__detalles
        )

    def confirmar_venta(self):

        if self.__confirmada:
            raise ValueError("La venta ya fue confirmada")

        if not self.__detalles:
            raise ValueError("La venta no tiene productos")

        # Validar todas las cantidades antes de descontar.
        cantidades = {}

        for detalle in self.__detalles:
            lote = detalle.lote
            cantidades[lote] = (
                cantidades.get(lote, 0) + detalle.cantidad
            )

        for lote, cantidad in cantidades.items():
            if lote.esta_vencido():
                raise ValueError("Hay un lote vencido")

            if cantidad > lote.cantidad:
                raise ValueError("Stock insuficiente")

        # Descontar después de validar toda la venta.
        for lote, cantidad in cantidades.items():
            lote.descontar_stock(cantidad)

        self.__confirmada = True

    def mostrar_resumen(self):

        print(f"\nVENTA N.º {self.__numero_venta}")
        print(f"Cliente: {self.__cliente.nombre}")
        print(f"Fecha: {self.__fecha}")

        print("-" * 45)

        for detalle in self.__detalles:
            detalle.mostrar_info()

        print("-" * 45)
        print(f"TOTAL: S/ {self.calcular_total():.2f}")

        estado = (
            "CONFIRMADA" if self.__confirmada
            else "PENDIENTE"
        )

        print(f"Estado: {estado}")
