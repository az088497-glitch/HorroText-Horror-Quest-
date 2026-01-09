import sqlite3
import pandas as pd

db = sqlite3.connect("quest.db")
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


