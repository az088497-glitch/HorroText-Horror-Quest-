import sqlite3
import pandas as pd
from duckdb.duckdb import query

# это вспомогательный файл для проверки работы БД SQLite

db = sqlite3.connect("../data/quest.db")
cursor = db.cursor()

def show_players():
    df = pd.read_sql_query("SELECT * FROM players;", db)
    print(df.to_string(index=False))


def show_choices():
    df = pd.read_sql_query("SELECT * FROM choices;", db)
    print(df.to_string(index=False))

show_players()
print()
show_choices()

# функция для очистки БД

# def delete_all_data():
#     cursor.execute("DELETE FROM choices")
#     cursor.execute("DELETE FROM players")
#     db.commit()
#     print("Данные удалены")
#
# delete_all_data()
