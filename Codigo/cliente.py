class Cliente:
    def __init__(self, documento, nombre, telefono):
        self.__documento = documento
        self.__nombre = nombre
        self.__telefono = telefono

    @property
    def documento(self):
        return self.__documento

    @property
    def nombre(self):
        return self.__nombre

    @property
    def telefono(self):
        return self.__telefono

    def actualizar_telefono(self, nuevo_telefono):
        if not nuevo_telefono.strip():
            raise ValueError("El teléfono no puede estar vacío")

        self.__telefono = nuevo_telefono

    def mostrar_info(self):
        print(f"Documento: {self.__documento}")
        print(f"Nombre: {self.__nombre}")
        print(f"Teléfono: {self.__telefono}")
