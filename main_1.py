# main.py
import json
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
from PIL import Image, ImageTk  # Установите: pip install Pillow #добавить эти библиотеки в отчет


class QuestGame:
    """Упрощенный класс игры"""
    def __init__(self, story_json):
        self.story = story_json
        self.current_scene = "start"
        self.player_name = ""
        self.choice_history = []

    def get_current_scene(self):
        """Получение текущей сцены"""
        return self.story.get(self.current_scene, {})

    def set_player_name(self, name):
        """Установка имени игрока"""
        if name and name.strip():
            self.player_name = name.strip()

    def make_choice(self, choice_index):
        """Обработка выбора игрока"""
        scene = self.get_current_scene()
        choices = self.get_available_choices(scene)

        if not choices or not (0 <= choice_index < len(choices)):
            return False

        choice = choices[choice_index]
        choice_text = choice.get("text", "")

        # Сохраняем в историю
        self.choice_history.append({
            "scene": self.current_scene,
            "choice": choice_text
        })

        # Переход к следующей сцене
        next_scene = choice.get("next")
        if next_scene in self.story:
            self.current_scene = next_scene
            return True

        return False

    def get_available_choices(self, scene):
        """Получение доступных выборов для сцены"""
        if "choices" not in scene:
            return []

        choices = scene["choices"]

        # Обработка сложных выборов
        if isinstance(choices, dict):
            # Используем default варианты
            variants = choices.get("variants", {})
            return variants.get("default", [])

        # Обычные выборы
        return choices if isinstance(choices, list) else []

    def get_journalist_choice(self):
        """Получить выбор у журналиста"""
        for item in self.choice_history:
            if item["scene"] == "journalist":
                if "Поговорить" in item["choice"]:
                    return "talk"
                elif "Отказаться" in item["choice"]:
                    return "refuse"
        return None

    def reset_game(self):
        """Сброс игры"""
        self.current_scene = "start"
        self.choice_history = []
        self.player_name = ""


