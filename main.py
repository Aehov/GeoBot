import os
import telebot

from dotenv import load_dotenv
from telebot.apihelper import ApiTelegramException

from game_modes.capitals_game import play_capitals
from game_modes.population_game import play_population
from game_modes.flags_game import play_flags

load_dotenv()
TOKEN_BOT = os.getenv('TOKEN_BOT')

try:
    bot = telebot.TeleBot(TOKEN_BOT)
except ApiTelegramException as e:
    print(f"Connection failure: {e}")

users: dict = {}

def set_commands() -> None:
    bot.set_my_commands([
        telebot.types.BotCommand("/start", "Инициализировать БОТ"),
        telebot.types.BotCommand("/capitals", "Режим соревнования столиц"),
        telebot.types.BotCommand("/population", "Режим «Больше-меньше»"),
        telebot.types.BotCommand("/flags", "Конкурс флагов"),
        telebot.types.BotCommand("/back", "Выйти из игрового режима"),
        telebot.types.BotCommand("/help", "Что может этот бот?")
    ])

@bot.message_handler(commands=["start"])
def start(message) -> None:
    users[message.chat.id] = {'hits': 0, 'index' : []}
    bot.send_message(message.chat.id, "Добро пожаловать, выбери режим игры. \n"
        "\n"
        "/capitals   : Классический игровой режим\n"
        "/population : Режим «Больше-меньше»\n"
        "/flags      : Конкурс флагов")

@bot.message_handler(commands=["help"])
def bot_help(message) -> None:
    bot.send_message(message.chat.id, "Тренируйте вместе с БОТом свои географические навыки в 3 игровых режимах.\n"
        "\n"
        "/capitals   : Классический игровой режим\n"
        "/population : Режим «Больше-меньше»\n"
        "/flags      : Конкурс флагов\n"
        "\n"
        "Используйте /back, чтобы выйти из текущего режима игры.\n"
        "\n"
        "На сколько вопросов подряд вы сможете ответить? У вас есть 5 секунд на вопрос, так что дерзайте!")

@bot.message_handler(commands=["capitals"])
def capitals(message) -> None:
    play_capitals(message, bot, users[message.chat.id])

@bot.message_handler(commands=["population"])
def population(message) -> None:
    play_population(message, bot, users[message.chat.id])

@bot.message_handler(commands=["flags"])
def flags(message) -> None:
    play_flags(message, bot, users[message.chat.id])

@bot.message_handler(commands=["back"])
def back(message) -> None:
    
    bot.send_message(message.chat.id, "Ни один игровой режим не активирован\n"
        "Select one\n"
        "\n"
        "/capitals   : Классический игровой режим\n"
        "/population : Режим «Больше-меньше»\n"
        "/flags      : Конкурс флагов\n"
        "\n")

# ------------- MAIN ------------- #
if __name__ == '__main__':
    print("Init BOT...")
    set_commands()
    try:
        bot.infinity_polling()
    except ApiTelegramException as e:
        print(f"Connection failure: {e}")