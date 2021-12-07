import telebot
from telebot import types
import psycopg2
import random
import datetime

bot = telebot.TeleBot('2104138555:AAEwwr13MBf_g4UnI6HXiLJEmEjMhifRgKQ')


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_help = types.KeyboardButton('/help')
    btn_dice = types.KeyboardButton('Кубик'+chr(127922))
    btn_ball = types.KeyboardButton('Шар судьбы'+chr(127921))
    btn_timetable = types.KeyboardButton('Расписание'+chr(128197))
    markup.row(btn_help)
    markup.row(btn_dice, btn_ball)
    markup.row(btn_timetable)
    bot.send_message(message.chat.id, 'Приветик\n/help', reply_markup=markup)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Основные команды:\n/start - Классичекое начало пользование.\n/help - Просто помощь.\nПрочий '
                     'функционал:\nКубик{0} - Бросает шестигранную кость.\nШар судьбы{1} - Ответит на все твои вопросы,'
                     ' на которые можно ответить да или нет.\nРасписание{2} - Покажет расписание.'.format(
                        chr(127922), chr(127921), chr(128197)))


@bot.message_handler(commands=['back'])
def back_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_help = types.KeyboardButton('/help')
    btn_dice = types.KeyboardButton('Кубик' + chr(127922))
    btn_ball = types.KeyboardButton('Шар судьбы' + chr(127921))
    btn_timetable = types.KeyboardButton('Расписание'+chr(128197))
    markup.row(btn_help)
    markup.row(btn_dice, btn_ball)
    markup.row(btn_timetable)
    bot.send_message(message.chat.id, 'Ты вернулся в меню\n/help', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle(call):
    if call.data == 'Вчера':
        conn = psycopg2.connect(database="raspisanie",
                                user="postgres",
                                password="4ds97n1JfdlnLDAlz",
                                host="localhost",
                                port="5432")
        cursor = conn.cursor()
        week = ["'Понедельник'", "'Вторник'", "'Среда'", "'Четверг'", "'Пятница'"]
        wd = datetime.datetime.today().weekday() - 1
        if wd > 4 or wd == -1:
            wd = 4
        cursor.execute("SELECT pos, subject, room, start FROM timetable WHERE day=" + week[wd])
        row = list(cursor.fetchall())
        mess = ''
        j = 1
        for i in row:
            mess += str(j) + '. '
            mess += '(' + str(i[0]) + ') '
            mess += str(i[1]) + ' '
            mess += str(i[2]) + ' '
            mess += str(i[3]) + '\n'
            j += 1
        bot.send_message(call.message.chat.id, mess)
        conn.close()
    if call.data == 'Сегодня':
        conn = psycopg2.connect(database="raspisanie",
                                user="postgres",
                                password="4ds97n1JfdlnLDAlz",
                                host="localhost",
                                port="5432")
        cursor = conn.cursor()
        week = ["'Понедельник'", "'Вторник'", "'Среда'", "'Четверг'", "'Пятница'"]
        wd = datetime.datetime.today().weekday()
        if wd > 4:
            wd = 1
        cursor.execute("SELECT pos, subject, room, start FROM timetable WHERE day=" + week[wd])
        row = list(cursor.fetchall())
        mess = ''
        j = 1
        for i in row:
            mess += str(j) + '. '
            mess += '(' + str(i[0]) + ') '
            mess += str(i[1]) + ' '
            mess += str(i[2]) + ' '
            mess += str(i[3]) + '\n'
            j += 1
        bot.send_message(call.message.chat.id, mess)
        conn.close()
    if call.data == 'Завтра':
        conn = psycopg2.connect(database="raspisanie",
                                user="postgres",
                                password="4ds97n1JfdlnLDAlz",
                                host="localhost",
                                port="5432")
        cursor = conn.cursor()
        week = ["'Понедельник'", "'Вторник'", "'Среда'", "'Четверг'", "'Пятница'"]
        wd = datetime.datetime.today().weekday() + 1
        if wd > 4 or wd == 7:
            wd = 1
        cursor.execute("SELECT pos, subject, room, start FROM timetable WHERE day=" + week[wd])
        row = list(cursor.fetchall())
        mess = ''
        j = 1
        for i in row:
            mess += str(j) + '. '
            mess += '(' + str(i[0]) + ') '
            mess += str(i[1]) + ' '
            mess += str(i[2]) + ' '
            mess += str(i[3]) + '\n'
            j += 1
        bot.send_message(call.message.chat.id, mess)
        conn.close()
    if call.data == 'День недели вручную':
        markup = types.InlineKeyboardMarkup()
        btn_mon = types.InlineKeyboardButton('Понедельник',callback_data='Понедельник')
        btn_tue = types.InlineKeyboardButton('Вторник',callback_data='Вторник')
        btn_wed = types.InlineKeyboardButton('Среда',callback_data='Среда')
        btn_thu = types.InlineKeyboardButton('Четверг',callback_data='Четверг')
        btn_fri = types.InlineKeyboardButton('Пятница',callback_data='Пятница')
        btn_all = types.InlineKeyboardButton('Вся неделя',callback_data='Вся неделя')
        markup.row(btn_all)
        markup.row(btn_mon, btn_tue, btn_wed)
        markup.row(btn_thu, btn_fri)
        bot.send_message(call.message.chat.id, 'Какой день недели?', reply_markup=markup)
    if call.data == 'Понедельник':
        conn = psycopg2.connect(database="raspisanie",
                                user="postgres",
                                password="4ds97n1JfdlnLDAlz",
                                host="localhost",
                                port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT pos, subject, room, start FROM timetable WHERE day='Понедельник';")
        row = list(cursor.fetchall())
        mess = ''
        j = 1
        for i in row:
            mess += str(j) + '. '
            mess += '(' + str(i[0]) + ') '
            mess += str(i[1]) + ' '
            mess += str(i[2]) + ' '
            mess += str(i[3]) + '\n'
            j += 1
        bot.send_message(call.message.chat.id, mess)
        conn.close()
    if call.data == 'Вторник':
        conn = psycopg2.connect(database="raspisanie",
                                user="postgres",
                                password="4ds97n1JfdlnLDAlz",
                                host="localhost",
                                port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT pos, subject, room, start FROM timetable WHERE day='Вторник';")
        row = list(cursor.fetchall())
        mess = ''
        j = 1
        for i in row:
            mess += str(j) + '. '
            mess += '(' + str(i[0]) + ') '
            mess += str(i[1]) + ' '
            mess += str(i[2]) + ' '
            mess += str(i[3]) + '\n'
            j += 1
        bot.send_message(call.message.chat.id, mess)
        conn.close()
    if call.data == 'Среда':
        conn = psycopg2.connect(database="raspisanie",
                                user="postgres",
                                password="4ds97n1JfdlnLDAlz",
                                host="localhost",
                                port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT pos, subject, room, start FROM timetable WHERE day='Среда';")
        row = list(cursor.fetchall())
        mess = ''
        j = 1
        for i in row:
            mess += str(j) + '. '
            mess += '(' + str(i[0]) + ') '
            mess += str(i[1]) + ' '
            mess += str(i[2]) + ' '
            mess += str(i[3]) + '\n'
            j += 1
        bot.send_message(call.message.chat.id, mess)
        conn.close()
    if call.data == 'Четверг':
        conn = psycopg2.connect(database="raspisanie",
                                user="postgres",
                                password="4ds97n1JfdlnLDAlz",
                                host="localhost",
                                port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT pos, subject, room, start FROM timetable WHERE day='Четверг';")
        row = list(cursor.fetchall())
        mess = ''
        j = 1
        for i in row:
            mess += str(j) + '. '
            mess += '(' + str(i[0]) + ') '
            mess += str(i[1]) + ' '
            mess += str(i[2]) + ' '
            mess += str(i[3]) + '\n'
            j += 1
        bot.send_message(call.message.chat.id, mess)
        conn.close()
    if call.data == 'Пятница':
        conn = psycopg2.connect(database="raspisanie",
                                user="postgres",
                                password="4ds97n1JfdlnLDAlz",
                                host="localhost",
                                port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT pos, subject, room, start FROM timetable WHERE day='Пятница';")
        row = list(cursor.fetchall())
        mess = ''
        j = 1
        for i in row:
            mess += str(j) + '. '
            mess += '(' + str(i[0]) + ') '
            mess += str(i[1]) + ' '
            mess += str(i[2]) + ' '
            mess += str(i[3]) + '\n'
            j += 1
        bot.send_message(call.message.chat.id, mess)
        conn.close()
    if call.data == 'Вся неделя':
        conn = psycopg2.connect(database="raspisanie",
                                user="postgres",
                                password="4ds97n1JfdlnLDAlz",
                                host="localhost",
                                port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT day, pos, subject, room, start FROM timetable")
        row = list(cursor.fetchall())
        mess = ''
        j = 1
        for i in row:
            mess += str(j) + '. '
            mess += str(i[0]) + ' '
            mess += '(' + str(i[1]) + ') '
            mess += str(i[2]) + ' '
            mess += str(i[3]) + ' '
            mess += str(i[4]) + '\n'
            j += 1
        bot.send_message(call.message.chat.id, mess)
        conn.close()
    bot.answer_callback_query(call.id)


@bot.message_handler(content_types='text')
def reply_message(message):
    if message.text == 'Шар судьбы'+chr(127921):
        ans = ['Бесспорно', 'Никаких сомнений', 'Да', 'Вероятнее всего', 'Наверное...\nДай подумать', 'Спроси позже',
               'Даже не думай', 'Мой ответ "нет"', 'Перспективы не очень хорошие']
        bot.send_message(message.chat.id, random.choice(ans))
    if message.text == 'Кубик' + chr(127922):
        dice = [9856, 9857, 9858, 9859, 9860, 9861]
        bot.send_message(message.chat.id, 'Ты получил: ' + chr(random.choice(dice)))
    if message.text == 'Расписание'+chr(128197):
        markup = types.InlineKeyboardMarkup()
        btn_yst = types.InlineKeyboardButton('Вчера',callback_data='Вчера')
        btn_tdy = types.InlineKeyboardButton('Сегодня',callback_data='Сегодня')
        btn_tmr = types.InlineKeyboardButton('Завтра',callback_data='Завтра')
        btn_wik = types.InlineKeyboardButton('День недели вручную',callback_data='День недели вручную')
        markup.row(btn_yst, btn_tdy, btn_tmr)
        markup.row(btn_wik)
        bot.send_message(message.chat.id, 'Какой день?', reply_markup=markup)


bot.infinity_polling()
