import messages
import time
import utils
from utils import getMessage
from utils import hasMessage
from telebot import types
from telebot import TeleBot
from datetime import datetime
from pyowm import OWM
from random import randint

class BotUserData:
    def __init__(self):
        self.firstMetting = False
        self.allowEchoMessages = False
        self.botMenuRequest = False
        self.botRequestName = False
        self.botWeatherRequest = False
        self.botMoodRequest = False
        self.botPolindromRequest = False
        self.userName = ""
        self.lastUserMessage = ""

user = BotUserData()
owm = OWM('51d3c02265db0c83b75b08a46af97a2d')
bot = TeleBot('1530216236:AAGPHyeGmEQJ4pOYjAVHUbK51UvMPgJvQ7o')

#===============================================
# Команды бота
#===============================================

def sendHiMessage(chatId, text):
    if hasMessage(text, messages.byeMessages):
        bot.send_message(chatId, "Лол, мы еще не здоровались :D")
        bot.send_message(chatId, "Напиши мне привет! Или хай к примеру.")
        return
    bot.send_message(chatId, getMessage(messages.hiAnsMessages))
    user.firstMetting = True

def sendDialogMessage(chatId, text):
    if text == messages.questionsMessages[0] or text == messages.questionsMessages[1]: #как дела
        bot.send_message(chatId, getMessage(messages.q0AnsMessages))
        time.sleep(5)

        markup = utils.createInlineKeyboard(["Хорошо", "Плохо"])
        bot.send_message(chatId, "А как ваше настроение?", reply_markup=markup)
        user.botMoodRequest = True
    elif text == messages.questionsMessages[2] or text == messages.questionsMessages[3]: #кто ты
        bot.send_message(chatId, messages.q1AnsMessage)

def sendTimeOrDateMessage(chatId, text):
    now = datetime.now()
    if   hasMessage(text, messages.timeMessages):
        bot.send_message(chatId, "Ваше время: " + str(now.hour) + ":" + str(now.minute))
    elif hasMessage(text, messages.dateMessages):
        bot.send_message(chatId, "Ваша дата: " + str(now.day) + "." + str(now.month) + "." + str(now.year))
    elif hasMessage(text, messages.dayMessages):
        bot.send_message(chatId, "Сегодня " + str(now.day) + " число.")
    elif hasMessage(text, messages.monthMessages):
        bot.send_message(chatId, "Сегодня " + str(now.month) + " месяц.")
    elif hasMessage(text, messages.yearMessages):
        bot.send_message(chatId, "Сегодня " + str(now.year) + " год.")

def sendWeatherMessage(chatId):
    bot.send_message(chatId, "Введите ваш регион/город.")
    user.botWeatherRequest = True

def sendPolindromMessage(chatId):
    bot.send_message(chatId, "Введите слово и я проверю полиндром это или нет.")
    user.botPolindromRequest = True

#===============================================
#Telebot эвенты-каллбаки (обратные вызовы в API)
#===============================================

@bot.message_handler(commands=['start'])
def sendStartMessage(message):
    bot.reply_to(message, messages.startMessage)

@bot.message_handler(commands=['help'])
def sendHelpMessage(message):
    bot.reply_to(message, messages.helpMessage)

@bot.message_handler(commands=['menu'])
def sendMenuMessage(message):
    markup = utils.createInlineKeyboard(["Привет", "Погода", "Время", "Дата", "Обшение", "Полиндром"])
    bot.send_message(message.chat.id, "Меню", reply_markup=markup)
    user.botMenuRequest = True

