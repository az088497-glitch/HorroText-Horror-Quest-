import json
import tkinter as tk
from tkinter import simpledialog, messagebox
from quest_statistics import QuestStatistics
import customtkinter as ctk

# json с текстом квеста
with open("../data/story_v2.json", "r", encoding="utf-8") as f: # json находится в папке data, туда же сохраняется история прохождений
    story = json.load(f)

# тема из customtkinter (в свою очередь, всплывающие окна остаются стандартными из tkinter)
ctk.set_default_color_theme("green")

# класс, отвечающий за работу квеста
class Quest:
    def __init__(self, root):
        self.root = root
        self.story = story
        self.current_scene = "start"
        self.player_name = ""
        self.statistics = QuestStatistics()
        self.player_id = self.statistics.create_player("player") # автоматически создаёт игрока
        self.state = {
            "refused_journalist": False,
            "close_seat_v1": False, # словарь со сценами, прохождение которых будет влиять на доступные игроку выборы
            "fire_alarm_cross2": False,
            "wait_stay_cross": False,
        }

        self.text_box = ctk.CTkTextbox(root, wrap="word", font=("Segoe UI", 18))
        self.text_box.pack(expand=True, fill="both", padx=10, pady=10)
        self.text_box.configure(state="disabled")

        self.buttons_frame = ctk.CTkFrame(root)
        self.buttons_frame.pack(fill="x", padx=10, pady=10)

    # функция, показывающая сцены и соответствующие выборы из json
    def show_scene(self, scene_id, mode="default"):
        self.current_scene = scene_id
        scene = self.story[scene_id]

        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", tk.END)
        self.text_box.insert(tk.END, scene["text"])
        self.text_box.configure(state="disabled")

        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        choices = self.get_choices(scene, mode)
        for choice in choices:
            button = ctk.CTkButton(
                self.buttons_frame,
                font=("Segoe UI", 14),
                text=choice["text"],
                command=lambda c=choice: self.manage_choice(c)
            )
            button.pack(fill="x", pady=5)

        if scene.get("type") == "game_over":
            self.restart_game_over()

    # функция получения выборов игрока
    def get_choices(self, scene, mode="default"):
        choices = scene.get("choices", [])
        if isinstance(choices, dict) and "variants" in choices:
            return choices["variants"].get(mode, [])
        if isinstance(choices, list):
            return choices
        return []

    # функция управления доступными игроку выборами в зависимости от state
    def manage_choice(self, choice):
        if "next" in choice:
            next_scene = choice["next"]

            if next_scene == "introduction" and not self.player_name:
                self.ask_name()

            if next_scene in self.state:
                self.state[next_scene] = True

            mode = "default" # default - стандартный набор выборов, add_var доступны при соблюдении условий state
            if next_scene == "corridor_cross":
                if self.state["refused_journalist"] and self.state["close_seat_v1"]:
                    mode = "add_var1"
                elif self.state["fire_alarm_cross2"]:
                    mode = "add_var2"

            if next_scene == "new_floor_cross" and self.state["wait_stay_cross"]:
                mode = "add_var1"

            self.statistics.save_choice(
                self.player_id,
                self.current_scene,
                choice.get("text", ""),
                next_scene
            )
            self.show_scene(next_scene, mode)

        elif "action" in choice:
            self.manage_action(choice["action"])

    # управление выборами на финальной странице, ключи финальной страницы заданы в json
    def manage_action(self, action, scene_id=None):
        if action == "restart":
            self.restart_game()
        elif action == "rollback":
            self.rollback(scene_id)
        elif action == "export_history":
            self.export_history()

    # перезапуск игры
    def restart_game(self):
        self.player_name = ""
        self.state = {k: False for k in self.state}
        self.show_scene("start")

    # кнопка перезапуска квеста в случае комбинации выборов, приводящей к проигрышу
    def restart_game_over(self):
        btn_restart = ctk.CTkButton(
            self.buttons_frame,
            text="Начать заново",
            command=self.restart_game
        )
        btn_restart.pack(fill="x", pady=5)

    # simpledialog для ввода имени игрока
    def ask_name(self):
        name = simpledialog.askstring("Имя", "Как вас зовут?")
        if not name:
            name = "Player"
        self.player_name = name
        self.statistics.update_player_name(self.player_id, name)

    # функция отката к выбранной сцене, получает историю из get_choices_history класса QuestStatistics, здесь задан как self.statistics
    def rollback(self, scene_id):
        history = self.statistics.get_choices_history(self.player_id)
        if not history:
            return

        scene_ids = [row["scene_id"] for row in history] # ключи сцен из json
        unique_scenes = list(dict.fromkeys(scene_ids))

        scene_list_str = "\n".join(f"{i+1}. {sid}" for i, sid in enumerate(unique_scenes))
        chosen_index = simpledialog.askinteger(
            "Выбор сцены",
            f"Выберите сцену для возврата:\n{scene_list_str}\nВведите номер:"
        )
        if chosen_index is None:  # обработка возможных ошибок пользователя
            return

        if not (1 <= chosen_index <= len(unique_scenes)):
            messagebox.showerror(
                "Ошибка",
                f"Некорректный номер сцены! Введите число от 1 до {len(unique_scenes)}"
            )
            return

        scene_id = unique_scenes[chosen_index - 1]
        self.statistics.rollback_to_scene(self.player_id, scene_id)
        self.show_scene(scene_id)

    # экспорт истории, запускает функцию из QuestStatistics
    def export_history(self):
        filename = self.statistics.export_history_to_csv(self.player_id)
        if filename:
            messagebox.showinfo("Экспорт истории", f"История успешно сохранена в {filename}")
        else:
            messagebox.showinfo("Экспорт истории", "История пуста.")

# запуск
if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("1200x800")
    root.title("Text Horror Quest: Тайна вузовской ёлки")
    game = Quest(root)
    game.show_scene("start")
    root.mainloop()





