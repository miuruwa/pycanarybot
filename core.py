import plugins, importlib
import traceback

# Модуль для загрузки плагинов к боту

class Plugin():
    def __init__(self, token, gid, v):
        self.pluginsList = plugins.__all__
        self.pluginsDict = {}
        self.bot = API(token, gid, v)
        self.db = ''
        self.load()

    def load(self):
        print('Загрузка плагинов: \n')
        self.pluginsDict = {}

        for module in self.pluginsList:
            if not module.startswith('debug_'):
                try:
                    self.pluginsDict[module] = getattr(importlib.import_module("plugins."+ module), 'Object')()
                    print(f"Плагин \"{self.pluginsDict[module].args['name']}\" загружен")

                except:
                    print(f'Загрузка плагина "{module}" невозможна: файл повреждён')
    def pluginlist(self):
        listtext = 'Вот список установленных модулей: '
        
        for plugin in self.pluginsList:
            try:
                listtext += f"\n\u2022 {self.pluginsDict[plugin].args['name']}"
            except:
                continue
        
        return listtext
    def getResponse(self, message):
        command =  {
            'plugin': 'bot',
            'peer_id': message['peer_id'],
            'from_id': message['from_id'],
            'cmd_class': 'err',
            'args': '',
            'uids': [], 'attachments': []
        }
        for key, plugin in self.pluginsDict.items():
            for cmd_class, cmd_object in plugin.getCommandDict()['cmd'].items():
                for word in cmd_object:
                    if message['text'][1:].startswith(word) and self.kind(message['peer_id'], plugin.getCommandDict()['type']):

                        command['plugin'] = key
                        command['cmd_class'] = cmd_class

                        if len(message['text'][1:]) > len(word + ' ') and message['text'][1:][len(word)] == ' ':
                            command['args'] = message['text'][1:][len(word)+1:]

                        if 'reply_message' in message:
                            command['uids'].append(message['reply_message']['from_id'])

                            if 'attachments' in message['reply_message']:
                                command['attachments'].extend(message['reply_message']['attachments'])

                        elif 'fwd_messages' in message:
                            for mes in message['fwd_messages']:
                                command['uids'].append(mes['from_id'])

                                if 'attachments' in mes:
                                    command['attachments'].extend(mes['attachments'])
        try:
            result = self.get(command['plugin']).response(command, vk = self.bot, database = self.db)

            if 'lim' in result:
                for m in result['lim']:
                    self.bot.send(message['peer_id'], m['message'], m['media'])

            if result['rules'] == 'unknown':
                self.bot.send(message['peer_id'], self.get('bot').getReply('err'), 'photo-195675828_457241068')
            elif result['rules'] == 'plugins':
                self.bot.send(message['peer_id'], self.pluginlist(), 'photo-195675828_457239072')

        except:
            print(traceback.format_exc())
    
    def get(self, plugin_name):
        try:
            return self.pluginsDict[plugin_name]

        except:
            return 'Неизвестный плагин.'

    def kind(self, chat_id, typer):
        if chat_id > 2000000000 and typer == 'chat':
            return True

        elif typer == 'user':
            return True

        else:
            return False

import vk_api, random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# модуль для работы с ВК. Можно будет заменить, например, телегой.

class API:
    def __init__(self, token, gid, v):
        self.id = -int(gid)

        self.session = vk_api.VkApi(login = '996990883896', password = '1904901902300a', token = token, app_id = 6146827,  api_version='5.120')
        self.longpoll = VkBotLongPoll(self.session, gid)
        self.api = self.session.get_api()

        print(f'\nCanaryBot Example {v}: vk.com/club{gid}')
        

    def listen(self):
        for event in self.longpoll.check():
            if event.type == VkBotEventType.MESSAGE_NEW:
                yield event.object['message']

    def send(self, chat_id, text, att):
        self.api.messages.send(random_id = random.randint(0,999999), peer_id = chat_id, message = text, expire_ttl = 120, attachment = att)

    def getChatInfo(self, chat_id):
        res = self.api.messages.getConversationsById(peer_ids = chat_id)['items'][0]['chat_settings']

        return {
            'owner_id': res['owner_id'],
            'admin_ids': res['admin_ids'],
            'active_ids': res['admin_ids'],
            'title': res['title']
            }
    def getInviteLink(self, chat_id):
        return self.api.messages.getConversationsById(peer_ids = chat_id)['items'][0]['chat_settings']['invite_link']

    def kick(self, chat_id, member_id):
        try:
            if member_id != self.id:
                self.api.messages.removeChatUser(chat_id = chat_id, member_id = member_id)

                return ''

            else:
                return 'selfkick'

        except:
            try:
                if not self.isInChat(chat_id, member_id):
                    return 'noch'

                elif self.isAdmin(chat_id, member_id) or self.isOwner(chat_id, member_id):
                    return 'adm'

                else:
                    return 'unkn'

            except:
                return 'noadm'

    def getMemberLists(self, chat_id):
        for i in self.api.messages.getConversationMembers(peer_id = chat_id)['items']:
            yield i['member_id']
        
    def isInChat(self, chat_id, member_id):
        return member_id in self.getMemberLists(chat_id)

    def isOwner(self, chat_id, member_id):
        return member_id == self.getChatInfo(chat_id)['owner_id']

    def isAdmin(self, chat_id, member_id):
        return member_id in self.getChatInfo(chat_id)['admin_ids']

    def getUserInfo(self, member_id, name_case = 'nom'):
        if type(member_id) is str:
            uid = self.getObjID(member_id)
        
        else:
            uid = int(member_id)
        

        if uid > 0:
            res = self.api.users.get(user_ids = uid, name_case = name_case, fields='online, domain')[0]

            return {
                'id': uid,
                'first_name': res['first_name'],
                'last_name': res['last_name'],
                'online': res['online'],
                'domain': res['domain'],
                'mention': f"[id{res['id']}|{res['first_name']}]"
                }
        else:
            res = self.api.groups.getById(group_id = uid)[0]

            return {
                'id': uid,
                'first_name': res['name'],
                'last_name': '',
                'online': '',
                'domain': res['screen_name'],
                'mention': f"[id{uid}|{res['name']}]"
                }

    def getShortURL(self, chat_id, url):
        try:
            stat = self.api.utils.checkLink(url = url)['status']
        except:
            stat = 'non'

        if stat == 'processing':
            return 'ссылка в обработке.'
            
        elif stat == 'banned':
            return 'ссылка заблокирована.'

        elif stat == 'non':
            return 'ссылки не существует.'

        else:
            return self.api.utils.getShortLink(url = url)['short_url']

    def getObjID(self, uid):
        try:
            if self.getObjKind(uid) == 'group' or self.getObjKind(uid) == 'page':
                return -self.api.utils.resolveScreenName(screen_name = uid)['object_id']

            elif self.getObjKind(uid) == 'user':
                return self.api.utils.resolveScreenName(screen_name = uid)['object_id']

            else:
                return 0

        except:
            return 0
    
    def getObjKind(self, uid):
        return self.api.utils.resolveScreenName(screen_name = uid)['type']

# Проверка

if __name__ == "__main__":
    test = Plugin('', '', '')
    print(str(test.get('bot').args['name']))