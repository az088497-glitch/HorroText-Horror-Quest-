def show_branch_end(self):
    """Показать конец ветки"""
    # ... существующий код (показ текста и других кнопок) ...

    # Кнопка 1: Начать игру заново с самого начала
    start_over_btn = tk.Button(
        self.choices_container,
        text="🔄 Начать заново",
        font=("Arial", 11, "bold"),
        bg="#27ae60",  # Зеленый
        fg="white",
        pady=10,
        command=self.start_over
    )
    start_over_btn.pack(pady=5, fill=tk.X, padx=20)

    # Кнопка 2: Вернуться к выбору журналиста
    back_to_journalist_btn = tk.Button(
        self.choices_container,
        text="↪️ Вернуться к выбору журналиста",
        font=("Arial", 11, "bold"),
        bg="#f39c12",  # Оранжевый
        fg="white",
        pady=10,
        command=self.back_to_journalist
    )
    back_to_journalist_btn.pack(pady=5, fill=tk.X, padx=20)

    # Кнопка 3: Попробовать противоположный выбор
    # Определяем, какой выбор был сделан изначально
    initial_choice = self.get_initial_journalist_choice()

    if initial_choice == "talk":
        # Если изначально говорили с журналистом, предлагаем отказаться
        opposite_btn = tk.Button(
            self.choices_container,
            text="🚫 Попробовать: Отказаться от разговора",
            font=("Arial", 11, "bold"),
            bg="#e74c3c",  # Красный
            fg="white",
            pady=10,
            command=lambda: self.try_opposite_choice("refuse")
        )
        opposite_btn.pack(pady=5, fill=tk.X, padx=20)

    elif initial_choice == "refuse":
        # Если изначально отказались, предлагаем поговорить
        opposite_btn = tk.Button(
            self.choices_container,
            text="💬 Попробовать: Поговорить с журналистом",
            font=("Arial", 11, "bold"),
            bg="#3498db",  # Синий
            fg="white",
            pady=10,
            command=lambda: self.try_opposite_choice("talk")
        )
        opposite_btn.pack(pady=5, fill=tk.X, padx=20)

    def show_branch_end(self):
        """Показать конец ветки"""
        # ... существующий код ...

        # Проверяем, какой выбор был у журналиста
        talked_to_journalist = self.did_talk_to_journalist()

        # Кнопка для противоположного выбора
        if talked_to_journalist:
            # Говорили → предлагаем отказаться
            opposite_btn = tk.Button(
                self.choices_container,
                text="🚫 Попробовать ветку: Отказаться от разговора",
                font=("Arial", 11, "bold"),
                bg="#e74c3c",
                fg="white",
                pady=10,
                command=self.try_refuse_journalist
            )
        else:
            # Отказались → предлагаем поговорить
            opposite_btn = tk.Button(
                self.choices_container,
                text="💬 Попробовать ветку: Поговорить с журналистом",
                font=("Arial", 11, "bold"),
                bg="#3498db",
                fg="white",
                pady=10,
                command=self.try_talk_to_journalist
            )
        opposite_btn.pack(pady=5, fill=tk.X, padx=20)

    def did_talk_to_journalist(self):
        """Проверить, говорил ли игрок с журналистом"""
        for item in self.game.choice_history:
            if item["scene"] == "journalist":
                return "Поговорить" in item["choice"]
        return False  # Если не нашли выбор

    def try_talk_to_journalist(self):
        """Попробовать поговорить с журналистом"""
        if messagebox.askokcancel("Новая ветка", "Начать ветку: Поговорить с журналистом?"):
            # Начинаем с разговора с журналистом
            self.game.current_scene = "talk_to_journalist"
            self.update_display()

    def try_refuse_journalist(self):
        """Попробовать отказаться от разговора"""
        if messagebox.askokcancel("Новая ветка", "Начать ветку: Отказаться от разговора?"):
            # Начинаем с отказа от разговора
            self.game.current_scene = "refuse"

            self.update_display()
