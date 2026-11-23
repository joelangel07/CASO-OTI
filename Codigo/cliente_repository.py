from cliente import Cliente

class ClienteRepository:

    def __init__(self, database):
        self.database = database

    def guardar(self, cliente):

        with self.database.conectar() as conexion:

            conexion.execute("""
                INSERT INTO clientes
                (documento, nombre, telefono)
                VALUES (?, ?, ?)
            """, (
                cliente.documento,
                cliente.nombre,
                cliente.telefono
            ))

    def buscar_por_documento(self, documento):

        with self.database.conectar() as conexion:

            fila = conexion.execute("""
                SELECT *
                FROM clientes
                WHERE documento = ?
            """, (documento,)).fetchone()

        if fila is None:
            return None

        return Cliente(
            fila["documento"],
            fila["nombre"],
            fila["telefono"]
        )

    
    def listar_todos(self):

        conexion = self.database.conectar()

        try:
            filas = conexion.execute(
                """
                SELECT
                    documento,
                    nombre,
                    telefono
                FROM clientes
                WHERE documento <> 'CF-GENERICO'
                ORDER BY nombre
                """
            ).fetchall()

            return [
                dict(fila)
                for fila in filas
            ]

        finally:
            conexion.close()
