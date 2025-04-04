# Importo las librerías que me hacen falta
from tkinter import * #Interfaz gráfica en python
import random #Para la aparición de la comida
import os  # Para manejar archivos

# Empiezo definiendo las dimensiones del juego
WIDTH = 500     # Anchura
HEIGHT = 500    # Altura
SPEED = 300     # Velocidad de la serpiente
SPACE_SIZE = 20 # Espacio de la pantalla
BODY_SIZE = 2   # Tamaño inicial de la serpiente, conforme empieza el juego
FOOD = '#FF0000' # Color para la comida
SNAKE = '#00FF00' # Color para la serpiente
BACKGROUND = '#000000' # Color para el fondo
SCORE_FILE = "highscore.txt"  # Archivo para guardar la mejor puntuación

 # Inicialización de la puntuación global
score = 0  # Puntuación inicial
high_score = 0
direction = "down"  # Dirección inicial de la serpiente 

# Cargar la mejor puntuación
def load_high_score():
    global high_score
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as file:
            try:
                high_score = int(file.read())
            except ValueError:
                high_score = 0

# Guardar la mejor puntuación
def save_high_score():
    global score, high_score
    if score > high_score:
        high_score = score
        with open(SCORE_FILE, "w") as file:
            file.write(str(high_score))

# Actualizar la puntuación en pantalla
def update_score(canvas, score):
    canvas.delete("score")
    canvas.create_text(
        300, 20, font=('consolas', 20),
        text=f"Puntuación: {score}  Mejor: {high_score}",
        fill="white", tag="score"
    )

#CREACIÓN DE CLASES:


# Creo la serpiente haciendo su clase
class Snake:

    # Defino el método inicializador para la clase
    def __init__(self, canvas):
        self.canvas = canvas  # Guardo el canvas dentro de la clase
        self.body_size = BODY_SIZE 
        self.coordinates = [[0, 0]] * BODY_SIZE  # Lista de coordenadas (x, y)
        self.squares = [
                self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE)
                for x, y in self.coordinates
            ]  


# Creo la clase comida 
class Food:
    def __init__(self, canvas, snake):
        self.canvas = canvas
        self.snake = snake # Para evitar que la comida aparezca sobre la serpiente
        self.coordinates = []  # Lista para almacenar la coordenada de la comida
        self.square = None  # Inicialmente, la comida no tiene un rectángulo
        self.food_image = PhotoImage(file="manzana.png")  # Cargar la imagen de la manzana

        # Crear la comida en una posición aleatoria dentro de los límites de la pantalla
        self.randomize_position()

    def randomize_position(self):
        while True:
            x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            if [x, y] not in self.snake.coordinates:
                self.coordinates = [x, y]
                if self.square:
                    # No es necesario usar coords con un rectángulo, solo con imágenes
                    self.canvas.coords(self.square, x + SPACE_SIZE / 2, y + SPACE_SIZE / 2)
                else:
                    # Colocamos la imagen en la posición (x + SPACE_SIZE / 2, y + SPACE_SIZE / 2)
                    self.square = self.canvas.create_image(x + SPACE_SIZE / 2, y + SPACE_SIZE / 2, image=self.food_image)
                break
            

# FUNCIONES: 

# FUNCIÓN para verificar si ha ocurrido una colisión / Para que no se salga de los limites de la pantalla. 
def check_collisions(snake):
    x, y = snake.coordinates[0]  # Obtener las coordenadas de la cabeza
    
    # Verificar si la serpiente ha colisionado con los bordes del juego
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        return True  # Si la cabeza está fuera de los límites, retornar True (colisión)
    
    if (x, y) in set(map(tuple, snake.coordinates[1:])):  # Si la cabeza toca alguna parte de su cuerpo
        return True  # Retornar True si ha colisionado
    
    return False  # Si no hay colisión, retornar False



# FUNCIÓN para MOSTRAR el mensaje de FIN DEL JUEGO
def game_over(canvas, window):
    canvas.delete(ALL)  # Eliminar todos los elementos del lienzo (serpiente, comida, etc.)
   
