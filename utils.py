from telebot import types
from random import randint
from telebot import TeleBot

def createInlineKeyboard(btnMessages: ...):
    markup = types.InlineKeyboardMarkup(row_width=4)
    btnCount = len(btnMessages)
    i = j = 0
    if btnCount == 2 or btnCount == 4:
        while(i < int(len(btnMessages)) / 2):
            markup.add(types.InlineKeyboardButton(btnMessages[j], callback_data=str(j)),     #B B
                       types.InlineKeyboardButton(btnMessages[j+1], callback_data=str(j+1))) #B B
            j =+ 2
            i += 1
    elif btnCount == 3 or btnCount >= 5:
        while(i < int(len(btnMessages)) / 3):
            markup.add(types.InlineKeyboardButton(btnMessages[j], callback_data=str(j)),     # B B B
                       types.InlineKeyboardButton(btnMessages[j+1], callback_data=str(j+1)), # B B B
                       types.InlineKeyboardButton(btnMessages[j+2], callback_data=str(j+2))) # B B B
            j += 3
            i += 1
    return markup

def deleteInlineKeyboard(bot: TeleBot, chatId, msgId):
    bot.edit_message_reply_markup(chatId, msgId, None, '')

def replaceAll(msg: str): 
    return msg.replace(",", " ").replace("?", "").replace("!", "").replace(".", "")

def hasMessage(userMsg: str, messages: ...):
    for i in range(len(messages)):
        if messages[i] == replaceAll(userMsg).lower():
            return True
    return False

def getMessage(userMsg: str):
    return userMsg[randint(0, len(userMsg) - 1)]