class Medicamento:
    def __init__(self, codigo, nombre, descripcion, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio

    def mostrar_info(self):
        print(f"Código: {self.codigo}")
        print(f"Nombre: {self.nombre}")
        print(f"Descripción: {self.descripcion}")
        print(f"Precio: S/ {self.precio:.2f}")

