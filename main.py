from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Define conversation states
CHOOSING, COMPANY, EMPLOYEE = range(3)

# Global variables to store user input
user_data = {}

# Function to start the conversation
def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Привет! Этот бот поможет вам зарегистрироваться как компания или работник. "
        "Используйте /register, чтобы начать."
    )
    return CHOOSING

# Function to handle the /register command
def register(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(
        "Выберите, кто вы: компания или работник?",
        reply_markup={
            "keyboard": [["Компания", "Работник"]],
            "one_time_keyboard": True,
            "resize_keyboard": True,
        },
    )
    return CHOOSING

# Function to handle the choice of company or employee
def choose_type(update: Update, context: CallbackContext) -> int:
    user_data["type"] = update.message.text
    update.message.reply_text(f"Вы выбрали: {user_data['type']}. Теперь укажите {user_data['type']}.\n"
                              "Введите название:")

    return COMPANY if user_data["type"] == "Компания" else EMPLOYEE

# Function to handle user input during registration
def process_input(update: Update, context: CallbackContext) -> int:
    user_input = update.message.text
    user_data["input"] = user_input

    # Ask for additional information based on user type
    if user_data["type"] == "Компания":
        prompts = ["Индустрия", "Описание", "Контактное лицо", "Email", "Телефон"]
    else:  # "Работник"
        prompts = ["Имя", "Фамилия", "Должность", "Зарплата", "Email", "Телефон"]

    next_prompt(update, prompts)
    return COMPANY if user_data["type"] == "Компания" else EMPLOYEE

# Function to handle the end of the registration process
def end_registration(update: Update, context: CallbackContext) -> int:
    update.message.reply_text(f"Регистрация {user_data['type']} завершена!\n\n"
                              f"Ваше название: {user_data['input']}\n"
                              f"Ваши данные: {user_data}")

    # Here you can save the registration information to your database
    # For example, user_data["type"], user_data["input"], etc.

    user_data.clear()  # Clear user_data for the next registration
    return ConversationHandler.END

# Function to prompt the user for the next information
def next_prompt(update: Update, prompts: list):
    if prompts:
        prompt = prompts.pop(0)
        update.message.reply_text(f"Введите {prompt}:")
    else:
        end_registration(update, None)

def main():
    # Set up the Telegram bot
    updater = Updater("6318182674:AAEEnk6kg86nnwcCpX3VZPz_K2G-iy_ms5M", use_context=True)
    dp = updater.dispatcher

    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(Filters.regex(r'^(Компания|Работник)$'), choose_type)],
            COMPANY: [MessageHandler(Filters.text & ~Filters.command, process_input)],
            EMPLOYEE: [MessageHandler(Filters.text & ~Filters.command, process_input)],
        },
        fallbacks=[MessageHandler(Filters.text & ~Filters.command, process_input)],
    )

    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
