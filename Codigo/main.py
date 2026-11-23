
import sys

from PySide6.QtWidgets import QApplication

from database import Database
from medicamento_repository import MedicamentoRepository
from lote_repository import LoteRepository
from cliente_repository import ClienteRepository
from venta_repository import VentaRepository

from ui.ventana_principal import VentanaPrincipal

def main():

    db = Database()
    db.crear_tablas()
    db.crear_consumidor_final()

    repositorio_medicamentos = MedicamentoRepository(db)
    repositorio_lotes = LoteRepository(db)
    repositorio_clientes = ClienteRepository(db)
    repositorio_ventas = VentaRepository(db)

    app = QApplication(sys.argv)

    ventana = VentanaPrincipal(
        repositorio_medicamentos,
        repositorio_lotes,
        repositorio_ventas,
        repositorio_clientes
    )

    ventana.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
