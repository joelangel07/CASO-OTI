
from datetime import datetime, date


class VentaRepository:

    def __init__(self, database):
        self.database = database

    
    def registrar_venta(
        self,
        numero_venta,
        documento_cliente,
        productos
    ):

        from datetime import date, datetime

        if not numero_venta.strip():
            raise ValueError("Número de venta obligatorio")

        if documento_cliente is None:
            documento_cliente = "CF-GENERICO"

        if not isinstance(documento_cliente, str):
            raise ValueError("Documento de cliente inválido")

        documento_cliente = documento_cliente.strip()

        if not documento_cliente:
            documento_cliente = "CF-GENERICO"

        if not productos:
            raise ValueError("La venta no tiene productos")

        # Agrupar cantidades si se repite un lote
        cantidades = {}

        for numero_lote, cantidad in productos:

            if type(cantidad) is not int or cantidad <= 0:
                raise ValueError("Cantidad inválida")

            cantidades[numero_lote] = (
                cantidades.get(numero_lote, 0) + cantidad
            )

        conexion = self.database.conectar()

        try:
            conexion.execute("BEGIN IMMEDIATE")

            # Comprobar cliente
            cliente = conexion.execute(
                """
                SELECT documento
                FROM clientes
                WHERE documento = ?
                """,
                (documento_cliente,)
            ).fetchone()

            if cliente is None:
                raise ValueError("El cliente no existe")

            detalles = []
            total_centimos = 0

            # Comprobar lotes y calcular total
            for numero_lote, cantidad in cantidades.items():

                fila = conexion.execute(
                    """
                    SELECT
                        l.numero_lote,
                        l.cantidad,
                        l.fecha_vencimiento,
                        m.precio_centimos
                    FROM lotes AS l
                    INNER JOIN medicamentos AS m
                        ON l.medicamento_codigo = m.codigo
                    WHERE l.numero_lote = ?
                    """,
                    (numero_lote,)
                ).fetchone()

                if fila is None:
                    raise ValueError(
                        f"No existe el lote {numero_lote}"
                    )

                if date.fromisoformat(
                    fila["fecha_vencimiento"]
                ) < date.today():
                    raise ValueError(
                        f"El lote {numero_lote} está vencido"
                    )

                if fila["cantidad"] < cantidad:
                    raise ValueError(
                        f"Stock insuficiente en {numero_lote}"
                    )

                precio = fila["precio_centimos"]
                subtotal = precio * cantidad

                total_centimos += subtotal

                detalles.append(
                    (numero_lote, cantidad, precio)
                )

            fecha = datetime.now().isoformat(
                timespec="seconds"
            )

            # Guardar venta
            conexion.execute(
                """
                INSERT INTO ventas (
                    numero_venta,
                    cliente_documento,
                    fecha,
                    total_centimos
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    numero_venta,
                    documento_cliente,
                    fecha,
                    total_centimos
                )
            )

            # Guardar detalles, descontar stock e historial
            for numero_lote, cantidad, precio in detalles:

                conexion.execute(
                    """
                    INSERT INTO detalles_venta (
                        venta_numero,
                        lote_numero,
                        cantidad,
                        precio_unitario_centimos
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        numero_venta,
                        numero_lote,
                        cantidad,
                        precio
                    )
                )

                cursor = conexion.execute(
                    """
                    UPDATE lotes
                    SET cantidad = cantidad - ?
                    WHERE numero_lote = ?
                      AND cantidad >= ?
                    """,
                    (
                        cantidad,
                        numero_lote,
                        cantidad
                    )
                )

                if cursor.rowcount != 1:
                    raise ValueError(
                        "No se pudo descontar el stock"
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
                        numero_lote,
                        "SALIDA",
                        cantidad,
                        f"Venta {numero_venta}",
                        fecha
                    )
                )

            conexion.commit()

            return total_centimos

        except Exception:
            conexion.rollback()
            raise

        finally:
            conexion.close()

    
    def listar_ventas(self):

        conexion = self.database.conectar()

        try:
            filas = conexion.execute(
                """
                SELECT
                    v.numero_venta,
                    v.fecha,
                    v.total_centimos,
                    CASE
                        WHEN v.cliente_documento IS NULL
                          OR v.cliente_documento = 'CF-GENERICO'
                        THEN 'Consumidor final'
                        ELSE COALESCE(
                            c.nombre,
                            'Cliente no disponible'
                        )
                    END AS cliente
                FROM ventas AS v
                LEFT JOIN clientes AS c
                    ON v.cliente_documento = c.documento
                ORDER BY v.fecha DESC, v.numero_venta DESC
                """
            ).fetchall()

            return [
                dict(fila)
                for fila in filas
            ]

        finally:
            conexion.close()

    def obtener_detalles(self, numero_venta):

        conexion = self.database.conectar()

        try:
            filas = conexion.execute(
                """
                SELECT
                    d.lote_numero,
                    m.nombre AS medicamento,
                    d.cantidad,
                    d.precio_unitario_centimos,
                    (
                        d.cantidad *
                        d.precio_unitario_centimos
                    ) AS subtotal_centimos
                FROM detalles_venta AS d
                INNER JOIN lotes AS l
                    ON d.lote_numero = l.numero_lote
                INNER JOIN medicamentos AS m
                    ON l.medicamento_codigo = m.codigo
                WHERE d.venta_numero = ?
                ORDER BY d.id
                """,
                (numero_venta,)
            ).fetchall()

            return [
                dict(fila)
                for fila in filas
            ]

        finally:
            conexion.close()

    
    def obtener_venta(self, numero_venta):

        conexion = self.database.conectar()

        try:
            fila = conexion.execute(
                """
                SELECT
                    v.numero_venta,
                    v.fecha,
                    v.total_centimos,
                    CASE
                        WHEN v.cliente_documento IS NULL
                          OR v.cliente_documento = 'CF-GENERICO'
                        THEN 'Consumidor final'
                        ELSE COALESCE(
                            c.nombre,
                            'Cliente no disponible'
                        )
                    END AS cliente
                FROM ventas AS v
                LEFT JOIN clientes AS c
                    ON v.cliente_documento = c.documento
                WHERE v.numero_venta = ?
                """,
                (numero_venta,)
            ).fetchone()

            return dict(fila) if fila else None

        finally:
            conexion.close()
