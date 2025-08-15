import cv2
from screeninfo import get_monitors

class ExhibidorImagenes:
    def __init__(self):
        """
        Resolución predeterminada de 1280x720.
        """
        self.width = 1280
        self.height = 720


    def get_screen_resolution(self):
        """
        Obtiene la resolución de la pantalla más pequeña entre todos los monitores detectados.
        """
        monitors = get_monitors()
        if monitors:
            # Inicializar con la resolución del primer monitor
            self.width = monitors[0].width
            self.height = monitors[0].height
            
            # Encontrar la resolución más pequeña entre todos los monitores
            for monitor in monitors:
                if monitor.width < self.width:
                    self.width = monitor.width
                if monitor.height < self.height:
                    self.height = monitor.height

        return self.width, self.height

    def _adjust_window_size(self, image, scale_factor=0.90):
        """
        Ajusta el tamaño de la imagen para que se ajuste a la pantalla.
        Devuelve la imagen redimensionada y sus nuevas dimensiones.
        """
        # Obtener la resolución de la pantalla
        screen_width, screen_height = self.get_screen_resolution()
        
        # Verificar si la imagen es válida
        if image is None or len(image.shape) < 2:
            raise ValueError("La imagen no es válida o no tiene dimensiones suficientes.")
        
        # Obtener las dimensiones de la imagen
        img_height, img_width = image.shape[:2]
        
        # Calcular el factor de escala para ajustar la imagen a la pantalla
        scale_width = screen_width / img_width
        scale_height = screen_height / img_height
        scale = scale_factor * min(scale_width, scale_height)
        
        # Asegurarse de que la escala no sea mayor que 1.0 (no ampliar la imagen)
        scale = min(scale, 1.0)
        
        # Calcular las nuevas dimensiones de la imagen
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        return new_width, new_height

    def mostrar_imagen(self, image, window_name="Imagen", callBack=None):
        """
        Muestra la imagen en una ventana redimensionada.
        """
        new_width, new_height = self._adjust_window_size(image)

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, new_width, new_height)
        cv2.imshow(window_name, image)
        if callBack:
            cv2.setMouseCallback(window_name, callBack)
        cv2.waitKey()
        cv2.destroyAllWindows()
 