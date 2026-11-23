from PySide6.QtWidgets import QLineEdit
import sqlite3

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QSpinBox,
    QDialogButtonBox,
    QMessageBox
)


class FormularioEntradaStock(QDialog):

    def __init__(
        self,
        repositorio_lotes,
        numero_lote,
        medicamento,
        stock_actual,
        parent=None
    ):
        super().__init__(parent)

        self.repositorio_lotes = repositorio_lotes
        self.numero_lote = numero_lote
        self.stock_actual = stock_actual

        self.setWindowTitle("Entrada de mercadería")
        self.setMinimumWidth(420)

        self.crear_interfaz(
            medicamento
        )

    def crear_interfaz(self, medicamento):

        layout = QVBoxLayout(self)

        titulo = QLabel("Registrar entrada de stock")
        titulo.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )
        layout.addWidget(titulo)

        formulario = QFormLayout()

        lbl_medicamento = QLabel(medicamento)
        lbl_lote = QLabel(self.numero_lote)

        lbl_stock = QLabel(
            f"{self.stock_actual} unidades"
        )

        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 1000000)
        self.spin_cantidad.setValue(1)
        self.txt_motivo = QLineEdit()
        self.txt_motivo.setPlaceholderText(
             "Ejemplo: Compra a proveedor"
        )

        formulario.addRow(
            "Medicamento:",
            lbl_medicamento
        )

        formulario.addRow(
            "Número de lote:",
            lbl_lote
        )

        formulario.addRow(
            "Stock actual:",
            lbl_stock
        )

        formulario.addRow(
            "Cantidad recibida:",
            self.spin_cantidad
        )
        
        formulario.addRow(
            "Motivo:",
            self.txt_motivo
        )

        layout.addLayout(formulario)

        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )

        botones.accepted.connect(self.guardar)
        botones.rejected.connect(self.reject)

        layout.addWidget(botones)

    def guardar(self):

        cantidad = self.spin_cantidad.value()
        
        motivo = self.txt_motivo.text().strip()
        if not motivo:
            QMessageBox.warning(
                self,
                "Motivo obligatorio",
                "Ingrese el motivo de la entrada."
            )
            return

        respuesta = QMessageBox.question(
            self,
            "Confirmar entrada",
            f"¿Agregar {cantidad} unidades "
            f"al lote {self.numero_lote}?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        if respuesta != QMessageBox.StandardButton.Yes:
            return

        try:
            self.repositorio_lotes.agregar_stock(
                self.numero_lote,
                cantidad,
                motivo
            )

        except (ValueError, sqlite3.Error) as error:
            QMessageBox.critical(
                self,
                "Error al actualizar stock",
                str(error)
            )
            return

        QMessageBox.information(
            self,
            "Entrada registrada",
            "Las existencias se actualizaron "
            "correctamente."
        )

        self.accept()
