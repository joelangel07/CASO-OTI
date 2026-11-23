
import sqlite3

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QDialogButtonBox,
    QMessageBox
)

from cliente import Cliente


class FormularioCliente(QDialog):

    def __init__(
        self,
        repositorio_clientes,
        parent=None
    ):
        super().__init__(parent)

        self.repositorio = repositorio_clientes

        self.setWindowTitle("Registrar cliente")
        self.setMinimumWidth(430)

        self.crear_interfaz()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)

        formulario = QFormLayout()

        self.txt_documento = QLineEdit()
        self.txt_documento.setPlaceholderText(
            "DNI o RUC"
        )

        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText(
            "Nombre o razón social"
        )

        self.txt_telefono = QLineEdit()
        self.txt_telefono.setPlaceholderText(
            "Teléfono (opcional)"
        )

        formulario.addRow(
            "Documento:",
            self.txt_documento
        )

        formulario.addRow(
            "Nombre:",
            self.txt_nombre
        )

        formulario.addRow(
            "Teléfono:",
            self.txt_telefono
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

        documento = self.txt_documento.text().strip()
        nombre = self.txt_nombre.text().strip()
        telefono = self.txt_telefono.text().strip()

        if not documento or not nombre:
            QMessageBox.warning(
                self,
                "Datos incompletos",
                "Ingrese documento y nombre."
            )
            return

        if documento == "CF-GENERICO":
            QMessageBox.warning(
                self,
                "Documento reservado",
                "Ese código está reservado para "
                "ventas rápidas."
            )
            return

        if not documento.isdigit() or len(documento) not in (8, 11):
            QMessageBox.warning(
                self,
                "Documento inválido",
                "Ingrese un DNI de 8 dígitos "
                "o un RUC de 11 dígitos."
            )
            return

        try:
            cliente = Cliente(
                documento,
                nombre,
                telefono
            )

            self.repositorio.guardar(cliente)

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Cliente duplicado",
                "Ya existe un cliente con ese documento."
            )
            return

        except (ValueError, sqlite3.Error) as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )
            return

        QMessageBox.information(
            self,
            "Registro exitoso",
            "Cliente registrado correctamente."
        )

        self.accept()
