import tkinter as tk
from tkinter import ttk, messagebox

class PoligonoFrame(tk.LabelFrame):
    """
    Un widget que encapsula toda la lógica y los componentes de un único polígono.
    Hereda de tk.LabelFrame para ser visualmente un grupo.
    """
    def __init__(self, parent, on_delete):
        super().__init__(parent, padx=10, pady=5, text="Polígono")
        self.on_delete = on_delete
        self.filas_componentes = []
        self._crear_interfaz()

    def _crear_interfaz(self):
        tk.Label(self, text="Código:").grid(row=0, column=0, sticky="e")
        self.codigo_entry = tk.Entry(self)
        self.codigo_entry.grid(row=0, column=1, padx=5)
        self.codigo_entry.focus_set()

        self.componentes_frame = tk.Frame(self)
        self.componentes_frame.grid(row=1, column=0, columnspan=4, pady=5)

        header = ["Concepto", "m2", "Valor m2", "Coef. antig.", "Acción"]
        for i, h in enumerate(header):
            tk.Label(self.componentes_frame, text=h, font=("Helvetica", 10, "bold")).grid(row=0, column=i, padx=5)

        tk.Button(self, text="Agregar Concepto", command=self._agregar_fila).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(self, text="Eliminar Polígono", fg="red", command=self._eliminar_poligono).grid(row=2, column=2, pady=5)
        
        self._agregar_fila() # Iniciar con una fila por defecto

    def _agregar_fila(self):
        row_index = len(self.filas_componentes) + 1
        
        concepto = ttk.Combobox(self.componentes_frame, values=["Cubierta", "Semicub.", "Negocio"], state="readonly", width=12)
        concepto.set("Cubierta")
        m2 = tk.Entry(self.componentes_frame, width=8)
        valor = tk.Entry(self.componentes_frame, width=8)
        coef = tk.Entry(self.componentes_frame, width=8)
        
        eliminar_btn = tk.Button(self.componentes_frame, text="X", fg="red", command=lambda r=row_index: self._eliminar_fila(r))

        concepto.grid(row=row_index, column=0, padx=5, pady=2)
        m2.grid(row=row_index, column=1)
        valor.grid(row=row_index, column=2)
        coef.grid(row=row_index, column=3)
        eliminar_btn.grid(row=row_index, column=4)

        fila_widgets = (concepto, m2, valor, coef, eliminar_btn)
        self.filas_componentes.append(fila_widgets)
        m2.focus_set()

    def _eliminar_fila(self, row_to_delete):
        # El índice en la lista es row_to_delete - 1
        idx_to_delete = row_to_delete - 1
        
        if idx_to_delete < 0 or idx_to_delete >= len(self.filas_componentes):
            return

        # Eliminar widgets de la GUI
        for widget in self.filas_componentes[idx_to_delete]:
            widget.destroy()
        
        # Eliminar de la lista
        self.filas_componentes.pop(idx_to_delete)

        # Re-dibujar las filas restantes para que no queden huecos
        for i, fila in enumerate(self.filas_componentes):
            row_new = i + 1
            for col, widget in enumerate(fila):
                widget.grid(row=row_new, column=col)
            # Actualizar el comando del botón de eliminar para que apunte a la nueva fila
            fila[4].config(command=lambda r=row_new: self._eliminar_fila(r))

    def _eliminar_poligono(self):
        self.on_delete(self)

    def get_data(self):
        """
        Valida y recopila los datos de este polígono y los devuelve como un diccionario.
        Lanza ValueError si hay un error de validación.
        """
        codigo = self.codigo_entry.get().strip()
        if not codigo:
            raise ValueError("Todos los polígonos deben tener un código.")

        componentes_data = []
        for concepto_e, m2_e, valor_e, coef_e, _ in self.filas_componentes:
            try:
                concepto = concepto_e.get()
                m2 = float(m2_e.get())
                valor_m2 = float(valor_e.get())
                coef_antig = float(coef_e.get())
                componentes_data.append({
                    "concepto": concepto, "m2": m2, "valor_m2": valor_m2, "coef_antig": coef_antig
                })
            except (ValueError, tk.TclError):
                # Captura error si el campo está vacío o no es un número
                raise ValueError(f"Datos numéricos inválidos en el polígono '{codigo}'. Revise todos los campos.")

        if not componentes_data:
            raise ValueError(f"El polígono '{codigo}' no tiene componentes.")

        return {"poligono": codigo, "componentes": componentes_data}


class PHApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("550x800")
        self.root.title("PLANILLA DE PH (Versión Mejorada)")
        
        # --- Estado encapsulado dentro de la clase ---
        self.ph_listado = []
        self.poligonos_widgets = []
        self.contador_unidades = 1
        self.ultimo_dpto = ""

        self._setup_ui()

    def _setup_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_carga = tk.Frame(self.notebook)
        self.tab_listado = tk.Frame(self.notebook)
        self.notebook.add(self.tab_carga, text="Carga de Datos")
        self.notebook.add(self.tab_listado, text="Listado de PHs")

        self._construir_pestana_carga()
        self._construir_pestana_listado()

    def _construir_pestana_carga(self):
        main_frame = tk.Frame(self.tab_carga)
        main_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(main_frame, text="Carga de Unidades Funcionales", font=("Helvetica", 16, "bold")).pack(pady=(10, 5))
        self.subtitulo_label = tk.Label(main_frame, text=f"Datos de la unidad funcional N° {self.contador_unidades}", font=("Helvetica", 12))
        self.subtitulo_label.pack(pady=(0, 10))

        form_frame = tk.Frame(main_frame)
        form_frame.pack()

        self.dpto_entry = self._crear_input(form_frame, "Dpto:", 0)
        self.padron_entry = self._crear_input(form_frame, "Padrón:", 1)
        self.unidad_entry = self._crear_input(form_frame, "UF:", 2)
        self.sup_entry = self._crear_input(form_frame, "Sup. m2 UF:", 3)
        self.coef_entry = self._crear_input(form_frame, "Coef. ajuste:", 4)
        self.unidad_entry.insert(0, "1")

        # Contenedor para los polígonos que permite scroll
        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.poligonos_container = tk.Frame(canvas)
        
        self.poligonos_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.poligonos_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, pady=10)
        scrollbar.pack(side="right", fill="y")

        # Botones de acción
        action_frame = tk.Frame(self.tab_carga)
        action_frame.pack(pady=10)
        tk.Button(action_frame, text="Agregar Polígono", command=self.agregar_poligono).pack(side="left", padx=5)
        tk.Button(action_frame, text="Guardar PH", command=self.guardar_ph, font=("Helvetica", 10, "bold")).pack(side="left", padx=5)

    def _crear_input(self, parent, label, row):
        tk.Label(parent, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(parent)
        entry.grid(row=row, column=1, padx=5, pady=2)
        return entry

    def agregar_poligono(self):
        poligono_widget = PoligonoFrame(self.poligonos_container, on_delete=self._eliminar_poligono_widget)
        poligono_widget.pack(pady=10, padx=5, fill="x", expand=True)
        self.poligonos_widgets.append(poligono_widget)

    def _eliminar_poligono_widget(self, widget_a_eliminar):
        widget_a_eliminar.destroy()
        self.poligonos_widgets.remove(widget_a_eliminar)

    def guardar_ph(self):
        dpto = self.dpto_entry.get().strip()
        padron_val = self.padron_entry.get().strip()

        if not dpto or not padron_val:
            messagebox.showerror("Error de Validación", "Los campos 'Dpto' y 'Padrón' son obligatorios.")
            return

        try:
            unidad = int(self.unidad_entry.get())
            sup_m2 = float(self.sup_entry.get())
            coef_ajus = float(self.coef_entry.get())
        except ValueError:
            messagebox.showerror("Error de Validación", "'Unidad', 'Sup m2' y 'Coef Ajuste' deben ser valores numéricos.")
            return

        if not self.poligonos_widgets:
            messagebox.showerror("Error de Validación", "Debe agregar al menos un polígono.")
            return

        # --- Lógica de datos simplificada ---
        poligonos_data = []
        try:
            for poligono_widget in self.poligonos_widgets:
                poligonos_data.append(poligono_widget.get_data())
        except ValueError as e:
            messagebox.showerror("Error en Polígono", str(e))
            return

        # --- Si todo es válido, se crea el diccionario final ---
        padron_final = f"{dpto}-{padron_val}"
        ph = {
            "padron": padron_final, "unidad": unidad, "sup_m2": sup_m2,
            "coef_ajus": coef_ajus, "poligonos": poligonos_data
        }

        self.ph_listado.append(ph)
        self._agregar_a_listado_treeview(ph)
        self._resetear_formulario(dpto, padron_val)
        
        messagebox.showinfo("Guardado", f"PH guardado correctamente. Total de PHs: {len(self.ph_listado)}")

    def _resetear_formulario(self, dpto_guardado, padron_guardado):
        """Limpia el formulario para la siguiente carga."""
        self.ultimo_dpto = dpto_guardado # Guardar el dpto para la siguiente carga
        
        # Incrementar unidad
        try:
            nueva_unidad = int(self.unidad_entry.get()) + 1
            self.unidad_entry.delete(0, tk.END)
            self.unidad_entry.insert(0, str(nueva_unidad))
        except ValueError:
            self.unidad_entry.delete(0, tk.END)

        # Incrementar padrón si es numérico
        try:
            nuevo_padron = int(padron_guardado) + 1
            self.padron_entry.delete(0, tk.END)
            self.padron_entry.insert(0, str(nuevo_padron))
        except ValueError:
            # Si no es numérico, simplemente lo limpia
            self.padron_entry.delete(0, tk.END)

        # Limpiar polígonos
        for widget in self.poligonos_widgets:
            widget.destroy()
        self.poligonos_widgets = []

        # Actualizar título y foco
        self.contador_unidades += 1
        self.subtitulo_label.config(text=f"Datos de la unidad funcional N° {self.contador_unidades}")
        self.padron_entry.focus_set()

    def _construir_pestana_listado(self):
        self.tree = ttk.Treeview(self.tab_listado, columns=("padron", "uf", "sup"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.heading("padron", text="Padrón")
        self.tree.heading("uf", text="UF")
        self.tree.heading("sup", text="Superficie (m2)")
        
        self.tree.column("padron", width=150)
        self.tree.column("uf", width=50, anchor="center")
        self.tree.column("sup", width=100, anchor="e")

        # Evento para mostrar detalles al seleccionar
        self.tree.bind("<<TreeviewSelect>>", self._mostrar_detalles)
        
        # Frame para mostrar los detalles
        self.detalles_frame = tk.LabelFrame(self.tab_listado, text="Detalles del PH seleccionado", padx=10, pady=10)
        self.detalles_frame.pack(fill="x", expand=True, padx=10, pady=5)
        self.detalles_label = tk.Label(self.detalles_frame, text="Seleccione un PH de la lista para ver sus detalles.", justify="left")
        self.detalles_label.pack(anchor="w")

    def _agregar_a_listado_treeview(self, ph):
        # El 'iid' es un identificador único, usamos el índice en la lista
        item_id = len(self.ph_listado) - 1
        self.tree.insert('', 'end', iid=item_id, values=(ph['padron'], ph['unidad'], ph['sup_m2']))

    def _mostrar_detalles(self, event):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        
        item_id = int(seleccion[0])
        ph = self.ph_listado[item_id]
        
        texto_detalles = f"Padrón: {ph['padron']}\n"
        texto_detalles += f"Unidad Funcional: {ph['unidad']}\n"
        texto_detalles += f"Superficie: {ph['sup_m2']} m²\n"
        texto_detalles += f"Coeficiente de Ajuste: {ph['coef_ajus']}\n\n"
        texto_detalles += "Polígonos:\n"

        for pol in ph["poligonos"]:
            texto_detalles += f"  - Polígono {pol['poligono']}:\n"
            for comp in pol["componentes"]:
                texto_detalles += f"    - {comp['concepto']}: {comp['m2']}m² @ ${comp['valor_m2']}/m² (Coef: {comp['coef_antig']})\n"
        
        self.detalles_label.config(text=texto_detalles)


if __name__ == "__main__":
    root = tk.Tk()
    app = PHApp(root)
    root.mainloop()
    
    # Al cerrar la ventana, imprime la lista de PHs (ahora desde la instancia de la app)
    print("--- Datos Finales Recopilados ---")
    import json
    print(json.dumps(app.ph_listado, indent=2))



"""
EL PROMPT QUE HICE EN GEMINI

 ¡Listo! He creado el archivo test_ia.py con el código refactorizado.

  ¿Qué ha cambiado y por qué?


   1. Clase `PoligonoFrame`:
       * Ahora existe una clase PoligonoFrame que hereda de tk.LabelFrame.
       * Beneficio: Esta clase maneja todo lo relacionado con un polígono: su
         código, sus componentes (conceptos, m2, etc.), y los botones para
         agregar/eliminar filas. La clase principal (PHApp) ya no tiene que
         preocuparse por los detalles internos de cada polígono.


   2. Encapsulamiento (`self.ph_listado`):
       * La lista ph_listado ya no es una variable global. Ahora es self.ph_listado,
         una propiedad de la instancia de PHApp.
       * Beneficio: Esto hace que la clase PHApp sea autocontenida y reutilizable.
         Toda la información que necesita está dentro de ella.


   3. Lógica de Datos Limpia (`get_data`):
       * La clase PoligonoFrame tiene un método get_data(). Cuando PHApp necesita
         guardar, simplemente llama a este método en cada uno de sus polígonos.
       * Beneficio: Si en el futuro cambias cómo se ven los campos de un polígono
         (la UI), solo necesitas actualizar la clase PoligonoFrame. El método
         guardar_ph de la clase principal no necesitará ningún cambio. El código es
         mucho más fácil de mantener.


   4. Mejoras en la Interfaz y Experiencia de Usuario:
       * He añadido un scrollbar al contenedor de polígonos. Si añades muchos,
         podrás desplazarte verticalmente.
       * La pestaña de "Listado" ahora muestra los detalles del PH que selecciones,
         lo cual es mucho más útil que el Treeview anterior.
       * Al guardar, el campo "Dpto" se mantiene, agilizando la carga de la
         siguiente unidad del mismo departamento.
       * La validación de errores es más específica, indicando qué polígono tiene el
         problema.


   5. Impresión Final:
       * Al cerrar la aplicación, ahora se imprime la lista de PHs en un formato JSON
          legible, lo que facilita la depuración y la visualización de los datos
         recopilados.

  Puedes ejecutar este nuevo script y verás que la funcionalidad es la misma, pero la
   estructura interna del código es mucho más robusta y profesional.

"""