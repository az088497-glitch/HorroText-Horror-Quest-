import json
import os
import tkinter as tk
from tkinter import simpledialog
from datetime import datetime


# =======================
# МОДЕЛЬ СЮЖЕТА
# =======================

class ChoiceNode:
    def __init__(self, node_id, text, next_a=None, next_b=None):
        self.id = node_id
        self.text = text
        self.next = {
            "A": next_a,
            "B": next_b
        }


# =======================
# ЗАГРУЗКА СЮЖЕТА
# =======================

def load_story_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    nodes = {}
    for node_id, data in raw.items():
        nodes[node_id] = ChoiceNode(
            node_id=node_id,
            text=data["text"],
            next_a=data.get("A"),
            next_b=data.get("B")
        )
    return nodes


# =======================
# СОСТОЯНИЕ ИГРЫ
# =======================

class GameState:
    def __init__(self, nodes, start_id):
        self.nodes = nodes
        self.start_id = start_id
        self.reset()

    def reset(self):
        """Состояние ДО первого выбора"""
        self.current = self.nodes[self.start_id]
        self.history = []

    def make_choice(self, choice):
        self.history.append((self.current.id, choice))
        next_id = self.current.next.get(choice)
        self.current = self.nodes.get(next_id)

    def is_finished(self):
        return self.current is None

    def restore_from_history(self, history):
        """Восстановление состояния по истории"""
        self.reset()
        for node_id, choice in history:
            if self.current is None:
                break
            if self.current.id != node_id:
                break
            self.make_choice(choice)

    def rollback_to(self, index):
        """
        index == 0 → начало игры (до первого выбора)
        index > 0  → соответствующий шаг истории
        """
        if index == 0:
            self.reset()
        else:
            new_history = self.history[:index]
            self.restore_from_history(new_history)


# =======================
# СОХРАНЕНИЕ
# =======================

class SaveManager:
    def __init__(self, player_name):
        self.player_name = player_name
        self.save_dir = "saves"
        os.makedirs(self.save_dir, exist_ok=True)
        self.path = os.path.join(self.save_dir, f"{player_name}.json")

    def save(self, history):
        data = {
            "player": self.player_name,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "history": history
        }
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self):
        if not os.path.exists(self.path):
            return None
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)


# =======================
# GUI
# =======================

class QuestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Текстовый квест")

        # --- игрок ---
        self.player_name = simpledialog.askstring(
            "Имя игрока", "Введите ваше имя:"
        ) or "Player"

        # --- данные ---
        self.story = load_story_from_json("story.json")
        self.game = GameState(self.story, "start")
        self.save_manager = SaveManager(self.player_name)

        save_data = self.save_manager.load()
        if save_data:
            self.game.restore_from_history(save_data["history"])

        # --- layout ---
        main = tk.Frame(root)
        main.pack(fill="both", expand=True)

        left = tk.Frame(main)
        left.pack(side="left", fill="both", expand=True, padx=10)

        right = tk.Frame(main, width=220)
        right.pack(side="right", fill="y", padx=10)

        # --- текст ---
        self.text_label = tk.Label(
            left,
            wraplength=450,
            justify="left",
            font=("Arial", 12)
        )
        self.text_label.pack(pady=10)

        self.button_a = tk.Button(
            left, text="A", width=20,
            command=lambda: self.choose("A")
        )
        self.button_b = tk.Button(
            left, text="B", width=20,
            command=lambda: self.choose("B")
        )
        self.button_a.pack(pady=5)
        self.button_b.pack(pady=5)

        # --- история ---
        tk.Label(right, text="История решений").pack()
        self.history_list = tk.Listbox(right)
        self.history_list.pack(fill="y", expand=True)
        self.history_list.bind("<<ListboxSelect>>", self.on_history_select)

        self.update_ui()

    def choose(self, choice):
        self.game.make_choice(choice)
        self.save_manager.save(self.game.history)
        self.update_ui()

    def on_history_select(self, event):
        if not self.history_list.curselection():
            return
        index = self.history_list.curselection()[0]
        self.game.rollback_to(index)
        self.save_manager.save(self.game.history)
        self.update_ui()

    def update_ui(self):
        # текст и кнопки
        if self.game.is_finished():
            self.text_label.config(text="Конец истории.")
            self.button_a.config(state="disabled")
            self.button_b.config(state="disabled")
        else:
            self.text_label.config(text=self.game.current.text)
            self.button_a.config(state="normal")
            self.button_b.config(state="normal")

        # история
        self.history_list.delete(0, tk.END)
        self.history_list.insert(tk.END, "0: [Начало игры]")
        for i, (node, choice) in enumerate(self.game.history, start=1):
            self.history_list.insert(
                tk.END, f"{i}: {node} → {choice}"
            )


# =======================
# ЗАПУСК
# =======================

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("820x420")
    QuestApp(root)
    root.mainloop()
