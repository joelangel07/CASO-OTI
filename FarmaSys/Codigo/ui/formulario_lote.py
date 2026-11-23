
import sqlite3
from datetime import date

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QLineEdit,
    QSpinBox,
    QDateEdit,
    QDialogButtonBox,
    QMessageBox
)

from PySide6.QtCore import QDate

from lote import Lote


class FormularioLote(QDialog):

    def __init__(
        self,
        repositorio_lotes,
        repositorio_medicamentos,
        parent=None
    ):
        super().__init__(parent)

        self.repositorio_lotes = repositorio_lotes
        self.repositorio_medicamentos = (
            repositorio_medicamentos
        )

        self.medicamentos = {}

        self.setWindowTitle("Registrar nuevo lote")
        self.setMinimumWidth(450)

        self.crear_interfaz()
        self.cargar_medicamentos()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)

        formulario = QFormLayout()

        # Lista desplegable de medicamentos
        self.combo_medicamento = QComboBox()

        # Número del lote
        self.txt_numero = QLineEdit()
        self.txt_numero.setPlaceholderText(
            "Ejemplo: L005"
        )

        # Cantidad inicial
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 1000000)
        self.spin_cantidad.setValue(1)

        # Fecha de vencimiento
        self.fecha_vencimiento = QDateEdit()
        self.fecha_vencimiento.setCalendarPopup(True)
        self.fecha_vencimiento.setDisplayFormat(
            "dd/MM/yyyy"
        )

        self.fecha_vencimiento.setDate(
            QDate.currentDate().addYears(1)
        )

        # Campos del formulario
        formulario.addRow(
            "Medicamento:",
            self.combo_medicamento
        )

        formulario.addRow(
            "Número de lote:",
            self.txt_numero
        )

        formulario.addRow(
            "Cantidad:",
            self.spin_cantidad
        )

        formulario.addRow(
            "Vencimiento:",
            self.fecha_vencimiento
        )

        layout.addLayout(formulario)

        # Botones Guardar y Cancelar
        botones = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save |
            QDialogButtonBox.StandardButton.Cancel
        )

        botones.accepted.connect(self.guardar)
        botones.rejected.connect(self.reject)

        layout.addWidget(botones)

    def cargar_medicamentos(self):

        try:
            lista = (
                self.repositorio_medicamentos.listar_todos()
            )

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudieron cargar medicamentos:\n{error}"
            )
            return

        self.combo_medicamento.clear()
        self.medicamentos.clear()

        for medicamento in lista:

            self.medicamentos[medicamento.codigo] = (
                medicamento
            )

            self.combo_medicamento.addItem(
                f"{medicamento.codigo} - "
                f"{medicamento.nombre}",
                medicamento.codigo
            )

    def guardar(self):

        numero = self.txt_numero.text().strip()
        codigo = self.combo_medicamento.currentData()
        cantidad = self.spin_cantidad.value()

        # Convertir QDate a date de Python
        fecha_qt = self.fecha_vencimiento.date()

        fecha = date(
            fecha_qt.year(),
            fecha_qt.month(),
            fecha_qt.day()
        )

        # Validar número de lote
        if not numero:
            QMessageBox.warning(
                self,
                "Datos incompletos",
                "Ingrese el número de lote."
            )
            return

        # Validar medicamento seleccionado
        if codigo is None:
            QMessageBox.warning(
                self,
                "Sin medicamentos",
                "Primero registre un medicamento."
            )
            return

        # Validar vencimiento
        if fecha <= date.today():
            QMessageBox.warning(
                self,
                "Fecha inválida",
                "El lote debe vencer después de hoy."
            )
            return

        # Obtener el objeto Medicamento
        medicamento = self.medicamentos[codigo]

        # Crear objeto Lote
        try:
            lote = Lote(
                numero,
                medicamento,
                cantidad,
                fecha
            )

            # Guardar lote en SQLite
            self.repositorio_lotes.guardar(lote)

        except sqlite3.IntegrityError:
            QMessageBox.warning(
                self,
                "Lote duplicado",
                "Ya existe un lote con ese número "
                "o hay un problema con sus referencias."
            )
            return

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )
            return

        # Confirmación
        QMessageBox.information(
            self,
            "Registro exitoso",
            "Lote registrado correctamente."
        )

        # Cerrar formulario y actualizar inventario
        self.accept()
