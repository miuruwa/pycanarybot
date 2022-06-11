import sqlite3, vk_api, random, math, traceback
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

class CanaryBot:
    def __init__(self, vktoken, vkid, drop):
        self.id = vkid

        self.session = vk_api.VkApi(token=vktoken)
        self.longpoll = VkBotLongPoll(self.session, vkid)
        self.api = self.session.get_api()

        self.db = self.Database('db.db', drop)
        self.media = {
            'attachment': {
                'img_standart': 'photo-195675828_457241078',
                'img_start': 'photo-195675828_457241070',
                'img_ban': 'photo-195675828_457241069',
                'img_bankick': 'photo-195675828_457241081',
                'img_unban': 'photo-195675828_457241072',
                'img_viphelp': 'photo-195675828_457241071',
                'img_vipfail': 'photo-195675828_457241076',
                'img_admfail': 'photo-195675828_457241068',
                'img_admcheck': 'photo-195675828_457241077',
                'video_admhelp': 'video-193595427_456239018',
                'video_work': 'video-193492235_456239027',
            },
            'calls': ['канарейка', 'канари', 'каня', '[club196752424|@canarybot]', '[club196752424|Канарейка | Чат-бот ВКонтакте]'],
            'cmds': [
                {'type': 'test', 'look': 'test'},
                #{'type': 'test', 'look': 'test'},
            ],
            'replicas': {
                'questionsimple': ['Нет', 'Не совсем', 'Совсем нет', 'Ну почти', 'Плюс-минус', 'Да', 'Ну почти', 'Да, скорее всего', 'ДАДАДА','НЕЕЕТ', 'НЕЕЕЕ'],
                'questionwhy': ['Потому что потому', 'Так как ты дебил', 'А ведь ты плахой', 'Потому что сам виноват'],
                'questionwhen': ['reactwhen'],
                'questionhow': ['reacthow'],
                'questioncost': ['reactcost'],
                'mention': ['Да-дая','Мяу','Мур','Мяф','ку','Я тут','Хехе, а ты хитёр)','ай авэ у','Хд','Машка харе дрочить',''],
                'group_appear': ['Не поняла.','Всмысле..','Что..','Бли..','Ну бляяяяять..','т-т', 'Ну всё я звоню копам','чё тож тебя привели сюда пытать?)','бибрбирббибрбибрб','ха-ха-ха.','сук']
            }
        }
        print('Canary bot v009\nСделано Андреем Прокофьевым')

    def react(self):
        try:
            check = self.longpoll.check()
            for event in check:
                print('[{}]'.format(event))
                if event.type == VkBotEventType.MESSAGE_NEW:
                    self.request(event.object['message'])

                    
                    #self.chat.show(self, event.object['message']['peer_id'])
                    #with request(event.object('message')) as res:
                    #    for i in res['listOfMessages']:
                    #        self.send(event.object['message']['peer_id'], i['messageText'], i['messageAttachment'])
                    #    if res['kind'] == '':
                    #        pass
                    #    elif res['kind'] == 'action':
                    #        if res['rule'] == 'chat':
                    #            self.chat.change(event.object['message']['peer_id'], res['arg']) #arg = 'kind;string';; kind = [name, descr]
                    #        elif res['rule'] == 'user':
                    #            for i in res['ids']:
                    #                self.user.change(event.object['message']['peer_id'], res['arg'], ids) #arg = 'kind;string';; kind = [name, admin, vip, ban, unban, kick]
                    #    elif res['kind'] == 'unknown':
                    #        pass
            return True
        except:
            print(traceback.format_exc())
            return False
    class Database:
        def __init__(self, file, drop):
            self.connection = sqlite3.connect(file)
            self.cursor = self.connection.cursor()
            if drop:
                self.drop()
        def user_exist(self, user_id):
            with self.connection:
                result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
                return bool(len(result))

        def user_add(self, user_id):
            if not self.user_exist(user_id):
                with self.connection:
                    return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id))

        def chat_exist(self, peer_id):
            with self.connection:
                result = self.cursor.execute("SELECT * FROM chats WHERE peer_id = ?", (peer_id,)).fetchall()
                return bool(len(result))
        class ban:
            def get(peer_id, user_id):
                return True
            def delete(peer_id, user_id):
                pass
            def add(peer_id, user_id, reason):
                pass

        def drop(self):
            with self.connection:
                self.cursor.execute("DROP TABLE chats IF EXISTS")
                self.cursor.execute("DROP TABLE users IF EXISTS")
                self.cursor.execute("""CREATE TABLE chats (
                    id	INTEGER DEFAULT 1,
                    "eer_id	INTEGER DEFAULT 1,
                    character	TEXT,
                    PRIMARY KEY(id,peer_id)
                );""")
                self.cursor.execute("""CREATE TABLE "users" (
                    "id"	INTEGER DEFAULT 1,
                    "user_id"	INTEGER DEFAULT 1,
                    "name"	TEXT DEFAULT 'user_nickname',
                    "character"	TEXT,
                    "money"	INTEGER DEFAULT 0,
                    PRIMARY KEY("user_id","id")
                );""")


        def close(self):
            self.connection.close()
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
    def send(self, peer_id, message, attachment):
        try:
            self.api.messages.send(random_id=random.randint(0, 999999), peer_id = peer_id, message = message, attachment = attachment)
        except:
            print('Fail')

    def request(self, message):
        kind, rule, arg, ids, lom = 'null','null','',[],[]
        if message['peer_id']<2000000000:
            if message['payload'] == '{"command":"start"}':
                kind, rule = 'start', 'user'
                lom.append({
                    'messageText': 'Ой, привет, {}, почему ты пишешь мне?'.format(self.user.getUserName(message['from_id'], )),
                    'messageAttachment': ''
                })
                lom.append({
                    'messageText': 'В беседу? Тогда прочитай статью: vk.com/@canarybot-rules',
                    'messageAttachment': self.media['attachment']['img_standart']
                })
        else:
            text = message['text']
            work, commandtyped = False, False
            namestr, text = text[0: text.find(" ")], text[text.find(" ")+1:len(text)]
            command, args = text[0: len(text)], ''
            try:
                if message['action']['type'] == 'chat_invite_user' or message['action']['type'] == 'chat_invite_user_by_link':
                    if message['action']['member_id'] == str(-self.id):
                        lom.append({
                                'messageText': 'Всем приветик! Все команды и инструкция по настройке находятся по ссылке vk.com/@canarybot-rules!',
                                'messageAttachment': ''
                            })
                        rule = 'send'
                    elif message['action']['member_id'] > 0:
                        if db.ban.get(message['peer_id'], message['from_id'])['ex']:
                            lom.append({
                                'messageText': '{}, {} находится в чёрном списке, поэтому я его кикну.'.format(self.user.getUserName(message['from_id']), self.user.getUserName(message['action']['member_id'])),
                                'messageAttachment': ''})
                            if db.ban.get(message['peer_id'], message['from_id'])['re'] != '':
                                lom.append({
                                    'messageText': 'Причина блокировки: '.format(db.ban.get(message['peer_id'], message['from_id'])['re']),
                                    'messageAttachment': ''})
                            rule = 'kick'
                            ids.append(message['action']['member_id'])
                        else:
                            lom.append({
                                'messageText': 'Приветик, {}, прочти статью для ознакомления с командами: vk.com/@canarybot-rules'.format(self.user.getUserName(message['action']['member_id'])),
                                'messageAttachment': ''})
                    else:
                        lom.append({
                            'messageText': self.media['replicas']['group_appear'][random.randint(0, len(self.media['replicas']['group_appear'])-1)],
                            'messageAttachment': ''})
            except:
                pass
            for i in self.media['calls']:
                if text[0:len(i)] == i:
                    if text[len(i)] == ' ':
                        work = True 
                        break
                    else:
                        kind = 'replica'
                        lom.append({
                            'messageText': self.media['replicas']['mention'][random.randint(0, len(self.media['replicas']['mention'])-1)],
                            'messageAttachment': 'standalone'
                        })
                        break
            if work:
                kind = 'unknown'
                for i in self.media['cmds']:
                    if command[0:len(i)] == i and command[len(i)] == ' ':
                        args, commandtyped, string = command[len(cmd)+1:len(command)], True, 'userid'
                        break
                    elif command == i:
                        commandtyped, string = True, 'userid'
                        break
                if command.count("?")>0:
                    kind = 'question'
                    commandtyped = False
                if commandtyped:
                    if string == 'userid':
                        arr = args.split()
                        for i in arr:
                            if i.count('|') == 1 and i.count(']') == 1:
                                if i[0:3] == '[id':
                                    ids.append(int(i[3:i.find('|')]))
                                elif i[0:5] == '[club':
                                    ids.append(-int(i[5:i.find('|')]))
                            else:
                                arg = arg + ' ' + i
                        else:
                            arg = args
                        for i in message['fwd_messages']:
                            ids.append(i['from_id'])
                        try:
                            ids.append(int(message['reply_message']['from_id']))
                        except:
                            pass
            #реакция на переменную kind, значение которой мы получили при обработке команды

        return {
            'kind': kind,
            'rule': rule,
            'arg': arg,
            'pages': {'kind': string, 'ids': ids},
            'listOfMessages': lom,
        }