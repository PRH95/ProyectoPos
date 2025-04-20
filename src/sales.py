
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QDoubleSpinBox, QListWidget, QComboBox
)
from PyQt5.QtCore import Qt
import sqlite3
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "pos_system.db")

class VentanaPOS(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Punto de Venta - Abarrotes Rocha Hernández")
        self.setGeometry(100, 100, 1000, 600)
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.productos_vendidos = []

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("Buscar por nombre o código")
        self.input_busqueda.textChanged.connect(self.actualizar_sugerencias)

        self.lista_sugerencias = QListWidget()
        self.lista_sugerencias.itemClicked.connect(self.seleccionar_producto)

        self.input_cantidad = QDoubleSpinBox()
        self.input_cantidad.setMinimum(0.01)
        self.input_cantidad.setValue(1.00)
        self.input_cantidad.setDecimals(2)

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["pieza", "kilo", "litro", "bolsa", "producto"])

        self.btn_agregar = QPushButton("Agregar producto")
        self.btn_agregar.clicked.connect(self.agregar_producto_seleccionado)

        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("Producto:"))
        top_bar.addWidget(self.input_busqueda)
        top_bar.addWidget(QLabel("Cantidad:"))
        top_bar.addWidget(self.input_cantidad)
        top_bar.addWidget(QLabel("Tipo:"))
        top_bar.addWidget(self.combo_tipo)
        top_bar.addWidget(self.btn_agregar)

        layout.addLayout(top_bar)
        layout.addWidget(self.lista_sugerencias)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(9)
        self.tabla.setHorizontalHeaderLabels([
            "Código", "Artículo", "Unidad", "Volumen", "Volumen", "Cantidad", "Tipo", "Precio unitario", "Precio neto", "Importe"
        ])
        self.tabla.cellClicked.connect(self.seleccionar_fila_tabla)
        layout.addWidget(self.tabla)

        self.label_total = QLabel("Total: $0.00")
        layout.addWidget(self.label_total)

        self.btn_registrar = QPushButton("Registrar Venta")
        self.btn_registrar.clicked.connect(self.registrar_venta)

        self.btn_eliminar = QPushButton("Eliminar producto seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_producto_seleccionado)
        layout.addWidget(self.btn_eliminar)

        layout.addWidget(self.btn_registrar)

        self.producto_seleccionado = None
        self.indice_fila_seleccionada = None

    def actualizar_sugerencias(self):
        texto = self.input_busqueda.text().strip().lower()
        self.lista_sugerencias.clear()

        if not texto:
            return

        self.cursor.execute("""
            SELECT id, nombre, unidad, codigo_barras, volumen
            FROM inventario
            WHERE LOWER(nombre) LIKE ? OR codigo_barras LIKE ? OR id LIKE ?
            LIMIT 10
        """, (f"%{texto}%", f"%{texto}%", f"%{texto}%"))
        resultados = self.cursor.fetchall()

        for r in resultados:
            item_texto = f"{r[0]} - {r[1]} ({r[2]}){f' - {r[4]}' if r[4] else ''}"
            if r[3]:
                item_texto += f" | CB: {r[3]}"
            self.lista_sugerencias.addItem(item_texto)
            self.lista_sugerencias.setProperty(str(r[0]), r)

    def seleccionar_producto(self, item):
        texto = item.text()
        id_producto = texto.split(" - ")[0]
        self.cursor.execute("SELECT id, nombre, precio, unidad, volumen FROM inventario WHERE id = ?", (id_producto,))
        
        producto = self.cursor.fetchone()
        self.producto_seleccionado = producto
        nombre = producto[1]
        volumen = producto[4] if len(producto) > 4 and producto[4] else ""
        if volumen:
            self.input_busqueda.setText(f"{nombre} ({volumen})")
        else:
            self.input_busqueda.setText(nombre)
        self.lista_sugerencias.clear()


    def agregar_producto_seleccionado(self):
        if not self.producto_seleccionado:
            QMessageBox.warning(self, "Error", "Selecciona un producto de la lista.")
            return

        cantidad = float(self.input_cantidad.value())
        tipo = self.combo_tipo.currentText()
        producto = self.producto_seleccionado
        precio_unitario = producto[2]
        importe = round(precio_unitario * cantidad, 2)

        self.productos_vendidos.append({
            "id": producto[0],
            "nombre": producto[1],
            "unidad": producto[3],
            "tipo": tipo,
            "cantidad": cantidad,
            "precio": precio_unitario,
            "neto": precio_unitario,
            "volumen": producto[4] if len(producto) > 4 else "", "volumen": producto[4] if len(producto) > 4 else "", "importe": importe
        })

        self.actualizar_tabla()
        self.input_busqueda.clear()
        self.lista_sugerencias.clear()
        self.producto_seleccionado = None

    def actualizar_tabla(self):
        self.tabla.setRowCount(len(self.productos_vendidos))
        total = 0

        for i, p in enumerate(self.productos_vendidos):
            self.tabla.setItem(i, 0, QTableWidgetItem(str(p["id"])))
            self.tabla.setItem(i, 1, QTableWidgetItem(p["nombre"]))
            self.tabla.setItem(i, 2, QTableWidgetItem(p["unidad"]))
            self.tabla.setItem(i, 3, QTableWidgetItem(p.get("volumen", "")))
            self.tabla.setItem(i, 4, QTableWidgetItem(f"{p['cantidad']}"))
            self.tabla.setItem(i, 4, QTableWidgetItem(p["tipo"]))
            self.tabla.setItem(i, 5, QTableWidgetItem(f"${p['precio']:.2f}"))
            self.tabla.setItem(i, 6, QTableWidgetItem(f"${p['neto']:.2f}"))
            self.tabla.setItem(i, 7, QTableWidgetItem(f"${p['importe']:.2f}"))
            total += p["importe"]

        self.label_total.setText(f"Total: ${total:.2f}")

    def seleccionar_fila_tabla(self, row, column):
        self.indice_fila_seleccionada = row
        producto = self.productos_vendidos[row]
        QMessageBox.information(self, "Producto seleccionado",
                                f"{producto['nombre']} ({producto['cantidad']} {producto['tipo']})")

    
    def eliminar_producto_seleccionado(self):
        if self.indice_fila_seleccionada is not None and 0 <= self.indice_fila_seleccionada < len(self.productos_vendidos):
            producto = self.productos_vendidos.pop(self.indice_fila_seleccionada)
            QMessageBox.information(self, "Eliminado", f"Se eliminó: {producto['nombre']}")
            self.actualizar_tabla()
            self.indice_fila_seleccionada = None
        else:
            QMessageBox.warning(self, "Error", "Selecciona un producto válido.")

    def registrar_venta(self):
        if not self.productos_vendidos:
            QMessageBox.warning(self, "Error", "No hay productos en la venta.")
            return

        total = sum(p["importe"] for p in self.productos_vendidos)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("INSERT INTO ventas (cliente_id, fecha, total) VALUES (?, ?, ?)",
                            (1, fecha, total))

        for item in self.productos_vendidos:
            self.cursor.execute("UPDATE inventario SET cantidad = cantidad - ? WHERE id = ?",
                                (item["cantidad"], item["id"]))

        self.conn.commit()
        QMessageBox.information(self, "Éxito", f"Venta registrada. Total: ${total:.2f}")
        self.productos_vendidos = []
        self.actualizar_tabla()
        self.input_busqueda.clear()
        self.input_cantidad.setValue(1.00)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPOS()
    ventana.show()
    sys.exit(app.exec_())
