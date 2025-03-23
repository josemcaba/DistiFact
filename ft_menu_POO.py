class Menu:
	def __init__(self, json):
		pass

	def error(self, mensaje):
		print (f'\n❌ ERROR: {mensaje}')
	
	def info(self, mensaje):
		print (f'{mensaje}')
	
	def salida(self):
		print ('\n👋 Saliendo del programa...\n')

# Instanciar la clase Mensaje
menu = Menu()

if __name__ == '__main__':
	print(menu)