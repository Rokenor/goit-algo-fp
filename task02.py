import turtle
import math

SQRT_2 = math.sqrt(2)

def pythagoras_tree(t, x, y, length, tilt, level):
    # Базовий випадок
    if level == 0:
        return
    
    # Встановлюємо колір залежно від рівня рекурсії
    if level > 5:
        t.color("#8B4513", "#8B4513")
    else:
        t.color("#228B22", "#228B22")
    
    # Малюємо одну "гілку" дерева Піфагора і одночасно визначаємо стартові точки для двох наступних
    t.up()
    t.goto(x,y)
    t.down()
    t.seth(tilt)
    t.fd(length)
    t.left(90)
    t.fd(length)
    t.left(45)
    t.fd(length/SQRT_2)
    x1,y1 = t.xcor(), t.ycor()    
    t.left(90)
    t.fd(length/SQRT_2)
    x2,y2 = t.xcor(), t.ycor()
    t.left(45)
    t.fd(length)
    t.left(90)

    # Рекурсивно малюємо наступні рівні
    pythagoras_tree(t, x1, y1, length/SQRT_2, tilt-45, level-1)
    pythagoras_tree(t, x2, y2, length/SQRT_2, tilt+45, level-1) 

def main():
    '''Основна функція для налаштування та запуску малювання'''
    
    # Отримуємо рівень рекурсії від користувача
    while True:
        try:
            level = int(input("Введіть рівень рекурсії (рекомендовано від 1 до 12): "))
            if 0 <= level <= 12: # Обмеження для уникнення занадто довгого виконання
                break
            else:
                print("Будь ласка, введіть число в діапазоні від 0 до 12.")
        except ValueError:
            print("Некоректне введення. Будь ласка, введіть ціле число.")

    # Налаштування екрана
    screen = turtle.Screen()
    screen.setup(width=1000, height=1000)
    screen.title("Дерево Піфагора")
    screen.bgcolor("lightblue")

    screen.setworldcoordinates(-1000,-1000,1000,1000)
    screen.tracer(0,0) # Закоментувати код для відображення анімації

    # Налаштування черепашки
    t = turtle.Turtle()
    t.speed(100)
    t.hideturtle()
    t.pensize(3)

    # Початкові координати
    x = -100
    y = -400
    initial_length = 200
    initial_tilt = 0

    # Запуск рекурсивної функції
    pythagoras_tree(t, x, y, initial_length, initial_tilt, level)

    screen.update()

    # Завершення
    print("Малювання завершено. Можете закрити вікно.")
    screen.mainloop()

if __name__ == "__main__":
    main()