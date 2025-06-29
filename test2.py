import tkinter as tk
from tkinter import ttk, messagebox

ph_listado = []

class PHApp:
    def __init__(self, root):
        self.root = root # Ventana principal        
        self.root.geometry("450x800") #ancho x alto        
        self.root.title("PLANILLA DE PH")
        self.contador_unidades = 1 # Contador de unidades funcionales
        self.contador_padron = None  # Se inicia al guardar el primer PH
        self.poligonos_frames = [] # Lista para almacenar los frames de polígonos  

        # Notebook para las pestañas
        self.notebook = ttk.Notebook(root)
        # Empaquetar el notebook para que ocupe todo el espacio disponible     
        self.notebook.pack(fill="both", expand=True)
        # Crear pestaña de carga de datos y listado de PHs 
        self.tab_carga = tk.Frame(self.notebook)        
        self.tab_listado = tk.Frame(self.notebook)
        # Agregar las pestañas al notebook
        self.notebook.add(self.tab_carga, text="Carga de Datos")
        self.notebook.add(self.tab_listado, text="Listado")

        self._construir_pestana_carga()
        #self._construir_pestana_listado()
    
    def _construir_pestana_carga(self):        
        # Título de la pestaña de carga
        self.titulo_label = tk.Label(self.tab_carga, text=f"Datos de la unidad funcional N° {self.contador_unidades}", font=(None, 12))        
        self.titulo_label.pack(pady=(10, 10))

        self.form_frame = tk.Frame(self.tab_carga, bd=1, relief="ridge", padx=10, pady=10)
        self.form_frame.pack()

        self.dpto_entry = self._crear_input(self.form_frame, "Dpto:", 0)
        self.padron_entry = self._crear_input(self.form_frame, "Padrón:", 1)
        self.unidad_entry = self._crear_input(self.form_frame, "UF:", 2)
        self.sup_entry = self._crear_input(self.form_frame, "Sup. m2 UF:", 3)
        self.coef_entry = self._crear_input(self.form_frame, "Coef. ajuste:", 4)

        self.unidad_entry.insert(0, "1")

        self.poligonos_container = tk.Frame(self.tab_carga)
        self.poligonos_container.pack(pady=10)

        #tk.Button(self.tab_carga, text="Agregar Polígono", command=self.agregar_poligono).pack(pady=5)
        #tk.Button(self.tab_carga, text="Guardar PH", command=self.guardar_ph).pack(pady=5)

    def _crear_input(self, parent, label, row):
        tk.Label(parent, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(parent)
        entry.grid(row=row, column=1, padx=5, pady=2)
        return entry


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("450x800")
    app = PHApp(root)
    root.mainloop()
    #print(ph_listado)