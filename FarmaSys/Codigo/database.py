import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RUTA_DB = BASE_DIR / "datos" / "farmasys.db"

class Database:

    def __init__(self):
        RUTA_DB.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.ruta = RUTA_DB

    def conectar(self):
        conexion = sqlite3.connect(self.ruta)
        conexion.row_factory = sqlite3.Row
        conexion.execute("PRAGMA foreign_keys = ON")
        return conexion

    def crear_tablas(self):

        with self.conectar() as conexion:

            conexion.executescript("""
                CREATE TABLE IF NOT EXISTS medicamentos (
                    codigo TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    precio_centimos INTEGER NOT NULL
                        CHECK(precio_centimos >= 0)
                );

                CREATE TABLE IF NOT EXISTS clientes (
                    documento TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    telefono TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS lotes (
                    numero_lote TEXT PRIMARY KEY,
                    medicamento_codigo TEXT NOT NULL,
                    cantidad INTEGER NOT NULL
                        CHECK(cantidad >= 0),
                    fecha_vencimiento TEXT NOT NULL,

                    FOREIGN KEY (medicamento_codigo)
                        REFERENCES medicamentos(codigo)
                );

                CREATE TABLE IF NOT EXISTS ventas (
                    numero_venta TEXT PRIMARY KEY,
                    cliente_documento TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    total_centimos INTEGER NOT NULL
                        CHECK(total_centimos >= 0),

                    FOREIGN KEY (cliente_documento)
                        REFERENCES clientes(documento)
                );

                CREATE TABLE IF NOT EXISTS detalles_venta (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venta_numero TEXT NOT NULL,
                    lote_numero TEXT NOT NULL,
                    cantidad INTEGER NOT NULL
                        CHECK(cantidad > 0),
                    precio_unitario_centimos INTEGER NOT NULL
                        CHECK(precio_unitario_centimos >= 0),

                    FOREIGN KEY (venta_numero)
                        REFERENCES ventas(numero_venta),

                    FOREIGN KEY (lote_numero)
                        REFERENCES lotes(numero_lote)
                );
                
                CREATE TABLE IF NOT EXISTS movimientos_inventario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero_lote TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                    motivo TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    FOREIGN KEY (numero_lote)
                        REFERENCES lotes(numero_lote)
                );
            """)

    
    def permitir_ventas_sin_cliente(self):

        conexion = self.conectar()

        try:
            columnas = conexion.execute(
                "PRAGMA table_info(ventas)"
            ).fetchall()

            columna_cliente = next(
                (
                    columna
                    for columna in columnas
                    if columna["name"] == "cliente_documento"
                ),
                None
            )

            if columna_cliente is None:
                raise RuntimeError(
                    "No existe la columna cliente_documento"
                )

            # Si ya admite NULL, no hace falta migrar
            if columna_cliente["notnull"] == 0:
                return

            conexion.execute("BEGIN IMMEDIATE")

            # Crear nueva tabla con cliente opcional
            conexion.execute(
                """
                CREATE TABLE ventas_nueva (
                    numero_venta TEXT PRIMARY KEY,
                    cliente_documento TEXT,
                    fecha TEXT NOT NULL,
                    total_centimos INTEGER NOT NULL,
                    FOREIGN KEY (cliente_documento)
                        REFERENCES clientes(documento)
                )
                """
            )

            # Conservar las ventas existentes
            conexion.execute(
                """
                INSERT INTO ventas_nueva (
                    numero_venta,
                    cliente_documento,
                    fecha,
                    total_centimos
                )
                SELECT
                    numero_venta,
                    cliente_documento,
                    fecha,
                    total_centimos
                FROM ventas
                """
            )

            # Reemplazar la tabla anterior
            conexion.execute("DROP TABLE ventas")

            conexion.execute(
                "ALTER TABLE ventas_nueva RENAME TO ventas"
            )

            conexion.commit()

        except Exception:
            conexion.rollback()
            raise

        finally:
            conexion.close()

    
    def crear_consumidor_final(self):

        conexion = self.conectar()

        try:
            conexion.execute(
                """
                INSERT OR IGNORE INTO clientes (
                    documento,
                    nombre,
                    telefono
                )
                VALUES (?, ?, ?)
                """,
                (
                    "CF-GENERICO",
                    "Consumidor final",
                    ""
                )
            )

            conexion.commit()

        finally:
            conexion.close()
