import telebot

TOKEN = "8410896801:AAEKn7cWHPPkoKFC1alFO_dOSJKaydy0ZEM"
MECHANIC_ID = -1003390990232

bot = telebot.TeleBot(TOKEN)

# Храним временные данные водителя
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Нажми кнопку ниже чтобы начать запись.",
        reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add("📝 Начать запись")
    )

@bot.message_handler(func=lambda msg: msg.text == "📝 Начать запись")
def ask_truck(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Введите номер трака:")
    bot.register_next_step_handler(message, ask_name)

def ask_name(message):
    user_data[message.chat.id]["truck"] = message.text
    bot.send_message(message.chat.id, "Введите ваше имя:")
    bot.register_next_step_handler(message, ask_mileage)

def ask_mileage(message):
    user_data[message.chat.id]["name"] = message.text
    bot.send_message(message.chat.id, "Введите пробег (в милях):")
    bot.register_next_step_handler(message, send_to_mechanic)

def send_to_mechanic(message):
    user_data[message.chat.id]["mileage"] = message.text

    text = (
        "🔧 *Новая заявка!*\n\n"
        f"🚚 Трак: *{user_data[message.chat.id]['truck']}*\n"
        f"👤 Имя: *{user_data[message.chat.id]['name']}*\n"
        f"📍 Пробег: *{user_data[message.chat.id]['mileage']}*\n\n"
        "Введите дату и время обслуживания:"
    )

    bot.send_message(
        MECHANIC_ID,
        text,
        parse_mode="Markdown"
    )

    bot.send_message(
        message.chat.id,
        "Спасибо! 🕘 Механик подтвердит время и вы получите уведомление."
    )

    # Сохраняем ID водителя для ответа
    user_data["last_driver"] = message.chat.id


@bot.message_handler(func=lambda msg: True)
def mechanic_reply(message):
    # Механик пишет дату/время → бот отправляет водителю
    if message.chat.id == MECHANIC_ID and "last_driver" in user_data:
        driver = user_data["last_driver"]
        bot.send_message(
            driver,
            f"✅ Ваша запись подтверждена!\n\n📅 {message.text}"
        )
        bot.send_message(MECHANIC_ID, "Готово! Сообщение отправлено водителю.")

bot.polling(none_stop=True)