# Creamos el mensaje de "HAS PERDIDO" en el centro de la pantalla. 
    canvas.create_text(
        WIDTH / 2, HEIGHT / 2,
        font=('consolas', 50),  # Tipo de letra y el tamaño del texto
        text="HAS PERDIDO", fill="red",  # Mostrar "HAS PERDIDO" en rojo  
        tag="gameover"  # Etiqueta para el mensaje de fin de juego
    )

    canvas.create_text(
        WIDTH / 2, HEIGHT / 4,
        font=('consolas', 20),
        text=f"TU PUNTACIÓN!!: {score}", fill="black",  # Mostrar la puntuación en el mensaje
    )

    canvas.create_text(
        WIDTH / 2, HEIGHT / 3, 
        font=('consolas', 20),
        text = " Pulsa R para reiniciar", fill = "green",
    )
    # Guardar la mejor puntuación
    save_high_score()

    window.bind('<r>', lambda event: restart_game(canvas,window))
   

 
#FUNCIÓN para REINICIAR el juego 
def restart_game(canvas, window):
    global score, direction, snake, food  # Asegurarse de resetear estas variables
    score = 0
    direction = "down"
    
    #¨LIMPIA¨ la pantalla y reinicia los objetos 
    canvas.delete(ALL)

     # Re-crear la imagen del fondo
    bg_image = PhotoImage(file="fondo_jungla.png") 
    canvas.create_image(0, 0, anchor=NW, image=bg_image)

   # Re-crear la serpiente y la comida
    snake = Snake(canvas)
    food = Food(canvas, snake)
    
    update_score(canvas, score)  # Mostrar la puntuación inicial  
    bind_keys(window)  # Volver a enlazar las teclas de dirección
    
    # Iniciar el movimiento de la serpiente
    next_turn(snake, food, window, canvas)

# FUNCIÓN para actualizar la posición de la serpiente
def next_turn(snake, food, window, canvas):
    # Inicialización de la puntuación global
    global score, direction # Puntuación inicial y dirección. 
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
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE)
    snake.squares.insert(0, square)  # Añadir el rectángulo creado a la lista de partes de la serpiente
    
    # Verifica si la serpiente ha comido la comida
    if [x, y] == food.coordinates:
         score += 1  # Aumentar la puntuación
         update_score(canvas, score)  # Actualizar la puntuación en pantalla
         food.randomize_position()  # Genera nueva comida  
    else:
        # Si no ha comido, eliminar la cola de la serpiente
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])  # Eliminar el último rectángulo de la cola
        del snake.squares[-1]  # Eliminar el último rectángulo de la lista de partes de la serpiente

    # Verificar si la serpiente ha colisionado con los bordes o consigo misma
    if check_collisions(snake):
        game_over(canvas, window)  # Si hubo una colisión, terminar el juego
    else:
        # Continuar el movimiento de la serpiente en el siguiente ciclo
        window.after(SPEED, next_turn, snake, food, window, canvas)  # Llamar a la función de nuevo después de un intervalo



# FUNCIÓN para cambiar la DIRECCIONES de la serpiente
def change_direction(new_direction):
    global direction
    # Cambiar la dirección de la serpiente, pero evitando que vaya en dirección opuesta
    if new_direction == 'left' and direction != 'right':
       direction = new_direction
    elif new_direction == 'right' and direction != 'left':
       direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction
    


# FUNCIÓN para enlazar las teclas con las DIRECCIONES
def bind_keys(window):
    # Asociar las teclas de dirección con las funciones de cambio de dirección 
    window.bind('<Left>', lambda event: change_direction('left'))  # Tecla izquierda
    window.bind('<Right>', lambda event: change_direction('right'))  # Tecla derecha
    window.bind('<Up>', lambda event: change_direction('up'))  # Tecla arriba
    window.bind('<Down>', lambda event: change_direction('down'))  # Tecla abajo


# FUNCIÓN principal del juego
def main():
    global window, canvas, snake, food, score, direction, bg_image
    window = Tk()  
    window.title("Juego de la Serpiente")  
    canvas = Canvas(window, width=WIDTH, height=HEIGHT)
   
   #Carga la imagen del fondo 
    bg_image = PhotoImage(file="fondo_jungla.png")
    canvas.create_image(0, 0, anchor=NW, image=bg_image)
    canvas.pack()  
    
    #carga la serpiente y la comida 
    snake = Snake(canvas)  
    food = Food(canvas, snake)  
   
   #Reinicia las variables
    score= 0
    direction = "down"
   
   #Muestra la puntación
    update_score(canvas, score)  # Muestra la puntuación inicial  
    bind_keys(window)  
    
    #Inicia el juego 
    next_turn(snake, food, window, canvas)  # Iniciar el juego  
    window.mainloop()  # Ejecutar la ventana

#INICIAR EL JUEGO
if __name__== "__main__":
    main()
    load_high_score()  # Cargar la mejor puntuación al iniciar el juego
    main()