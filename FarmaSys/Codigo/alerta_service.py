
from datetime import date, timedelta


class AlertaService:

    def __init__(
        self,
        stock_minimo=5,
        dias_alerta_vencimiento=30
    ):
        self.stock_minimo = stock_minimo
        self.dias_alerta_vencimiento = (
            dias_alerta_vencimiento
        )

    def analizar_lote(self, lote):

        alertas = []

        cantidad = int(lote["cantidad"])

        vencimiento = date.fromisoformat(
            lote["fecha_vencimiento"]
        )

        hoy = date.today()

        limite = hoy + timedelta(
            days=self.dias_alerta_vencimiento
        )

        # Alerta por cantidad
        if cantidad == 0:

            alertas.append("SIN STOCK")

        elif 0 < cantidad <= self.stock_minimo:

            alertas.append("STOCK BAJO")

        # Alerta por fecha de vencimiento
        if vencimiento < hoy:

            alertas.append("VENCIDO")

        elif hoy <= vencimiento <= limite:

            alertas.append("PRÓXIMO A VENCER")

        return alertas

    def generar_alertas(self, inventario):

        resultado = []

        for lote in inventario:

            estados = self.analizar_lote(lote)

            for estado in estados:

                resultado.append({
                    "numero_lote": lote["numero_lote"],
                    "medicamento": lote["medicamento"],
                    "cantidad": lote["cantidad"],
                    "fecha_vencimiento": (
                        lote["fecha_vencimiento"]
                    ),
                    "estado": estado
                })

        return resultado

    def obtener_resumen(self, alertas):

        resumen = {
            "STOCK BAJO": 0,
            "SIN STOCK": 0,
            "PRÓXIMO A VENCER": 0,
            "VENCIDO": 0
        }

        for alerta in alertas:

            estado = alerta["estado"]

            if estado in resumen:
                resumen[estado] += 1

        return resumen
