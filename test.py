import tkinter as tk
from tkinter import simpledialog, messagebox

ph_listado = []

class PHApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario PH")

        # Lista para polígonos temporales y componentes
        self.poligonos = []

        # --- Campos PH ---
        tk.Label(root, text="Padrón").grid(row=0, column=0)
        self.padron_entry = tk.Entry(root)
        self.padron_entry.grid(row=0, column=1)

        tk.Label(root, text="Unidad").grid(row=1, column=0)
        self.unidad_entry = tk.Entry(root)
        self.unidad_entry.grid(row=1, column=1)

        tk.Label(root, text="Sup m2").grid(row=2, column=0)
        self.sup_entry = tk.Entry(root)
        self.sup_entry.grid(row=2, column=1)

        tk.Label(root, text="Coef Ajuste").grid(row=3, column=0)
        self.coef_entry = tk.Entry(root)
        self.coef_entry.grid(row=3, column=1)

        # Botón para agregar polígonos
        self.agregar_poligono_btn = tk.Button(root, text="Agregar Polígono", command=self.agregar_poligono)
        self.agregar_poligono_btn.grid(row=4, column=0, columnspan=2, pady=5)

        # Botón para guardar PH completo
        self.guardar_ph_btn = tk.Button(root, text="Guardar PH", command=self.guardar_ph)
        self.guardar_ph_btn.grid(row=5, column=0, columnspan=2, pady=5)

        # Label para mostrar polígonos agregados
        self.poligonos_label = tk.Label(root, text="Polígonos agregados: 0")
        self.poligonos_label.grid(row=6, column=0, columnspan=2)

    def agregar_poligono(self):
        # Pedir código de polígono
        codigo = simpledialog.askstring("Polígono", "Ingrese código del polígono (ej: 00-01):", parent=self.root)
        if not codigo:
            return

        componentes = []
        while True:
            agregar = messagebox.askyesno("Agregar componente", "¿Desea agregar un componente al polígono?")
            if not agregar:
                break

            concepto = simpledialog.askstring("Componente", "Concepto:", parent=self.root)
            if not concepto:
                break
            try:
                m2 = float(simpledialog.askstring("Componente", "Metros cuadrados (m2):", parent=self.root))
                valor_m2 = float(simpledialog.askstring("Componente", "Valor por m2:", parent=self.root))
                coef_antig = float(simpledialog.askstring("Componente", "Coeficiente antigüedad:", parent=self.root))
            except (TypeError, ValueError):
                messagebox.showerror("Error", "Valores numéricos inválidos. Intente de nuevo.")
                continue

            comp = {
                "concepto": concepto,
                "m2": m2,
                "valor_m2": valor_m2,
                "coef_antig": coef_antig
            }
            componentes.append(comp)

        if componentes:
            self.poligonos.append({"poligono": codigo, "componentes": componentes})
            self.poligonos_label.config(text=f"Polígonos agregados: {len(self.poligonos)}")

    def guardar_ph(self):
        padron = self.padron_entry.get()
        try:
            unidad = int(self.unidad_entry.get())
            sup_m2 = float(self.sup_entry.get())
            coef_ajus = float(self.coef_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Unidad, Sup m2 y Coef Ajuste deben ser numéricos.")
            return

        if not padron:
            messagebox.showerror("Error", "El padrón es obligatorio.")
            return

        if not self.poligonos:
            messagebox.showerror("Error", "Debe agregar al menos un polígono.")
            return

        ph = {
            "padron": padron,
            "unidad": unidad,
            "sup_m2": sup_m2,
            "coef_ajus": coef_ajus,
            "poligonos": self.poligonos
        }
        ph_listado.append(ph)

        messagebox.showinfo("Guardado", f"PH guardado correctamente.\nTotal PH: {len(ph_listado)}")

        # Limpiar entradas para nuevo PH
        self.padron_entry.delete(0, tk.END)
        self.unidad_entry.delete(0, tk.END)
        self.sup_entry.delete(0, tk.END)
        self.coef_entry.delete(0, tk.END)
        self.poligonos = []
        self.poligonos_label.config(text="Polígonos agregados: 0")

        print("Estado actual ph_listado:")
        for p in ph_listado:
            print(p)


if __name__ == "__main__":
    root = tk.Tk()
    app = PHApp(root)
    root.mainloop()
