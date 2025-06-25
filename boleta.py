from fpdf import FPDF
from datetime import datetime

class BoletaPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "BOLETA DE PEDIDO", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", 0, 0, "C")

    def generar_boleta(self, pedido, cliente, menu, ingredientes):
        self.add_page()
        self.set_font("Arial", "", 11)

        self.cell(0, 10, f"Fecha: {pedido.fecha.strftime('%Y-%m-%d %H:%M')}", ln=True)
        self.cell(0, 10, f"Cliente: {cliente.nombre} ({cliente.email})", ln=True)
        self.cell(0, 10, f"Menú: {menu.nombre_menu}", ln=True)
        self.multi_cell(0, 10, f"Descripción: {pedido.descripcion}")
        self.ln(5)

        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Ingredientes:", ln=True)
        self.set_font("Arial", "", 11)

        for ing in ingredientes:
            self.cell(0, 10, f"• {ing.nombre} - {ing.cantidad} {ing.unidad_de_medida}", ln=True)

        # Guardar archivo
        filename = f"boleta_{pedido.id}.pdf"
        self.output(filename)
        return filename
