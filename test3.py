import tkinter as tk

def crear_label(contenedor, texto, fila, columna):
    label = tk.Label(contenedor, text=texto)
    label.grid(row=fila, column=columna, padx=5, pady=5, sticky="e")
    return label

def crear_input(contenedor, fila, columna):
    entrada = tk.Entry(contenedor)
    entrada.grid(row=fila, column=columna, padx=5, pady=5, sticky="w")
    return entrada

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Formulario modular")

# Crear Frame como contenedor
frame = tk.Frame(ventana)
frame.pack(padx=10, pady=10)

# Usar las funciones para crear widgets
crear_label(frame, "Nombre:", 0, 0)
entrada_nombre = crear_input(frame, 0, 1)

crear_label(frame, "Apellido:", 1, 0)
entrada_apellido = crear_input(frame, 1, 1)

crear_label(frame, "Email:", 2, 0)
entrada_email = crear_input(frame, 2, 1)

ventana.mainloop()
