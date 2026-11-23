
from datetime import date, timedelta


class DashboardRepository:

    def __init__(self, database):
        self.database = database

    def obtener_resumen(self):

        conexion = self.database.conectar()

        try:
            medicamentos = conexion.execute(
                """
                SELECT COUNT(*)
                FROM medicamentos
                """
            ).fetchone()[0]

            hoy = date.today().isoformat()

            ventas_hoy = conexion.execute(
                """
                SELECT COUNT(*)
                FROM ventas
                WHERE substr(fecha, 1, 10) = ?
                """,
                (hoy,)
            ).fetchone()[0]

            ingresos_hoy = conexion.execute(
                """
                SELECT COALESCE(
                    SUM(total_centimos), 0
                )
                FROM ventas
                WHERE substr(fecha, 1, 10) = ?
                """,
                (hoy,)
            ).fetchone()[0]

            lotes_stock_bajo = conexion.execute(
                """
                SELECT COUNT(*)
                FROM lotes
                WHERE cantidad BETWEEN 1 AND 5
                  AND fecha_vencimiento >= ?
                """,
                (hoy,)
            ).fetchone()[0]

            return {
                "medicamentos": medicamentos,
                "ventas_hoy": ventas_hoy,
                "ingresos_hoy_centimos": ingresos_hoy,
                "stock_bajo": lotes_stock_bajo
            }

        finally:
            conexion.close()

    def obtener_ventas_ultimos_7_dias(self):

        hoy = date.today()
        inicio = hoy - timedelta(days=6)

        conexion = self.database.conectar()

        try:
            filas = conexion.execute(
                """
                SELECT
                    substr(fecha, 1, 10) AS dia,
                    SUM(total_centimos) AS total
                FROM ventas
                WHERE substr(fecha, 1, 10) BETWEEN ? AND ?
                GROUP BY substr(fecha, 1, 10)
                """,
                (
                    inicio.isoformat(),
                    hoy.isoformat()
                )
            ).fetchall()

            totales = {
                fila["dia"]: fila["total"]
                for fila in filas
            }

            resultado = []

            for i in range(7):

                dia = inicio + timedelta(days=i)
                clave = dia.isoformat()

                resultado.append({
                    "fecha": clave,
                    "total_centimos": totales.get(
                        clave, 0
                    )
                })

            return resultado

        finally:
            conexion.close()
