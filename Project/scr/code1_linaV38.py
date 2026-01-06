import time
import random
import json
import tkinter as tk

# root = tk.Tk()
# root.title("Текстовое приключение")
#
# output = tk.Text(root, height=20, width=60, state="disabled")
# output.pack(padx=10, pady=10)
#
# entry = tk.Entry(root, width=50)
# entry.pack(side=tk.LEFT, padx=5)
#
# def print_text(text):
#     output.config(state="normal")
#     output.insert(tk.END, text + "\n")
#     output.config(state="disabled")
#     output.see(tk.END)
#
# def handle_command():
#     cmd = entry.get().lower()
#     entry.delete(0, tk.END)
#     print_text(f"> {cmd}")
#     # здесь будет вызов твоей логики
#     #global process_command(cmd)
#
#
#
# btn = tk.Button(root, text="OK", command=handle_command)
# btn.pack(side=tk.LEFT)
#
# print_text("Добро пожаловать в игру!")
#
# root.mainloop()

"Примечание: использовался код из статьи skypro и джпт. Надо подумать, как оформить в tkinter. Сюжет случайный"

# КОНСТАНТЫ И СОСТОЯНИЕ

VERSION = "1.0"
AUTHOR = "Ваше имя"

player_health = 100
player_attack = 10
player_defense = 5
player_inventory = []

current_location = "starting_room"
game_running = True


# ======================
# МИР ИГРЫ
# ======================
locations = {
    "starting_room": {
        "name": "Начальная комната",
        "description": "Вы в небольшой тускло освещённой комнате. Дверь на север ведёт в коридор.",
        "exits": {"север": "corridor"},
        "items": ["факел", "коробка спичек"],
        "npcs": []
    },
    "corridor": {
        "name": "Коридор",
        "description": "Длинный коридор тянется на восток и запад.",
        "exits": {"восток": "treasure_room", "запад": "monster_room", "юг": "starting_room"},
        "items": [],
        "npcs": ["старый мудрец"]
    },
    "treasure_room": {
        "name": "Сокровищница",
        "description": "Комната полна золота и драгоценностей.",
        "exits": {"запад": "corridor"},
        "items": ["золотая монета", "драгоценный камень"],
        "npcs": []
    },
    "monster_room": {
        "name": "Логово чудовища",
        "description": "Тёмная комната. Здесь живёт чудовище!",
        "exits": {"восток": "corridor"},
        "items": ["меч героя"],
        "npcs": ["чудовище"]
    }
}


# ======================
# ИНТРО
# ======================
def show_intro():
    print("=" * 50)
    print(f"ТЕКСТОВОЕ ПРИКЛЮЧЕНИЕ v{VERSION}")
    print("=" * 50)
    print("Введите 'помощь' для списка команд.")
    print("=" * 50)


# ======================
# БОЙ
# ======================
def battle(enemy_name):
    global player_health

    enemies = {
        "чудовище": {"health": 50, "attack": 8, "defense": 3, "exp": 20},
        "гоблин": {"health": 30, "attack": 5, "defense": 1, "exp": 10},
        "скелет": {"health": 40, "attack": 7, "defense": 2, "exp": 15}
    }

    enemy = enemies[enemy_name]
    enemy_health = enemy["health"]

    print(f"\n⚔ Начинается бой с {enemy_name}!")

    defense_bonus = 0

    while player_health > 0 and enemy_health > 0:
        print(f"\nВаше HP: {player_health} | HP врага: {enemy_health}")
        print("1. Атаковать\n2. Защищаться\n3. Убежать")

        action = input("> ")

        if action == "1":
            damage = max(1, player_attack - enemy["defense"])
            enemy_health -= damage
            print(f"Вы нанесли {damage} урона!")

        elif action == "2":
            defense_bonus = 5
            print("Вы заняли оборонительную позицию.")

        elif action == "3":
            if random.random() < 0.3:
                print("Вы успешно сбежали!")
                return False
            else:
                print("Побег не удался!")

        if enemy_health > 0:
            defense = player_defense + defense_bonus
            enemy_damage = max(1, enemy["attack"] - defense)
            player_health -= enemy_damage
            print(f"{enemy_name} наносит {enemy_damage} урона!")
            defense_bonus = 0

    if player_health <= 0:
        print("Вы проиграли...")
        return False

    print(f"Вы победили {enemy_name}!")
    return True


