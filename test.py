import tkinter as tk
from tkinter import ttk, messagebox

ph_listado = []

class PHApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PLANILLA DE PH")
        self.contador_unidades = 1
        self.contador_padron = None  # Se inicia al guardar el primer PH
        self.poligonos_frames = []

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_carga = tk.Frame(self.notebook)
        self.tab_listado = tk.Frame(self.notebook)
        self.notebook.add(self.tab_carga, text="Carga de Datos")
        self.notebook.add(self.tab_listado, text="Listado")

        self._construir_pestana_carga()
        self._construir_pestana_listado()

    def _construir_pestana_carga(self):
        tk.Label(self.tab_carga, text="Carga de Unidades Funcionales", font=("Helvetica", 16, "bold")).pack(pady=(10, 5))
        self.subtitulo_label = tk.Label(self.tab_carga, text=f"Datos de la unidad funcional N° {self.contador_unidades}", font=("Helvetica", 12))
        self.subtitulo_label.pack(pady=(0, 10))

        form_frame = tk.Frame(self.tab_carga)
        form_frame.pack()

        self.dpto_entry = self._crear_input(form_frame, "Dpto:", 0)
        self.padron_entry = self._crear_input(form_frame, "Padrón:", 1)
        self.unidad_entry = self._crear_input(form_frame, "UF:", 2)
        self.sup_entry = self._crear_input(form_frame, "Sup. m2 UF:", 3)
        self.coef_entry = self._crear_input(form_frame, "Coef. ajuste:", 4)

        self.unidad_entry.insert(0, "1")

        self.poligonos_container = tk.Frame(self.tab_carga)
        self.poligonos_container.pack(pady=10)

        tk.Button(self.tab_carga, text="Agregar Polígono", command=self.agregar_poligono).pack(pady=5)
        tk.Button(self.tab_carga, text="Guardar PH", command=self.guardar_ph).pack(pady=5)

    def _crear_input(self, parent, label, row):
        tk.Label(parent, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(parent)
        entry.grid(row=row, column=1, padx=5, pady=2)
        return entry

    def agregar_poligono(self):        
        frame = tk.LabelFrame(self.poligonos_container, padx=10, pady=5)
        frame.pack(pady=10, fill="x", expand=True)

        tk.Label(frame, text="Polígono:").grid(row=0, column=0, sticky="e")
        codigo_entry = tk.Entry(frame)
        codigo_entry.grid(row=0, column=1, padx=5)
        codigo_entry.focus_set()

        componentes_frame = tk.Frame(frame)
        componentes_frame.grid(row=1, column=0, columnspan=3, pady=5)

        header = ["Concepto", "m2", "Valor m2", "Coef. antig.", "Acción"]
        for i, h in enumerate(header):
            tk.Label(componentes_frame, text=h, font=("Helvetica", 10, "bold")).grid(row=0, column=i, padx=5)

        filas_componentes = []

        def agregar_fila():
            row = len(filas_componentes) + 1
            concepto = ttk.Combobox(
                componentes_frame,
                values=["Cubierta", "Semicub.", "Negocio"],
                state="readonly",
                width=12
            )
            concepto.set("Cubierta")
            m2 = tk.Entry(componentes_frame, width=8)
            valor = tk.Entry(componentes_frame, width=8)
            coef = tk.Entry(componentes_frame, width=8)
            eliminar_btn = tk.Button(componentes_frame, text="Eliminar", command=lambda: eliminar_fila(row))

            concepto.grid(row=row, column=0, padx=5, pady=2)
            m2.grid(row=row, column=1)
            valor.grid(row=row, column=2)
            coef.grid(row=row, column=3)
            eliminar_btn.grid(row=row, column=4)

            filas_componentes.append((concepto, m2, valor, coef, eliminar_btn))
            concepto.focus_set()
        
        def eliminar_fila(row_index):
            for widget in componentes_frame.grid_slaves(row=row_index):
                widget.destroy()
            filas_componentes.pop(row_index - 1)
            for idx, fila in enumerate(filas_componentes, start=1):
                for col, widget in enumerate(fila):
                    widget.grid(row=idx, column=col)

        tk.Button(frame, text="Agregar Concepto", command=agregar_fila).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(frame, text="Eliminar Polígono", fg="red", command=lambda: self.eliminar_poligono(frame)).grid(row=2, column=2, pady=5)

        self.poligonos_frames.append((frame, codigo_entry, filas_componentes, agregar_fila))

    def eliminar_poligono(self, frame):
        frame.destroy()
        self.poligonos_frames = [f for f in self.poligonos_frames if f[0] != frame]

    def guardar_ph(self):
        dpto = self.dpto_entry.get().strip()
        padron_val = self.padron_entry.get().strip()

        if not dpto or not padron_val:
            messagebox.showerror("Error", "Dpto y Padrón son obligatorios.")
            return

        try:
            unidad = int(self.unidad_entry.get())
            sup_m2 = float(self.sup_entry.get())
            coef_ajus = float(self.coef_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Unidad, Sup m2 y Coef Ajuste deben ser numéricos.")
            return

        if not self.poligonos_frames:
            messagebox.showerror("Error", "Debe agregar al menos un polígono.")
            return

        poligonos = []
        total_componentes = 0

        for frame, codigo_entry, filas_componentes, _ in self.poligonos_frames:
            codigo = codigo_entry.get().strip()
            if not codigo:
                messagebox.showerror("Error", "Todos los polígonos deben tener un código.")
                return

            componentes = []
            for concepto_e, m2_e, valor_e, coef_e, _ in filas_componentes:
                try:
                    concepto = concepto_e.get()
                    m2 = float(m2_e.get())
                    valor_m2 = float(valor_e.get())
                    coef_antig = float(coef_e.get())
                    componentes.append({
                        "concepto": concepto,
                        "m2": m2,
                        "valor_m2": valor_m2,
                        "coef_antig": coef_antig
                    })
                except ValueError:
                    messagebox.showerror("Error", f"Datos inválidos en polígono {codigo}.")
                    return

            if not componentes:
                messagebox.showerror("Error", f"El polígono {codigo} no tiene componentes.")
                return

            total_componentes += len(componentes)
            poligonos.append({"poligono": codigo, "componentes": componentes})

        padron_final = f"{dpto}-{padron_val}"
        ph = {
            "padron": padron_final,
            "unidad": unidad,
            "sup_m2": sup_m2,
            "coef_ajus": coef_ajus,
            "poligonos": poligonos
        }

        ph_listado.append(ph)
        self._agregar_a_listado(ph)

        self.unidad_entry.delete(0, tk.END)
        self.unidad_entry.insert(0, str(unidad + 1))

        try:
            padron_num = int(padron_val)
            self.contador_padron = padron_num + 1
            self.padron_entry.delete(0, tk.END)
            self.padron_entry.insert(0, str(self.contador_padron))
        except ValueError:
            self.padron_entry.delete(0, tk.END)

        for frame, *_ in self.poligonos_frames:
            frame.destroy()
        self.poligonos_frames = []

        self.contador_unidades += 1
        self.subtitulo_label.config(text=f"Datos de la unidad funcional N° {self.contador_unidades}")

        self.padron_entry.focus_set()
        messagebox.showinfo("Guardado", f"PH guardado correctamente. Total PH: {len(ph_listado)}")

    def _construir_pestana_listado(self):
        self.tree = ttk.Treeview(self.tab_listado)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.heading("#0", text="PHs y Detalles")

    def _agregar_a_listado(self, ph):
        ph_id = self.tree.insert('', 'end', text=f"{ph['padron']} | UF {ph['unidad']} | Sup: {ph['sup_m2']} m2")
        for pol in ph["poligonos"]:
            pol_id = self.tree.insert(ph_id, 'end', text=f"Polígono {pol['poligono']}")
            if "componentes" in pol:
                for comp in pol["componentes"]:
                    desc = f"{comp['concepto']} : {comp['m2']}m2 x ${comp['valor_m2']} x {comp['coef_antig']}"
                    self.tree.insert(pol_id, 'end', text=desc)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x800")
    app = PHApp(root)
    root.mainloop()
    print(ph_listado)
