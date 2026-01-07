import json
import tkinter as tk
from tkinter import simpledialog

# загрузка json
with open("story.json", "r", encoding="utf-8") as f:
    story = json.load(f)

current_scene = "start"
player_name = ""

def show_scene(scene_id):
    global current_scene
    current_scene = scene_id
    scene = story[scene_id]
    text_box.config(state ='normal')
    text_box.delete('1.0', tk.END)
    text = scene['text']
    if '{name}' in text:
        text = text.replace('{name}', player_name)
    text_box.insert(tk.END, text)
    text_box.config(state='disabled')
    for widget in buttons_frame.winfo_children(): # очистка кнопок
        widget.destroy()

    for choice in scene.get("choices", []):
        button = tk.Button(
            buttons_frame,
            text=choice['text'],
            wraplength=400,
            width=10,
            command=lambda n=choice["next"]: on_choice(n)
        )
        button.pack(fill='x', pady=5)
def on_choice(next_scene):
    if next_scene == "introduction" and not player_name:
        ask_name()
    show_scene(next_scene)

def ask_name():
    global player_name
    player_name = simpledialog.askstring(
        "Имя",
        "Как вас зовут?"
    )
    if not player_name:
        player_name = "Player 1"

# Tkinter
root = tk.Tk()
root.title("Text Horror Quest: Пропавшая Ёлка ИТМО")
# root.geometry("1200x800")
text_box = tk.Text(root, wrap="word", font=("Montserrat", 14))
text_box.pack(expand=True, fill="both", padx=10, pady=10)
text_box.config(state="disabled")
buttons_frame = tk.Frame(root)
buttons_frame.pack(fill="x", padx=10, pady=10)

# старт игры
show_scene("start")

root.mainloop()






