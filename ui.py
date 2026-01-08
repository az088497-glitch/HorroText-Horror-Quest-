"""
Модуль графического интерфейса на Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from datetime import datetime


class GameUI:
    """Класс для управления графическим интерфейсом игры"""

    def __init__(self, root, game_engine):
        """
        Инициализация интерфейса

        Args:
            root: Корневое окно Tkinter
            game_engine: Объект игрового движка
        """
        self.root = root
        self.game_engine = game_engine

        # Переменные интерфейса
        self.text_vars = {}
        self.button_widgets = []

        # Инициализация базы данных SQLite
        self.init_database()

        # Создание интерфейса
        self.create_widgets()
        self.update_display()

    def init_database(self):
        """Инициализация базы данных SQLite"""
        try:
            self.conn = sqlite3.connect('data/database.db')
            self.cursor = self.conn.cursor()

            # Создание таблицы для статистики игроков
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS game_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT,
                    final_score INTEGER,
                    choices_count INTEGER,
                    play_time_seconds REAL,
                    end_date TIMESTAMP
                )
            ''')

            # Создание таблицы для детальной статистики
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS choice_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id INTEGER,
                    scene_id TEXT,
                    choice_text TEXT,
                    timestamp TIMESTAMP,
                    FOREIGN KEY (game_id) REFERENCES game_stats (id)
                )
            ''')

            self.conn.commit()
            print("✓ База данных инициализирована")
        except Exception as e:
            print(f"✗ Ошибка инициализации БД: {e}")
            self.conn = None

    def create_widgets(self):
        """Создание виджетов интерфейса"""
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Настройка расширения
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Заголовок
        title_label = ttk.Label(
            main_frame,
            text="Text Horror Quest: Пропавшая Ёлка ИТМО",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # Левая панель - текст истории
        left_frame = ttk.LabelFrame(main_frame, text="История", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))

        # Текстовое поле с прокруткой
        self.story_text = scrolledtext.ScrolledText(
            left_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=("Arial", 11)
        )
        self.story_text.pack(fill=tk.BOTH, expand=True)
        self.story_text.config(state=tk.DISABLED)

        # Центральная панель - выбор действий
        center_frame = ttk.LabelFrame(main_frame, text="Выбор действий", padding="10")
        center_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Фрейм для кнопок выбора
        self.choices_frame = ttk.Frame(center_frame)
        self.choices_frame.pack(fill=tk.BOTH, expand=True)

        # Правая панель - статистика и управление
        right_frame = ttk.LabelFrame(main_frame, text="Статистика", padding="10")
        right_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))

        # Информация об игроке
        self.player_info_text = tk.Text(
            right_frame,
            wrap=tk.WORD,
            width=25,
            height=8,
            font=("Arial", 10)
        )
        self.player_info_text.pack(fill=tk.X, pady=(0, 10))
        self.player_info_text.config(state=tk.DISABLED)

        # Кнопки управления
        buttons_frame = ttk.Frame(right_frame)
        buttons_frame.pack(fill=tk.X)

        ttk.Button(
            buttons_frame,
            text="Сохранить игру",
            command=self.save_game
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            buttons_frame,
            text="Загрузить игру",
            command=self.load_game
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            buttons_frame,
            text="Показать статистику",
            command=self.show_statistics
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            buttons_frame,
            text="О программе",
            command=self.show_about
        ).pack(fill=tk.X, pady=2)

        ttk.Button(
            buttons_frame,
            text="Выход",
            command=self.root.quit
        ).pack(fill=tk.X, pady=2)

        # Фрейм для ввода имени
        name_frame = ttk.Frame(main_frame)
        name_frame.grid(row=2, column=0, columnspan=3, pady=(10, 0), sticky=(tk.W, tk.E))

        ttk.Label(name_frame, text="Ваше имя:").pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(name_frame, width=20)
        self.name_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            name_frame,
            text="Установить имя",
            command=self.set_player_name
        ).pack(side=tk.LEFT)

    def update_display(self):
        """Обновление отображения игры"""
        # Очистка предыдущих виджетов
        for widget in self.choices_frame.winfo_children():
            widget.destroy()

        # Получение текущей сцены
        scene = self.game_engine.get_current_scene()
        scene_text = scene.get("text", "Текст сцены не найден")

        # Замена плейсхолдера имени
        if "{player_name}" in scene_text:
            scene_text = scene_text.replace("{player_name}", self.game_engine.player.name)

        # Обновление текста истории
        self.story_text.config(state=tk.NORMAL)
        self.story_text.delete(1.0, tk.END)
        self.story_text.insert(1.0, scene_text)
        self.story_text.config(state=tk.DISABLED)

        # Создание кнопок выбора
        choices = scene.get("choices", [])

        if not choices:
            # Если нет выборов - игра окончена
            self.show_game_over()
        else:
            for i, choice in enumerate(choices):
                button = ttk.Button(
                    self.choices_frame,
                    text=choice["text"],
                    command=lambda idx=i: self.handle_choice(idx),
                    width=40
                )
                button.pack(pady=5, fill=tk.X)

        # Обновление информации об игроке
        self.update_player_info()

    def handle_choice(self, choice_index):
        """Обработка выбора игрока"""
        if self.game_engine.make_choice(choice_index):
            self.update_display()

            # Проверка завершения игры
            if self.game_engine.is_game_over():
                self.save_final_stats()

    def set_player_name(self):
        """Установка имени игрока"""
        name = self.name_entry.get().strip()
        if name:
            self.game_engine.player.name = name
            messagebox.showinfo("Имя установлено", f"Привет, {name}!")
            self.update_player_info()

    def update_player_info(self):
        """Обновление информации об игроке"""
        player = self.game_engine.player
        stats = self.game_engine.get_game_stats()

        info_text = f"""Игрок: {player.name}
