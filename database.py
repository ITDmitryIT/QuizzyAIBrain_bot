import aiosqlite

# Название базы данных
DB_NAME = "quiz_bot.db"

# Создание таблиц в базе данных
async def create_table():
    async with aiosqlite.connect(DB_NAME) as db:
        # Таблица для хранения состояния квиза
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (
            user_id INTEGER PRIMARY KEY,
            question_index INTEGER
        )''')

        # Таблица для хранения результатов
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_results (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            last_score INTEGER
        )''')
        await db.commit()

# Обновление индекса вопроса для пользователя
async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()

# Получение текущего индекса вопроса для пользователя
async def get_quiz_index(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

# Сохранение результата квиза
async def save_quiz_result(user_id, username, score):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_results (user_id, username, last_score) VALUES (?, ?, ?)', (user_id, username, score))
        await db.commit()

# Получение статистики игроков
async def get_quiz_statistics():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT username, last_score FROM quiz_results ORDER BY last_score DESC') as cursor:
            results = await cursor.fetchall()
            return results