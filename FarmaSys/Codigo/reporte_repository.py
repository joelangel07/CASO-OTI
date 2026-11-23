
class ReporteRepository:

    def __init__(self, database):
        self.database = database

    def resumen_ventas(self, fecha_inicio, fecha_fin):

        conexion = self.database.conectar()

        try:
            fila = conexion.execute(
                """
                SELECT
                    COUNT(*) AS cantidad_ventas,
                    COALESCE(
                        SUM(total_centimos), 0
                    ) AS ingresos_centimos
                FROM ventas
                WHERE substr(fecha, 1, 10)
                    BETWEEN ? AND ?
                """,
                (fecha_inicio, fecha_fin)
            ).fetchone()

            return dict(fila)

        finally:
            conexion.close()

    def listar_ventas(self, fecha_inicio, fecha_fin):

        conexion = self.database.conectar()

        try:
            filas = conexion.execute(
                """
                SELECT
                    v.numero_venta,
                    v.fecha,
                    CASE
                        WHEN v.cliente_documento IS NULL
                          OR v.cliente_documento = 'CF-GENERICO'
                        THEN 'Consumidor final'
                        ELSE COALESCE(
                            c.nombre,
                            'Cliente no disponible'
                        )
                    END AS cliente,
                    v.total_centimos
                FROM ventas AS v
                LEFT JOIN clientes AS c
                    ON v.cliente_documento = c.documento
                WHERE substr(v.fecha, 1, 10)
                    BETWEEN ? AND ?
                ORDER BY v.fecha DESC
                """,
                (fecha_inicio, fecha_fin)
            ).fetchall()

            return [
                dict(fila)
                for fila in filas
            ]

        finally:
            conexion.close()

    def medicamentos_mas_vendidos(
        self,
        fecha_inicio,
        fecha_fin
    ):

        conexion = self.database.conectar()

        try:
            filas = conexion.execute(
                """
                SELECT
                    m.codigo,
                    m.nombre,
                    SUM(d.cantidad) AS unidades,
                    SUM(
                        d.cantidad *
                        d.precio_unitario_centimos
                    ) AS ingresos_centimos
                FROM detalles_venta AS d
                INNER JOIN ventas AS v
                    ON d.venta_numero = v.numero_venta
                INNER JOIN lotes AS l
                    ON d.lote_numero = l.numero_lote
                INNER JOIN medicamentos AS m
                    ON l.medicamento_codigo = m.codigo
                WHERE substr(v.fecha, 1, 10)
                    BETWEEN ? AND ?
                GROUP BY m.codigo, m.nombre
                ORDER BY unidades DESC, m.nombre
                LIMIT 10
                """,
                (fecha_inicio, fecha_fin)
            ).fetchall()

            return [
                dict(fila)
                for fila in filas
            ]

        finally:
            conexion.close()

    def reporte_inventario(self):

        conexion = self.database.conectar()

        try:
            filas = conexion.execute(
                """
                SELECT
                    l.numero_lote,
                    m.codigo,
                    m.nombre AS medicamento,
                    l.cantidad,
                    l.fecha_vencimiento
                FROM lotes AS l
                INNER JOIN medicamentos AS m
                    ON l.medicamento_codigo = m.codigo
                ORDER BY m.nombre, l.fecha_vencimiento
                """
            ).fetchall()

            return [
                dict(fila)
                for fila in filas
            ]

        finally:
            conexion.close()
