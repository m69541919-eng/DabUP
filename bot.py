"""
DabUP — Telegram-бот, который открывает мини-апп с играми.

Установка:   pip install -U aiogram
Запуск:      BOT_TOKEN=123:ABC WEBAPP_URL=https://твой-домен.com/ python bot.py

WEBAPP_URL — HTTPS-ссылка на папку, где лежат index.html и style.css
(GitHub Pages, Vercel, Netlify, свой сервер и т.д.).
"""
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    MenuButtonWebApp,
    Message,
    WebAppInfo,
)

BOT_TOKEN = os.getenv("BOT_TOKEN", "ВСТАВЬ_ТОКЕН_СЮДА")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://example.com/")

# ---------- тексты сообщений бота ----------
TEXT_START = (
    "🎰 <b>Добро пожаловать в DabUP!</b>\n\n"
    "Баланс стартует с нуля. Открой бесплатный ежедневный кейс "
    "(от 0 до 15 монет) и играй:\n"
    "🪙 Монетка\n"
    "🎲 Кости\n"
    "7️⃣ Слоты\n"
    "🚀 Ракета\n"
    "⚡ Апгрейд: умножь монеты на колесе\n\n"
    "Нажми зелёную кнопку 👇"
)
TEXT_HELP = (
    "ℹ️ <b>Как это работает</b>\n\n"
    "• Баланс начинается с 0\n"
    "• Бесплатный кейс можно открыть раз в 24 часа: 0–15 монет\n"
    "• В «Апгрейде» выбери множитель: чем он больше, тем меньше шанс\n\n"
    "Команды: /start, /play, /about"
)
TEXT_ABOUT = (
    "🎲 <b>DabUP</b> — развлекательное мини-приложение.\n\n"
    "Игры идут на виртуальные монеты. Реальных денег в DabUP нет: "
    "выигрыш нельзя вывести или обменять."
)
TEXT_PLAY = "Готов? Жми кнопку 👇"
TEXT_OTHER = "Я открываю игры DabUP. Нажми кнопку ниже 👇"


def play_keyboard() -> InlineKeyboardMarkup:
    # style="success" — зелёная кнопка (Bot API 9.4+). В старых клиентах кнопка будет обычной.
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🎰 Играть в DabUP",
                web_app=WebAppInfo(url=WEBAPP_URL),
                style="success",
            )
        ]]
    )


dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(m: Message):
    await m.answer(TEXT_START, reply_markup=play_keyboard())


@dp.message(Command("play"))
async def cmd_play(m: Message):
    await m.answer(TEXT_PLAY, reply_markup=play_keyboard())


@dp.message(Command("help"))
async def cmd_help(m: Message):
    await m.answer(TEXT_HELP, reply_markup=play_keyboard())


@dp.message(Command("about"))
async def cmd_about(m: Message):
    await m.answer(TEXT_ABOUT, reply_markup=play_keyboard())


@dp.message()
async def any_message(m: Message):
    await m.answer(TEXT_OTHER, reply_markup=play_keyboard())


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить DabUP"),
        BotCommand(command="play", description="Открыть игры"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="about", description="О проекте"),
    ])
    # кнопка «DabUP» слева от поля ввода тоже открывает мини-апп
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(text="DabUP", web_app=WebAppInfo(url=WEBAPP_URL))
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
