import telebot
import config
from telebot import types
import os
import re
import schedule
import json
from multiprocessing import Process
import time

import get_followers as fol
import save_followers as save
import check_followers as check
import add_to_user_list as add
import delete_user as delete

bot = telebot.TeleBot(config.TOKEN)
print(time.asctime(), 'Bot is successfully started')

queue = []
list_of_requests = []


def requests_queue():
    global markup
    while queue:
        message = queue.pop(0)
        if message[1]:
            message = message[0]
            username = message.text
            tg_id = message.from_user.id

            print(time.asctime(), 'Bot starts checking followers of user %s' % message.from_user.id)
            followers = fol.get_followers(username)
            if followers == 'ERROR':
                print(time.asctime(), 'Checking followers error')
                bot.send_message(message.chat.id, 'Что-то не так с твоим никнеймом. Попробуй ещё раз.')
                list_of_requests.remove(tg_id)
            else:
                print(time.asctime(), 'Bot successfully checked %s followers' % message.from_user.id)
                bot.send_message(message.chat.id,
                                 'Отлично! У тебя %i подписчиков! Теперь я смогу сообщать тебе об изменениях!' % len(
                                     followers), reply_markup=markup)
                list_of_requests.remove(tg_id)
                add.add_user(tg_id)
                print(time.asctime(), '%s added to userlist' % tg_id)
                save.savind_followers(followers, username, tg_id)
                print(time.asctime(), 'Bot saved %s\'s followers' % message.from_user.id)
        else:
            message = message[0]
            tg_id = message.from_user.id
            answer = check.check_followers(tg_id)
            print(time.asctime(), 'Successfully checked followers of %s' % message.from_user.id)
            followers_report(answer, message.chat.id, user_initialised=True)
            print(time.asctime(), 'Successfully sent a report to user %s' % message.from_user.id)
            list_of_requests.remove(tg_id)


@bot.message_handler(commands=['start'])
def welcome(message):
    print(time.asctime(), 'Got a new user %s' % message.from_user.id)
    bot.send_message(message.chat.id,
                     'Привет, {0.first_name}!\nЭтот бот отслеживает твоих подписчиков в Twitter.'.format(
                         message.from_user), parse_mode='html')
    bot.send_message(message.chat.id, 'Введи свой ник:')


# keyboard button for checking followers, changing user and unfollowing bot
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Проверить подписчиков')
item2 = types.KeyboardButton('Отписаться от рассылки')
item3 = types.KeyboardButton('Другой пользователь')
markup.add(item1, item2, item3)

inline = types.InlineKeyboardMarkup(row_width=2)
item1 = types.InlineKeyboardButton("Уверен", callback_data='yes')
item2 = types.InlineKeyboardButton("Не уверен", callback_data='no')
inline.add(item1, item2)

inline2 = types.InlineKeyboardMarkup(row_width=2)
item1 = types.InlineKeyboardButton("Уверен", callback_data='unfollow')
item2 = types.InlineKeyboardButton("Не уверен", callback_data='cancel')
inline2.add(item1, item2)


@bot.message_handler(func=lambda message: not os.path.exists(
    'followers/{}.json'.format(message.from_user.id)))
def get_nickname(message):
    tg_id = message.from_user.id
    global queue
    global list_of_requests
    if re.match('([a-zA-Z_]){1,15}', message.text) == None:
        print(time.asctime(), 'Username error')
        bot.send_message(message.chat.id, 'Мне нужен твой никнейм в Твиттере. Тогда я смогу сделить за подписчиками.')
    else:
        if tg_id not in list_of_requests:
            list_of_requests.append(tg_id)
            bot.send_message(message.chat.id, 'Сейчас проверю твоих подписчиков. Это займет некоторое время.')
            print(time.asctime(), 'Checking followers of %s...' % message.from_user.id)
            queue.append([message, True])
            if len(queue) <= 1:
                requests_queue()
        else:
            print(time.asctime(), 'Got repeated request by %s' % message.from_user.id)
            bot.send_message(message.chat.id, 'Я уже обрабатываю твой запрос. Подожди немного :)')


