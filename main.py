import pyodbc
import telebot

# Устанавливаем соединение с базой данных
connectionString = ('DRIVER={SQL Server};'
                    'SERVER=DESKTOP-PP1PFRF\SQLEXPRESS;'
                    'DATABASE=TalentConnectDB;'
                    'Trusted_Connection=yes;'  # Использовать Windows аутентификацию
                    )

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
TOKEN = '6318182674:AAEEnk6kg86nnwcCpX3VZPz_K2G-iy_ms5M'

nameCompany = ""
nameEmployee = ""
contactPersonName = ""
jobTitle = ""
salaryForCompany = 0
salaryForEmployee = 0
contactInfo = ""
aboutCompany = ""
aboutEmployee = ""
prospectiveEmployees = ""
isReg = True
# Создаем объект бота
bot = telebot.TeleBot(TOKEN)


def check_existing_data(chat_id, table_name):
    # Check if the chat ID already exists in the database
    conn = pyodbc.connect(connectionString)
    query = f"SELECT * FROM {table_name} WHERE ChatID = ?"
    # Создаем объект курсора для выполнения SQL-запросов
    cursor = conn.cursor()
    cursor.execute(query, (chat_id,))
    existing_user = cursor.fetchone()
    conn.close()
    return existing_user


def update_data_employee(chat_id, new_EmployeeName, new_Salary, new_JobTitle, new_ContactInfo, new_AboutEmployee):
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Employees "
                   f"SET EmployeeName = ?, "
                   f"DesiredSalary = ? ,"
                   f"JobTitle = ? ,"
                   f"ContactInfo = ? ,"
                   f"AboutEmployee = ? "
                   f"WHERE ChatID = ?",
                   (new_EmployeeName,
                    new_Salary,
                    new_JobTitle,
                    new_ContactInfo,
                    new_AboutEmployee,
                    chat_id
                    ))

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()


def update_data_company(chat_id,
                        new_CompanyName,
                        new_ContactPersonName,
                        new_Salary,
                        ContactInfo,
                        new_AboutCompany,
                        new_ProspectiveEmployees):
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Companies "
                   f"SET CompanyName = ?, "
                   f"ContactPersonName = ? ,"
                   f"Salary = ? ,"
                   f"ContactInfo = ? ,"
                   f"AboutCompany = ? ,"
                   f"ProspectiveEmployees = ? "
                   f"WHERE ChatID = ?",
                   (new_CompanyName,
                    new_ContactPersonName,
                    new_Salary,
                    ContactInfo,
                    new_AboutCompany,
                    new_ProspectiveEmployees,
                    chat_id
                    ))

    # Commit the changes to the database
    conn.commit()

    # Close the database connection
    conn.close()


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я твой простой бот.")


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Это простой бот. Введите /start для начала.")


# Обработчик команды /changeemplayee
@bot.message_handler(commands=['changeemplayee'])
def handle_help(message):
    global isReg
    isReg = False
    bot.send_message(message.chat.id, "Введите ФИО:")
    bot.register_next_step_handler(message, name_employee)


# Обработчик команды /changecompany
@bot.message_handler(commands=['changecompany'])
def handle_help(message):
    global isReg
    isReg = False
    bot.send_message(message.chat.id, "Введите Название компании:")
    bot.register_next_step_handler(message, name_company)


# Обработчик команды /dbtestcompanies
@bot.message_handler(commands=['dbtestcompanies'])
def handle_help(message):
    # Создаем объект курсора для выполнения SQL-запросов
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    # Пример выполнения запроса
    cursor.execute('SELECT * FROM Companies')

    # Получаем результат запроса
    for row in cursor:
        bot.send_message(message.chat.id, f"CompanyName: {row[1]}\n"
                                          f"ContactPersonName: {row[2]}\n"
                                          f"Salary: {row[3]}\n"
                                          f"ContactInfo: {row[6]}\n"
                                          f"AboutCompany: {row[7]}\n"
                                          f"ProspectiveEmployees: {row[8]}")

    # Закрываем соединение
    conn.close()


# Обработчик команды /dbtestemployees
@bot.message_handler(commands=['dbtestemployees'])
def handle_help(message):
    # Создаем объект курсора для выполнения SQL-запросов
    conn = pyodbc.connect(connectionString)
    cursor = conn.cursor()

    # Пример выполнения запроса
    cursor.execute('SELECT * FROM Employees')

    # Получаем результат запроса
    for row in cursor:
        bot.send_message(message.chat.id, f"EmployeeName: {row[1]}\n"
                                          f"DesiredSalary: {row[2]}\n"
                                          f"JobTitle: {row[3]}\n"
                                          f"ContactInfo: {row[6]}\n"
                                          f"AboutEmployee: {row[7]}\n")

    # Закрываем соединение
    conn.close()


# NOTE: Добавить возможность отменить и изменить введенные данные
# Обработчик команды /companyregistation
# region @bot.message_handler(commands=['companyregistation'])
@bot.message_handler(commands=['companyregistation'])
def handle_help(message):
    existing_company = check_existing_data(message.chat.id, 'Companies')
    if existing_company:
        bot.send_message(message.chat.id, "You are already registered.")
    else:
        bot.send_message(message.chat.id, "Введите Название компании:")
        bot.register_next_step_handler(message, name_company)


def name_company(message):
    global nameCompany
    nameCompany = message.text.strip()
    bot.send_message(message.chat.id, "Введите Имя Контактного лица:")
    bot.register_next_step_handler(message, contact_person_name)


def contact_person_name(message):
    global contactPersonName
    contactPersonName = message.text.strip()
    bot.send_message(message.chat.id, "Введите Зарплату:")
    bot.register_next_step_handler(message, salary_for_employee)


