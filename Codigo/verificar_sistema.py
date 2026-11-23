
import sqlite3

from database import Database


TABLAS_REQUERIDAS = [
    "medicamentos",
    "clientes",
    "lotes",
    "ventas",
    "detalles_venta",
    "movimientos_inventario"
]


def verificar_base_datos():

    database = Database()
    conexion = database.conectar()

    try:
        print("=" * 50)
        print("VERIFICACIÓN DE FARMASYS")
        print("=" * 50)

        tablas = {
            fila[0]
            for fila in conexion.execute(
                """
                SELECT name
                FROM sqlite_master
                WHERE type = 'table'
                """
            ).fetchall()
        }

        faltantes = [
            nombre
            for nombre in TABLAS_REQUERIDAS
            if nombre not in tablas
        ]

        if faltantes:
            print("FALTAN TABLAS:")
            for tabla in faltantes:
                print(f" - {tabla}")
            return False

        print("OK: Todas las tablas principales existen.")

        for tabla in TABLAS_REQUERIDAS:

            cantidad = conexion.execute(
                f"SELECT COUNT(*) FROM {tabla}"
            ).fetchone()[0]

            print(f"{tabla}: {cantidad} registros")

        errores = conexion.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        if errores:
            print(
                "ERROR: Se encontraron relaciones "
                "inconsistentes."
            )

            for error in errores:
                print(tuple(error))

            return False

        print("OK: Relaciones de claves foráneas.")
        print("VERIFICACIÓN COMPLETADA")

        return True

    except sqlite3.Error as error:
        print(f"ERROR DE SQLITE: {error}")
        return False

    finally:
        conexion.close()


if __name__ == "__main__":
    verificar_base_datos()
