class Mensaje:
	def __init__(self):
		pass

	def error(self, mensaje):
		print (f'\n❌ ERROR: {mensaje}')
	
	def info(self, mensaje):
		print (f'{mensaje}')
	
	def salida(self):
		print ('\n👋 Saliendo del programa...\n')

# Instanciar la clase Mensaje
msg = Mensaje()

if __name__ == '__main__':
	msg.error('Error de conexión')
	msg.info('Conexión exitosa')
