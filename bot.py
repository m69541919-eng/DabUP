"""DabUP Telegram bot that opens the static Mini App.

Install:  python -m pip install -r requirements.txt
Run:     BOT_TOKEN=<token-from-BotFather> python bot.py

Set WEBAPP_URL to the HTTPS URL hosting index.html (optional; defaults to
this project's GitHub Pages URL).
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

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv(
    "WEBAPP_URL", "https://m69541919-eng.github.io/DabUP/"
)

if not BOT_TOKEN:
    raise RuntimeError("Set the BOT_TOKEN environment variable using a fresh token from BotFather.")
if not WEBAPP_URL.startswith("https://"):
    raise RuntimeError("WEBAPP_URL must be an HTTPS URL.")

TEXT_START = (
    "🎮 <b>Добро пожаловать в DabUP!</b>\n\n"
    "Открой мини-приложение с играми на виртуальные монеты. "
    "Нажми кнопку ниже 👇"
)
TEXT_HELP = (
    "ℹ️ <b>Как это работает</b>\n\n"
    "Открой DabUP кнопкой ниже. Монеты виртуальные и не имеют денежной ценности."
)
TEXT_ABOUT = (
    "🎮 <b>DabUP</b> — развлекательное мини-приложение.\n\n"
    "Монеты виртуальные: их нельзя вывести или обменять на деньги."
)


def play_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎮 Играть в DabUP", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
    )


dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(TEXT_START, reply_markup=play_keyboard())


@dp.message(Command("play"))
async def cmd_play(message: Message) -> None:
    await message.answer("Готов? Жми кнопку 👇", reply_markup=play_keyboard())


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(TEXT_HELP, reply_markup=play_keyboard())


@dp.message(Command("about"))
async def cmd_about(message: Message) -> None:
    await message.answer(TEXT_ABOUT, reply_markup=play_keyboard())


@dp.message()
async def any_message(message: Message) -> None:
    await message.answer("Я открываю игры DabUP. Нажми кнопку ниже 👇", reply_markup=play_keyboard())


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Запустить DabUP"),
                BotCommand(command="play", description="Открыть игры"),
                BotCommand(command="help", description="Помощь"),
                BotCommand(command="about", description="О проекте"),
            ]
        )
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="DabUP", web_app=WebAppInfo(url=WEBAPP_URL)
            )
        )
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
