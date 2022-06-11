import vk_api, random, math, traceback

import media
import database

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class CanaryBot:
    def __init__(self, vktoken, vkid, drop):
        self.id = vkid

        self.session = vk_api.VkApi(token=vktoken)
        self.longpoll = VkBotLongPoll(self.session, vkid)
        self.api = self.session.get_api()

        self.db = database.Database('db.db', drop)

    def check(self):
        for event in self.longpoll.check():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.react(event.object['message'])
    def formatt_tool(self, kind = 'unknown', peer_id = 2000000001, from_id = 1, sel_id = 1, ):
        fin, sin, cn, d, mc, mcbl, mco, bl, br, o, al = '', '', '', '', '', '', '', '', '', '', ''
        if kind = 'null':
            fin = self.db.getUserName(from_id)
        elif kind = 'user_info':
            fin = self.db.getUserName(from_id)
            sin = self.db.getUserName(sel_id)
        elif kind = 'chat_al':
            fin = self.db.getUserName(from_id)
            al = 'Вот список администраторов: \n' + self.chat.getAdminsList(peer_id)
        elif kind = 'chat_bl':
            fin = self.db.getUserName(from_id)
            bl = 'Вот список администраторов: \n' + self.chat.getBlackList(peer_id)
        elif kind = 'chat_online':
            fin = self.db.getUserName(from_id)
            o = ''
            mco = ''
        elif kind = 'chat_review':
            fin = self.db.getUserName(from_id)
            cn = ''
            d = ''
        elif kind = 'chat_name':
            fin = self.db.getUserName(from_id)
            cn = ''
        elif kind = 'chat_descr':
            fin = self.db.getUserName(from_id)
        elif kind = 'chat_kick':
            fin = self.db.getUserName(from_id)
        elif kind = 'chat_unban':
            fin = self.db.getUserName(from_id)
        elif kind = 'chat_ban':
            fin = self.db.getUserName(from_id)
            br = ''
        elif kind = 'chat_nickname':
            fin = self.db.getUserName(from_id)
        elif kind = 'unknown':
            fin = self.db.getUserName(from_id)
        #     null - fin
        #     user_info - fin, sin
        #     chat_al - al
        #     chat_bl - bl
        #     chat_online - mco, o
        #     chat_review - cn, d, mco
        #     chat_name - cn
        #     chat_descr -
        #     chat_ban - br, 
        #     user_nickname - fin,
        
        formatt = {
            'from_id_name': fin, 
            'second_id_name': sin,
            'chat_name': cn, 
            'descr': d, 
            'member_count': mc, 
            'member_count_bl': mcbl,
            'member_count_online': mco,
            'admin_list': al,
            'black_list': bl,
            'ban_reason': br,
            'online': o,
          }
        return formatt
    def react(self, message):
        if message['peer_id'] > 2000000000:
            lim, ids, cmd_type = [], []
            try:
                if message['action']['type'] == 'chat_invite_user' or message['action']['type'] == 'chat_invite_user_by_link':
                    if message['action']['member_id'] == -int(self.id):
                        lim.append({'messageText': 'Приветствую вас, пользователи! Осталось настроить бота, обратитесь к команде "@canarybot помощь".'})
                    elif message['action']['member_id'] > 0:
                        if self.db.getUserBan(message['action']['member_id'], message['peer_id']) == 0:
                            lim.append({'messageText': 'Приветствую вас, {from_id_name}! Для начала пропишите "@canarybot помощь" и ознакомьтесь с командами!'})
                        else:
                            self.api.messages.removeChatUser(chat_id=messages['peer_id']-2000000000, member_id = message['action']['member_id'])
                            lim.append({'messageText': 'Пользователь в чёрном списке, исключаю'})
            except:
                pass
            if self.db.getUserBan(message['from_id'], message['peer_id']) == 0:
                defined = self.media.define(message['text'])
                if defined['cmd'] != '':
                    formatt = 0

                    # formatt = {
                    #   'from_id_name': '', 
                    #   'second_id_name': '',
                    #   'chat_name': '', 
                    #   'descr': '', 
                    #   'member_count': '', 
                    #   'member_count_bl': '',
                    #   'black_list': '',
                    #   'ban_reason': '',
                    #   'online': '',
                    #   'your_text': ''
                    # }
                    lim.append(self.media.get(defined['cmd'], formatt))
            else:
                self.api.messages.removeChatUser(chat_id=messages['peer_id']-2000000000, member_id = message['from_id'])
                lim.append({'messageText': 'Пользователь в чёрном списке, исключаю'})
                lim.append({'messageText': 'Причина блокировки: {ban_reason}'})
                #команды
    class chat:
        def change(self, peer_id, arg):
            if arg[0:arg.find(';')] == 'name':
                pass
            elif arg[0:arg.find(';')] == 'descr':
                pass
        def show(self, peer_id):
            self.send(peer_id, db.chat(peer_id)['descr']+'Количество участников: ' + self.chat.getMembersCount(self, peer_id), '')
            self.send(peer_id, 'Администраторы беседы:' + self.chat.getAdminMembers(self, peer_id), '')

        def getMembersCount(self, peer_id):
            listOfMembers = self.api.messages.getConversationMembers(peer_id=peer_id)['items']
            return str(len(listOfMembers))
        def getMembersList(self, peer_id):
            listOfMembers = self.api.messages.getConversationMembers(peer_id=peer_id)['items']
            for i in listOfMembers:
                yield i['member_id']
        def getAdminsList(self, peer_id):
            listOfMembers = self.api.messages.getConversationMembers(peer_id=peer_id)['items']
            for i in listOfMembers:
                try:
                    if i['is_admin']:
                        try:
                            if i['is_owner'] == True:
                                yield {'id': i['member_id'], 'isOwner': True}  
                        except:
                            yield {'id': i['member_id'], 'isOwner': False}  
                except:
                    pass
        def getChatMembers(self, peer_id): #canarybot.chat
            text = ''
            for i in self.chat.getMembersList(peer_id):
                text = text + '\n\u2022 {}'.format(self.user.getUserName(self, i, False))
                for y in self.getAdminsList(peer_id):
                    if i == y:
                        if i['isOwner']:
                            text = text + ' (Создатель)'
                        else:
                            text = text + ' (Админ)'
                        break
            return text
        def getAdminMembers(self, peer_id):
            text = ''
            for i in self.chat.getAdminsList(self, peer_id):
                text = text + '\n\u2022 {}'.format(self.user.getUserName(self, i['id'], False))
                if i['isOwner']:
                    text = text + ' (Создатель)'
            return text
        def getBlackList(self, peer_id):
            text = ''
            for i in self.db.getChatBL(peer_id):
                text = text + '\n\u2022 {}'.format(self.user.getUserName(self, i['id'], False))
            return text
    class user:
        def change(peer_id, arg, ids):
            for uid in ids:
                if arg[0:arg.find(';')] == 'name':
                    pass
                elif arg[0:arg.find(';')] == 'admin':
                    pass
                elif arg[0:arg.find(';')] == 'vip':
                    pass
                elif arg[0:arg.find(';')] == 'ban':
                    if not db.ban.add(peer_id, uid, arg[arg.find(';')+1:len(arg)]):
                        self.send(peer_id, 'Не получилось забанить пользователя: страница уже занесена в чёрный список')
                elif arg == 'unban':
                    if not db.ban.delete(peer_id, uid):
                        self.send(peer_id, 'Не получилось раззабанить пользователя: страница не занесена в чёрный список')
                elif arg == 'kick':
                    try:
                        self.api.messages.removeChatUser(peer_id = peer_id, member_id = uid)
                    except:
                        exist = False
                        for member in self.getMembersList(peer_id):
                            if member == uid:
                                exist = True
                                break
                        if exist:
                            for member in self.getMembersList(peer_id):
                                if member == uid:
                                    self.send(peer_id, 'Не получилось кикнуть пользователя: это администратор чата.')
                                    break
                        else:
                            self.send(peer_id, 'Не получилось кикнуть пользователя: страница не состоит в беседе.')
        def getUserInfo(self, user_id: int):
            pass
    
        def getUserName(self, user_id, link):
            if link == True:
                return '[id'+str(user_id)+'|{first_name} {last_name}]'.format(**self.api.users.get(user_ids = user_id)[0]) if user_id>0 else '[club{}|{}]'.format(str(-user_id),self.api.groups.getById(group_id=-user_id)[0]['name'])
            elif link == False:
                return '{first_name} {last_name}'.format(**self.api.users.get(user_ids = user_id)[0]) if user_id>0 else self.api.groups.getById(group_id=-user_id)[0]['name']
            else:
                return '{first_name}'.format(**self.api.users.get(user_ids = user_id)[0])