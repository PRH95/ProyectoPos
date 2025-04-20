
import sys
from PyQt5.QtWidgets import (
    QPushButton,
    QApplication, QWidget, QLabel, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QTabWidget
)
import sqlite3
from src.pdf_report import generar_reporte_pdf, generar_reporte_inventario_pdf

class VentanaListados(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Listados de Inventario y Ventas")
        self.setGeometry(100, 100, 600, 400)

        self.tabs = QTabWidget()
        self.tab_inventario = QWidget()
        self.tab_ventas = QWidget()

        self.tabs.addTab(self.tab_inventario, "Inventario")
        self.tabs.addTab(self.tab_ventas, "Ventas")

        self.crear_tabla_inventario()
        self.crear_tabla_ventas()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.boton_pdf = QPushButton("Generar PDF de Ventas")
        self.boton_pdf.clicked.connect(self.exportar_pdf)
        layout.addWidget(self.boton_pdf)
        self.boton_pdf_inv = QPushButton("Generar PDF de Inventario")
        self.boton_pdf_inv.clicked.connect(self.exportar_pdf_inventario)
        layout.addWidget(self.boton_pdf_inv)


        self.setLayout(layout)

    def crear_tabla_inventario(self):
        layout = QVBoxLayout()
        tabla = QTableWidget()
        layout.addWidget(QLabel("Listado de Inventario"))
        layout.addWidget(tabla)

        conn = sqlite3.connect("database/pos_system.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, cantidad, precio FROM inventario")
        datos = cursor.fetchall()
        conn.close()

        tabla.setColumnCount(3)
        tabla.setHorizontalHeaderLabels(["Producto", "Cantidad", "Precio"])
        tabla.setRowCount(len(datos))

        for row_idx, row_data in enumerate(datos):
            for col_idx, value in enumerate(row_data):
                tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        self.tab_inventario.setLayout(layout)

    def crear_tabla_ventas(self):
        layout = QVBoxLayout()
        tabla = QTableWidget()
        layout.addWidget(QLabel("Listado de Ventas"))
        layout.addWidget(tabla)

        conn = sqlite3.connect("database/pos_system.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ventas.id, clientes.nombre, ventas.fecha, ventas.total
            FROM ventas
            JOIN clientes ON ventas.cliente_id = clientes.id
        """)
        datos = cursor.fetchall()
        conn.close()

        tabla.setColumnCount(4)
        tabla.setHorizontalHeaderLabels(["ID Venta", "Cliente", "Fecha", "Total"])
        tabla.setRowCount(len(datos))

        for row_idx, row_data in enumerate(datos):
            for col_idx, value in enumerate(row_data):
                tabla.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        self.tab_ventas.setLayout(layout)


    def exportar_pdf(self):
        archivo = generar_reporte_pdf()
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Reporte Generado", f"Archivo guardado en:\n{archivo}")

    def exportar_pdf_inventario(self):
        archivo = generar_reporte_inventario_pdf()
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(self, "Reporte Generado", f"Archivo guardado en:\n{archivo}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaListados()
    ventana.show()
    sys.exit(app.exec_())
