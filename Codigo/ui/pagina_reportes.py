
import csv
import sqlite3

from datetime import date

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QDateEdit,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QMessageBox,
    QFrame
)


class PaginaReportes(QWidget):

    def __init__(self, repositorio):
        super().__init__()

        self.repositorio = repositorio

        self.datos_ventas = []
        self.datos_productos = []
        self.datos_inventario = []

        self.crear_interfaz()
        self.generar_reporte()

    def crear_tabla(self, columnas):

        tabla = QTableWidget()
        tabla.setColumnCount(len(columnas))
        tabla.setHorizontalHeaderLabels(columnas)

        tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        tabla.setAlternatingRowColors(True)

        return tabla

    def crear_interfaz(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(18)

        titulo = QLabel("Reportes")
        titulo.setStyleSheet(
            "font-size: 27px; font-weight: bold;"
        )
        layout.addWidget(titulo)

        descripcion = QLabel(
            "Analiza las ventas y el inventario de FarmaSys"
        )
        layout.addWidget(descripcion)

        filtros = QHBoxLayout()

        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_inicio.setDisplayFormat("dd/MM/yyyy")

        hoy = date.today()

        self.fecha_inicio.setDate(
            QDate(hoy.year, hoy.month, 1)
        )

        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        self.fecha_fin.setDisplayFormat("dd/MM/yyyy")
        self.fecha_fin.setDate(QDate.currentDate())

        self.btn_generar = QPushButton(
            "Generar reporte"
        )
        self.btn_generar.clicked.connect(
            self.generar_reporte
        )

        self.btn_exportar = QPushButton(
            "Exportar CSV"
        )
        self.btn_exportar.clicked.connect(
            self.exportar_csv
        )

        filtros.addWidget(QLabel("Desde:"))
        filtros.addWidget(self.fecha_inicio)

        filtros.addWidget(QLabel("Hasta:"))
        filtros.addWidget(self.fecha_fin)

        filtros.addWidget(self.btn_generar)
        filtros.addWidget(self.btn_exportar)

        layout.addLayout(filtros)

        indicadores = QGridLayout()
        indicadores.setSpacing(15)

        self.lbl_ventas = QLabel("Ventas: 0")
        self.lbl_ingresos = QLabel("Ingresos: S/ 0.00")

        for etiqueta in (
            self.lbl_ventas,
            self.lbl_ingresos
        ):
            etiqueta.setStyleSheet("""
                QLabel {
                    background-color: #1e293b;
                    color: #f8fafc;
                    border: 1px solid #334155;
                    border-radius: 12px;
                    padding: 20px;
                    font-size: 19px;
                    font-weight: bold;
                }
            """)

        indicadores.addWidget(self.lbl_ventas, 0, 0)
        indicadores.addWidget(self.lbl_ingresos, 0, 1)

        layout.addLayout(indicadores)

        self.pestanas = QTabWidget()

        self.tabla_ventas = self.crear_tabla([
            "Número de venta",
            "Fecha",
            "Cliente",
            "Total"
        ])

        self.tabla_productos = self.crear_tabla([
            "Código",
            "Medicamento",
            "Unidades vendidas",
            "Ingresos"
        ])

        self.tabla_inventario = self.crear_tabla([
            "Lote",
            "Código",
            "Medicamento",
            "Stock",
            "Vencimiento"
        ])

        self.pestanas.addTab(
            self.tabla_ventas,
            "Ventas"
        )

        self.pestanas.addTab(
            self.tabla_productos,
            "Más vendidos"
        )

        self.pestanas.addTab(
            self.tabla_inventario,
            "Inventario"
        )

        layout.addWidget(self.pestanas)

    def llenar_tabla(self, tabla, registros, columnas):

        tabla.setRowCount(len(registros))

        for fila, registro in enumerate(registros):

            for columna, clave in enumerate(columnas):

                valor = registro[clave]

                if clave in (
                    "total_centimos",
                    "ingresos_centimos"
                ):
                    valor = f"S/ {valor / 100:.2f}"

                tabla.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(str(valor))
                )

    def generar_reporte(self):

        inicio = self.fecha_inicio.date().toString(
            "yyyy-MM-dd"
        )

        fin = self.fecha_fin.date().toString(
            "yyyy-MM-dd"
        )

        if inicio > fin:
            QMessageBox.warning(
                self,
                "Fechas inválidas",
                "La fecha inicial no puede ser "
                "posterior a la fecha final."
            )
            return

        try:
            resumen = self.repositorio.resumen_ventas(
                inicio, fin
            )

            self.datos_ventas = (
                self.repositorio.listar_ventas(
                    inicio, fin
                )
            )

            self.datos_productos = (
                self.repositorio.medicamentos_mas_vendidos(
                    inicio, fin
                )
            )

            self.datos_inventario = (
                self.repositorio.reporte_inventario()
            )

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Error de base de datos",
                str(error)
            )
            return

        self.lbl_ventas.setText(
            f"Ventas: {resumen['cantidad_ventas']}"
        )

        self.lbl_ingresos.setText(
            "Ingresos: S/ "
            f"{resumen['ingresos_centimos'] / 100:.2f}"
        )

        self.llenar_tabla(
            self.tabla_ventas,
            self.datos_ventas,
            [
                "numero_venta",
                "fecha",
                "cliente",
                "total_centimos"
            ]
        )

        self.llenar_tabla(
            self.tabla_productos,
            self.datos_productos,
            [
                "codigo",
                "nombre",
                "unidades",
                "ingresos_centimos"
            ]
        )

        self.llenar_tabla(
            self.tabla_inventario,
            self.datos_inventario,
            [
                "numero_lote",
                "codigo",
                "medicamento",
                "cantidad",
                "fecha_vencimiento"
            ]
        )

    def exportar_csv(self):

        indice = self.pestanas.currentIndex()

        configuraciones = [
            (
                "ventas",
                self.datos_ventas,
                [
                    "numero_venta",
                    "fecha",
                    "cliente",
                    "total_centimos"
                ]
            ),
            (
                "medicamentos_mas_vendidos",
                self.datos_productos,
                [
                    "codigo",
                    "nombre",
                    "unidades",
                    "ingresos_centimos"
                ]
            ),
            (
                "inventario",
                self.datos_inventario,
                [
                    "numero_lote",
                    "codigo",
                    "medicamento",
                    "cantidad",
                    "fecha_vencimiento"
                ]
            )
        ]

        nombre, datos, columnas = configuraciones[indice]

        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar reporte",
            f"farmasys_{nombre}.csv",
            "Archivos CSV (*.csv)"
        )

        if not ruta:
            return

        if not ruta.lower().endswith(".csv"):
            ruta += ".csv"

        try:
            with open(
                ruta,
                "w",
                newline="",
                encoding="utf-8-sig"
            ) as archivo:

                escritor = csv.writer(archivo)

                escritor.writerow(columnas)

                for registro in datos:

                    escritor.writerow([
                        registro[columna]
                        for columna in columnas
                    ])

        except OSError as error:
            QMessageBox.critical(
                self,
                "Error al exportar",
                str(error)
            )
            return

        QMessageBox.information(
            self,
            "Exportación exitosa",
            "El reporte se guardó correctamente."
        )