@bot.message_handler(content_types=['text'])
def startDialog(message):
    chatId = message.chat.id
    text = message.text
    user.lastUserMessage = text
    dialog = True

    while dialog:
        #приветстиве
        if not user.firstMetting: 
            sendHiMessage(chatId, text)
            break
    
        #диалог после приветствия
        if user.firstMetting:
            if hasMessage(text, messages.hiMessages):
                answerDobHiMessage = getMessage(messages.dobHiAnsMessages)
                if answerDobHiMessage == messages.dobHiAnsMessages[4]:
                    bot.send_message(chatId, "Доброго дня!")
                else:
                    bot.send_message(chatId, answerDobHiMessage)
                break

            #бот получает имя пользователя
            if user.botRequestName:
                if not hasMessage(text, messages.reqNameMessages):
                    user.userName = text
                    user.botRequestName = False
                    bot.send_message(chatId, "Я вас запомнил, " + user.userName + ".")
                else:
                    bot.send_message(chatId, getMessage(messages.reqNameAnsMessages))

            #бот получает погоду (PyOWM)
            if user.botWeatherRequest:
                mgr = owm.weather_manager()
                try:
                    observation = mgr.weather_at_place(text)
                    w = observation.weather
                    temp = w.temperature("celsius")
                    t = [temp["temp"], temp["feels_like"], temp["temp_max"], temp["temp_min"]]
                    bot.send_message(chatId, messages.wheatherAnsMessage[0] + str(text) + ":\n" 
                        "Температура " + str(t[0]) + ", ошушаеться как " + str(t[1]) + ", максимальная " + str(t[2]) + ", минимальная " + str(t[3]))
                except Exception:
                    bot.send_message(chatId, "Вы ввели не существующий город, и/или не удалось его распознать!")
                    break
                finally: user.botWeatherRequest = False
            
            #бот проверяет полиндром
            if user.botPolindromRequest:
                text = utils.replaceAll(text).lower()
                if text[::-1] == text:
                    bot.send_message(chatId, "Все верно это полиндром.")
                else: 
                    bot.send_message(chatId, "Упс! Это не полиндром!")
                user.botPolindromRequest = False
                break

            #обшение
            while(True):
                if user.botMoodRequest:
                    user.botMoodRequest = False

                sendDialogMessage(chatId, utils.replaceAll(text).lower())
                break

            #ответ на последние сообшение 
            if hasMessage(user.lastUserMessage, messages.forgotMessages):
                bot.send_message(chatId, getMessage(messages.forgotAnsMessages))
                user.botRequestName = True
            elif hasMessage(user.lastUserMessage, messages.setNameMessages):
                bot.send_message(chatId, "Как вас называть?")
                user.botRequestName = True
            elif hasMessage(user.lastUserMessage, messages.byeMessages):
                bot.send_message(chatId, getMessage(messages.byeAnsMessages))
                user.firstMetting = False
                user.userName = ""
            elif hasMessage(user.lastUserMessage, messages.wheatherMessages):
                sendWeatherMessage(chatId)
            elif text == "Полиндром".lower():
                sendPolindromMessage(chatId)

            sendTimeOrDateMessage(chatId, user.lastUserMessage)

            print(user.lastUserMessage)
        break

@bot.callback_query_handler(func=lambda call: True)
def callbackInline(call):
    chatId = call.message.chat.id
    msgId = call.message.message_id
    if call.message and user.botMenuRequest:
        if call.data == '0': sendHiMessage(chatId, "привет")
        if call.data == '1': sendWeatherMessage(chatId)
        if call.data == "2": sendTimeOrDateMessage(chatId, "время")
        if call.data == "3": sendTimeOrDateMessage(chatId, "дата")
        if call.data == "4": sendDialogMessage(chatId, "как дела")
        if call.data == "5": sendPolindromMessage(chatId)
        utils.deleteInlineKeyboard(bot, chatId, msgId)
        user.botMenuRequest = False
    elif call.message:       
        if   call.data == '0': bot.send_message(chatId, getMessage(messages.q00AnsMessages))
        elif call.data == '1': bot.send_message(chatId, getMessage(messages.q01AnsMessages))
        utils.deleteInlineKeyboard(bot, chatId, msgId)

#OnUpdate
bot.polling(True, 0)
