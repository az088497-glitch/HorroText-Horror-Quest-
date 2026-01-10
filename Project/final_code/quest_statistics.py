import sqlite3
from datetime import datetime
import csv

# этот код запускать не нужно для работы квеста, quest.db находится в папке data

class QuestStatistics:
    def __init__(self, db_path="../data/quest.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()

    # создание двух таблиц - players и choices
    def _create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS choices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_id INTEGER NOT NULL,
                scene_id TEXT NOT NULL,
                choice_text TEXT NOT NULL,
                next_scene TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        """)

        self.conn.commit()

    # добавление строки с данными игрока в таблицу players
    def create_player(self, name):
        self.cursor.execute(
            "INSERT INTO players (name, created_at) VALUES (?, ?)",
            (name, datetime.now().isoformat())
        )
        self.conn.commit()
        return self.cursor.lastrowid

    # обновление имени игрока при его вводе в специальное окно
    def update_player_name(self, player_id, name):
        self.cursor.execute(
            "UPDATE players SET name = ? WHERE id = ?",
            (name, player_id)
        )
        self.conn.commit()

    # добавление строки с выборами игрока с таблицу choices
    def save_choice(self, player_id, scene_id, choice_text, next_scene):
        self.cursor.execute("""
            INSERT INTO choices (
                player_id, scene_id, choice_text, next_scene, timestamp
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            player_id,
            scene_id,
            choice_text,
            next_scene,
            datetime.now().isoformat()
        ))
        self.conn.commit()

    # извлечение из choices выборов текущего игрока
    def get_choices_history(self, player_id):
        self.cursor.execute("""
            SELECT * FROM choices
            WHERE player_id = ?
            ORDER BY id
        """, (player_id,))
        return self.cursor.fetchall()

    # функция отката к заданной сцене
    def rollback_to_scene(self, player_id, scene_id):
        self.cursor.execute("""
            DELETE FROM choices
            WHERE player_id = ?
            AND id > (
                SELECT id FROM choices
                WHERE player_id = ?
                AND scene_id = ?
                ORDER BY id DESC
                LIMIT 1
            )
        """, (player_id, player_id, scene_id))
        self.conn.commit()

    # функция сохранения в scv истории прохождения текущего игрока
    def export_history_to_csv(self, player_id, filename=None):
        self.cursor.execute("""
            SELECT * FROM choices
            WHERE player_id = ?
            ORDER BY id
        """, (player_id,))
        rows = self.cursor.fetchall()
        if not rows:
            return None

        columns = [description[0] for description in self.cursor.description]

        if filename is None:
            # создание имени файла по игроку и дате
            filename = f"../data/history_player_{player_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            for row in rows:
                writer.writerow([row[col] for col in columns])

        return filename

    def close(self):
        self.conn.close()

