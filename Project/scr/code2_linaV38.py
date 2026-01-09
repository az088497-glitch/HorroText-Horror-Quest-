# код змейки для дальнейшей адаптации
import tkinter as tk
import random

class Game:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title('Text Horror Quest: Пропавшая Ёлка ИТМО')
        self.root.resizable(False, False)

        self.WIDTH = 600 # константы
        self.HEIGHT = 400
        self.SEGMENT_SIZE = 20
        self.GAME_SPEED = 150

        self.direction = "Right" # начальные значения
        self.score = 0
        self.player = [(100, 100), (80, 100), (60, 100)]
        self.events = self.create_events()

        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT, bg="white") # создание холста
        self.canvas.pack()

        self.score_display = self.canvas.create_text(
            50, 20, text=f"Счёт: {self.score}", fill="black", font=("Arial", 14)) # счёт

        self.root.bind("<KeyPress>", self.on_key_press) # привязка клавиш
        self.move_player()

    def create_events(self):
        x = random.randint(
            1, (self.WIDTH - self.SEGMENT_SIZE) // self.SEGMENT_SIZE
        ) * self.SEGMENT_SIZE

        y = random.randint(
            1, (self.HEIGHT - self.SEGMENT_SIZE) // self.SEGMENT_SIZE
        ) * self.SEGMENT_SIZE

        return x, y

    def draw_player(self):
        self.canvas.delete("player")
        for x, y in self.player:
            self.canvas.create_rectangle(
                x, y,
                x + self.SEGMENT_SIZE,
                y + self.SEGMENT_SIZE,
                fill="green",
                tags="player"
            )

    def draw_events(self):
        self.canvas.delete("events")
        x, y = self.events
        self.canvas.create_oval(
        x, y, x + self.SEGMENT_SIZE, y + self.SEGMENT_SIZE,
        fill="red", tags="events")

    def on_key_press(self, event):
        new_direction = event.keysym # предотвращение разворота
        if (new_direction == "Up" and self.direction != "Down" or
                new_direction == "Down" and self.direction != "Up" or
                new_direction == "Left" and self.direction != "Right" or
                new_direction == "Right" and self.direction != "Left"):
            self.direction = new_direction

    def move_player(self):
        head_x, head_y = self.player[0]
        if self.direction == "Up":
            new_head = (head_x, head_y - self.SEGMENT_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + self.SEGMENT_SIZE)
        elif self.direction == "Left":
            new_head = (head_x - self.SEGMENT_SIZE, head_y)
        elif self.direction == "Right":
            new_head = (head_x + self.SEGMENT_SIZE, head_y)

        self.player.insert(0, new_head)

        # Проверяем, съела ли змейка еду
        if self.player[0] == self.events:
            self.score += 1
            self.canvas.itemconfig(self.score_display, text=f"Счёт: {self.score}")
            self.events = self.create_events()
            self.draw_events()
            self.GAME_SPEED = max(50, self.GAME_SPEED - 5)
        else:
            self.player.pop()

        if self.check_collisions():
            self.game_over()
            return
        self.draw_player()
        self.draw_events()

        # Планируем следующий ход
        self.root.after(self.GAME_SPEED, self.move_player)

    def check_collisions(self):
        head_x, head_y = self.player[0]
        if (head_x < 0 or head_x >= self.WIDTH or
            head_y < 0 or head_y >= self.HEIGHT):
            return True
        if len(self.player) > 3 and self.player[0] in self.player[3:]:
            return True

        else:
            return False

    def game_over(self):
        self.canvas.create_text(
        self.WIDTH // 2, self.HEIGHT // 2,
        text=f"Игра окончена! Счёт: {self.score}",
        fill="black", font=("Arial", 24))
        restart_button = tk.Button(
        self.root, text="Начать заново", command=self.restart_game)
        restart_button_window = self.canvas.create_window(
        self.WIDTH // 2, self.HEIGHT // 2 + 40,
        window=restart_button)

    def restart_game(self):
        self.direction = "Right"
        self.score = 0
        self.player = [(100, 100), (80, 100), (60, 100)]
        self.events = self.create_events()
        self.GAME_SPEED = 150
        self.canvas.delete("all") # очищаем холст
        self.score_display = self.canvas.create_text(
            50, 20, text=f"Счёт: {self.score}", fill="black", font=("Arial", 14))

        self.move_player()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()






