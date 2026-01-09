import json
import tkinter as tk
from tkinter import simpledialog

with open("story_v2.json", "r", encoding="utf-8") as f:
    story = json.load(f)

class Quest:
    def __init__(self, root):
        self.root = root
        self.story = story
        self.current_scene = "start"
        self.player_name = ""
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
                text=choice["text"],
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
            self.on_choice(choice["next"])
        elif "action" in choice:
            self.manage_action(choice["action"])

    def on_choice(self, next_scene):
        if next_scene == "introduction" and not self.player_name:
            self.ask_name()

        if next_scene == "refuse":
            self.state["refused_journalist"] = True

        if next_scene == "close_seat_v1":
            self.state["close_seat_v1"] = True

        if next_scene == "wait_stay_cross":
            self.state["wait_stay_cross"] = True

        if next_scene == "fire_alarm_cross2":
            self.state["fire_alarm_cross2"] = True

        self.mode = "default"
        if next_scene == "corridor_cross":
            if self.state["refused_journalist"] and self.state["close_seat_v1"]:
                self.mode = "add_var1"
            elif self.state["fire_alarm_cross2"]:
                self.mode = "add_var2"

        if next_scene == "new_floor_cross":
            if self.state["wait_stay_cross"]:
                self.mode = "add_var1"

        self.show_scene(next_scene, mode=self.mode)

    def manage_action(self, action):
        if action == "restart":
            self.restart_game() # TODO добавить другие действия и написать функции для них

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
        self.player_name = simpledialog.askstring(
            "Имя",
            "Как вас зовут?"
        )
        if not self.player_name:
            self.player_name = "Player 1" # TODO добавить айди из SQLite

root = tk.Tk()
root.title("Text Horror Quest")

game = Quest(root)
game.show_scene("start")

root.mainloop()






