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


# Creo la clase comida 
class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.coordinates = []  # Lista para almacenar la coordenada de la comida
        self.square = None  # Inicialmente, la comida no tiene un rectángulo

        # Crear la comida en una posición aleatoria dentro de los límites de la pantalla
        self.randomize_position()
        
        # Crear el rectángulo que representa la comida en el canvas
        self.square = self.canvas.create_rectangle(
            self.coordinates[0], self.coordinates[1],
            self.coordinates[0] + SPACE_SIZE, self.coordinates[1] + SPACE_SIZE,
            fill=FOOD, tag="food"
        )

    # Método para colocar la comida en una posición aleatoria
    def randomize_position(self):
        # Genera una posición aleatoria para la comida dentro de los límites de la pantalla
        self.coordinates = [
            random.randint(0, (WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE,
            random.randint(0, (HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        ]



# Función para actualizar la posición de la serpiente
def next_turn(snake, food, direction, window, canvas):
    x, y = snake.coordinates[0]  # Obtener la coordenada actual de la cabeza de la serpiente

    # Actualizar la dirección de la serpiente
    if direction == "up":
        y -= SPACE_SIZE  # Si la dirección es "arriba", disminuye el valor de y
    elif direction == "down":
        y += SPACE_SIZE  # Si la dirección es "abajo", aumenta el valor de y
    elif direction == "left":
        x -= SPACE_SIZE  # Si la dirección es "izquierda", disminuye el valor de x
    elif direction == "right":
        x += SPACE_SIZE  # Si la dirección es "derecha", aumenta el valor de x

    snake.coordinates.insert(0, (x, y))  # Inserta la nueva coordenada de la cabeza de la serpiente

    # Crear el nuevo rectángulo en la cabeza de la serpiente
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE
    )
    snake.squares.insert(0, square)  # Añadir el rectángulo creado a la lista de partes de la serpiente


    # Verifica si la serpiente ha comido la comida
    if x == food.coordinates[0] and y == food.coordinates[1]:
        food = Food(canvas)  # Si ha comido, crear una nueva comida en una posición aleatoria
    else:
        # Si no ha comido, eliminar la cola de la serpiente
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])  # Eliminar el último rectángulo de la cola
        del snake.squares[-1]  # Eliminar el último rectángulo de la lista de partes de la serpiente

    # Verificar si la serpiente ha colisionado con los bordes o consigo misma
    if check_collisions(snake):
        game_over(canvas)  # Si hubo una colisión, terminar el juego
    else:
        # Continuar el movimiento de la serpiente en el siguiente ciclo
        window.after(SPEED, next_turn, snake, food, direction, canvas)  # Llamar a la función de nuevo después de un intervalo


# Función para cambiar la dirección de la serpiente
def change_direction(new_direction, direction):
    # Cambiar la dirección de la serpiente, pero evitando que vaya en dirección opuesta
    if new_direction == 'left' and direction != 'right':
        direction = new_direction  # Cambiar a la izquierda solo si no va a la derecha
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction  # Cambiar a la derecha solo si no va a la izquierda
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction  # Cambiar hacia arriba solo si no va hacia abajo
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction  # Cambiar hacia abajo solo si no va hacia arriba
    return direction  # Devolver la nueva dirección


# Función para enlazar las teclas con las direcciones
def bind_keys(direction, window):
    # Asociar las teclas de dirección con las funciones de cambio de dirección 
    window.bind('<Left>', lambda event: change_direction('left', direction))  # Tecla izquierda
    window.bind('<Right>', lambda event: change_direction('right', direction))  # Tecla derecha
    window.bind('<Up>', lambda event: change_direction('up', direction))  # Tecla arriba
    window.bind('<Down>', lambda event: change_direction('down', direction))  # Tecla abajo


# Función para verificar si ha ocurrido una colisión / Para que no se salga de los limites de la pantalla. 
def check_collisions(snake):
    x, y = snake.coordinates[0]  # Obtener las coordenadas de la cabeza

    # Verificar si la serpiente ha colisionado con los bordes del juego
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True  # Si la cabeza está fuera de los límites, retornar True (colisión)

    # Verificar si la serpiente ha colisionado consigo misma
    for body_part in snake.coordinates[1:]:  # Comprobar cada parte del cuerpo de la serpiente
        if x == body_part[0] and y == body_part[1]:  # Si la cabeza toca alguna parte de su cuerpo
            return True  # Retornar True si ha colisionado

    return False  # Si no hay colisión, retornar False


# Función para mostrar el mensaje de fin de juego
def game_over(canvas):
    canvas.delete(ALL)  # Eliminar todos los elementos del lienzo (serpiente, comida, etc.)
    canvas.create_text(
        canvas.winfo_width() / 2,  # Posicionar el mensaje en el centro del lienzo
        canvas.winfo_height() / 2,
        font=('consolas', 70),  # Configurar la fuente y el tamaño del texto
        text="GAME OVER", fill="red",  # Mostrar "GAME OVER" en rojo
        tag="gameover"  # Etiqueta para el mensaje de fin de juego
    )