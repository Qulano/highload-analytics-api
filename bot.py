import asyncio
import httpx
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN, API_URL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Финансовая аналитика")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start_hendler(message: types.Message):
    await message.answer(
        "👋 Приветствую, Шеф!\n"
        "Я ваш персональный складской аналитик.\n"
        "Нажмите кнопку ниже, чтобы запросить актуальный финансовый отчет:",
        reply_markup=main_keyboard
    )
    
@dp.message(F.text == "📊 Финансовая аналитика")
async def analytics_handler(message: types.Message):
    await message.answer("⏳ Запрашиваю данные из хранилища...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/analytics", timeout=5.0)
            
        if response.status_code == 200:
            data = response.json()
            
            report_text = "📈 **СВОДКА ВЫРУЧКИ ПО КЛИЕНТАМ:**\n\n"
            total_revenue = 0
            
            for client_info in data:
                name = client_info["client_name"]
                orders_count = client_info["total_orders"]
                spent = client_info["total_spent"]
                total_revenue += spent
                
                report_text += f"👤 **{name}**: {orders_count} заказов на сумму **{spent:,} руб.**\n"
                
            report_text += f"\n💰 **ОБЩАЯ ВЫРУЧКА СКЛАДА: {total_revenue:,} руб.**"
            
            await message.answer(report_text, parse_mode="Markdown")
        
        else:
            await message.answer(f"❌ Ошибка API: сервер вернул статус {response.status_code}")
            
    except Exception as e:
        await message.answer("⚠️ Не удалось связаться с сервером FastAPI. Убедитесь, что бэкенд запущен!")
        
async def main():
    print("🤖 Бот успешно запущен и слушает команды...")
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
