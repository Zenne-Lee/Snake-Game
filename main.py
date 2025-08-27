from tkinter import *
import random

# --- Config ---
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "pink"
FOOD_COLOR = "green"
BACKGROUND_COLOR = "black"

# --- State ---
score = 0
direction = "down"

# --- UI ---
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

label = Label(window, text=f"Score: {score}", font=("Consolas", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

# --- Snake class ---
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        start_x, start_y = 100, 100
        for i in range(self.body_size):
            self.coordinates.append([start_x - i * SPACE_SIZE, start_y])

        for x, y in self.coordinates:
            sq = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(sq)

# --- Food class ---
class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]

        RADIUS = SPACE_SIZE + 10  # slightly bigger food
        canvas.create_oval(
            x, y, x + RADIUS, y + RADIUS,
            fill=FOOD_COLOR, tag="food"
        )

# --- Game functions ---
def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("Consolas", 70),
        text="GAME OVER",
        tag="gameover"
    )

def change_direction(new_direction):
    global direction
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
    if new_direction != opposites.get(direction):
        direction = new_direction

def next_turn(snake, food):
    global score

    # Current head
    x, y = snake.coordinates[0]

    # Calculate new head position
    if direction == "up":
        new_x, new_y = x, y - SPACE_SIZE
    elif direction == "down":
        new_x, new_y = x, y + SPACE_SIZE
    elif direction == "left":
        new_x, new_y = x - SPACE_SIZE, y
    elif direction == "right":
        new_x, new_y = x + SPACE_SIZE, y

    # --- Check wall collisions BEFORE creating the head ---
    if new_x < 0 or new_x >= GAME_WIDTH or new_y < 0 or new_y >= GAME_HEIGHT:
        game_over()
        return

    # --- Check self collisions BEFORE creating the head ---
    for part in snake.coordinates:
        if [new_x, new_y] == part:
            game_over()
            return

    # Add new head
    snake.coordinates.insert(0, [new_x, new_y])
    square = canvas.create_rectangle(
        new_x, new_y, new_x + SPACE_SIZE, new_y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    # Check if food is eaten
    if new_x == food.coordinates[0] and new_y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        # Remove tail to simulate movement
        tail_square = snake.squares.pop()
        canvas.delete(tail_square)
        snake.coordinates.pop()

    # Schedule next move
    window.after(SPEED, next_turn, snake, food)

# --- Bind keys ---
window.bind('<Left>', lambda e: change_direction('left'))
window.bind('<Right>', lambda e: change_direction('right'))
window.bind('<Up>', lambda e: change_direction('up'))
window.bind('<Down>', lambda e: change_direction('down'))

# --- Start game ---
snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()


