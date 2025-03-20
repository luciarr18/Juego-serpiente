# Importo las librerías que me hacen falta
from tkinter import * #Interfaz gráfica en python
import random #Para la aparición de la comida

# Empiezo definiendo las dimensiones del juego
WIDTH = 500     # Anchura
HEIGHT = 500    # Altura
SPEED = 200     # Velocidad de la serpiente
SPACE_SIZE = 20 # Espacio de la pantalla
BODY_SIZE = 2   # Tamaño inicial de la serpiente, conforme empieza el juego
FOOD = '#FFFFFF' # Color para la comida
SNAKE = '#00FF00' # Color para la serpiente
BACKGROUND = '#000000' # Color para el fondo

# Creo la serpiente haciendo su clase
class Snake:

    # Defino el método inicializador para la clase
    def __init__(self, canvas):
        self.canvas = canvas  # Guardo el canvas dentro de la clase
        self.body_size = BODY_SIZE 
        self.coordinates = []  # Lista de coordenadas (x, y)
        self.squares = []  # Lista con las partes de la serpiente 

        for i in range(0, BODY_SIZE): # Este bucle hace que los cuadraditos que mida la serpiente estén unidos. 
            self.coordinates.append([0, 0])  # Inicialmente, la serpiente está en (0,0)

        for x, y in self.coordinates:
            square = self.canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE, tag='snake'
            )
            self.squares.append(square)


# Función principal para ejecutar el juego
def main():
    global canvas

    root = Tk()
    root.title("Juego de la serpiente")
    root.resizable(False, False)

    canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg=BACKGROUND)
    canvas.pack()

    snake = Snake(canvas)  # Paso el canvas a la clase Snake

    root.mainloop()

#Para iniciar la función main que hace que ejecute el juego. 
if __name__ == "__main__": 
    main() 