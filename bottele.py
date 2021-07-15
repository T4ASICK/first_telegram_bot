# Мой первый бот для телеграмма
# была создана колхозная база данных в виде файла,
# в которую добавляются id пользователей при вводе
# комманды /subscribe
# +реализована команда для создания макетного сообщения
# для рассылки

import telebot
from telebot import types  # еще не реализовано
import string
from config import token
import time  # еще не реализовано
from colorama import Fore
h = []
z = []
time = ''
name = ''
bot = telebot.TeleBot(token)


def log(a, b):
    print(Fore.RED + 'COMMAND: {}'.format(a))
    print(Fore.BLUE + 'ID: {}'.format(b))
    print(Fore.WHITE + '_________________')


@bot.message_handler(commands=['start'])
def start(message):
    log(message.text, message.from_user.id)
    if message.text == '/start':
        bot.send_message(message.from_user.id, '''Привет, я Даня Морозов. Я буду переодически звать тебя на кутежи. Ну и помогу распространять инфу о приближающихся.
        \n Напиши /subscribe, чтобы подписаться на рассылку.\n Напиши /tuse, чтобы назначить кутеж ''')


@bot.message_handler(commands=['subscribe'])
def get_info(message):
    log(message.text, message.from_user.id)
    print(Fore.YELLOW + 'Открывается база данных')
    print(Fore.YELLOW + 'Идет проверка на наличие пользвователя в Базе данных')

    def stop():
        f = open('baza.txt', 'a')
        f.write('stop' + '\n')
        f.close
    if message.text == '/subscribe':
        b = 0
        f = open('baza.txt', 'r')
        while b < 1:
            for line in f:
                z.append(line.replace('\n', ''))
                if line.replace('\n', '') == 'stop':
                    z.remove('stop')
                    b += 1

        f.close()
        f = open('baza.txt', 'w')
        for i in range(0, len(z)):
            f.write(z[i] + '\n')
        f.close()
        n = 0
        l = 0
        for i in range(0, len(z)):
            x = int(z[i])
            while True:
                if x == message.from_user.id:
                    n += 1
                    break
                if x != message.from_user.id:
                    l -= 1
                    break

        if n == 1:
            print(Fore.YELLOW + 'ID уже есть в базе данных')
            print(Fore.WHITE + '_________________')
            bot.send_message(message.from_user.id, 'Ты уже подписан')
            stop()
        elif l == -(len(z)):
            print(Fore.YELLOW + 'ID был добавлен в базу данных')
            print(Fore.WHITE + '_________________')
            f = open("baza.txt", 'a')
            f.write('{}\n'.format(message.from_user.id))
            f.close()
            stop()
            bot.send_message(message.from_user.id,
                             'Ты был добавлен в список рассылки на тусичи')


@bot.message_handler(commands=['tuse'])
def start_tuse(message):
    log(message.text, message.from_user.id)
    bot.send_message(message.from_user.id, 'Напиши время для кутежа')
    bot.register_next_step_handler(message, get_time)


def get_time(message):
    log(message.text, message.from_user.id)
    global time
    time = message.text
    bot.send_message(message.from_user.id, 'Время назначено: {}'.format(time))
    bot.send_message(message.from_user.id, 'Введите организатора кутежа')
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    log(message.text, message.from_user.id)
    global name
    name = message.text
    bot.send_message(message.from_user.id,
                     'Организатор определен: {}'.format(name))
    bot.send_message(message.from_user.id, 'Приглашение составлено')
    bot.send_message(message.from_user.id,
                     '{} НАМЕЧАЕТСЯ КУТЕЖ!!!\nОрганизатор: {}'.format(time, name))
    bot.send_message(message.from_user.id,
                     'Начинается отправка сообщения. Напишите что нибудь')
    bot.register_next_step_handler(message, send_tuse)


def send_tuse(message):
    log(message.text, message.from_user.id)
    h = []
    f = open('baza.txt', 'r')
    for line in f:
        h.append(line.replace('\n', ''))
        if line.replace('\n', '') == 'stop':
            h.remove('stop')
            print(h)
    f.close()
    for i in range(0, len(h)):
        bot.send_message(
            int(h[i]), '{} НАМЕЧАЕТСЯ КУТЕЖ!!!\nОрганизатор: {}'.format(time, name))

bot.polling()