@bot.message_handler(content_types=['text'])
def check_followers(message):
    tg_id = message.from_user.id

    global markup
    global list_of_requests

    if message.text == 'Проверить подписчиков':
        if tg_id not in list_of_requests:
            list_of_requests.append(tg_id)
            bot.send_message(message.chat.id, 'Проверяю подписчиков. Это займет некоторое время.')
            print(time.asctime(), 'Checking followers of %s..' % message.from_user.id)
            queue.append([message, False])
            if len(queue) <= 1:
                requests_queue()
        else:
            bot.send_message(message.chat.id, 'Я уже обрабатываю твой запрос. Подожди немного :)')

    elif message.text == 'Отписаться от рассылки':
        bot.send_message(message.chat.id, 'Уверен? Мне будет грустно без тебя :\'(',
                         reply_markup=inline2)

    elif message.text == 'Другой пользователь':
        bot.send_message(message.chat.id, 'Уверен? Все данные о предыдущем пользователе будут удалены.',
                         reply_markup=inline)

    else:
        print(time.asctime(), 'Get unknown request')
        bot.send_message(message.chat.id,
                         'Я всего лишь глупый бот, умею только проверять подписчиков... Выбери что-нибудь из предложенных вариантов.',
                         reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == 'yes':
            delete.delete_user(call.message.chat.id)
            bot.send_message(call.message.chat.id, 'ОК. Введи новый никнейм:')
            print(time.asctime(), "User %s changes nickname" % call.message.chat.id)
        elif call.data == 'no':
            bot.send_message(call.message.chat.id, 'Хорошо, продолжу работу с текущим пользователем.')
        elif call.data == 'unfollow':
            delete.delete_user(call.message.chat.id)
            print(time.asctime(), 'User %s has been deleted' % call.message.chat.id)
            bot.send_message(call.message.chat.id,
                             'До свидания, я буду скучать :(\nНадеюсь, мы ещё встретимся!'
                             )
        elif call.data == 'cancel':
            bot.send_message(call.message.chat.id,
                             'Ураа!!! Я знал, что ты не уйдешь от меня, ведь я такой ПОЛЕЗНЫЙ бот!')


def followers_report(answer, chat, user_initialised=False):
    if not answer[0] and not answer[1]:
        if user_initialised:
            bot.send_message(chat, 'Пока всё без изменений.', reply_markup=markup)
    elif not answer[0] and answer[1]:
        bot.send_message(chat, 'У тебя новые подписчики: https://twitter.com/{}'.format(
            '\nhttps://twitter.com/'.join(answer[1])),
                         reply_markup=markup)
    elif answer[0] and not answer[1]:
        bot.send_message(chat, 'От тебя отписались пользователи: https://twitter.com/{}'.format(
            '\nhttps://twitter.com/'.join(answer[0])),
                         reply_markup=markup)
    elif answer[0] and answer[1]:
        bot.send_message(chat, 'От тебя отписались пользователи: https://twitter.com/{}.'.format(
            '\nhttps://twitter.com/'.join(answer[0])),
                         reply_markup=markup)
        bot.send_message(chat, 'У тебя новые подписчики: https://twitter.com/{}.'.format(
            '\nhttps://twitter.com/'.join(answer[1])),
                         reply_markup=markup)
    print(time.asctime(), 'Bot has sent a report to / checked user %s' % chat)


def message_schedule():
    schedule.every().day.at("14:00").do(send_followers_update)
    while True:
        schedule.run_pending()
        time.sleep(1)


def send_followers_update():
    with open('list_of_users.json') as file:
        users = json.load(file)
    for user_id in users:
        answer = check.check_followers(user_id)
        followers_report(answer, user_id)
    print(time.asctime(), "Daily checking finished successfully")


p1 = Process(target=message_schedule, args=())
p1.start()

while True:
    try:
        bot.polling(none_stop=True)
    except Exception:
        print(time.asctime(), "Unsuccessful request to tg server")
        time.sleep(15)