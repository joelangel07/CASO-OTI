
import sqlite3

from datetime import date, datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QFont
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMessageBox
)


class TarjetaEstadistica(QFrame):

    def __init__(self, titulo, valor="0"):
        super().__init__()

        self.setObjectName("tarjetaEstadistica")

        self.setStyleSheet("""
            QFrame#tarjetaEstadistica {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 14px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        self.lbl_titulo = QLabel(titulo)
        self.lbl_titulo.setStyleSheet(
            "color: #94a3b8; font-size: 13px;"
        )

        self.lbl_valor = QLabel(valor)
        self.lbl_valor.setStyleSheet(
            """
            color: #f8fafc;
            font-size: 27px;
            font-weight: bold;
            """
        )

        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.lbl_valor)

    def establecer_valor(self, valor):
        self.lbl_valor.setText(str(valor))


class GraficoVentas(QWidget):

    def __init__(self):
        super().__init__()

        self.datos = []
        self.setMinimumHeight(260)

    def establecer_datos(self, datos):

        self.datos = datos
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        ancho = self.width()
        alto = self.height()

        margen_izquierdo = 65
        margen_derecho = 25
        margen_superior = 30
        margen_inferior = 55

        area_ancho = max(
            1,
            ancho - margen_izquierdo - margen_derecho
        )

        area_alto = max(
            1,
            alto - margen_superior - margen_inferior
        )

        base_y = alto - margen_inferior

        painter.setPen(
            QPen(QColor("#64748b"), 1)
        )

        painter.drawLine(
            margen_izquierdo,
            margen_superior,
            margen_izquierdo,
            base_y
        )

        painter.drawLine(
            margen_izquierdo,
            base_y,
            ancho - margen_derecho,
            base_y
        )

        if not self.datos:
            painter.setPen(QColor("#94a3b8"))
            painter.drawText(
                self.rect(),
                Qt.AlignmentFlag.AlignCenter,
                "No hay datos disponibles"
            )
            return

        maximo = max(
            dato["total_centimos"]
            for dato in self.datos
        )

        escala_maxima = max(maximo, 100)

        cantidad = len(self.datos)
        espacio = area_ancho / cantidad
        ancho_barra = min(48, espacio * 0.58)

        painter.setFont(QFont("Arial", 9))

        for indice, dato in enumerate(self.datos):

            total = dato["total_centimos"]

            altura_barra = (
                total / escala_maxima
            ) * area_alto

            x = (
                margen_izquierdo
                + indice * espacio
                + (espacio - ancho_barra) / 2
            )

            y = base_y - altura_barra

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor("#22c55e"))

            painter.drawRoundedRect(
                int(x),
                int(y),
                int(ancho_barra),
                int(altura_barra),
                5,
                5
            )

            painter.setPen(QColor("#cbd5e1"))

            fecha = datetime.strptime(
                dato["fecha"],
                "%Y-%m-%d"
            ).strftime("%d/%m")

            painter.drawText(
                int(
                    margen_izquierdo
                    + indice * espacio
                ),
                base_y + 8,
                int(espacio),
                24,
                Qt.AlignmentFlag.AlignCenter,
                fecha
            )

            valor = f"{total / 100:.0f}"

            painter.drawText(
                int(
                    margen_izquierdo
                    + indice * espacio
                ),
                int(max(0, y - 24)),
                int(espacio),
                20,
                Qt.AlignmentFlag.AlignCenter,
                valor
            )

        painter.end()


class PaginaDashboard(QWidget):

    def __init__(self, repositorio_dashboard):
        super().__init__()

        self.repositorio = repositorio_dashboard

        self.crear_interfaz()
        self.actualizar_datos()

    def crear_interfaz(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        encabezado = QHBoxLayout()

        titulo = QLabel("Dashboard")
        titulo.setStyleSheet(
            """
            color: #f8fafc;
            font-size: 27px;
            font-weight: bold;
            """
        )

        self.btn_actualizar = QPushButton(
            "Actualizar datos"
        )

        self.btn_actualizar.clicked.connect(
            self.actualizar_datos
        )

        encabezado.addWidget(titulo)
        encabezado.addStretch()
        encabezado.addWidget(self.btn_actualizar)

        layout.addLayout(encabezado)

        descripcion = QLabel(
            "Resumen de operaciones de FarmaSys"
        )
        descripcion.setStyleSheet(
            "color: #94a3b8; font-size: 14px;"
        )

        layout.addWidget(descripcion)

        tarjetas = QGridLayout()
        tarjetas.setSpacing(15)

        self.tarjeta_medicamentos = TarjetaEstadistica(
            "Medicamentos registrados"
        )

        self.tarjeta_ventas = TarjetaEstadistica(
            "Ventas de hoy"
        )

        self.tarjeta_stock = TarjetaEstadistica(
            "Lotes con stock bajo"
        )

        self.tarjeta_ingresos = TarjetaEstadistica(
            "Ingresos de hoy"
        )

        tarjetas.addWidget(
            self.tarjeta_medicamentos, 0, 0
        )
        tarjetas.addWidget(
            self.tarjeta_ventas, 0, 1
        )
        tarjetas.addWidget(
            self.tarjeta_stock, 1, 0
        )
        tarjetas.addWidget(
            self.tarjeta_ingresos, 1, 1
        )

        layout.addLayout(tarjetas)

        contenedor_grafico = QFrame()
        contenedor_grafico.setStyleSheet(
            """
            QFrame {
                background-color: #1e293b;
                border-radius: 14px;
            }
            """
        )

        grafico_layout = QVBoxLayout(
            contenedor_grafico
        )
        grafico_layout.setContentsMargins(
            20, 20, 20, 20
        )

        titulo_grafico = QLabel(
            "Ingresos por ventas — Últimos 7 días"
        )
        titulo_grafico.setStyleSheet(
            """
            color: #f8fafc;
            font-size: 17px;
            font-weight: bold;
            """
        )

        grafico_layout.addWidget(titulo_grafico)

        self.grafico = GraficoVentas()
        grafico_layout.addWidget(self.grafico)

        layout.addWidget(contenedor_grafico)

        self.lbl_actualizacion = QLabel()
        self.lbl_actualizacion.setStyleSheet(
            "color: #94a3b8;"
        )

        layout.addWidget(self.lbl_actualizacion)

    def actualizar_datos(self):

        try:
            resumen = self.repositorio.obtener_resumen()

            ventas = (
                self.repositorio
                .obtener_ventas_ultimos_7_dias()
            )

        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Error de base de datos",
                str(error)
            )
            return

        self.tarjeta_medicamentos.establecer_valor(
            resumen["medicamentos"]
        )

        self.tarjeta_ventas.establecer_valor(
            resumen["ventas_hoy"]
        )

        self.tarjeta_stock.establecer_valor(
            resumen["stock_bajo"]
        )

        self.tarjeta_ingresos.establecer_valor(
            f"S/ "
            f"{resumen['ingresos_hoy_centimos'] / 100:.2f}"
        )

        self.grafico.establecer_datos(ventas)

        hora = datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        self.lbl_actualizacion.setText(
            f"Última actualización: {hora}"
        )

    def showEvent(self, event):

        super().showEvent(event)

        if hasattr(self, "grafico"):
            self.actualizar_datos()