# ======================
# ЛОКАЦИИ
# ======================
def show_location():
    location = locations[current_location]
    print(f"\n📍 {location['name']}")
    print(location["description"])

    if location["exits"]:
        print("\nВыходы:")
        for d, dest in location["exits"].items():
            print(f" {d} → {locations[dest]['name']}")

    if location["items"]:
        print("\nПредметы:")
        for item in location["items"]:
            print(f" {item}")

    if location["npcs"]:
        print("\nПерсонажи:")
        for npc in location["npcs"]:
            print(f" {npc}")


def move(direction):
    global current_location
    location = locations[current_location]

    if direction in location["exits"]:
        current_location = location["exits"][direction]
        show_location()
    else:
        print("Туда нельзя идти.")


# ======================
# ИНВЕНТАРЬ
# ======================
def take_item(item):
    loc = locations[current_location]
    if item in loc["items"]:
        loc["items"].remove(item)
        player_inventory.append(item)
        print(f"Вы взяли {item}.")
    else:
        print("Такого предмета здесь нет.")


def show_inventory():
    if not player_inventory:
        print("Инвентарь пуст.")
    else:
        print("Инвентарь:")
        for item in player_inventory:
            print(f" {item}")


# ======================
# NPC
# ======================
def talk_to_npc(npc):
    if npc not in locations[current_location]["npcs"]:
        print("Здесь нет такого персонажа.")
        return

    if npc == "чудовище":
        print("Чудовище бросается на вас!")
        if battle("чудовище"):
            locations[current_location]["npcs"].remove("чудовище")
        return

    dialogues = {
        "старый мудрец": [
            "Приветствую тебя, путник.",
            "На востоке — сокровища.",
            "Но на западе таится зло."
        ]
    }

    for line in dialogues.get(npc, []):
        print(f"{npc}: {line}")
        time.sleep(1)


# ======================
# СОХРАНЕНИЕ
# ======================
def save_game():
    state = {
        "location": current_location,
        "inventory": player_inventory,
        "locations": locations
    }
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    print("Игра сохранена.")


def load_game():
    global current_location, player_inventory, locations
    try:
        with open("save.json", "r", encoding="utf-8") as f:
            state = json.load(f)
        current_location = state["location"]
        player_inventory = state["inventory"]
        locations = state["locations"]
        print("Игра загружена.")
        show_location()
    except FileNotFoundError:
        print("Сохранение не найдено.")


# ======================
# ПОМОЩЬ
# ======================
def show_help():
    print("""
север / юг / восток / запад — движение
взять <предмет>
инвентарь
поговорить с <персонаж>
сохранить / загрузить
выход
""")


# ======================
# ИГРОВОЙ ЦИКЛ
# ======================
def main_game_loop():
    global game_running
    show_location()

    while game_running:
        cmd = input("\n> ").lower().strip()

        if cmd in ["выход", "exit"]:
            game_running = False

        elif cmd == "помощь":
            show_help()

        elif cmd in ["север", "юг", "восток", "запад"]:
            move(cmd)

        elif cmd.startswith("взять "):
            take_item(cmd[6:])

        elif cmd == "инвентарь":
            show_inventory()

        elif cmd.startswith("поговорить с "):
            talk_to_npc(cmd[13:])

        elif cmd == "сохранить":
            save_game()

        elif cmd == "загрузить":
            load_game()

        else:
            print("Неизвестная команда.")


# ======================
# ЗАПУСК
# ======================
if __name__ == "__main__":
    show_intro()
    main_game_loop()