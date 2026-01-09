import json
import tkinter as tk
from tkinter import simpledialog

# загрузка json
with open("story.json", "r", encoding="utf-8") as f:
    story = json.load(f)

current_scene = "start"
player_name = ""
state = {
    "refused_journalist": False,
    "close_seat": False,
    "that_news_true": False
}

def get_choices(scene, mode="default"):
    choices = scene.get("choices", [])

    # если choices — словарь с вариантами
    if isinstance(choices, dict) and "variants" in choices:
        return choices["variants"].get(mode, [])

    # если choices — обычный список
    elif isinstance(choices, list):
        return choices

    return []

def show_scene(scene_id, mode="default"):
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

    choices = get_choices(scene, mode)
    for choice in choices:
        button = tk.Button(
            buttons_frame,
            text=choice['text'],
            wraplength=400,
            width=15,
            command=lambda n=choice["next"]: on_choice(n)
        )
        button.pack(fill='x', pady=5)

    if scene.get("type")== "ending":
        restart_button()


def on_choice(next_scene):
    global player_name, state

    if next_scene == "introduction" and not player_name:
        ask_name()

    if next_scene == "refuse":
        state["refused_journalist"] = True

    if next_scene == "close_seat_v1":
        state["close_seat"] = True

    mode = "default"
    if next_scene == "corridor_cross":
        if state["refused_journalist"] and state["close_seat"]:
            mode = "add_var1"
        elif state["that_news_true"]:
            mode = "add_var2"
    show_scene(next_scene, mode=mode)


def ask_name():
    global player_name
    player_name = simpledialog.askstring(
        "Имя",
        "Как вас зовут?"
    )
    if not player_name:
        player_name = "Player 1"

def restart_button():
    btn_restart = tk.Button(
        buttons_frame,
        text="Пройти заново",
        width=15,
        command=lambda: show_scene("start")
    )
    btn_restart.pack(fill="x", pady=5)


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






