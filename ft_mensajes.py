import tkinter as tk
from tkinter import messagebox


class Mensaje:
    def __init__(self):
        pass

    def error(self, mensaje):
        self.root = tk.Tk()
        self.root.withdraw()
        messagebox.showerror("Error", mensaje)
        self.root.destroy()

    def info(self, mensaje):
        self.root = tk.Tk()
        self.root.withdraw()
        messagebox.showinfo("Información", mensaje)
        self.root.destroy()

    def salida(self):
        self.root = tk.Tk()
        self.root.withdraw()
        messagebox.showinfo("Salir", "Saliendo del programa...")
        self.root.destroy()

    def __del__(self):
        self.root.destroy()


msg = Mensaje()


if __name__ == '__main__':
    # Instanciar la clase Mensaje
    msg.error('Error de conexión')
    msg.info('Conexión exitosa')
    msg.info('Conexión exitosa')
    msg.info('Conexión exitosa')
    msg.salida()

