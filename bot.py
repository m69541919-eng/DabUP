"""DabUP Telegram Mini App launcher bot.

Install:
    python -m pip install -U aiogram

Set BOT_TOKEN as an environment variable before running.
"""
import asyncio
import logging

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

BOT_TOKEN = "8816989537:AAH7snUdU7AX_iziPjm23Rfbdtn6sKPsU_8"
WEBAPP_URL = "https://m69541919-eng.github.io/DabUP/"


bot_dispatcher = Dispatcher()


def app_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🚀 Открыть DabUP",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ]
    )


@bot_dispatcher.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "🎮 <b>Добро пожаловать в DabUP!</b>\n\n"
        "Нажми кнопку ниже, чтобы открыть мини-приложение.",
        reply_markup=app_keyboard(),
    )


@bot_dispatcher.message(Command("play"))
async def play(message: Message) -> None:
    await message.answer("Открывай DabUP 👇", reply_markup=app_keyboard())


@bot_dispatcher.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "Команды бота:\n"
        "/start — главное меню\n"
        "/play — открыть мини-приложение\n"
        "/help — помощь",
        reply_markup=app_keyboard(),
    )


@bot_dispatcher.message()
async def other_messages(message: Message) -> None:
    await message.answer(
        "Чтобы открыть мини-приложение, нажми кнопку ниже или отправь /play.",
        reply_markup=app_keyboard(),
    )


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запустить DabUP"),
            BotCommand(command="play", description="Открыть мини-приложение"),
            BotCommand(command="help", description="Помощь"),
        ]
    )
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="DabUP",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )
    )

    try:
        await bot_dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
