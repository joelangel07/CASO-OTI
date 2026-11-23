from decimal import Decimal, InvalidOperation
import sqlite3

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QDialogButtonBox
)

from medicamento import Medicamento

class FormularioMedicamento(QDialog):

    def __init__(self, repositorio, parent=None):
        super().__init__(parent)

        self.repositorio = repositorio

        self.setWindowTitle("Registrar medicamento")
        self.setMinimumWidth(420)

        self.crear_interfaz()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)

        formulario = QFormLayout()

        self.txt_codigo = QLineEdit()
        self.txt_nombre = QLineEdit()
        self.txt_descripcion = QLineEdit()
        self.txt_precio = QLineEdit()

        self.txt_codigo.setPlaceholderText("MED004")
        self.txt_nombre.setPlaceholderText("Nombre del producto")
        self.txt_descripcion.setPlaceholderText("Descripción")
        self.txt_precio.setPlaceholderText("Ejemplo: 4.50")

        formulario.addRow("Código:", self.txt_codigo)
        formulario.addRow("Nombre:", self.txt_nombre)
        formulario.addRow("Descripción:", self.txt_descripcion)
        formulario.addRow("Precio (S/):", self.txt_precio)

        layout.addLayout(formulario)

        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )

        botones.accepted.connect(self.guardar)
        botones.rejected.connect(self.reject)

        layout.addWidget(botones)

    def guardar(self):

        codigo = self.txt_codigo.text().strip()
        nombre = self.txt_nombre.text().strip()
        descripcion = self.txt_descripcion.text().strip()
        texto_precio = self.txt_precio.text().strip()

        if not all([codigo, nombre, descripcion, texto_precio]):
            QMessageBox.warning(
                self,
                "Datos incompletos",
                "Complete todos los campos."
            )
            return

        try:
            precio = Decimal(texto_precio)

            if (
                not precio.is_finite()
                or precio < 0
                or precio.as_tuple().exponent < -2
            ):
                raise ValueError

        except (InvalidOperation, ValueError):
            QMessageBox.warning(
                self,
                "Precio inválido",
                "Ingrese un precio válido con máximo "
                "dos decimales."
            )
            return

        medicamento = Medicamento(
            codigo,
            nombre,
            descripcion,
            precio
        )

        try:
            self.repositorio.guardar(medicamento)

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Código duplicado",
                "Ya existe un medicamento con ese código."
            )
            return

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )
            return

        QMessageBox.information(
            self,
            "Registro exitoso",
            "Medicamento guardado correctamente."
        )

        self.accept()
