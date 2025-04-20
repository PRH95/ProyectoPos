
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
)
from PyQt5.QtCore import Qt
import subprocess
import os

class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema POS - Abarrotes Rocha Hernández")
        self.showFullScreen()

        layout = QVBoxLayout()

        titulo = QLabel("🛒 Abarrotes Rocha Hernández")
        titulo.setStyleSheet("font-size: 32px; font-weight: bold; color: #2c3e50;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        self.btn_inventario = QPushButton("➕ Agregar Producto")
        self.btn_inventario.setStyleSheet("font-size: 18px; padding: 10px;")
        self.btn_inventario.clicked.connect(lambda: self.abrir_script("src/inventory.py"))
        layout.addWidget(self.btn_inventario)

        self.btn_ventas = QPushButton("💵 Registrar Venta")
        self.btn_ventas.setStyleSheet("font-size: 18px; padding: 10px;")
        self.btn_ventas.clicked.connect(lambda: self.abrir_script("src/sales.py"))
        layout.addWidget(self.btn_ventas)

        self.btn_reportes = QPushButton("📊 Ver Reportes")
        self.btn_reportes.setStyleSheet("font-size: 18px; padding: 10px;")
        self.btn_reportes.clicked.connect(lambda: self.abrir_script("src/reports.py"))
        layout.addWidget(self.btn_reportes)

        self.btn_salir = QPushButton("❌ Salir")
        self.btn_salir.setStyleSheet("font-size: 16px; padding: 8px;")
        self.btn_salir.clicked.connect(lambda: self.close())
        layout.addWidget(self.btn_salir)

        self.setLayout(layout)

    def abrir_script(self, ruta):
        ruta_absoluta = os.path.abspath(ruta)
        subprocess.Popen(["python3", ruta_absoluta])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MenuPrincipal()
    menu.show()
    sys.exit(app.exec_())
