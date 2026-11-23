from decimal import Decimal
from medicamento import Medicamento

class MedicamentoRepository:

    def __init__(self, database):
        self.database = database

    def guardar(self, medicamento):

        precio = Decimal(str(medicamento.precio))
        centimos = precio * 100

        if (
            not centimos.is_finite()
            or centimos < 0
            or centimos != centimos.to_integral_value()
        ):
            raise ValueError(
                "El precio debe ser válido y tener "
                "como máximo dos decimales"
            )

        with self.database.conectar() as conexion:

            conexion.execute("""
                INSERT INTO medicamentos
                (codigo, nombre, descripcion, precio_centimos)
                VALUES (?, ?, ?, ?)
            """, (
                medicamento.codigo,
                medicamento.nombre,
                medicamento.descripcion,
                int(centimos)
            ))

    def buscar_por_codigo(self, codigo):

        with self.database.conectar() as conexion:

            fila = conexion.execute("""
                SELECT *
                FROM medicamentos
                WHERE codigo = ?
            """, (codigo,)).fetchone()

        if fila is None:
            return None

        return Medicamento(
            fila["codigo"],
            fila["nombre"],
            fila["descripcion"],
            Decimal(fila["precio_centimos"]) / 100
        )

    def listar_todos(self):

        with self.database.conectar() as conexion:

            filas = conexion.execute("""
                SELECT *
                FROM medicamentos
                ORDER BY nombre
            """).fetchall()

        medicamentos = []

        for fila in filas:
            medicamento = Medicamento(
                fila["codigo"],
                fila["nombre"],
                fila["descripcion"],
                Decimal(fila["precio_centimos"]) / 100
            )

            medicamentos.append(medicamento)

        return medicamentos
