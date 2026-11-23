from ui.ticket_venta import TicketVenta
import sqlite3

from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QDialog
)


class DialogoDetalleVenta(QDialog):

    def __init__(
        self,
        repositorio,
        numero_venta,
        parent=None
    ):
        super().__init__(parent)

        self.repositorio = repositorio
        self.numero_venta = numero_venta

        self.setWindowTitle(
            f"Detalle de venta {numero_venta}"
        )
        self.resize(750, 420)

        self.crear_interfaz()
        self.cargar_detalles()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)

        titulo = QLabel(
            f"Detalle de venta: {self.numero_venta}"
        )
        titulo.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        layout.addWidget(titulo)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)

        self.tabla.setHorizontalHeaderLabels([
            "Medicamento",
            "Lote",
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
            "font-size: 20px; font-weight: bold;"
        )

        layout.addWidget(self.lbl_total)

    def cargar_detalles(self):

        try:
            detalles = self.repositorio.obtener_detalles(
                self.numero_venta
            )

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )
            return

        self.tabla.setRowCount(len(detalles))

        total_centimos = 0

        for fila, detalle in enumerate(detalles):

            total_centimos += detalle[
                "subtotal_centimos"
            ]

            valores = [
                detalle["medicamento"],
                detalle["lote_numero"],
                str(detalle["cantidad"]),
                (
                    f"S/ "
                    f"{detalle['precio_unitario_centimos'] / 100:.2f}"
                ),
                (
                    f"S/ "
                    f"{detalle['subtotal_centimos'] / 100:.2f}"
                )
            ]

            for columna, valor in enumerate(valores):

                self.tabla.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(valor)
                )

        self.lbl_total.setText(
            f"TOTAL: S/ {total_centimos / 100:.2f}"
        )


class HistorialVentas(QWidget):

    def __init__(self, repositorio_ventas):
        super().__init__()

        self.repositorio = repositorio_ventas
        self.ventas = []

        self.crear_interfaz()
        self.cargar_ventas()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(18)

        titulo = QLabel("Historial de ventas")
        titulo.setObjectName("tituloPagina")
        layout.addWidget(titulo)

        descripcion = QLabel(
            "Consulta las operaciones registradas"
        )
        descripcion.setObjectName("descripcion")
        layout.addWidget(descripcion)

        barra = QHBoxLayout()

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText(
            "Buscar por número, cliente o fecha..."
        )

        self.txt_buscar.textChanged.connect(
            self.filtrar
        )

        self.btn_actualizar = QPushButton(
            "Actualizar"
        )

        self.btn_actualizar.clicked.connect(
            self.cargar_ventas
        )

        self.btn_detalle = QPushButton(
            "Ver detalle"
        )

        self.btn_detalle.setObjectName(
            "botonPrincipal"
        )

        self.btn_detalle.clicked.connect(
            self.ver_detalle
        )
        self.btn_ticket = QPushButton(
            "Ver ticket"
        )
        
        self.btn_ticket.setObjectName(
            "botonPrincipal"
        )
        
        self.btn_ticket.clicked.connect(
            self.ver_ticket
        )

        barra.addWidget(self.txt_buscar)
        barra.addWidget(self.btn_actualizar)
        barra.addWidget(self.btn_detalle)
        barra.addWidget(self.btn_ticket)

        layout.addLayout(barra)

        self.lbl_resumen = QLabel(
            "Ventas registradas: 0"
        )
        layout.addWidget(self.lbl_resumen)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)

        self.tabla.setHorizontalHeaderLabels([
            "Número de venta",
            "Fecha",
            "Cliente",
            "Total"
        ])

        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabla.doubleClicked.connect(
            self.ver_detalle
        )

        layout.addWidget(self.tabla)

    def cargar_ventas(self):

        try:
            self.ventas = self.repositorio.listar_ventas()

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )
            return

        self.filtrar()

    def filtrar(self):

        texto = self.txt_buscar.text().strip().lower()

        filtradas = []

        for venta in self.ventas:

            fecha = self.formatear_fecha(
                venta["fecha"]
            )

            contenido = (
                f"{venta['numero_venta']} "
                f"{venta['cliente']} "
                f"{venta['fecha']} "
                f"{fecha}"
            ).lower()

            if texto in contenido:
                filtradas.append(venta)

        self.tabla.setRowCount(len(filtradas))

        total_centimos = 0

        for fila, venta in enumerate(filtradas):

            total_centimos += venta["total_centimos"]

            valores = [
                venta["numero_venta"],
                self.formatear_fecha(venta["fecha"]),
                venta["cliente"],
                f"S/ {venta['total_centimos'] / 100:.2f}"
            ]

            for columna, valor in enumerate(valores):

                self.tabla.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(valor)
                )

        self.lbl_resumen.setText(
            f"Ventas mostradas: {len(filtradas)}"
            f"   |   Total: S/ {total_centimos / 100:.2f}"
        )

    def formatear_fecha(self, fecha):

        try:
            return datetime.fromisoformat(
                fecha
            ).strftime("%d/%m/%Y %H:%M")

        except (ValueError, TypeError):
            return str(fecha)

    def ver_detalle(self, *args):

        fila = self.tabla.currentRow()

        if fila < 0:
            QMessageBox.warning(
                self,
                "Seleccione una venta",
                "Primero seleccione una venta."
            )
            return

        item = self.tabla.item(fila, 0)

        if item is None:
            return

        numero_venta = item.text()

        dialogo = DialogoDetalleVenta(
            self.repositorio,
            numero_venta,
            self
        )

        dialogo.exec()

    def showEvent(self, event):

        super().showEvent(event)

        if hasattr(self, "tabla"):
            self.cargar_ventas()
            
    
    def ver_ticket(self):

        fila = self.tabla.currentRow()

        if fila < 0:
            QMessageBox.warning(
                self,
                "Seleccione una venta",
                "Primero seleccione una venta."
            )
            return

        item = self.tabla.item(fila, 0)

        if item is None:
            return

        numero_venta = item.text()

        ticket = TicketVenta(
            self.repositorio,
            numero_venta,
            self
        )

        ticket.exec()

