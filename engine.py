import vk_api, random, math, traceback

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import media, search, weather
import requests

class CanaryBot:
    def __init__(self, token, gid):
        self.id = -int(gid)

        self.session = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.session, gid)
        self.api = self.session.get_api()
        
        self.media = media.Media()
        self.search = search.Search()
        self.vkPhoto = self.api.photos.getMessagesUploadServer()
        self.weather = weather.WeatherWidget()

    def check(self):
        for event in self.longpoll.check():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if self.obr(event.object['message']):
                    return False
        else:
            return True

    def send(self, reader, text='', media=''):
        self.api.messages.send(random_id = random.randint(0,999999), peer_id = reader, message = text, attachment = media)

    def isAdmin(self, chat_id, member_id):
        try:
            return member_id in self.api.messages.getConversationsById(peer_ids = chat_id)['items'][0]['chat_settings']['admin_ids']
        except:
            return False

    def isOwner(self, chat_id, member_id):
            return member_id == self.api.messages.getConversationsById(peer_ids = chat_id)['items'][0]['chat_settings']['owner_id']

    def isInChat(self, chat_id, member_id):
        for i in self.api.messages.getConversationMembers(peer_id = chat_id)['items']:
            if i['member_id'] == member_id:
                return True
        else:
            return False

    def kick(self, chat_id, member_id):
        if member_id == self.id:
            self.send(chat_id+2000000000, self.media.get('selfkick'))
        else:
            try:
                if member_id != 0:
                    self.api.messages.removeChatUser(chat_id = chat_id, member_id = member_id)
            except:
                if self.isAdmin(chat_id+2000000000, member_id) or self.isOwner(chat_id+2000000000, member_id):
                    self.send(chat_id+2000000000, self.media.get('kickadm'))
                elif not self.isInChat(chat_id+2000000000, member_id):
                    self.send(chat_id+2000000000, self.media.get('kickfalse'))
                else:
                    self.send(chat_id+2000000000, self.media.get('kicknoadm'))
        

    def ban(self, chat_id, member_id):
        if member_id == self.id:
            self.send(chat_id+2000000000, self.media.get('selfban'))
        elif self.isAdmin(chat_id+2000000000, member_id) or self.isOwner(chat_id+2000000000, member_id):
            self.send(chat_id, self.media.get('banadm'))
        else:
            pass
            #блокировка пользователя
    def unban(self, chat_id, member_id):
        pass

    def getShortURL(self, chat_id, url):
        stat = self.api.utils.checkLink(url = url)['status']
        if stat == 'processing':
            self.send(chat_id, self.media.get('processingURL'))
        elif stat == 'banned':
            self.send(chat_id, self.media.get('bannedURL'))
        else:
            self.send(chat_id, 'Результат: ' + self.api.utils.getShortLink(url = url)['short_url'])

    def getObjID(self, uid):    
        try:
            if self.getObjKind(uid) == 'group':
                return -self.api.utils.resolveScreenName(screen_name = uid)['object_id']
            elif self.getObjKind(uid) == 'user':
                return self.api.utils.resolveScreenName(screen_name = uid)['object_id']
            else:
                return 0
        except:
            return 0


    def getObjKind(self, uid):
        return self.api.utils.resolveScreenName(screen_name = uid)['type']

    def getObjName(self, uid, rettype = 0):
        if type(uid) is str:
            if self.getObjKind(uid) == 'group':
                if rettype == 0:
                    return "{screen_name}".format(**self.api.groups.getById(group_id = uid)[0])
                elif rettype == 1:
                    return "[id{id}|{screen_name}]".format(**self.api.groups.getById(group_id = uid)[0])
            elif self.getObjKind(uid) == 'user':
                if rettype == 0:
                    return "{first_name}".format(**self.api.users.get(user_ids = uid)[0])
                elif rettype == 1:
                    return "[id{id}|{first_name}]".format(**self.api.users.get(user_ids = uid)[0])
            else:
                return "unknown object"
        elif type(uid) is int:
            if  uid < 0:
                if rettype == 0:
                    return "{screen_name}".format(**self.api.groups.getById(group_id = uid)[0])
                elif rettype == 1:
                    return "[id{id}|{screen_name}]".format(**self.api.groups.getById(group_id = uid)[0])
            elif uid > 0:
                if rettype == 0:
                    return "{first_name}".format(**self.api.users.get(user_ids = uid)[0])
                elif rettype == 1:
                    return "[id{id}|{first_name}]".format(**self.api.users.get(user_ids = uid)[0])
            else:
                return "unknown object"
    def uploadPhoto(self, url):
        b = requests.post(self.vkPhoto['upload_url'], files={'photo': url}).json()
        c = self.api.photos.saveMessagesPhoto(photo= b['photo'], server= b['server'], hash= b['hash'])[0]
        return 'photo{}_{}'.format(c['owner_id'], c['id'])

    def obr(self, message):
        reboot = False
        if message['peer_id'] > 2000000000:
            try:
                pass
            except:
                pass
            try:
                [mention, cmd] = message['text'].split(" ", 1) 
            except:
                mention = ''
            if self.media.isCommand(mention) == 'beta':
                lim, uids = [], []
                self.api.messages.setActivity(peer_id = message['peer_id'], type = 'typing')
                try:
                    [cmd, string] = cmd.split(" ", 1)
                except:
                    string = ''
                cmd = self.media.typeCommand(cmd)
                if cmd != 'unknown':
                    try:
                        uids.append(message['reply_message']['from_id'])
                    except:
                        pass
                    try:
                        for i in message['fwd_messages']:
                            uids.append(i['from_id'])
                    except:
                        pass
                    for i in string.split():
                        if i[0:3] == '[id':
                            uids.append(i[3:i.find('|')])
                        elif i[0:5] == '[club':
                            uids.append(-int(i[5:i.find('|')]))
                        elif i[0:7] == 'vk.com/' or i[0:14] == 'http://vk.com/' or i[0:15] == 'https://vk.com/':
                            uids.append(self.getObjID(i[i.rfind('/')+1:len(i)]))

                if cmd == 'kick':
                    if self.isAdmin(message['peer_id'], message['from_id']) or self.isOwner(message['peer_id'], message['from_id']):
                        if len(uids) == 0:
                            self.send(message['peer_id'], self.media.get('kick_noids'), '')
                        elif len(uids) == 1:
                            self.send(message['peer_id'], self.media.get('kick_one'), '')
                        else:
                            self.send(message['peer_id'], self.media.get('kick_more'), '')
                        for uid in uids:
                            self.kick(message['peer_id']-2000000000, uid)
                    else:
                        self.send(message['peer_id'], self.media.get('noadmrole'), '')

                elif cmd == 'ban':
                    if self.isAdmin(message['peer_id'], message['from_id']) or self.isOwner(message['peer_id'], message['from_id']):
                        if len(uids) == 0:
                            self.send(message['peer_id'], self.media.get('ban_noids'), '')
                        elif len(uids) == 1:
                            self.send(message['peer_id'], self.media.get('ban_one'), '')
                        else:
                            self.send(message['peer_id'], self.media.get('ban_more'), '')
                        for uid in uids:
                            self.ban(message['peer_id']-2000000000, uid)
                    else:
                        self.send(message['peer_id'], self.media.get('noadmrole'), '')
                elif cmd == 'unban':
                    if self.isAdmin(message['peer_id'], message['from_id']) or self.isOwner(message['peer_id'], message['from_id']):
                        if len(uids) == 0:
                            self.send(message['peer_id'], self.media.get('unban_noids'), '')
                        elif len(uids) == 1:
                            self.send(message['peer_id'], self.media.get('unban_one'), '')
                        else:
                            self.send(message['peer_id'], self.media.get('unban_more'), '')
                        for uid in uids:
                            self.unban(message['peer_id']-2000000000, uid)
                    else:
                        self.send(message['peer_id'], self.media.get('noadmrole'), '')
                elif cmd == 'chat':
                    if string in self.media.args['cmdargs']['chat_info']:
                        self.send(message['peer_id'], self.media.get('chat_info'), '')
                    elif string in self.media.args['cmdargs']['chat_admins']:
                        self.send(message['peer_id'], self.media.get('chat_admins'), '')
                    elif string in self.media.args['cmdargs']['chat_bl']:
                        self.send(message['peer_id'], self.media.get('chat_bl'), '')
                elif cmd == 'search':
                    self.send(message['peer_id'], self.media.get('search') + self.search.request(string), '') 
                elif cmd == 'trans':
                    e = string.split(" ", 1)
                    self.send(message['peer_id'], self.search.translate(e[1], e[0]), '') 
                elif cmd == 'rule':
                    for key, value in self.media.args['cmdargs'].items():
                        if key[0:5] == 'rule_' and string in value:
                            #rule db func
                            self.send(message['peer_id'], self.media.get('rule_att'), '')
                            break
                    else:
                        self.send(message['peer_id'], self.media.get('rule_empt'), '')
                elif cmd == 'weather':
                    self.send(message['peer_id'], self.weather.search(string), '')
                elif cmd == 'reboot':
                    if message['from_id'] in self.media.adms:
                        lim.append({'messageText': 'Хорошо, перезагружаюсь', 'messageAttachment': ''})
                    else:
                        lim.append({'messageText': self.media.get(cmd), 'messageAttachment': ''})

                elif cmd == 'url':
                    self.getShortURL(message['peer_id'], string)
                else:
                    lim.append({'messageText': self.media.get(cmd), 'messageAttachment': ''})
                
                for i in lim:
                    self.send(message['peer_id'], i['messageText'], i['messageAttachment'])
        elif message['text'] == 'Начать' or message['payload'] == '{"command":"start"}':
            self.send(message['peer_id'], self.media.get('startst1').format(name = self.getObjName(message['from_id'], 0)), '')
            self.send(message['peer_id'], self.media.get('startst2'), '')
        return reboot
                    


