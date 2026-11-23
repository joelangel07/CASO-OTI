from datetime import datetime
from movimiento_inventario import MovimientoInventario
from datetime import date

from lote import Lote
from medicamento_repository import MedicamentoRepository

class LoteRepository:

    def __init__(self, database):
        self.database = database
        self.medicamentos = MedicamentoRepository(database)

    
    def guardar(self, lote):

        from datetime import datetime

        conexion = self.database.conectar()

        try:
            # Iniciar una transacción de escritura
            conexion.execute("BEGIN IMMEDIATE")

            # 1. Guardar el lote
            conexion.execute(
                """
                INSERT INTO lotes (
                    numero_lote,
                    medicamento_codigo,
                    cantidad,
                    fecha_vencimiento
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    lote.numero_lote,
                    lote.medicamento.codigo,
                    lote.cantidad,
                    lote.fecha_vencimiento.isoformat()
                )
            )

            # 2. Registrar la entrada inicial
            conexion.execute(
                """
                INSERT INTO movimientos_inventario (
                    numero_lote,
                    tipo,
                    cantidad,
                    motivo,
                    fecha
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    lote.numero_lote,
                    "ENTRADA",
                    lote.cantidad,
                    "Registro inicial del lote",
                    datetime.now().isoformat(
                        timespec="seconds"
                    )
                )
            )

            # 3. Confirmar ambas operaciones
            conexion.commit()

        except Exception:
            # Si algo falla, deshacer todo
            conexion.rollback()
            raise

        finally:
            conexion.close()


    def buscar_por_numero(self, numero):

        with self.database.conectar() as conexion:

            fila = conexion.execute("""
                SELECT *
                FROM lotes
                WHERE numero_lote = ?
            """, (numero,)).fetchone()

        if fila is None:
            return None

        medicamento = self.medicamentos.buscar_por_codigo(
            fila["medicamento_codigo"]
        )

        return Lote(
            fila["numero_lote"],
            medicamento,
            fila["cantidad"],
            date.fromisoformat(fila["fecha_vencimiento"])
        )
        
    
    def listar_inventario(self):

        with self.database.conectar() as conexion:

            filas = conexion.execute("""
                SELECT
                    l.numero_lote,
                    l.medicamento_codigo,
                    m.nombre AS medicamento_nombre,
                    l.cantidad,
                    l.fecha_vencimiento
                FROM lotes AS l
                INNER JOIN medicamentos AS m
                    ON l.medicamento_codigo = m.codigo
                ORDER BY m.nombre, l.fecha_vencimiento
            """).fetchall()

        return [
            {
                "numero_lote": fila["numero_lote"],
                "codigo": fila["medicamento_codigo"],
                "medicamento": fila["medicamento_nombre"],
                "cantidad": fila["cantidad"],
                "fecha_vencimiento": fila["fecha_vencimiento"]
            }
            for fila in filas
        ]
    
    def agregar_stock(
        self,
        numero_lote,
        cantidad,
        motivo="Entrada de mercadería"
    ):

        movimiento = MovimientoInventario(
            numero_lote,
            "ENTRADA",
            cantidad,
            motivo
        )

        conexion = self.database.conectar()

        try:
            conexion.execute("BEGIN IMMEDIATE")

            cursor = conexion.execute(
                """
                UPDATE lotes
                SET cantidad = cantidad + ?
                WHERE numero_lote = ?
                """,
                (cantidad, numero_lote)
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    "El lote indicado no existe."
                )

            conexion.execute(
                """
                INSERT INTO movimientos_inventario (
                    numero_lote,
                    tipo,
                    cantidad,
                    motivo,
                    fecha
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    movimiento.numero_lote,
                    movimiento.tipo,
                    movimiento.cantidad,
                    movimiento.motivo,
                    movimiento.fecha.isoformat(
                        timespec="seconds"
                    )
                )
            )

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            conexion.close()
            
   
    def listar_movimientos(self, numero_lote):

        with self.database.conectar() as conexion:

            filas = conexion.execute(
                """
                SELECT
                    id,
                    numero_lote,
                    tipo,
                    cantidad,
                    motivo,
                    fecha
                FROM movimientos_inventario
                WHERE numero_lote = ?
                ORDER BY fecha DESC, id DESC
                """,
                (numero_lote,)
            ).fetchall()

        return [
            dict(fila)
            for fila in filas
        ]


    
    def listar_lotes_disponibles(self):

        from datetime import date

        with self.database.conectar() as conexion:

            filas = conexion.execute(
                """
                SELECT
                    l.numero_lote,
                    l.medicamento_codigo,
                    m.nombre AS medicamento_nombre,
                    m.precio_centimos,
                    l.cantidad,
                    l.fecha_vencimiento
                FROM lotes AS l
                INNER JOIN medicamentos AS m
                    ON l.medicamento_codigo = m.codigo
                WHERE l.cantidad > 0
                  AND l.fecha_vencimiento >= ?
                ORDER BY m.nombre, l.fecha_vencimiento
                """,
                (date.today().isoformat(),)
            ).fetchall()

        return [
            dict(fila)
            for fila in filas
        ]