Очки: {player.score}

Статистика:
- Смелость: {player.stats['courage']}
- Интеллект: {player.stats['intelligence']}
- Удача: {player.stats['luck']}
- Расследование: {player.stats['investigation']}

Инвентарь: {', '.join(player.inventory) if player.inventory else 'пуст'}

Всего выборов: {stats['choices_made']}
Время игры: {int(stats['game_duration_seconds'])} сек."""

        self.player_info_text.config(state=tk.NORMAL)
        self.player_info_text.delete(1.0, tk.END)
        self.player_info_text.insert(1.0, info_text)
        self.player_info_text.config(state=tk.DISABLED)

    def save_game(self):
        """Сохранение игры"""
        filename = f"save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        if self.game_engine.save_game(filename):
            messagebox.showinfo("Сохранение", f"Игра сохранена как {filename}")
        else:
            messagebox.showerror("Ошибка", "Не удалось сохранить игру")

    def load_game(self):
        """Загрузка игры"""
        # В реальном приложении здесь был бы диалог выбора файла
        messagebox.showinfo("Загрузка", "Функция загрузки в разработке")

    def show_statistics(self):
        """Показать статистику игры"""
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Статистика игры")
        stats_window.geometry("600x400")

        # Получаем статистику
        stats = self.game_engine.get_game_stats()

        # Создаем график с помощью matplotlib
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))

        # График статистики игрока
        player_stats = stats['player_stats']
        stat_names = list(player_stats.keys())
        stat_values = list(player_stats.values())

        axes[0].bar(stat_names, stat_values, color=['blue', 'green', 'red', 'purple'])
        axes[0].set_title('Статистика игрока')
        axes[0].set_ylabel('Значение')

        # Круговая диаграмма истории выборов
        choice_counts = {}
        for choice in self.game_engine.choices_history:
            scene = choice['scene']
            choice_counts[scene] = choice_counts.get(scene, 0) + 1

        if choice_counts:
            labels = list(choice_counts.keys())
            sizes = list(choice_counts.values())
            axes[1].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            axes[1].set_title('Распределение по сценам')
        else:
            axes[1].text(0.5, 0.5, 'Нет данных о выборах',
                         ha='center', va='center')

        plt.tight_layout()

        # Встраиваем график в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def save_final_stats(self):
        """Сохранение финальной статистики в БД"""
        if not self.conn:
            return

        stats = self.game_engine.get_game_stats()

        try:
            # Сохраняем основную статистику
            self.cursor.execute('''
                INSERT INTO game_stats 
                (player_name, final_score, choices_count, play_time_seconds, end_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                stats['player_name'],
                stats['player_stats'].get('investigation', 0) * 10,
                stats['choices_made'],
                stats['game_duration_seconds'],
                datetime.now().isoformat()
            ))

            game_id = self.cursor.lastrowid

            # Сохраняем детальную статистику выборов
            for choice in self.game_engine.choices_history:
                self.cursor.execute('''
                    INSERT INTO choice_stats 
                    (game_id, scene_id, choice_text, timestamp)
                    VALUES (?, ?, ?, ?)
                ''', (
                    game_id,
                    choice['scene'],
                    choice['choice'],
                    choice['timestamp']
                ))

            self.conn.commit()
            print("✓ Финальная статистика сохранена в БД")
        except Exception as e:
            print(f"✗ Ошибка сохранения статистики: {e}")

    def show_game_over(self):
        """Показать экран завершения игры"""
        messagebox.showinfo(
            "Игра завершена",
            "Поздравляем! Вы завершили квест.\n\n"
            "Ваша статистика сохранена.\n"
            "Спасибо за игру!"
        )

    def show_about(self):
        """Показать информацию о программе"""
        about_text = """Text Horror Quest: Пропавшая Ёлка ИТМО

Версия: 1.0
Разработчик: Команда курса "Основы программирования"

Игра разработана в рамках учебного проекта.
Используемые технологии:
- Python 3.8+
- Tkinter для GUI
- JSON для хранения данных
- SQLite для статистики
- Matplotlib для визуализации

© 2024 Все права защищены."""

        messagebox.showinfo("О программе", about_text)