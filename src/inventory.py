
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
    QVBoxLayout, QMessageBox
)
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "pos_system.db")

class FormularioInventario(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agregar Producto al Inventario")
        self.setGeometry(100, 100, 450, 550)

        self.label_nombre = QLabel("Nombre del producto:")
        self.input_nombre = QLineEdit()

        self.label_codigo = QLabel("Código de barras:")
        self.input_codigo = QLineEdit()

        self.label_cantidad = QLabel("Cantidad:")
        self.input_cantidad = QLineEdit()

        self.label_precio = QLabel("Precio unitario de venta:")
        self.input_precio = QLineEdit()

        self.label_unidad = QLabel("Unidad de venta:")
        self.combo_unidad = QComboBox()
        self.combo_unidad.addItems([
            "pieza", "kilo", "litro", "bolsa", "bulto", "caja", "garrafón", "otros"
        ])

        self.label_equivalente = QLabel("Equivalente por unidad (pzas/kg/L):")
        self.input_equivalente = QLineEdit()

        self.label_volumen = QLabel("Volumen por unidad (ml o L):")
        self.input_volumen = QLineEdit()

        self.label_envase = QLabel("Tipo de envase:")
        self.combo_envase = QComboBox()
        self.combo_envase.addItems(["no aplica", "retornable", "desechable"])

        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.clicked.connect(self.guardar_producto)

        layout = QVBoxLayout()
        layout.addWidget(self.label_nombre)
        layout.addWidget(self.input_nombre)
        layout.addWidget(self.label_codigo)
        layout.addWidget(self.input_codigo)
        layout.addWidget(self.label_cantidad)
        layout.addWidget(self.input_cantidad)
        layout.addWidget(self.label_precio)
        layout.addWidget(self.input_precio)
        layout.addWidget(self.label_unidad)
        layout.addWidget(self.combo_unidad)
        layout.addWidget(self.label_equivalente)
        layout.addWidget(self.input_equivalente)
        layout.addWidget(self.label_volumen)
        layout.addWidget(self.input_volumen)
        layout.addWidget(self.label_envase)
        layout.addWidget(self.combo_envase)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def guardar_producto(self):
        nombre = self.input_nombre.text().strip()
        codigo = self.input_codigo.text().strip()
        try:
            cantidad = float(self.input_cantidad.text())
            precio = float(self.input_precio.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "Cantidad y precio deben ser numéricos.")
            return

        unidad = self.combo_unidad.currentText()
        equivalente = self.input_equivalente.text().strip()
        volumen = self.input_volumen.text().strip()
        envase = self.combo_envase.currentText()

        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre no puede estar vacío.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        for columna in ["unidad TEXT", "equivalente TEXT", "volumen TEXT", "envase TEXT", "codigo_barras TEXT"]:
            try:
                cursor.execute(f"ALTER TABLE inventario ADD COLUMN {columna}")
            except:
                pass

        cursor.execute(
            "INSERT INTO inventario (nombre, codigo_barras, cantidad, precio, unidad, equivalente, volumen, envase) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (nombre, codigo, cantidad, precio, unidad, equivalente, volumen, envase)
        )
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Éxito", "Producto agregado correctamente.")
        self.input_nombre.clear()
        self.input_codigo.clear()
        self.input_cantidad.clear()
        self.input_precio.clear()
        self.input_equivalente.clear()
        self.input_volumen.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormularioInventario()
    window.show()
    sys.exit(app.exec_())
