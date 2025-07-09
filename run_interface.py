#!/usr/bin/env python3
"""
Ejecutor de la interfaz de gestión de PH
"""

import tkinter as tk
from ph_interface import PHInterface

def main():
    root = tk.Tk()
    app = PHInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main() 