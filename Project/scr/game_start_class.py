import json
import tkinter as tk
from tkinter import simpledialog
from quest_statistics import QuestStatistics
from tkinter import messagebox

# json с текстом квеста
with open("story_v2.json", "r", encoding="utf-8") as f:
    story = json.load(f)

class Quest:
    def __init__(self, root):
        self.root = root
        self.story = story
        self.current_scene = "start"
        self.player_name = ""
        self.statistics = QuestStatistics()
        self.player_id = self.statistics.create_player("player")
        self.state = {
            "refused_journalist": False,
            "close_seat_v1": False,
            "fire_alarm_cross2": False,
            "wait_stay_cross": False,
        }
        self.text_box = tk.Text(root, wrap="word", font=("Montserrat", 14))
        self.text_box.pack(expand=True, fill="both", padx=10, pady=10)
        self.text_box.config(state="disabled")
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(fill="x", padx=10, pady=10)

    def show_scene(self, scene_id, mode="default"):
        self.current_scene = scene_id
        scene = self.story[scene_id]
        self.text_box.config(state="normal")
        self.text_box.delete("1.0", tk.END)
        text = scene["text"]
        self.text_box.insert(tk.END, text)
        self.text_box.config(state="disabled")

        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
        choices = self.get_choices(scene, mode)
        for choice in choices:
            button = tk.Button(
                self.buttons_frame,
                text=choice.get("text", "???"),
                width=25,
                command=lambda c=choice: self.manage_choice(c)
            )
            button.pack(fill="x", pady=5)

        if scene.get("type") == "game_over":
            self.restart_game_over()

    def get_choices(self, scene, mode="default"):
        choices = scene.get("choices", [])

        if isinstance(choices, dict) and "variants" in choices:
            return choices["variants"].get(mode, [])

        if isinstance(choices, list):
            return choices

        return []

    def manage_choice(self, choice):
        if "next" in choice:
            next_scene = choice["next"]

            if next_scene == "introduction" and not self.player_name:
                self.ask_name()

            if next_scene in self.state:
                self.state[next_scene] = True

            mode = "default"
            if next_scene == "corridor_cross":
                if self.state["refused_journalist"] and self.state["close_seat_v1"]:
                    mode = "add_var1"
                elif self.state["fire_alarm_cross2"]:
                    mode = "add_var2"

            if next_scene == "new_floor_cross":
                if self.state["wait_stay_cross"]:
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

    def on_choice(self, choice):
        next_scene = choice["next"] # ЛОМАЕТСЯ ЗДЕСЬ

        if next_scene == "introduction" and not self.player_name:
            self.ask_name()

        if next_scene in self.state:
            self.state[next_scene] = True

        mode = "default"

        if next_scene == "corridor_cross":
            if self.state["refused_journalist"] and self.state["close_seat_v1"]:
                mode = "add_var1"
            elif self.state["fire_alarm_cross2"]:
                mode = "add_var2"

        if next_scene == "new_floor_cross":
            if self.state["wait_stay_cross"]:
                mode = "add_var1"

        self.statistics.save_choice(
            self.player_id,
            self.current_scene,
            choice["text"],
            next_scene
        )

        self.show_scene(next_scene, mode)

    def manage_action(self, action, scene_id=None): # Эта функция отвечает за последнюю страницу и 3 кнопки на ней
        if action == "restart":
            self.restart_game()
        elif action == "rollback":
            self.rollback(scene_id)
        elif action == "export_history":
            self.export_history()


    def restart_game(self):
        self.player_name = ""
        self.state = {k: False for k in self.state}
        self.show_scene("start")

    def restart_game_over(self):
        btn_restart = tk.Button(
            self.buttons_frame,
            text="Начать заново",
            width=15,
            command=lambda: self.restart_game()
        )
        btn_restart.pack(fill="x", pady=5)

    def ask_name(self):
        name = simpledialog.askstring(
            "Имя",
            "Как вас зовут?"
        )

        if not name:
            name = "Player"

        self.player_name = name
        self.statistics.update_player_name(self.player_id, name)

    def rollback(self, scene_id):
        history = self.statistics.get_choices_history(self.player_id)
        if not history:
            return

        scene_ids = [row["scene_id"] for row in history]
        unique_scenes = list(dict.fromkeys(scene_ids))  # сохраняем порядок

        scene_list_str = "\n".join(f"{i + 1}. {sid}" for i, sid in enumerate(unique_scenes))
        chosen_index = simpledialog.askinteger(
            "Выбор сцены",
            f"Выберите сцену для возврата:\n{scene_list_str}\nВведите номер:"
        )

        if chosen_index is None:
            return

        if 1 <= chosen_index <= len(unique_scenes):
            scene_id = unique_scenes[chosen_index - 1]
            self.statistics.rollback_to_scene(self.player_id, scene_id)
            self.show_scene(scene_id)

    def export_history(self):
        filename = self.statistics.export_history_to_csv(self.player_id)
        if filename:
            tk.messagebox.showinfo("Экспорт истории", f"История успешно сохранена в {filename}")
        else:
            tk.messagebox.showinfo("Экспорт истории", "История пуста.")

root = tk.Tk()
root.title("Text Horror Quest")

game = Quest(root)
game.show_scene("start")

root.mainloop()