def salary_for_employee(message):
    try:
        global salaryForEmployee
        salaryForEmployee = int(message.text.strip())

        # Continue with the next step
        bot.send_message(message.chat.id, "Введите контактную информацию (телефон, почта и тд):")
        bot.register_next_step_handler(message, contact_info_company)

    except ValueError:
        # If the user didn't enter a valid number, handle the error
        bot.send_message(message.chat.id, "Пожалуйста, введите корректную сумму зарплаты. Это должно быть число.")
        bot.register_next_step_handler(message, salary_for_employee)


def contact_info_company(message):
    global contactInfo
    contactInfo = message.text.strip()
    bot.send_message(message.chat.id, "Введите Информацию о себе:")
    bot.register_next_step_handler(message, about_company)


def about_company(message):
    global aboutCompany
    aboutCompany = message.text.strip()
    bot.send_message(message.chat.id, "Введите профессии необходимые Вам:")
    bot.register_next_step_handler(message, prospective_employees)


def prospective_employees(message):
    global prospectiveEmployees
    conn = pyodbc.connect(connectionString)
    prospectiveEmployees = message.text.strip()
    bot.send_message(message.chat.id, "Регистрация окончена:\n"
                                      f"Название компании: {nameCompany}\n"
                                      f"Имя Контактного лица: {contactPersonName}\n"
                                      f"Зарплата: {salaryForEmployee}\n"
                                      f"Контактная информация: {contactInfo}\n"
                                      f"Информация о компании: {aboutCompany}\n"
                                      f"Профессии необходимые Вам: {prospectiveEmployees}")
    # Создаем объект курсора для выполнения SQL-запросов
    cursor = conn.cursor()
    if isReg:
        # Пример выполнения запроса
        cursor.execute(
            "INSERT INTO Companies (CompanyName, "
            "ContactPersonName, "
            "Salary, "
            "TelegramUserID, "
            "ChatID, "
            "ContactInfo, "
            "AboutCompany, "
            "ProspectiveEmployees) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (nameCompany,
             contactPersonName,
             salaryForEmployee,
             '@' + message.from_user.username,
             message.chat.id,
             contactInfo,
             aboutCompany,
             prospectiveEmployees))
    else:
        update_data_company(message.chat.id,
                            nameCompany,
                            contactPersonName,
                            salaryForEmployee,
                            contactInfo,
                            aboutCompany,
                            prospectiveEmployees)
    conn.commit()
    # Закрываем соединение
    conn.close()


# endregion

# NOTE: Добавить возможность отменить и изменить введенные данные
# Обработчик команды /employeeregistation
# region @bot.message_handler(commands=['employeeregistation'])
@bot.message_handler(commands=['employeeregistation'])
def handle_help(message):
    existing_employee = check_existing_data(message.chat.id, 'Employees')
    if existing_employee:
        bot.send_message(message.chat.id, "You are already registered.")
    else:
        bot.send_message(message.chat.id, "Введите ФИО:")
        bot.register_next_step_handler(message, name_employee)


def name_employee(message):
    global nameEmployee
    nameEmployee = message.text.strip()
    bot.send_message(message.chat.id, "Введите Зарплату:")
    bot.register_next_step_handler(message, salary_for_company)


def salary_for_company(message):
    try:
        global salaryForCompany
        salaryForCompany = int(message.text.strip())

        # Continue with the next step
        bot.send_message(message.chat.id, "Введите профессию по которой вы можете работать")
        bot.register_next_step_handler(message, job_title)

    except ValueError:
        # If the user didn't enter a valid number, handle the error
        bot.send_message(message.chat.id, "Пожалуйста, введите корректную сумму зарплаты. Это должно быть число.")
        bot.register_next_step_handler(message, salary_for_company)


def job_title(message):
    global jobTitle
    jobTitle = message.text.strip()
    bot.send_message(message.chat.id, "Введите контактную информацию (телефон, почта и тд)::")
    bot.register_next_step_handler(message, contact_info_employee)


def contact_info_employee(message):
    global contactInfo
    contactInfo = message.text.strip()
    bot.send_message(message.chat.id, "Введите Информацию о себе:")
    bot.register_next_step_handler(message, about_employee)


def about_employee(message):
    global aboutEmployee
    aboutEmployee = message.text.strip()
    conn = pyodbc.connect(connectionString)
    global isReg
    bot.send_message(message.chat.id, "Регистрация окончена:\n"
                                      f"ФИО: {nameEmployee}\n"
                                      f"Зарплата: {salaryForCompany}\n"
                                      f"Профессия: {jobTitle}\n"
                                      f"Контактная информация: {contactInfo}\n"
                                      f"Информация о себе: {aboutEmployee}\n")
    # Создаем объект курсора для выполнения SQL-запросов
    cursor = conn.cursor()

    # Пример выполнения запроса
    if isReg:
        cursor.execute(
            "INSERT INTO Employees ("
            "EmployeeName, "
            "DesiredSalary, "
            "JobTitle, "
            "TelegramUserID, "
            "ChatID, "
            "ContactInfo, "
            "AboutEmployee)"
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (nameEmployee,
             salaryForCompany,
             jobTitle,
             '@' + message.from_user.username,
             message.chat.id,
             contactInfo,
             aboutEmployee))
    else:
        update_data_employee(message.chat.id,
                             nameEmployee,
                             salaryForCompany,
                             jobTitle,
                             contactInfo,
                             aboutEmployee)

    conn.commit()
    # Закрываем соединение
    conn.close()


# endregion

# Обработчик всех текстовых сообщений
# @bot.message_handler(func=lambda message: True)
# def handle_text(message):
#     text = message.text
#     bot.send_message(message.chat.id, f'Вы написали: {text}')


# Запускаем бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
