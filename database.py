import asyncpg
from config import DB_CONFIG, REDIS_HOST, REDIS_PORT
import redis.asyncio as aioredis

db_pool = None
redis_client = None

async def init_db_pool():
    global db_pool, redis_client
    db_pool = await asyncpg.create_pool(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        min_size=5,
        max_size=20
    
    )
    redis_client = aioredis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True
    )
    print("""
Асинхронный пул соединений с PostgreSQL успешно запущен
Асинхронный клиент Redis подключен!
""")
    
    
async def close_db_pool():
    global db_pool
    if db_pool:
        await db_pool.close()
        print("Пул соединений закрыт")
        
def get_db_pool():
    return db_pool

def get_redis():
    return redis_client