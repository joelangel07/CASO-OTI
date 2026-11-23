
import sqlite3

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

from ui.formulario_cliente import FormularioCliente


class PaginaClientes(QWidget):

    def __init__(self, repositorio_clientes):
        super().__init__()

        self.repositorio = repositorio_clientes
        self.clientes = []

        self.crear_interfaz()
        self.cargar_clientes()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(18)

        titulo = QLabel("Gestión de clientes")
        titulo.setObjectName("tituloPagina")
        layout.addWidget(titulo)

        descripcion = QLabel(
            "Registro opcional de clientes identificados"
        )
        descripcion.setObjectName("descripcion")
        layout.addWidget(descripcion)

        barra = QHBoxLayout()

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText(
            "Buscar por documento o nombre..."
        )

        self.txt_buscar.textChanged.connect(
            self.filtrar
        )

        self.btn_actualizar = QPushButton(
            "Actualizar"
        )

        self.btn_actualizar.clicked.connect(
            self.cargar_clientes
        )

        self.btn_nuevo = QPushButton(
            "+ Nuevo cliente"
        )
        self.btn_nuevo.setObjectName("botonPrincipal")

        self.btn_nuevo.clicked.connect(
            self.abrir_formulario
        )

        barra.addWidget(self.txt_buscar)
        barra.addWidget(self.btn_actualizar)
        barra.addWidget(self.btn_nuevo)

        layout.addLayout(barra)

        self.lbl_resumen = QLabel()
        layout.addWidget(self.lbl_resumen)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)

        self.tabla.setHorizontalHeaderLabels([
            "Documento",
            "Nombre / Razón social",
            "Teléfono"
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

        layout.addWidget(self.tabla)

    def cargar_clientes(self):

        try:
            self.clientes = self.repositorio.listar_todos()

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

        filtrados = [
            cliente
            for cliente in self.clientes
            if texto in cliente["documento"].lower()
            or texto in cliente["nombre"].lower()
        ]

        self.tabla.setRowCount(len(filtrados))

        for fila, cliente in enumerate(filtrados):

            valores = [
                cliente["documento"],
                cliente["nombre"],
                cliente["telefono"] or ""
            ]

            for columna, valor in enumerate(valores):

                self.tabla.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(str(valor))
                )

        self.lbl_resumen.setText(
            f"Clientes registrados: {len(self.clientes)}"
        )

    def abrir_formulario(self):

        formulario = FormularioCliente(
            self.repositorio,
            self
        )

        if formulario.exec():
            self.cargar_clientes()
