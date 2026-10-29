import asyncpg
from config import  DB_CONFIG

db_pool = None

async def init_db_pool():
    global db_pool
    db_pool = await asyncpg.create_pool(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        min_size=5,
        max_size=20
    )
    print("Асинхронный пул соединений с PostgreSQL успешно запущен")
    
async def close_db_pool():
    global db_pool
    if db_pool:
        await db_pool.close()
        print("Пул соединений закрыт")
        
def get_db_pool():
    return db_pool