class QuestGameUI:
    """Графический интерфейс игры с новогодним дизайном"""

    def __init__(self, root, story_json, image_path=None):
        self.root = root
        self.root.title("🎄 Текстовый квест: Пропавшая ёлка ИТМО 🎄")

        # Новогодние цвета
        self.colors = {
            "bg_dark": "#0c1a2d",  # Темно-синий (ночное небо)
            "bg_medium": "#1a2d4a",  # Средний синий
            "bg_light": "#2d4a6a",  # Светло-синий
            "accent_green": "#2d7d46",  # Еловый зеленый
            "accent_red": "#c93c3c",  # Ягодный красный
            "accent_gold": "#d4af37",  # Золотой
            "text_light": "#ffffff",  # Белый
            "text_dim": "#b0c4de",  # Светло-стальной
            "snow_white": "#f0f8ff",  # Снежно-белый
            "pine_green": "#0d5c36",  # Темно-зеленый (хвоя)
            "berry_red": "#b90e0e",  # Ярко-красный
            "ice_blue": "#a0d2f7"  # Ледяной голубой
        }

        # Установка размера окна
        window_width = 850
        window_height = 700

        # Получение размеров экрана
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Центрирование окна
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Установка новогоднего фона
        self.root.configure(bg=self.colors["bg_dark"])

        self.story_json = story_json
        self.game = QuestGame(story_json)
        self.image_path = image_path  # Путь к изображению

        # Загрузка изображения
        self.title_image = None
        if image_path:
            self.load_title_image()

        self.create_widgets()
        self.update_display()

    def load_title_image(self):
        """Загрузка заглавного изображения"""
        try:
            pil_image = Image.open(self.image_path)
            # Ресайз для оптимального отображения
            pil_image = pil_image.resize((800, 200), Image.Resampling.LANCZOS)
            self.title_image = ImageTk.PhotoImage(pil_image)
        except Exception as e:
            print(f"Не удалось загрузить изображение: {e}")
            self.title_image = None

    def create_widgets(self):
        """Создание виджетов с новогодним дизайном"""
        main_container = tk.Frame(self.root, bg=self.colors["bg_dark"])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # === ЗАГОЛОВОЧНОЕ ИЗОБРАЖЕНИЕ ===
        if self.title_image:
            # Рамка для изображения с новогодним стилем
            img_frame = tk.Frame(
                main_container,
                bg=self.colors["pine_green"],
                relief=tk.RAISED,
                borderwidth=3
            )
            img_frame.pack(fill=tk.X, pady=(0, 15))

            # Само изображение
            img_label = tk.Label(
                img_frame,
                image=self.title_image,
                bg=self.colors["pine_green"]
            )
            img_label.pack(pady=5, padx=5)

            # Украшение под изображением
            decoration = tk.Label(
                img_frame,
                text="✦ ⋆⋅☆⋅⋆ ✦ ⋆⋅☆⋅⋆ ✦ ⋆⋅☆⋅⋆ ✦",
                font=("Arial", 12),
                bg=self.colors["pine_green"],
                fg=self.colors["accent_gold"]
            )
            decoration.pack(pady=(0, 5))
        else:
            # Альтернативный красивый заголовок
            title_frame = tk.Frame(
                main_container,
                bg=self.colors["bg_dark"],
                height=80
            )
            title_frame.pack(fill=tk.X, pady=(0, 15))

            # Украшение сверху
            tk.Label(
                title_frame,
                text="🎄 ✧･ﾟ:*✧･ﾟ:*  *:･ﾟ✧*:･ﾟ✧ 🎄",
                font=("Arial", 14),
                bg=self.colors["bg_dark"],
                fg=self.colors["accent_gold"]
            ).pack(pady=(10, 5))

            # Главный заголовок
            tk.Label(
                title_frame,
                text="ПРОПАВШАЯ ЁЛКА ИТМО",
                font=("Georgia", 24, "bold"),
                bg=self.colors["bg_dark"],
                fg=self.colors["snow_white"]
            ).pack(pady=5)

            # Подзаголовок
            tk.Label(
                title_frame,
                text="Новогодний детективный квест",
                font=("Arial", 12, "italic"),
                bg=self.colors["bg_dark"],
                fg=self.colors["ice_blue"]
            ).pack(pady=(0, 10))

            # Украшение снизу
            tk.Label(
                title_frame,
                text="🎄 ✧･ﾟ:*✧･ﾟ:*  *:･ﾟ✧*:･ﾟ✧ 🎄",
                font=("Arial", 14),
                bg=self.colors["bg_dark"],
                fg=self.colors["accent_gold"]
            ).pack()

        # === ПАНЕЛЬ ИСТОРИИ ===
        story_frame = tk.LabelFrame(
            main_container,
            text=" 📖 ИСТОРИЯ ",
            font=("Arial", 11, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_light"],
            relief=tk.GROOVE,
            borderwidth=2,
            labelanchor='n'
        )
        story_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.story_text = scrolledtext.ScrolledText(
            story_frame,
            wrap=tk.WORD,
            font=("Georgia", 12),
            bg=self.colors["snow_white"],
            fg="#1a1a2e",
            height=12,
            padx=20,
            pady=20,
            relief=tk.SUNKEN,
            borderwidth=1,
            insertbackground=self.colors["accent_red"]
        )
        self.story_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.story_text.config(state=tk.DISABLED)

        # Декоративная рамка вокруг текста
        story_frame.config(
            highlightbackground=self.colors["accent_green"],
            highlightcolor=self.colors["accent_green"],
            highlightthickness=1
        )

        # === ПАНЕЛЬ ВЫБОРА ===
        choices_frame = tk.LabelFrame(
            main_container,
            text=" 🎯 ВАШ ВЫБОР ",
            font=("Arial", 11, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["text_light"],
            relief=tk.RIDGE,
            borderwidth=2,
            labelanchor='n'
        )
        choices_frame.pack(fill=tk.BOTH, pady=(0, 10))

        self.choices_container = tk.Frame(
            choices_frame,
            bg=self.colors["bg_medium"]
        )
        self.choices_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

    def update_display(self):
        """Обновление отображения игры"""
        # Очистка старых кнопок
        for widget in self.choices_container.winfo_children():
            widget.destroy()

        # Получение текущей сцены
        scene = self.game.get_current_scene()

        # Получение текста сцены
        scene_text = scene.get("text", "")
        if not scene_text:
            scene_text = "Текст сцены не найден"

        # Замена имени игрока в тексте
        if self.game.player_name:
            # Заменяем плейсхолдеры для имени
            scene_text = scene_text.replace("{player_name}", self.game.player_name)
            if "Добрый день!" in scene_text:
                scene_text = scene_text.replace("Добрый день!", f"Добрый день, {self.game.player_name}!")

        # Обновление текста истории
        self.story_text.config(state=tk.NORMAL)
        self.story_text.delete(1.0, tk.END)

        # Специальное форматирование для новостной статьи
        if "МЕСТЬ ЛЕСНИКА" in scene_text:
            self.story_text.insert(1.0, scene_text)
            self.story_text.tag_add("headline", "1.0", "1.lineend")
            self.story_text.tag_config("headline",
                                       font=("Georgia", 14, "bold"),
                                       foreground=self.colors["berry_red"]
                                       )
        else:
            self.story_text.insert(1.0, scene_text)

        self.story_text.config(state=tk.DISABLED)

        # Получаем доступные выборы
        choices = self.game.get_available_choices(scene)

        # Проверяем тип сцены
        scene_type = scene.get("type", "")

        # Обработка специальных сцен
        if scene_type == "game_over":
            self.show_end_screen("💀 ВЫ ПОТЕРЯЛИ СОЗНАНИЕ\n\nКонец игры", self.colors["accent_red"])
        elif scene_type == "final":
            self.show_end_screen("🎉 ПОЗДРАВЛЯЕМ!\n\nВы закончили прохождение квеста", self.colors["accent_green"])
        elif self.game.current_scene == "player_name":
            # Специальная обработка сцены запроса имени
            self.show_name_input()
        elif choices and len(choices) > 0:
            # Есть выборы - показываем стилизованные кнопки
            self.show_choices(choices)
        else:
            # Нет выборов - это конец ветки
            self.show_branch_end()

        # Прокрутка к началу
        self.story_text.see(1.0)

    def show_name_input(self):
        """Стилизованное поле для ввода имени"""
        name_frame = tk.Frame(
            self.choices_container,
            bg=self.colors["bg_medium"],
            pady=20
        )
        name_frame.pack()

        tk.Label(
            name_frame,
            text="✨ ВАШЕ ИМЯ ✨",
            font=("Arial", 12, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["accent_gold"]
        ).pack(pady=(0, 10))

        # Декоративная рамка для поля ввода
        entry_frame = tk.Frame(
            name_frame,
            bg=self.colors["accent_green"],
            relief=tk.RAISED,
            borderwidth=2
        )
        entry_frame.pack(pady=10)

        name_entry = tk.Entry(
            entry_frame,
            font=("Arial", 12),
            width=25,
            bg=self.colors["snow_white"],
            fg=self.colors["bg_dark"],
            relief=tk.FLAT,
            justify='center'
        )
        name_entry.pack(pady=3, padx=3)

        # Стилизованная кнопка подтверждения
        submit_btn = tk.Button(
            name_frame,
            text="🎄 НАЧАТЬ ИСТОРИЮ 🎄",
            font=("Arial", 11, "bold"),
            bg=self.colors["berry_red"],
            fg=self.colors["text_light"],
            activebackground=self.colors["accent_red"],
            activeforeground=self.colors["text_light"],
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=8,
            cursor="hand2",
            command=lambda: self.submit_name(name_entry.get())
        )
        submit_btn.pack(pady=15)

        # Украшение
        tk.Label(
            name_frame,
            text="❄️ ❄️ ❄️",
            font=("Arial", 12),
            bg=self.colors["bg_medium"],
            fg=self.colors["ice_blue"]
        ).pack()

    def submit_name(self, name):
        """Обработка ввода имени"""
        if name and name.strip():
            self.game.set_player_name(name.strip())
            # Переходим к следующей сцене после ввода имени
            self.game.current_scene = "introduction"
            self.update_display()
        else:
            messagebox.showwarning(
                "Внимание",
                "Пожалуйста, введите ваше имя!",
                parent=self.root
            )

    def show_choices(self, choices):
        """Показать стилизованные выборы"""
        for i, choice in enumerate(choices):
            button_text = choice["text"]

            # Цвета кнопок в новогодней тематике
            button_colors = [
                {"bg": self.colors["accent_green"], "fg": self.colors["text_light"]},  # Зеленый
                {"bg": self.colors["berry_red"], "fg": self.colors["text_light"]},  # Красный
                {"bg": self.colors["accent_gold"], "fg": self.colors["bg_dark"]},  # Золотой
                {"bg": self.colors["ice_blue"], "fg": self.colors["bg_dark"]},  # Голубой
            ]

            color = button_colors[i % len(button_colors)]

            # Специальные стили для разных типов кнопок
            if "Продолжить" in button_text:
                color = {"bg": self.colors["pine_green"], "fg": self.colors["text_light"]}
                icon = "➤ "
            elif "Завершить" in button_text:
                color = {"bg": self.colors["berry_red"], "fg": self.colors["text_light"]}
                icon = "🏁 "
            elif any(word in button_text for word in ["Поговорить", "Поискать", "Спросить"]):
                icon = "💬 "
            elif any(word in button_text for word in ["Отказаться", "Убежать", "Уйти"]):
                icon = "🚫 "
            else:
                icons = ["🎯 ", "❄️ ", "✨ ", "🎄 "]
                icon = icons[i % len(icons)]

            # Создание стилизованной кнопки
            button = tk.Button(
                self.choices_container,
                text=f"{icon}{button_text}",
                font=("Arial", 10),
                bg=color["bg"],
                fg=color["fg"],
                activebackground=color["bg"],
                activeforeground=color["fg"],
                relief=tk.RAISED,
                borderwidth=2,
                wraplength=350,
                justify=tk.LEFT,
                padx=15,
                pady=10,
                cursor="hand2",
                command=lambda idx=i: self.handle_choice(idx)
            )

            # Эффект при наведении
            def on_enter(e, btn=button, col=color):
                btn.config(bg=self.lighten_color(col["bg"]))

            def on_leave(e, btn=button, col=color):
                btn.config(bg=col["bg"])

            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)

            button.pack(pady=5, fill=tk.X)

    def lighten_color(self, hex_color, factor=0.2):
        """Осветление цвета для эффекта наведения"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        lighter = tuple(min(int(c * (1 + factor)), 255) for c in rgb)
        return f'#{lighter[0]:02x}{lighter[1]:02x}{lighter[2]:02x}'

    def handle_choice(self, choice_index):
        """Обработка выбора игрока"""
        result = self.game.make_choice(choice_index)

        if result:
            self.update_display()
        else:
            # Если не удалось сделать выбор, показываем конец ветки
            self.show_branch_end()

    def show_end_screen(self, message, color):
        """Показать экран окончания игры"""
        label = tk.Label(
            self.choices_container,
            text=message,
            font=("Arial", 12, "bold"),
            bg=self.colors["bg_medium"],
            fg=color,
            pady=15
        )
        label.pack()

        self.show_end_buttons()

    def show_branch_end(self):
        """Показать конец ветки"""
        label = tk.Label(
            self.choices_container,
            text="🏁 КОНЕЦ ВЕТКИ",
            font=("Arial", 12, "bold"),
            bg=self.colors["bg_medium"],
            fg=self.colors["accent_gold"],
            pady=15
        )
        label.pack()

        self.show_end_buttons()

    def show_end_buttons(self):
        """Показать кнопки в конце игры/ветки"""
        # Кнопка "Начать заново" (уменьшенная)
        start_over_btn = tk.Button(
            self.choices_container,
            text="🔄 НАЧАТЬ ЗАНОВО",
            font=("Arial", 10, "bold"),
            bg=self.colors["pine_green"],
            fg=self.colors["text_light"],
            activebackground=self.lighten_color(self.colors["pine_green"]),
            activeforeground=self.colors["text_light"],
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.start_over
        )
        start_over_btn.pack(pady=5, fill=tk.X, padx=15)

        # Определяем, какой выбор был у журналиста
        journalist_choice = self.game.get_journalist_choice()

        if journalist_choice == "talk":
            # Если говорили с журналистом, предлагаем отказаться
            opposite_btn = tk.Button(
                self.choices_container,
                text="🚫 ПОПРОБОВАТЬ: ОТКАЗАТЬСЯ ОТ РАЗГОВОРА",
                font=("Arial", 10, "bold"),
                bg=self.colors["berry_red"],
                fg=self.colors["text_light"],
                activebackground=self.lighten_color(self.colors["berry_red"]),
                activeforeground=self.colors["text_light"],
                relief=tk.RAISED,
                borderwidth=2,
                padx=20,
                pady=8,
                cursor="hand2",
                command=self.try_refuse_journalist
            )
            opposite_btn.pack(pady=5, fill=tk.X, padx=15)

        elif journalist_choice == "refuse":
            # Если отказались, предлагаем поговорить
            opposite_btn = tk.Button(
                self.choices_container,
                text="💬 ПОПРОБОВАТЬ: ПОГОВОРИТЬ С ЖУРНАЛИСТОМ",
                font=("Arial", 10, "bold"),
                bg=self.colors["accent_green"],
                fg=self.colors["text_light"],
                activebackground=self.lighten_color(self.colors["accent_green"]),
                activeforeground=self.colors["text_light"],
                relief=tk.RAISED,
                borderwidth=2,
                padx=20,
                pady=8,
                cursor="hand2",
                command=self.try_talk_to_journalist
            )
            opposite_btn.pack(pady=5, fill=tk.X, padx=15)

        # Кнопка для просмотра истории
        history_btn = tk.Button(
            self.choices_container,
            text="📊 ПОСМОТРЕТЬ ИСТОРИЮ ВЫБОРОВ",
            font=("Arial", 10),
            bg=self.colors["accent_gold"],
            fg=self.colors["bg_dark"],
            activebackground=self.lighten_color(self.colors["accent_gold"]),
            activeforeground=self.colors["bg_dark"],
            relief=tk.RAISED,
            borderwidth=2,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.show_player_history
        )
        history_btn.pack(pady=5, fill=tk.X, padx=15)

    def start_over(self):
        """Начать игру заново"""
        if messagebox.askokcancel("Начать заново", "Начать игру с самого начала?"):
            self.game.reset_game()
            self.update_display()

    def try_talk_to_journalist(self):
        """Попробовать поговорить с журналистом"""
        if messagebox.askokcancel("Новая ветка", "Начать ветку: Поговорить с журналистом?"):
            self.game.reset_game()
            # Устанавливаем сцену журналиста
            self.game.current_scene = "journalist"
            # Добавляем выбор в историю
            self.game.choice_history.append({
                "scene": "journalist",
                "choice": "Поговорить с журналистом"
            })
            # Переходим к соответствующей сцене
            self.game.current_scene = "talk_to_journalist"
            self.update_display()

    def try_refuse_journalist(self):
        """Попробовать отказаться от разговора"""
        if messagebox.askokcancel("Новая ветка", "Начать ветку: Отказаться от разговора?"):
            self.game.reset_game()
            # Устанавливаем сцену журналиста
            self.game.current_scene = "journalist"
            # Добавляем выбор в историю
            self.game.choice_history.append({
                "scene": "journalist",
                "choice": "Отказаться от разговора"
            })
            # Переходим к соответствующей сцене
            self.game.current_scene = "refuse"
            self.update_display()

    def show_player_history(self):
        """Показать историю выборов"""
        if not self.game.choice_history:
            messagebox.showinfo("История", "Вы еще не сделали ни одного выбора!")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("📊 История ваших выборов")
        history_window.geometry("600x450")
        history_window.configure(bg=self.colors["bg_dark"])

        # Заголовок
        tk.Label(
            history_window,
            text=f"🎄 ИСТОРИЯ: {self.game.player_name if self.game.player_name else 'ИГРОК'} 🎄",
            font=("Georgia", 14, "bold"),
            bg=self.colors["bg_dark"],
            fg=self.colors["accent_gold"],
            pady=15
        ).pack()

        # Декоративная линия
        tk.Label(
            history_window,
            text="─" * 50,
            font=("Arial", 10),
            bg=self.colors["bg_dark"],
            fg=self.colors["ice_blue"]
        ).pack()

        # Текстовая область
        text_frame = tk.Frame(history_window, bg=self.colors["bg_medium"])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        text_widget = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=("Courier New", 10),
            bg=self.colors["snow_white"],
            fg=self.colors["bg_dark"],
            height=15,
            padx=15,
            pady=15,
            relief=tk.SUNKEN,
            borderwidth=1
        )
        text_widget.pack(fill=tk.BOTH, expand=True)

        # Форматирование истории
        history_text = "✨ ВАШИ ВЫБОРЫ ✨\n" + "═" * 45 + "\n\n"
        for i, item in enumerate(self.game.choice_history, 1):
            scene_icon = "🎯" if item["scene"] == "journalist" else "❄️"
            history_text += f"{i:2d}. {scene_icon} {item['scene']}:\n"
            history_text += f"    → {item['choice']}\n"

            if i < len(self.game.choice_history):
                history_text += "    " + "·" * 35 + "\n"

        text_widget.insert(1.0, history_text)
        text_widget.config(state=tk.DISABLED)

        # Кнопка закрытия
        close_btn = tk.Button(
            history_window,
            text="ЗАКРЫТЬ",
            font=("Arial", 10, "bold"),
            bg=self.colors["berry_red"],
            fg=self.colors["text_light"],
            relief=tk.RAISED,
            borderwidth=2,
            padx=30,
            pady=8,
            cursor="hand2",
            command=history_window.destroy
        )
        close_btn.pack(pady=15)

    def run(self):
        """Запуск игры"""
        self.root.mainloop()


def main():
    """Основная функция запуска"""
    try:
        # JSON с историей (ваш полный JSON)
        story_json = {
            "start": {
                "text": "Вечером после работы так не хочется идти на пары — вокруг темно и не видно ничего-ничего. Хочется вместо этого пойти домой, включить новогодний фильм и есть сладости под ёлкой. Но вместо этого вы идете в вуз \n\nПальцы мёрзнут, но вы открываете приложение на телефоне, чтобы посмотреть, где пары. Главный экран приложения приветствует вас по имени: «Добрый день!»",
                "choices": [
                    {"text": "Продолжить", "next": "player_name"}
                ]
            },
            "player_name": {
                "text": "Кстати, как вас зовут? Напишите ваше имя:",
                "choices": []  # Обрабатывается отдельно в show_name_input()
            },
            # ... (вставьте ВЕСЬ ваш JSON сценарий сюда) ...
            # Продолжение вашего JSON должно быть здесь
        }

        root = tk.Tk()

        # === УКАЖИТЕ ПУТЬ К ВАШЕМУ ИЗОБРАЖЕНИЮ ЗДЕСЬ ===
        image_path = "путь/к/вашему/изображению.png"  # Измените на ваш путь

        # Создание и запуск игры
        game = QuestGameUI(root, story_json, image_path)
        game.run()

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось запустить игру:\n{str(e)}")
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    # Установите библиотеку для работы с изображениями:
    # pip install Pillow
    main()