
from fpdf import FPDF
import sqlite3
from datetime import datetime
import os

class ReportePDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Reporte de Ventas", 0, 1, "C")

    def generar_tabla(self, encabezados, datos):
        self.set_font("Arial", "B", 10)
        for encabezado in encabezados:
            self.cell(40, 10, encabezado, 1)
        self.ln()
        self.set_font("Arial", "", 10)
        for fila in datos:
            for item in fila:
                self.cell(40, 10, str(item), 1)
            self.ln()

def generar_reporte_pdf():
    conn = sqlite3.connect("database/pos_system.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ventas.id, clientes.nombre, ventas.fecha, ventas.total
        FROM ventas
        JOIN clientes ON ventas.cliente_id = clientes.id
    """)
    datos = cursor.fetchall()
    conn.close()

    encabezados = ["ID Venta", "Cliente", "Fecha", "Total"]
    pdf = ReportePDF()
    pdf.add_page()
    pdf.generar_tabla(encabezados, datos)

    if not os.path.exists("reports"):
        os.makedirs("reports")

    nombre_archivo = f"reports/reporte_ventas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(nombre_archivo)
    return nombre_archivo
