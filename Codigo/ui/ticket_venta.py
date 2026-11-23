
import sqlite3
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument
from PySide6.QtPrintSupport import QPrinter, QPrintDialog

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QMessageBox
)

from html import escape


class TicketVenta(QDialog):

    def __init__(
        self,
        repositorio_ventas,
        numero_venta,
        parent=None
    ):
        super().__init__(parent)

        self.repositorio = repositorio_ventas
        self.numero_venta = numero_venta

        self.setWindowTitle(
            f"Ticket de venta - {numero_venta}"
        )
        self.resize(500, 650)

        self.crear_interfaz()
        self.cargar_ticket()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)

        titulo = QLabel("Ticket de venta")
        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        titulo.setStyleSheet(
            "font-size: 20px; font-weight: bold;"
        )

        layout.addWidget(titulo)

        self.vista = QTextEdit()
        self.vista.setReadOnly(True)

        layout.addWidget(self.vista)

        botones = QHBoxLayout()

        self.btn_imprimir = QPushButton(
            "Imprimir ticket"
        )
        self.btn_imprimir.clicked.connect(
            self.imprimir_ticket
        )

        self.btn_cerrar = QPushButton(
            "Cerrar"
        )
        self.btn_cerrar.clicked.connect(
            self.accept
        )

        botones.addWidget(self.btn_imprimir)
        botones.addWidget(self.btn_cerrar)

        layout.addLayout(botones)

    def cargar_ticket(self):

        try:
            venta = self.repositorio.obtener_venta(
                self.numero_venta
            )

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

        if venta is None:
            QMessageBox.warning(
                self,
                "Venta no encontrada",
                "No existe la venta solicitada."
            )
            return

        try:
            fecha = datetime.fromisoformat(
                venta["fecha"]
            ).strftime("%d/%m/%Y %H:%M")

        except (ValueError, TypeError):
            fecha = str(venta["fecha"])

        filas_html = ""

        for detalle in detalles:

            nombre = escape(
                str(detalle["medicamento"])
            )

            cantidad = detalle["cantidad"]

            precio = (
                detalle["precio_unitario_centimos"] / 100
            )

            subtotal = (
                detalle["subtotal_centimos"] / 100
            )

            filas_html += f"""
                <tr>
                    <td>{nombre}</td>
                    <td align="center">{cantidad}</td>
                    <td align="right">S/ {precio:.2f}</td>
                    <td align="right">S/ {subtotal:.2f}</td>
                </tr>
            """

        numero = escape(str(venta["numero_venta"]))
        cliente = escape(str(venta["cliente"]))

        total = venta["total_centimos"] / 100

        html = f"""
        <html>
        <body style="
            font-family: Arial;
            color: #222222;
            background-color: white;
        ">

            <h2 align="center">FARMASYS</h2>

            <p align="center">
                Sistema de gestión de farmacia<br>
                TICKET INTERNO DE VENTA
            </p>

            <hr>

            <p>
                <b>Venta:</b> {numero}<br>
                <b>Fecha:</b> {escape(fecha)}<br>
                <b>Cliente:</b> {cliente}
            </p>

            <hr>

            <table width="100%" cellspacing="5">
                <tr>
                    <th align="left">Producto</th>
                    <th>Cant.</th>
                    <th>Precio</th>
                    <th>Subtotal</th>
                </tr>

                {filas_html}
            </table>

            <hr>

            <h2 align="right">
                TOTAL: S/ {total:.2f}
            </h2>

            <p align="center">
                ¡Gracias por su compra!
            </p>

            <p align="center">
                <small>
                    Documento interno.<br>
                    No es comprobante tributario.
                </small>
            </p>

        </body>
        </html>
        """

        self.vista.setHtml(html)

    def imprimir_ticket(self):

        documento = self.vista.document()

        if not documento.toPlainText().strip():
            QMessageBox.warning(
                self,
                "Sin contenido",
                "No hay un ticket para imprimir."
            )
            return

        impresora = QPrinter(
            QPrinter.PrinterMode.HighResolution
        )

        dialogo = QPrintDialog(
            impresora,
            self
        )

        if dialogo.exec() == QDialog.DialogCode.Accepted:
            documento.print_(impresora)
