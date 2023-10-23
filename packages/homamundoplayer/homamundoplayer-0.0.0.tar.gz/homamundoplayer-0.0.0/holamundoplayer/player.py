"""
Esta es el módulo que incluye la clase de reproductor de música
"""


class Player:
    """
    Esta clase crea un reproductor de música.
    """

    def play(self, song):
        """
        Reproduce la canción que recibió como parámetro.

        Parameters:
        song (str): Este es un sgring con el path de la canción a escuchar.

        Returns:
        int: devuelve 1 si se reproduce con exito, en caso contrario devuelve 0.
        """
        print("Reproducción canción")

    def stop(self):
        print("Stopping")
