import asyncio
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from dotenv import load_dotenv
from utils.db import add_user, delete_user, get_all_user_ids, init_db

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_PASSWORD = os.getenv("ADMIN_PASS")  # пароль для /kick и /users

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))  # type: ignore
dp = Dispatcher()

init_db()


@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    add_user(message.from_user.id)  # type: ignore
    await message.answer(
        "✅ Привет! Ты подключён к анонимному чату. Пиши сообщение, и я отправлю его другим."
    )


@dp.message(Command("users"))
async def show_users(message: types.Message):
    try:
        args = message.text.replace("/users", "", 1).strip().split()  # type: ignore
        if len(args) != 1:
            raise ValueError("Неверное количество аргументов.")
        if args[0] != ADMIN_PASSWORD:
            raise PermissionError("Неверный пароль.")

        users = get_all_user_ids()
        if not users:
            return await message.answer("📭 Пользователей нет.")
        await message.answer("📋 Пользователи:\n" + "\n".join(map(str, users)))
    except PermissionError:
        await message.answer("❌ Неверный пароль.")
    except Exception:
        await message.answer("⚠️ Неверная команда. Используй: /users &lt;пароль&gt;")


@dp.message(Command("kick"))
async def kick_user(message: types.Message):
    try:
        args = message.text.replace("/kick", "", 1).strip().split()  # type: ignore
        if len(args) != 2:
            raise ValueError("Неверное количество аргументов.")
        user_id_str, password = args

        if password != ADMIN_PASSWORD:
            raise PermissionError("Неверный пароль.")

        user_id = int(user_id_str)  # может бросить ValueError

        delete_user(user_id)
        await message.answer(f"✅ Пользователь {user_id} удалён из базы.")
    except ValueError:
        await message.answer(
            "⚠️ Используй: /kick &lt;user_id&gt; &lt;пароль&gt; (user_id должен быть числом)"
        )

    except PermissionError:
        await message.answer("❌ Неверный пароль.")
    except Exception:
        await message.answer("⚠️ Неверная команда. Используй: /kick <user_id> <пароль>")


@dp.message(F.text)
async def handle_message(message: types.Message):
    sender_id = message.from_user.id  # type: ignore
    add_user(sender_id)

    recipients = get_all_user_ids(exclude_id=sender_id)
    if not recipients:
        return await message.answer("❗ Нет других участников чата.")

    error_shown = False  # флаг, чтобы показать ошибку один раз

    for user_id in recipients:
        try:
            await bot.send_message(user_id, f"\n{message.text}")  # type: ignore
        except Exception:
            if not error_shown:
                await message.answer(
                    "❗ Не удалось отправить сообщение нескольким участникам."
                )
                error_shown = True

    if not error_shown:
        await message.answer("✅ Сообщение отправлено.")


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    sender_id = message.from_user.id  # type: ignore
    add_user(sender_id)

    recipients = get_all_user_ids(exclude_id=sender_id)
    if not recipients:
        return await message.answer("❗ Нет других участников чата.")

    error_shown = False
    for user_id in recipients:
        try:
            await bot.send_photo(
                chat_id=user_id,  # type: ignore
                photo=message.photo[-1].file_id,  # type: ignore
                caption=message.caption or "",
            )
        except Exception:
            delete_user(user_id)  # type: ignore
            if not error_shown:
                await message.answer(
                    f"❗ Ошибка при отправке фото. Пользователь {user_id} удалён из базы."
                )
                error_shown = True

    if not error_shown:
        await message.answer("✅ Фото отправлено.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
