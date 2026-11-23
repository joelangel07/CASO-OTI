
class Farmacia:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__medicamentos = {}
        self.__lotes = {}
        self.__clientes = {}
        self.__ventas = []

    @property
    def nombre(self):
        return self.__nombre

    def registrar_medicamento(self, medicamento):

        codigo = medicamento.codigo

        if codigo in self.__medicamentos:
            raise ValueError(
                "Ya existe un medicamento con ese código"
            )

        self.__medicamentos[codigo] = medicamento

    def buscar_medicamento(self, codigo):
        return self.__medicamentos.get(codigo)

    def registrar_lote(self, lote):

        numero = lote.numero_lote

        if numero in self.__lotes:
            raise ValueError("El lote ya está registrado")

        codigo = lote.medicamento.codigo

        if codigo not in self.__medicamentos:
            raise ValueError(
                "Primero debe registrar el medicamento"
            )

        if self.__medicamentos[codigo] is not lote.medicamento:
            raise ValueError(
                "El lote debe usar el medicamento registrado"
            )

        self.__lotes[numero] = lote

    def buscar_lote(self, numero):
        return self.__lotes.get(numero)

    def registrar_cliente(self, cliente):

        documento = cliente.documento

        if documento in self.__clientes:
            raise ValueError("El cliente ya existe")

        self.__clientes[documento] = cliente

    def buscar_cliente(self, documento):
        return self.__clientes.get(documento)

    def registrar_venta(self, venta):

        if not venta.confirmada:
            raise ValueError(
                "No se puede registrar una venta pendiente"
            )

        if any(
            existente.numero_venta == venta.numero_venta
            for existente in self.__ventas
        ):
            raise ValueError(
                "El número de venta ya está registrado"
            )

        self.__ventas.append(venta)

    def mostrar_inventario(self):

        print(f"\nINVENTARIO DE {self.__nombre}")
        print("-" * 45)

        for lote in self.__lotes.values():
            print(
                f"{lote.medicamento.nombre} | "
                f"Lote: {lote.numero_lote} | "
                f"Stock: {lote.cantidad}"
            )

    def calcular_total_ventas(self):
        return sum(
            venta.calcular_total()
            for venta in self.__ventas
        )
