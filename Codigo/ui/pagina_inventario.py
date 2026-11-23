from ui.historial_movimientos import HistorialMovimientos
from ui.formulario_entrada_stock import FormularioEntradaStock
from ui.formulario_lote import FormularioLote
from datetime import date


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
from PySide6.QtGui import QColor

from inventario_service import InventarioService


class PaginaInventario(QWidget):

    def __init__(self,
       repositorio_lotes,
       repositorio_medicamentos
       ):
       super().__init__()

       self.repositorio = repositorio_lotes
       self.repositorio_medicamentos = (
       repositorio_medicamentos
        )

       self.servicio = InventarioService(stock_minimo=5)
       self.registros = []

       self.crear_interfaz()
       self.cargar_inventario()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        titulo = QLabel("Control de inventario")
        titulo.setObjectName("tituloPagina")
        layout.addWidget(titulo)

        descripcion = QLabel(
            "Consulta existencias, lotes y vencimientos"
        )
        descripcion.setObjectName("descripcion")
        layout.addWidget(descripcion)

        barra = QHBoxLayout()

        self.txt_buscar = QLineEdit()
        self.txt_buscar.setPlaceholderText(
            "Buscar medicamento o número de lote..."
        )
        self.txt_buscar.textChanged.connect(self.filtrar)

        self.btn_actualizar = QPushButton("Actualizar")
        self.btn_actualizar.setObjectName("botonPrincipal")
        self.btn_actualizar.clicked.connect(
            self.cargar_inventario
        )
        
        self.btn_nuevo = QPushButton("+ Nuevo lote")
        self.btn_nuevo.setObjectName("botonPrincipal")
        self.btn_nuevo.clicked.connect(
            self.abrir_formulario
        )
        
        self.btn_entrada = QPushButton("+ Entrada de stock")
        self.btn_entrada.setObjectName("botonPrincipal")
        self.btn_entrada.clicked.connect(
            self.abrir_entrada_stock
        )
        
        self.btn_historial = QPushButton("Historial")
        self.btn_historial.setObjectName("botonPrincipal")

        self.btn_historial.clicked.connect(
            self.abrir_historial
        )

        barra.addWidget(self.txt_buscar)
        barra.addWidget(self.btn_actualizar)
        barra.addWidget(self.btn_nuevo)
        barra.addWidget(self.btn_entrada)
        barra.addWidget(self.btn_historial)

        layout.addLayout(barra)

        self.lbl_resumen = QLabel()
        self.lbl_resumen.setObjectName("descripcion")
        layout.addWidget(self.lbl_resumen)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)

        self.tabla.setHorizontalHeaderLabels([
            "Lote",
            "Medicamento",
            "Stock",
            "Vencimiento",
            "Estado"
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

    def cargar_inventario(self):

        try:
            self.registros = self.repositorio.listar_inventario()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error de inventario",
                str(error)
            )
            return

        self.filtrar()

    def filtrar(self):

        texto = self.txt_buscar.text().strip().lower()

        registros = [
            r for r in self.registros
            if texto in r["medicamento"].lower()
            or texto in r["numero_lote"].lower()
        ]

        self.tabla.setRowCount(len(registros))

        stock_bajo = 0
        vencidos = 0

        for fila, registro in enumerate(registros):

            fecha = date.fromisoformat(
                registro["fecha_vencimiento"]
            )

            estado = self.servicio.obtener_estado(
                registro["cantidad"],
                fecha
            )

            if estado == "Stock bajo":
                stock_bajo += 1

            if estado == "Vencido":
                vencidos += 1

            valores = [
                registro["numero_lote"],
                registro["medicamento"],
                str(registro["cantidad"]),
                registro["fecha_vencimiento"],
                estado
            ]

            for columna, valor in enumerate(valores):

                item = QTableWidgetItem(valor)

                item.setFlags(
                    item.flags() &
                    ~Qt.ItemFlag.ItemIsEditable
                )

                if columna == 4:

                    if estado == "Vencido":
                        item.setForeground(QColor("#C0392B"))

                    elif estado == "Stock bajo":
                        item.setForeground(QColor("#D68910"))

                    elif estado == "Sin stock":
                        item.setForeground(QColor("#C0392B"))

                    else:
                        item.setForeground(QColor("#16845D"))

                self.tabla.setItem(
                    fila,
                    columna,
                    item
                )

        self.lbl_resumen.setText(
            f"Lotes mostrados: {len(registros)}   |   "
            f"Stock bajo: {stock_bajo}   |   "
            f"Vencidos: {vencidos}"
        )
    def abrir_formulario(self):

       formulario = FormularioLote(
           self.repositorio,
           self.repositorio_medicamentos,
          self
       )

       if formulario.exec():
           self.cargar_inventario()
           
    
    def abrir_entrada_stock(self):

        fila = self.tabla.currentRow()

        if fila < 0:
            QMessageBox.warning(
                self,
                "Seleccione un lote",
                "Primero seleccione un lote de la tabla."
            )
            return

        item_lote = self.tabla.item(fila, 0)

        if item_lote is None:
            return

        numero_lote = item_lote.text()

        # Buscar el registro original por su identificador
        registro = next(
            (
                r for r in self.registros
                if r["numero_lote"] == numero_lote
            ),
            None
        )

        if registro is None:
            QMessageBox.warning(
                self,
                "Lote no encontrado",
                "No se encontró el lote seleccionado."
            )
            return

        formulario = FormularioEntradaStock(
            self.repositorio,
            registro["numero_lote"],
            registro["medicamento"],
            registro["cantidad"],
            self
        )

        if formulario.exec():
            self.cargar_inventario()
            
    
    def abrir_historial(self):

        fila = self.tabla.currentRow()

        if fila < 0:
            QMessageBox.warning(
                self,
                "Seleccione un lote",
                "Primero seleccione un lote de la tabla."
            )
            return

        item = self.tabla.item(fila, 0)

        if item is None:
            return

        numero_lote = item.text()

        ventana = HistorialMovimientos(
            self.repositorio,
            numero_lote,
            self
        )

        ventana.exec()

    def abrir_historial(self):

        fila = self.tabla.currentRow()

        if fila < 0:
            QMessageBox.warning(
                self,
                "Seleccione un lote",
                "Primero seleccione un lote de la tabla."
            )
            return

        item = self.tabla.item(fila, 0)

        if item is None:
            return

        numero_lote = item.text()

        ventana = HistorialMovimientos(
            self.repositorio,
            numero_lote,
            self
        )

        ventana.exec()


