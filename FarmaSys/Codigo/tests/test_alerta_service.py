
import unittest

from datetime import date, timedelta

from alerta_service import AlertaService


class TestAlertaService(unittest.TestCase):

    def setUp(self):

        self.service = AlertaService(
            stock_minimo=5,
            dias_alerta_vencimiento=30
        )

    def crear_lote(self, cantidad, dias_para_vencer):

        fecha = (
            date.today()
            + timedelta(days=dias_para_vencer)
        )

        return {
            "numero_lote": "L001",
            "medicamento": "Paracetamol",
            "cantidad": cantidad,
            "fecha_vencimiento": fecha.isoformat()
        }

    def test_stock_bajo(self):

        lote = self.crear_lote(
            cantidad=3,
            dias_para_vencer=100
        )

        alertas = self.service.analizar_lote(lote)

        self.assertIn(
            "STOCK BAJO",
            alertas
        )

    def test_sin_stock(self):

        lote = self.crear_lote(
            cantidad=0,
            dias_para_vencer=100
        )

        alertas = self.service.analizar_lote(lote)

        self.assertIn(
            "SIN STOCK",
            alertas
        )

        self.assertNotIn(
            "STOCK BAJO",
            alertas
        )

    def test_lote_vencido(self):

        lote = self.crear_lote(
            cantidad=20,
            dias_para_vencer=-1
        )

        alertas = self.service.analizar_lote(lote)

        self.assertIn(
            "VENCIDO",
            alertas
        )

    def test_proximo_a_vencer(self):

        lote = self.crear_lote(
            cantidad=20,
            dias_para_vencer=10
        )

        alertas = self.service.analizar_lote(lote)

        self.assertIn(
            "PRÓXIMO A VENCER",
            alertas
        )

    def test_dos_alertas_en_un_lote(self):

        lote = self.crear_lote(
            cantidad=2,
            dias_para_vencer=7
        )

        alertas = self.service.analizar_lote(lote)

        self.assertEqual(
            len(alertas),
            2
        )

        self.assertIn(
            "STOCK BAJO",
            alertas
        )

        self.assertIn(
            "PRÓXIMO A VENCER",
            alertas
        )

    def test_lote_sin_alertas(self):

        lote = self.crear_lote(
            cantidad=50,
            dias_para_vencer=180
        )

        alertas = self.service.analizar_lote(lote)

        self.assertEqual(
            alertas,
            []
        )


if __name__ == "__main__":
    unittest.main()
    