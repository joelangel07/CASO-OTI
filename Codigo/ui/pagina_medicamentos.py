
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
    QMessageBox
)

from PySide6.QtCore import Qt

from ui.formulario_medicamento import FormularioMedicamento


class PaginaMedicamentos(QWidget):

    def __init__(self, repositorio):
        super().__init__()

        self.repositorio = repositorio
        self.medicamentos = []

        self.crear_interfaz()
        self.cargar_medicamentos()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        titulo = QLabel("Gestión de medicamentos")
        titulo.setObjectName("tituloPagina")

        layout.addWidget(titulo)

        descripcion = QLabel(
            "Registra, consulta y busca medicamentos"
        )
        descripcion.setObjectName("descripcion")

        layout.addWidget(descripcion)

        barra = QHBoxLayout()

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText(
            "Buscar por código o nombre..."
        )

        self.txt_buscar.textChanged.connect(
            self.filtrar_medicamentos
        )

        self.btn_nuevo = QPushButton("+ Nuevo medicamento")
        self.btn_nuevo.setObjectName("botonPrincipal")

        self.btn_nuevo.clicked.connect(
            self.abrir_formulario
        )

        barra.addWidget(self.txt_buscar)
        barra.addWidget(self.btn_nuevo)

        layout.addLayout(barra)

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels([
            "Código",
            "Nombre",
            "Descripción",
            "Precio"
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

        self.tabla.setAlternatingRowColors(True)

        layout.addWidget(self.tabla)

    def cargar_medicamentos(self):

        try:
            self.medicamentos = (
                self.repositorio.listar_todos()
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error de base de datos",
                str(error)
            )
            return

        self.filtrar_medicamentos()

    def filtrar_medicamentos(self):

        texto = self.txt_buscar.text().strip().lower()

        filtrados = [
            medicamento
            for medicamento in self.medicamentos
            if texto in medicamento.codigo.lower()
            or texto in medicamento.nombre.lower()
        ]

        self.tabla.setRowCount(len(filtrados))

        for fila, medicamento in enumerate(filtrados):

            valores = [
                medicamento.codigo,
                medicamento.nombre,
                medicamento.descripcion,
                f"S/ {medicamento.precio:.2f}"
            ]

            for columna, valor in enumerate(valores):

                item = QTableWidgetItem(valor)

                item.setFlags(
                    item.flags() &
                    ~Qt.ItemFlag.ItemIsEditable
                )

                self.tabla.setItem(
                    fila,
                    columna,
                    item
                )

    def abrir_formulario(self):

        formulario = FormularioMedicamento(
            self.repositorio,
            self
        )

        if formulario.exec():
            self.cargar_medicamentos()
