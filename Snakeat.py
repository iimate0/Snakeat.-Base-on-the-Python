import tkinter as tk
import random

#Настройки игры
WIDHT = 400
HEIGHT = 400
direction = "Right"
DIRECTIONS = ["Up","Down","Left","Right"]
CELL_SIZE = 10  # Размер одной клетки змейки и еды
DELAY = 100     # Скорость игры (задержка между движениями змейки в мс)

#Создание главного окна
root = tk.Tk()
root.title("Змейка | Счёт: 0")
root.resizable(False, False)

#Холст
canvas = tk.Canvas(
    root,
    width=WIDHT,
    height=HEIGHT,
    bg="black",
    highlightthickness=0
)
canvas.pack()

#Место змейки
def create_snake():
    max_x = (WIDHT // CELL_SIZE) - 3
    max_y = (HEIGHT / CELL_SIZE) - 1

    x = random.randint(0, max_x) * CELL_SIZE
    y = random.randint(0, max_y) * CELL_SIZE
    return [(x, y), (x - CELL_SIZE, y), (x - 2 * CELL_SIZE, y)]

#Модель змейки
snake = create_snake()
score = 0
game_over = False

#Еда
def create_food():  #Функция, создающая еду в случайном месте на игровом поле.
    while True:
        x = random.randint(0, (WIDHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
        if (x,y) not in snake:  #Проверяем, не находится ли еда внутри змейки
            return(x,y)
food = create_food()

# Отрисовка еды
def draw_food():
    canvas.create_rectangle(
        food[0], food[1],     # Верхний левый угол (x1, y1)
        food[0] + CELL_SIZE,  # x-координата правого края
        food[1] + CELL_SIZE,  # y-координата нижнего края
        fill= "red",           # Цвет заливки
    )

#Рисунок змейки
snake = [
    (100, 100), #голова
    (90, 100), #Первый сегмент тела
    (80,100), #Второй сегмент тела
]

def draw_snake():
    for segment in snake:
        canvas.create_rectangle(
            segment[0], segment[1],
            segment[0] + CELL_SIZE,
            segment[1] + CELL_SIZE,
            fill="green", #цвет заливки
            outline="darkgreen" #цвет обводки
        )

#Движение змейки вперед
def move_snake():
    head_x, head_y = snake[0]

    if direction == "Up":
        new_head = (head_x, head_y - CELL_SIZE)
    elif direction == "Down":
        new_head = (head_x, head_y + CELL_SIZE)
    elif direction == "Left":
        new_head = (head_x - CELL_SIZE, head_y)
    elif direction == "Right":
        new_head = (head_x + CELL_SIZE, head_y)

    snake.insert(0, new_head) #Добавляем новую голову

    if not check_food_collision(): #Если еда не съедена
        snake.pop() #Удаляем хвост(Если не поел)

#Поедание еды
def check_food_collision():
    global food, score
    if snake[0] == food:
        score += 1              #Увеличиваем счёт
        food = create_food()    #Генерируем новую еду
        return True             #Сообщаем, что еда съедена
    return False                #Еда не съедена

#Обновление заголовка со счётом
def update_title():
    root.title(f"Змейка | Счёт: {score}")

#Проверка на столкновение со стенами
def check_wall_collision():
    head_x, head_y = snake[0]
    return (
        head_x < 0 or head_x >= WIDHT or
        head_y < 0 or head_y >= HEIGHT
    )

#Самостолкновение
def check_self_collision():
    return snake[0] in snake[1:]

#Завершение игры
def end_game():
    global game_over
    game_over = True #Больше не обновляем игру
    canvas.create_text(
        WIDHT // 2, HEIGHT // 2,
        text= f"Игра окончена! Счёт {score}",
        fill = "white",
        font = ("Arial", 24)
    )

#Перезапуск игры
def restart_game():
    global snake, direction, food, score, game_over

    # Начальное положение змейки
    snake = create_snake()
    direction = "Right"

    # Новая еда
    food = create_food()

    # Сброс счёта и статуса
    score = 0
    game_over = False

    # Очистим холст и обновим
    canvas.delete("all")
    draw_food()
    draw_snake()
    update_title()

    # Перезапускаем игровой цикл
    root.after(DELAY, game_loop)

#Движение
def on_key_press(event):
    global direction
    key = event.keysym
    if key in DIRECTIONS:
        #Запрещаем поворот в противоположную сторону
        if (key == "Up" and direction != "Down" or
            key == "Down" and direction != "Up" or
            key == "Left" and direction != "Right" or
            key == "Right" and direction != "Left"):
            direction = key
        
        #Перезапуск игры
    elif key == "space" and game_over:
        restart_game()

root.bind("<KeyPress>", on_key_press) #Привязываем обработчик к окну

#Игровой цикл
def game_loop():
    global snake, food, score

    if game_over:
        return #Останавливаем цикл, если игра окончена
    
    move_snake()            #Двигаем змейку

    if check_wall_collision() or check_self_collision():
        end_game()
        return
    
    canvas.delete("all")    #Очищаем холст
    draw_food()             #Рисуем еду
    draw_snake()            #Рисуем змейку
    update_title()          #Обновляем счёт
    root.after(DELAY, game_loop)    #Повторяем через DELAY мс

#Первоначальная отрисовка
draw_food()
draw_snake()
root.after(DELAY, game_loop)

#Запуск главного цикла
root.mainloop()
