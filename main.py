# DESCRIPTION
# This bot was created with target for automation routine study tasks


from telebot import types as t 
import telebot
import pymysql

# config used to import token nd save him hidden 
bot = telebot.TeleBot(token='$YOUR_TOKEN$')

connection = pymysql.connect(
    host='$YOUT_HOST$',
    port='$YOUR_PORT$',
    user='$YOUR_USERNAME$',
    password='$YOUR_PASSWORD$',
    database='$YOUR_DB$',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = connection.cursor()


# HANDLERS 
# START MESSAGE
@bot.message_handler(commands=['admin'])
def admin(message):
    if message.chat.id == '$YOUR_ID$': # int without quotes
        markup = t.InlineKeyboardMarkup()
        btn1 = t.InlineKeyboardButton(text='Список юзер айди', callback_data='users_ids')
        btn2 = t.InlineKeyboardButton(text='Статистика', callback_data='stats')
        markup.add(btn1,btn2) 
        bot.send_message(message.chat.id, 'Приветствую в админ меню,создатель!', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Вы не админ!')

@bot.message_handler(commands=['start'])
def start(message):
        
            try:
                markup = t.InlineKeyboardMarkup()
                button1 = t.InlineKeyboardButton(text='🌟Меню🌟', callback_data='data1')
                markup.add(button1)
                bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}  я бот для парсинга расписания, нажми на кнопку чтобы открыть меню :)', reply_markup=markup) 
                print('Successfully connected...')
                print('#' * 20)
                
                with connection.cursor() as cursor:
                    x = cursor.execute(f'SELECT * FROM `users` WHERE user_id={message.chat.id}')

                    if x == 1:
                        bot.send_message(message.chat.id,'Рад тебя снова видеть!')
                    elif x == 0: 
                        bot.send_message(message.chat.id, 'Ты здесь впервые, но надеюсь ты еще зайдешь!') 
                        cursor.execute('INSERT INTO `users` (user_id) VALUES ('f"{message.chat.id}"')')      
                        connection.commit()
            except Exception as ex:
                print('Connection refused...')
                print(ex)
# MENU

# CALLBACK

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == 'users_ids':
        cursor.execute('SELECT * FROM `users`')
        resu = cursor.fetchall()

        for res in resu:
            bot.send_message(call.message.chat.id, res.get('user_id')) 
    if call.data == 'stats':
        cursor.execute('SELECT user_id FROM `users`')
        results = cursor.fetchall()
        count_Users = 0 

        for result in results:
            count_Users += 1

        bot.send_message(call.message.chat.id, f'📄Статистика📄:\n\n Количество пользователей: {count_Users}')
    if call.data == 'pdf':
        bot.answer_callback_query(call.id, 'Отлично, подождите пару секунду')
        bot.send_document(call.message.chat.id, document='$YOUR_LINK$')
    if call.data == 'names':
        bot.answer_callback_query(call.id, 'Отлично, подождите пару секунду')
        bot.send_message(call.message.chat.id, '\n'.join('$YOUR_LIST$'))
    if call.data == 'calls':
        bot.answer_callback_query(call.id, 'Отлично, подождите пару секунду')
        bot.send_photo(call.message.chat.id , '$YOUR_PHOTO$')
    if call.data == 'data1':
        markup = t.InlineKeyboardMarkup() # --> кнопки
        btn1 = t.InlineKeyboardButton(text='👔Файл расписания (ФОРМАТ PDF)👔', callback_data='pdf') # Для получения простого файла с сервера. 
        btn2 = t.InlineKeyboardButton(text='👥Имена преподавателей👥',callback_data='names') # имена учителей 
        btn3 = t.InlineKeyboardButton(text='💫Расписание звонков 💫', callback_data='calls')
        btn4 = t.InlineKeyboardButton(text='❄️Сайт❄️', url='') # YOUR LINK
        markup.add(btn1,btn2, btn3, btn4) # кнопки <--
        bot.send_message(call.message.chat.id, '💼Меню💼 ' , reply_markup=markup)

@bot.message_handler(commands=['call'])
def calling(message):
    count_True = 0
    count_False = 0
    try:
        cursor.execute('SELECT * FROM `users`')
        results = cursor.fetchall()
        

        for result in results:
            bot.send_message(result.get('user_id'), message.text[message.text.find(' '):])
            count_True += 1
        
    except Exception as ex:
        count_False += 1
    finally:
        bot.send_message(message.chat.id, f'Рассылка была проведена🔔\n\n\nУспешно✅ - {count_True}\nОшибки❌ - {count_False}')
        
# POOLING
bot.infinity_polling()


# Thanks for read my code :3 :1