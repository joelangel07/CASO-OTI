
import sqlite3

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QComboBox
)

from PySide6.QtGui import QColor

from alerta_service import AlertaService


class PaginaAlertas(QWidget):

    def __init__(self, repositorio_lotes):
        super().__init__()

        self.repositorio = repositorio_lotes
        self.service = AlertaService()

        self.alertas = []

        self.crear_interfaz()
        self.actualizar_alertas()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(18)

        encabezado = QHBoxLayout()

        titulo = QLabel("Alertas de inventario")
        titulo.setStyleSheet(
            """
            font-size: 27px;
            font-weight: bold;
            """
        )

        self.btn_actualizar = QPushButton(
            "Actualizar alertas"
        )

        self.btn_actualizar.clicked.connect(
            self.actualizar_alertas
        )

        encabezado.addWidget(titulo)
        encabezado.addStretch()
        encabezado.addWidget(self.btn_actualizar)

        layout.addLayout(encabezado)

        descripcion = QLabel(
            "Control de stock y fechas de vencimiento"
        )

        layout.addWidget(descripcion)

        indicadores = QGridLayout()
        indicadores.setSpacing(12)

        self.lbl_stock_bajo = QLabel()
        self.lbl_sin_stock = QLabel()
        self.lbl_proximos = QLabel()
        self.lbl_vencidos = QLabel()

        tarjetas = [
            self.lbl_stock_bajo,
            self.lbl_sin_stock,
            self.lbl_proximos,
            self.lbl_vencidos
        ]

        for tarjeta in tarjetas:

            tarjeta.setStyleSheet("""
                QLabel {
                    background-color: #1e293b;
                    color: #f8fafc;
                    border: 1px solid #334155;
                    border-radius: 12px;
                    padding: 20px;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)

        indicadores.addWidget(
            self.lbl_stock_bajo, 0, 0
        )
        indicadores.addWidget(
            self.lbl_sin_stock, 0, 1
        )
        indicadores.addWidget(
            self.lbl_proximos, 1, 0
        )
        indicadores.addWidget(
            self.lbl_vencidos, 1, 1
        )

        layout.addLayout(indicadores)

        filtros = QHBoxLayout()

        self.combo_filtro = QComboBox()

        self.combo_filtro.addItems([
            "Todas las alertas",
            "STOCK BAJO",
            "SIN STOCK",
            "PRÓXIMO A VENCER",
            "VENCIDO"
        ])

        self.combo_filtro.currentIndexChanged.connect(
            self.filtrar_alertas
        )

        filtros.addWidget(
            QLabel("Filtrar por estado:")
        )

        filtros.addWidget(self.combo_filtro)
        filtros.addStretch()

        layout.addLayout(filtros)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)

        self.tabla.setHorizontalHeaderLabels([
            "Lote",
            "Medicamento",
            "Stock",
            "Vencimiento",
            "Alerta"
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

    def actualizar_alertas(self):

        try:
            inventario = (
                self.repositorio.listar_inventario()
            )

            self.alertas = (
                self.service.generar_alertas(
                    inventario
                )
            )

        except (sqlite3.Error, ValueError) as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )
            return

        resumen = self.service.obtener_resumen(
            self.alertas
        )

        self.lbl_stock_bajo.setText(
            "Stock bajo\n"
            f"{resumen['STOCK BAJO']} lotes"
        )

        self.lbl_sin_stock.setText(
            "Sin stock\n"
            f"{resumen['SIN STOCK']} lotes"
        )

        self.lbl_proximos.setText(
            "Próximos a vencer\n"
            f"{resumen['PRÓXIMO A VENCER']} lotes"
        )

        self.lbl_vencidos.setText(
            "Vencidos\n"
            f"{resumen['VENCIDO']} lotes"
        )

        self.filtrar_alertas()

    def filtrar_alertas(self, *args):

        filtro = self.combo_filtro.currentText()

        if filtro == "Todas las alertas":

            registros = self.alertas

        else:

            registros = [
                alerta
                for alerta in self.alertas
                if alerta["estado"] == filtro
            ]

        self.tabla.setRowCount(len(registros))

        colores = {
            "STOCK BAJO": "#f59e0b",
            "SIN STOCK": "#ef4444",
            "PRÓXIMO A VENCER": "#f59e0b",
            "VENCIDO": "#ef4444"
        }

        for fila, alerta in enumerate(registros):

            valores = [
                alerta["numero_lote"],
                alerta["medicamento"],
                str(alerta["cantidad"]),
                alerta["fecha_vencimiento"],
                alerta["estado"]
            ]

            for columna, valor in enumerate(valores):

                item = QTableWidgetItem(valor)

                if columna == 4:

                    item.setForeground(
                        QColor(
                            colores.get(
                                alerta["estado"],
                                "#ffffff"
                            )
                        )
                    )

                self.tabla.setItem(
                    fila,
                    columna,
                    item
                )

    def showEvent(self, event):

        super().showEvent(event)

        if hasattr(self, "tabla"):
            self.actualizar_alertas()
