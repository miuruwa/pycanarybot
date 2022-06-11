from tkinter import *
import vk_api, sqlite3, random, datetime, math, sys, requests
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

def send():
    sended(int(chat_id.get()), message.get(), atty.get())
def sended(a,b,c):
    vk.messages.send(random_id=random.randint(0, 999999), message=b, attachment=c, peer_id=a+2000000000)

def init(t,i):
    global vk, chat_id, message, atty
    vk_session = vk_api.VkApi(token=t)
    longpoll, vk = VkBotLongPoll(vk_session, i), vk_session.get_api()
    root = Tk()
    root.title('Отправить сообщение через Канарейку')
    label1 = Label(root, text="Введите номер беседы: ")
    label2 = Label(root, text="Введите сообщение: ")
    label3 = Label(root, text="Вложения: ")
    chat_id = Entry(root, width=50)
    message = Entry(root, width=50)
    atty = Entry(root, width=50)
    buttonsend = Button(root, text="Отправить", command=send)

    label1.pack()
    chat_id.pack()
    label2.pack()
    message.pack()
    label3.pack()
    atty.pack()
    buttonsend.pack()


    root.mainloop()