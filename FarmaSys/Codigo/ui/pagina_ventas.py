
import sqlite3
import uuid
from ui.ticket_venta import TicketVenta

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QComboBox,
    QSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QCheckBox    
)


class PaginaVentas(QWidget):

    def __init__(
        self,
        repositorio_ventas,
        repositorio_lotes,
        repositorio_clientes
    ):
        super().__init__()

        self.repositorio_ventas = repositorio_ventas
        self.repositorio_lotes = repositorio_lotes
        self.repositorio_clientes = repositorio_clientes

        self.lotes = {}
        self.carrito = {}

        self.crear_interfaz()
        self.cargar_datos()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(18)

        titulo = QLabel("Nueva venta")
        titulo.setObjectName("tituloPagina")
        layout.addWidget(titulo)

        descripcion = QLabel(
            "Selecciona un cliente y agrega medicamentos"
        )
        descripcion.setObjectName("descripcion")
        layout.addWidget(descripcion)

        formulario = QFormLayout()

        self.chk_venta_rapida = QCheckBox(
            "Venta rápida — Consumidor final"
        )
        
        self.chk_venta_rapida.setChecked(True)
        
        self.combo_cliente = QComboBox()
        self.combo_cliente.setEnabled(False)
        
        self.chk_venta_rapida.toggled.connect(
            lambda activado: self.combo_cliente.setEnabled(
                not activado
            )
        )

        self.combo_lote = QComboBox()

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 1000000)

        formulario.addRow(
            "Cliente:",
            self.combo_cliente
        )

        formulario.addRow(
            "Medicamento / lote:",
            self.combo_lote
        )

        formulario.addRow(
            "Cantidad:",
            self.spin_cantidad
        )
        
        layout.addWidget(self.chk_venta_rapida)
        layout.addLayout(formulario)

        botones = QHBoxLayout()

        self.btn_agregar = QPushButton(
            "+ Agregar al carrito"
        )
        self.btn_agregar.setObjectName("botonPrincipal")
        self.btn_agregar.clicked.connect(
            self.agregar_producto
        )

        self.btn_quitar = QPushButton(
            "Quitar seleccionado"
        )
        self.btn_quitar.clicked.connect(
            self.quitar_producto
        )

        self.btn_actualizar = QPushButton(
            "Actualizar datos"
        )
        self.btn_actualizar.clicked.connect(
            self.cargar_datos
        )

        botones.addWidget(self.btn_agregar)
        botones.addWidget(self.btn_quitar)
        botones.addWidget(self.btn_actualizar)

        layout.addLayout(botones)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)

        self.tabla.setHorizontalHeaderLabels([
            "Lote / Medicamento",
            "Cantidad",
            "Precio unitario",
            "Subtotal"
        ])

        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout.addWidget(self.tabla)

        self.lbl_total = QLabel("TOTAL: S/ 0.00")
        self.lbl_total.setStyleSheet(
            "font-size: 24px; font-weight: bold;"
        )
        layout.addWidget(self.lbl_total)

        self.btn_confirmar = QPushButton(
            "Confirmar venta"
        )
        self.btn_confirmar.setObjectName("botonPrincipal")
        self.btn_confirmar.clicked.connect(
            self.confirmar_venta
        )

        layout.addWidget(self.btn_confirmar)

    def cargar_datos(self):

        try:
            lotes = (
                self.repositorio_lotes.listar_lotes_disponibles()
            )

            # Consulta directa temporal de clientes
            with self.repositorio_clientes.database.conectar() as conexion:
                clientes = conexion.execute(
                    """
                    SELECT documento, nombre
                    FROM clientes
                    WHERE documento <> 'CF-GENERICO'
                    ORDER BY nombre
                    """
                ).fetchall()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )
            return

        self.lotes = {
            lote["numero_lote"]: lote
            for lote in lotes
        }

        self.combo_lote.clear()
        self.combo_cliente.clear()

        for lote in lotes:

            self.combo_lote.addItem(
                f"{lote['medicamento_nombre']} "
                f"({lote['numero_lote']}) "
                f"- Stock: {lote['cantidad']}",
                lote["numero_lote"]
            )

        for cliente in clientes:

            self.combo_cliente.addItem(
                f"{cliente['documento']} - "
                f"{cliente['nombre']}",
                cliente["documento"]
            )

    def agregar_producto(self):

        numero_lote = self.combo_lote.currentData()
        cantidad = self.spin_cantidad.value()

        if numero_lote is None:
            QMessageBox.warning(
                self,
                "Sin productos",
                "No hay lotes disponibles."
            )
            return

        lote = self.lotes[numero_lote]

        cantidad_anterior = self.carrito.get(
            numero_lote,
            0
        )

        nueva_cantidad = cantidad_anterior + cantidad

        if nueva_cantidad > lote["cantidad"]:
            QMessageBox.warning(
                self,
                "Stock insuficiente",
                "La cantidad supera las existencias."
            )
            return

        self.carrito[numero_lote] = nueva_cantidad

        self.actualizar_carrito()

    def quitar_producto(self):

        fila = self.tabla.currentRow()

        if fila < 0:
            QMessageBox.warning(
                self,
                "Seleccione un producto",
                "Seleccione una fila del carrito."
            )
            return

        item = self.tabla.item(fila, 0)

        if item is None:
            return

        numero_lote = item.data(256)

        self.carrito.pop(numero_lote, None)

        self.actualizar_carrito()

    def actualizar_carrito(self):

        self.tabla.setRowCount(len(self.carrito))

        total_centimos = 0

        for fila, (numero_lote, cantidad) in enumerate(
            self.carrito.items()
        ):

            lote = self.lotes.get(numero_lote)
            if lote is None:
                # El lote ya no está disponible en el catálogo actual.
                # No intentamos calcular su precio ni mostrarlo como válido.
                continue

            precio = lote["precio_centimos"]
            subtotal = precio * cantidad

            total_centimos += subtotal

            valores = [
                f"{numero_lote} - "
                f"{lote['medicamento_nombre']}",
                str(cantidad),
                f"S/ {precio / 100:.2f}",
                f"S/ {subtotal / 100:.2f}"
            ]

            for columna, valor in enumerate(valores):

                item = QTableWidgetItem(valor)

                if columna == 0:
                    item.setData(256, numero_lote)

                self.tabla.setItem(
                    fila,
                    columna,
                    item
                )

        self.lbl_total.setText(
            f"TOTAL: S/ {total_centimos / 100:.2f}"
        )

    def confirmar_venta(self):

        if self.chk_venta_rapida.isChecked():

            documento = None

        else:

             documento = self.combo_cliente.currentData()

             if documento is None:
                 QMessageBox.warning(
                     self,
                     "Sin cliente",
                     "Seleccione un cliente registrado "
                     "o active la venta rápida."
                 )
                 return

        if not self.carrito:
            QMessageBox.warning(
                self,
                "Carrito vacío",
                "Agregue productos antes de vender."
            )
            return

        numero_venta = (
            "V-" + uuid.uuid4().hex[:12].upper()
        )

        productos = list(self.carrito.items())

        respuesta = QMessageBox.question(
            self,
            "Confirmar venta",
            "¿Desea confirmar esta venta?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if respuesta != QMessageBox.StandardButton.Yes:
            return

        try:
            total = self.repositorio_ventas.registrar_venta(
                numero_venta,
                documento,
                productos
            )

        except (ValueError, sqlite3.Error) as error:
            QMessageBox.critical(
                self,
                "No se pudo registrar la venta",
                str(error)
            )
            return


        QMessageBox.information(
            self,
            "Venta registrada",
            f"Venta: {numero_venta}\n"
            f"Total: S/ {total / 100:.2f}"
        )

        # Limpiar carrito y actualizar productos
        self.carrito.clear()

        self.cargar_datos()
        self.actualizar_carrito()

        # Mostrar ticket de la venta confirmada
        ticket = TicketVenta(
            self.repositorio_ventas,
            numero_venta,
            self
        )

        ticket.exec()

        
    
    def showEvent(self, event):

        super().showEvent(event)

        if hasattr(self, "combo_cliente"):
            self.cargar_datos()

