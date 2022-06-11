import vk_api
import traceback, random
import media, database

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

class CanaryBot:
    def __init__(self, **kwargs):
        self.id = kwargs['gid']
        self.session = vk_api.VkApi(token=kwargs['token'])
        self.longpoll = VkBotLongPoll(self.session, kwargs['gid'])
        self.api = self.session.get_api()
        self.media = media.Media()
        self.db = database.Database('db.db', True)


    def check(self):
        for event in self.longpoll.check():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.react(event.object['message'])


    def send(self, **kwargs):
        self.api.messages.send(random_id=random.randint(0,999999), 
            peer_id = kwargs['peer_id'], 
            message = kwargs['messageText'], 
            attachment = kwargs['messageAttachment'])

    def getUserInfo(self, **kwargs):
        user_id = kwargs['user_id']
        chat_id = kwargs['peer_id']
        name = self.db.getUserName(user_id)
        ban, vip, adm = self.db.ban.get(chat_id, user_id), self.db.vip.get(user_id), self.db.admin.get(user_id)
        #модератор, есть ли в беседе, онлайн
        pass
    def react(self, message):
        self.db.user_add(message['from_id'])
        if message['peer_id'] < 2000000000:
            if message['text'] == 'Начать' or message['payload'] == '{"command":"start"}': 
                #реакция на сообщение пользователя
                self.send(peer_id = message['peer_id'], messageText = 'Ой, привет, {from_id_name}, почему ты пишешь мне?', attachment='photo-195675828_457241078') 
                self.send(peer_id = message['peer_id'], messageText = 'Нужно добавиться в беседу? Ох, тогда смотри статью: vk.com/@canarybot-rules', attachment='photo-195675828_457241078') 
        else:
            #реакция на сообщение в чате
            lim, ids, maxid = [],[],0
            self.db.chat_add(message['peer_id'])
            #проверка на action
            try:
                if message['action']['type'] == 'chat_invite_user' or message['action']['type'] == 'chat_invite_user_by_link':
                    if message['action']['member_id'] == -int(self.id):
                        #приветствие по приглашению бота
                    elif message['action']['member_id'] > 0:
                        #реакция на приглашение пользователя
                        #бан либо приветствие
            except:
                #проверка на наличие бана

                defined = self.media.define(message['messageText'])

                lim.append(self.media.add_replies())
            
            #ответ
