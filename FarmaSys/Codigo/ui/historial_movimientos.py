
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox
)


class HistorialMovimientos(QDialog):

    def __init__(
        self,
        repositorio_lotes,
        numero_lote,
        parent=None
    ):
        super().__init__(parent)

        self.repositorio = repositorio_lotes
        self.numero_lote = numero_lote

        self.setWindowTitle(
            f"Historial del lote {numero_lote}"
        )
        self.resize(750, 450)

        self.crear_interfaz()
        self.cargar_movimientos()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)

        titulo = QLabel(
            f"Historial de movimientos — {self.numero_lote}"
        )

        titulo.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        layout.addWidget(titulo)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)

        self.tabla.setHorizontalHeaderLabels([
            "Fecha",
            "Tipo",
            "Cantidad",
            "Motivo"
        ])

        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        layout.addWidget(self.tabla)

    def cargar_movimientos(self):

        try:
            movimientos = (
                self.repositorio.listar_movimientos(
                    self.numero_lote
                )
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                str(error)
            )
            return

        self.tabla.setRowCount(len(movimientos))

        for fila, movimiento in enumerate(movimientos):

            valores = [
                movimiento["fecha"],
                movimiento["tipo"],
                str(movimiento["cantidad"]),
                movimiento["motivo"]
            ]

            for columna, valor in enumerate(valores):

                self.tabla.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(valor)
                )
