import sqlite3

# Создание и подключение к базе данных
connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

# Создание таблицы Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
)
''')

# Очистка таблицы перед заполнением (если требуется)
cursor.execute("DELETE FROM Users")

# Заполнение таблицы 10 записями
users = [
    (f"User{i}", f"example{i}@gmail.com", i * 10, 1000) for i in range(1, 11)
]
cursor.executemany("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)", users)

# Обновление balance у каждой 2-ой записи начиная с 1-ой
cursor.execute("SELECT id FROM Users")
all_ids = [row[0] for row in cursor.fetchall()]
for i, user_id in enumerate(all_ids):
    if i % 2 == 0:  # Индексы начинаются с 0
        cursor.execute("UPDATE Users SET balance = 500 WHERE id = ?", (user_id,))

# Удаление каждой 3-ей записи начиная с 1-ой
cursor.execute("SELECT id FROM Users")
all_ids = [row[0] for row in cursor.fetchall()]
for i, user_id in enumerate(all_ids):
    if i % 3 == 0:  # Индексы начинаются с 0
        cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))

### 1.  Удаление пользователя с id=6
cursor.execute("DELETE FROM Users WHERE id = ?", (6,))

### 2.  Подсчёт общего количества записей
cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]

### 3.  Подсчёт суммы всех балансов
cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]

### 4.  Вывод среднего баланса всех пользователей
if total_users > 0:
    print(all_balances / total_users)
else:
    print("Нет пользователей в базе данных.")

# Сохранение изменений и закрытие подключения
connection.commit()
connection.close()

###   Вывод на консоль:   => 700.0