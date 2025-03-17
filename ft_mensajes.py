import tkinter as tk
from tkinter import messagebox


class Mensaje:
    def __init__(self):
        """Crea una ventana raíz oculta solo para gestionar los cuadros de mensaje."""
        self.root = tk.Tk()
        self.root.withdraw()  # Oculta la ventana principal

    def error(self, mensaje):
        messagebox.showerror("Error", mensaje)

    def info(self, mensaje):
         messagebox.showinfo("Información", mensaje)

    def salida(self):
        messagebox.showinfo("Salir", "Saliendo del programa...")

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

