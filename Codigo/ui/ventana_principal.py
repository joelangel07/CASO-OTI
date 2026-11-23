from ui.pagina_clientes import PaginaClientes
from ui.pagina_ventas import PaginaVentas
from ui.pagina_medicamentos import  PaginaMedicamentos
from ui.pagina_inventario import PaginaInventario 
from ui.historial_ventas import HistorialVentas
from dashboard_repository import DashboardRepository
from ui.pagina_dashboard import PaginaDashboard 
from reporte_repository import ReporteRepository
from ui.pagina_reportes import PaginaReportes
from ui.pagina_alertas import PaginaAlertas

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QFrame,
    QGridLayout
)

from PySide6.QtCore import Qt

class VentanaPrincipal(QMainWindow):

   def __init__(
      self,
      repositorio,
      repositorio_lotes,
      repositorio_ventas,
      repositorio_clientes
   ):
      super().__init__()

      self.repositorio = repositorio
      self.repositorio_lotes = repositorio_lotes
      self.repositorio_ventas = repositorio_ventas
      self.repositorio_clientes = repositorio_clientes
      self.repositorio_dashboard = DashboardRepository(
          self.repositorio_ventas.database
      ) 
      self.repositorio_reportes = ReporteRepository(
          self.repositorio_ventas.database
      )
      
      self.setWindowTitle("FarmaSys - Sistema de Farmacia")
      self.resize(1100, 700)

      self.crear_interfaz()
      self.aplicar_estilos()

   def crear_interfaz(self):

        contenedor = QWidget()
        self.setCentralWidget(contenedor)

        layout_principal = QHBoxLayout(contenedor)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # Menú lateral
        self.menu = QFrame()
        self.menu.setObjectName("menu")
        self.menu.setFixedWidth(230)

        layout_menu = QVBoxLayout(self.menu)
        layout_menu.setContentsMargins(15, 25, 15, 20)
        layout_menu.setSpacing(10)

        titulo = QLabel("FarmaSys")
        titulo.setObjectName("logo")

        layout_menu.addWidget(titulo)

        subtitulo = QLabel("Sistema de Farmacia")
        subtitulo.setObjectName("subtitulo")

        layout_menu.addWidget(subtitulo)
        layout_menu.addSpacing(30)

        # Área de páginas
        self.paginas = QStackedWidget()

        nombres = [
            "Dashboard",
            "Medicamentos",
            "Inventario",
            "Alertas",
            "Ventas",
            "Historial de ventas",
            "Clientes",
            "Reportes"
        ]

        for indice, nombre in enumerate(nombres):

            boton = QPushButton(nombre)
            boton.setObjectName("botonMenu")
            boton.setCursor(Qt.CursorShape.PointingHandCursor)

            boton.clicked.connect(
                lambda checked=False, i=indice:
                    self.paginas.setCurrentIndex(i)
            )

            layout_menu.addWidget(boton)

            if nombre == "Dashboard":
                 pagina = PaginaDashboard(
                     self.repositorio_dashboard
                 )    
            
            elif nombre == "Medicamentos":
                pagina = PaginaMedicamentos(
                    self.repositorio
                )
            elif nombre == "Inventario":
                pagina = PaginaInventario(
                    self.repositorio_lotes,
                    self.repositorio
                )
                
            elif nombre == "Alertas":
                pagina = PaginaAlertas(
                     self.repositorio_lotes
               )
            
            elif nombre == "Ventas":
                pagina = PaginaVentas(
                    self.repositorio_ventas,
                    self.repositorio_lotes,
                    self.repositorio_clientes
                )
            
            elif nombre == "Historial de ventas":
                pagina = HistorialVentas(
                    self.repositorio_ventas
                )
                
            elif nombre == "Clientes":
                pagina = PaginaClientes(
                    self.repositorio_clientes
                )
            
            elif nombre == "Reportes":
                pagina = PaginaReportes(
                    self.repositorio_reportes
                )
                
            else:
                pagina = self.crear_pagina(nombre)

            self.paginas.addWidget(pagina)

        layout_menu.addStretch()

        pie_menu = QLabel("FarmaSys v1.0")
        pie_menu.setObjectName("subtitulo")
        layout_menu.addWidget(pie_menu)

        layout_principal.addWidget(self.menu)
        layout_principal.addWidget(self.paginas)

   def crear_dashboard(self):

        pagina = QWidget()
        layout = QVBoxLayout(pagina)

        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(25)

        titulo = QLabel("Panel de control")
        titulo.setObjectName("tituloPagina")
        layout.addWidget(titulo)

        descripcion = QLabel(
            "Bienvenido al sistema de gestión de farmacia"
        )
        descripcion.setObjectName("descripcion")
        layout.addWidget(descripcion)

        grid = QGridLayout()
        grid.setSpacing(20)

        tarjetas = [
            ("Medicamentos", "120"),
            ("Ventas del día", "28"),
            ("Stock bajo", "5"),
            ("Ingresos", "S/ 850.00")
        ]

        for indice, (nombre, valor) in enumerate(tarjetas):

            tarjeta = self.crear_tarjeta(nombre, valor)

            fila = indice // 2
            columna = indice % 2

            grid.addWidget(tarjeta, fila, columna)

        layout.addLayout(grid)
        layout.addStretch()

        return pagina

   def crear_tarjeta(self, nombre, valor):

        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")

        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(20, 20, 20, 20)

        etiqueta = QLabel(nombre)
        etiqueta.setObjectName("descripcion")

        numero = QLabel(valor)
        numero.setObjectName("numeroTarjeta")

        layout.addWidget(etiqueta)
        layout.addWidget(numero)

        return tarjeta

   def crear_pagina(self, nombre):

        pagina = QWidget()
        layout = QVBoxLayout(pagina)

        layout.setContentsMargins(35, 30, 35, 30)

        titulo = QLabel(nombre)
        titulo.setObjectName("tituloPagina")

        descripcion = QLabel(
            f"Módulo de {nombre} de FarmaSys"
        )
        descripcion.setObjectName("descripcion")

        layout.addWidget(titulo)
        layout.addWidget(descripcion)
        layout.addStretch()

        return pagina

   def aplicar_estilos(self):

        self.setStyleSheet("""
            QMainWindow {
                background-color: #F3F6FA;
            }

            #menu {
                background-color: #172B36;
            }

            #logo {
                color: #FFFFFF;
                font-size: 26px;
                font-weight: bold;
            }

            #subtitulo {
                color: #9FB0BD;
                font-size: 12px;
            }

            #botonMenu {
                background-color: transparent;
                color: #D9E4EC;
                border: none;
                border-radius: 8px;
                padding: 14px;
                text-align: left;
                font-size: 14px;
            }

            #botonMenu:hover {
                background-color: #294653;
            }

            #tituloPagina {
                color: #172B36;
                font-size: 28px;
                font-weight: bold;
            }

            #descripcion {
                color: #687782;
                font-size: 14px;
            }

            #tarjeta {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E2E8F0;
            }

            #numeroTarjeta {
                color: #172B36;
                font-size: 30px;
                font-weight: bold;
            }
            QLineEdit {
    background-color: white;
    border: 1px solid #D5DEE5;
    border-radius: 8px;
    padding: 10px;
    font-size: 13px;
}

QLineEdit:focus {
    border: 2px solid #16A085;
}

#botonPrincipal {
    background-color: #16A085;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 18px;
    font-weight: bold;
}

#botonPrincipal:hover {
    background-color: #138D75;
}

QTableWidget {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    gridline-color: #EDF2F7;
    selection-background-color: #D5F5E3;
    selection-color: #172B36;
}

QHeaderView::section {
    background-color: #EAF0F5;
    padding: 10px;
    border: none;
    font-weight: bold;
}
        """)
