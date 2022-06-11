import vk_api, database, datetime, math, traceback, json, random
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType



def init(init_token, init_group_id):
    global vk, session, group_id
    group_id = init_group_id
    session = True
    try:
        vk_session = vk_api.VkApi(token=init_token)
        longpoll = VkBotLongPoll(vk_session, init_group_id)
        vk = vk_session.get_api()

        print('VK API has been connected')
    except:
        print('Err: VK API has not been connected')
        session = False
    try:
        database.init()
        print('DataBase has been connected')
    except:
        print('Err: DataBase has not been connected')
        session = False
        print(traceback.format_exc())

    while session:
        #события для оболочки

        for event in longpoll.check():
            if event.type == VkBotEventType.MESSAGE_NEW:
                response(req(event.object['message']))

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Функции пользователей
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def getUserBD(chat_id, user_id):
    name, banReason = '', ''
    banStatus, modStatus, vipStatus, admStatus = False, False, 0, 0

    if user_id > 0:
        try:
            database.insert(insertstr="{}, '[id{}|{}]', 0, 0".format(user_id,str(user_id), vk.users.get(user_ids = user_id)[0]['first_name']), intostr="usrlist(id, name, admrole, viprole)")
            database.insert(intostr="chtlist(id, name, description)", insertstr="{}, '{}', '{} участников'".format(str(chat_id), vk.messages.getConversationsById(peer_ids = chat_id)['items'][0]['chat_settings']['title'], vk.messages.getConversationsById(peer_ids = chat_id)['items'][0]['chat_settings']['members_count']))
        except:
            pass
        (name, admStatus, vipStatus) = database.findw(selectstr = "name, admrole, viprole", fromstr = "usrlist", where = "id = " + str(user_id))[0]
        conv = vk.messages.getConversationsById(peer_ids = chat_id)['items'][0]['chat_settings']
        if conv['owner_id'] == user_id:
            modStatus = True
        else:
            for i in conv['admin_ids']:
                if user_id == i:
                    modStatus = True
        if banStatus == False and chat_id > 2000000000:
            (string,) = database.findw(selectstr="blacklist", fromstr= 'chtlist', where='id = '+ str(chat_id))[0]
            bl = toDict(string)
            for i in bl:
                if i['id'] == user_id:
                    banReason = i['reason']
                    banStatus = True
    else:
        name = name = '[club'+str(vk.groups.getById(group_id=str(math.fabs(user_id)))[0]['id'])+'|'+vk.groups.getById(group_id=str(math.fabs(user_id)))[0]['name']+']'
    return {
        'name': name, 'banReason': banReason,
        'banStatus': banStatus, 'modStatus': modStatus, 'admStatus': admStatus, 'vipStatus': vipStatus
    }
def updName(user_id: int, newName: str):
    if len(newName) > 30:
        return 0
    elif newName.lower() == 'admin':
        return 1
    else:
        database.update(updatestr="usrlist", setstr="name = '[id{}|{}]'".format(str(user_id), newName), where="id = " + str(user_id))
        return 2
def addBan(chat_id: int, user_id:int, reason: str):
    (string,) = database.findw(selectstr="blacklist", fromstr= 'chtlist', where='id = '+ str(chat_id))
    bl = toDict(string)
    bl.append({'id': user_id, 'reason': reason})
    database.update(updatestr="chtlist", setstr="blacklist = "+toStr(bl), where="id = "+ str(chat_id))
def remBan(chat_id: int, user_id:int):
    (string,) = database.findw(selectstr="blacklist", fromstr= 'chtlist', where='id = '+ str(chat_id))
    bl = toDict(string)
    for i in bl:
        if i['id'] == user_id:
            del i
    database.update(updatestr="chtlist", setstr="blacklist = "+toStr(bl), where="id = "+ str(chat_id))

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# перевод строки в словарь данных и обратно.
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def toDict(string):
    #return json.loads(string)
    return eval(string)
def toStr(Dict):
    #return json.dumps(Dict)
    return str(Dict)
    
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Информация о чате
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def getChatInfo(chat_id: int):
    try:
        database.insert(intostr="chtlist(id, name, description)", insertstr="{}, '{}', '{} участников'".format(str(chat_id), vk.messages.getConversationsById(peer_ids = chat_id)['items'][0]['chat_settings']['title'], vk.messages.getConversationsById(peer_ids = chat_id)['items'][0]['chat_settings']['members_count']))
    except:
        pass
    (name, description) = database.findw(selectstr="name, description", fromstr="chtlist", where="id = "+str(chat_id))[0]
    return {'name': name,
            'description': description}
def updChatInfo_name(chat_id: int, chatName: str):
    getChatInfo(chat_id)
    database.update(updatestr="chtlist", setstr="name = '{}'".format(chatName), where="id = " + str(chat_id))
def updChatInfo_description(chat_id: int, chatDescr: str):
    getChatInfo(chat_id)
    database.update(updatestr="chtlist", setstr="description = '{}'".format(chatDescr), where="id = " + str(chat_id))
def getChatBan(chat_id: int):
    text = ''
    (string,) = database.findw(selectstr="blacklist", fromstr= 'chtlist', where='id = '+ str(chat_id))
    bl = toDict(string)
    for i in bl:
        text = text + '\u2022 ' + getUserBD(chat_id, i['id'])['name'] + ' ('+ i['reason'] +')\n'
    return text
def getChatAdmin(chat_id: int):
    resource = vk.messages.getConversationsById(peer_ids = chat_id)['items'][0]['chat_settings']
    text = '\u2022 '+getUserBD(chat_id, resource['owner_id'])['name'] + ' (Основатель беседы)'
    for i in resource['admin_ids']:
        text = text + '\n\u2022 '+getUserBD(chat_id, i)['name']
    return text

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Обработка сообщения
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

def req(message):
    kind, string, ids = '', '', []
    if message['peer_id']<2000000000:
        if event.object['message']['payload'] == '{"command":"start"}':
            kind = 'starthelp'
    else:
        text = message['text']
        string ='userid'
        work, commandtyped = False, False
        namestr, text = text[0: text.find(" ")], text[text.find(" ")+1:len(text)]
        command, args = text[0: len(text)], ''
        for i in database.find(selectstr="name", fromstr="names"):
            if (namestr,) == i:
                work = True 
                break
        if work == True:
            kind = 'unknown'
            for i in database.find(selectstr="name, kind", fromstr="commands"):
                (cmd, kind) = i
                #print("{} - {}".format(cmd, command))
                if command[0:len(cmd)] == cmd:
                    args, commandtyped = command[len(cmd)+1:len(command)], True
                    break
                elif command == cmd:
                    commandtyped = True
                    break
            if command.count("?")>0:
                kind = 'question'
        if commandtyped:
            if string == 'userid':
                if args.count('[') > 0 and args.count('|') > 0 and args.count(']') > 0:
                    for i in args.split(' '):
                        if i[1:3] == 'id':
                            ids.append(int(i[3:i.find('|')]))
                else:
                    string = args
                for i in message['fwd_messages']:
                    ids.append(i['from_id'])
                try:
                    ids.append(int(message['reply_message']['from_id']))
                except:
                    pass
        #print("{}\n{}\n{}".format(str(kind), str(string), str(ids)))
    return {
        'kind': kind, 
        'message': {
            'peer_id': message['peer_id'],
            'from_id': message['from_id'],},
        'attachments': {
            'string': string,
            'ids': ids}
        }

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Сборка реакции
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

# request is {
#    'kind': 'testcmd',
#    'message': {'peer_id': 2000000001,
#        'from_id': 1},
#    'attachments': {'string': '',
#        'ids': []}
#    }

def response(req):
    listOfMessages = []
    messageType = ''
    rule = '' #kick, ban, unban, chatinfo, chatban, chatadmin
    kind = ''
    reason = ''
    #обработка request, сборка инструкции
    if req['kind'] == 'starthelp':
        listOfMessages.append({'messageText': 'Hello world!', 'messageAttachment': ''})
        messageType = 'START'
        rule = 'send'
    elif req['message']['peer_id']>2000000000:
        user = getUserBD(req['message']['peer_id'], req['message']['from_id'])
        if req['kind'] == 'ping':
            listOfMessages.append({'messageText': 'Hello world!', 'messageAttachment': ''})
            messageType = 'messageReact'
            rule = 'send'
        elif req['kind'] == 'greetings':
            listOfMessages.append({'messageText': 'greetings!', 'messageAttachment': ''})
            messageType = 'messageReact'
            rule = 'send'
        elif req['kind'] == 'help':
            listOfMessages.append({'messageText': 'Приветик, {}'.format(user['name']), 'messageAttachment': ''})
            messageType = 'messageReact'
            rule = 'send'
        elif req['kind'] == 'question':
            listOfMessages.append({'messageText': 'Ответ на вопрос!', 'messageAttachment': ''})
            messageType = 'messageReact'
            rule = 'send'
        elif req['kind'] == 'chatInfo':
            listOfMessages.append({'messageText': 'chatInfo', 'messageAttachment': ''})
            messageType = 'messageChatInfoShort'
            rule = 'send'
        elif req['kind'] == 'chatInfoAdm':
            listOfMessages.append({'messageText': 'chatInfoAdm', 'messageAttachment': ''})
            messageType = 'messageChatInfoAdm'
            rule = 'send' #Администраторы
        elif req['kind'] == 'chatInfoBL':
            listOfMessages.append({'messageText': 'chatInfoBL', 'messageAttachment': ''})
            messageType = 'messageChatInfoBL'
            rule = 'send' #Чёрный список
        elif req['kind'] == 'userInfo':
            listOfMessages.append({'messageText': 'userInfo', 'messageAttachment': ''})
            messageType = 'messageUserInfo'
            rule = 'send' #Инфа о пользователе
        elif req['kind'] == 'kick':
            if user['modStatus'] == True:
                listOfMessages.append({'messageText': 'kick', 'messageAttachment': ''})
                messageType = 'modUserKick'
                rule = 'kick'
        elif req['kind'] == 'ban':
            if user['modStatus'] == True:
                listOfMessages.append({'messageText': 'ban', 'messageAttachment': ''})
                messageType = 'modUserBan'
                rule = 'ban'
        elif req['kind'] == 'unban':
            if user['modStatus'] == True:
                listOfMessages.append({'messageText': 'unban', 'messageAttachment': ''})
                messageType = 'modUserUnban'
                rule = 'unban'
        elif req['kind'] == 'chatName':
            if user['modStatus'] == True:
                listOfMessages.append({'messageText': 'chatName', 'messageAttachment': ''})
                messageType = 'modChatName'
                rule = 'send'
        elif req['kind'] == 'chatDescr':
            if user['modStatus'] == True:
                listOfMessages.append({'messageText': 'chatDescr', 'messageAttachment': ''})
                messageType = 'modChatDescr'
                rule = 'send'
        elif req['kind'] == 'addAdm':
            if user['admStatus'] == True:
                listOfMessages.append({'messageText': 'addadm', 'messageAttachment': ''})
                messageType = 'admin_addAdm'
                rule = 'send'
        elif req['kind'] == 'remAdm':
            if user['admStatus'] == True:
                listOfMessages.append({'messageText': 'remAdm', 'messageAttachment': ''})
                messageType = 'admin_remAdm'
                rule = 'send'
        elif req['kind'] == 'addVIP':
            if user['admStatus'] == True:
                listOfMessages.append({'messageText': 'addVIP', 'messageAttachment': ''})
                messageType = 'admin_addVIP'
                rule = 'send'
        elif req['kind'] == 'remVIP':
            if user['admStatus'] == True:
                listOfMessages.append({'messageText': 'remVIP', 'messageAttachment': ''})
                messageType = 'admin_remVIP'
                rule = 'send'
        if req['kind'] != '' and len(listOfMessages) == 0:
            listOfMessages.append({'messageText': 'Чево? ":D', 'messageAttachment': ''})
            messageType = 'chatUnknownCMD'
            rule = 'send'
    #обработка инструкции

    if messageType != '':
        print('\u0009{} {}-{}\n\u0009\u0009Message: {}\n\u0009\u0009ReactType: {}\n'.format(str(datetime.datetime.now()), req['message']['peer_id'], req['message']['from_id'], req['kind'], messageType))
    for item in listOfMessages:
        vk.messages.send(random_id=random.randint(0, 999999), message=item['messageText'], attachment = item['messageAttachment'], peer_id=req['message']['peer_id'])
    
    if rule == 'send':
        pass
    elif rule == 'chat_info':
        resource = getChatInfo(req['message']['peer_id'])
        vk.messages.send(random_id=random.randint(0, 999999), message='"{}"\nID чата в базе данных: {}\n\nОписание: {}'.format(resource['name'],str(req['message']['peer_id']-2000000000), resource['description']), attachment=listOfMessages['messageAttachment'], peer_id=req['message']['peer_id'])
    elif rule == 'chat_blacklist':
        resource = getChatBan(req['message']['peer_id'])
        try:
            vk.messages.send(random_id=random.randint(0, 999999), message=resource, peer_id=req['message']['peer_id'])
        except:
            vk.messages.send(random_id=random.randint(0, 999999), message='а где', peer_id=req['message']['peer_id'])
    elif rule == 'chat_adminlist':
        resource = getChatAdmin(req['message']['peer_id'])
        vk.messages.send(random_id=random.randint(0, 999999), message=resource, peer_id=req['message']['peer_id'])
    elif rule == 'kick' and req['attachments']['string'] == 'userid':
        try:
            for i in req['attachments']['ids']:
                #print(i)
                vk.messages.removeChatUser(chat_id = req['message']['peer_id']-2000000000, user_id = i)
        except:
            vk.messages.send(random_id=random.randint(0, 999999), message='Не получилось кикнуть пользователя.', attachment = '', peer_id=req['message']['peer_id'])
    elif rule == 'ban' and req['attachments']['string'] == 'userid':
        try:
            for i in req['attachments']['ids']:
                addBan(req['message']['peer_id'], i, reason)
        except:
            vk.messages.send(random_id=random.randint(0, 999999), message='Не получилось забанить пользователя.', attachment = '', peer_id=req['message']['peer_id'])
    elif rule == 'unban' and req['attachments']['string'] == 'userid':
        try:
            for i in req['attachments']['ids']:
                remBan(req['message']['peer_id'], i)
        except:
            vk.messages.send(random_id=random.randint(0, 999999), message='Не получилось разбанить пользователя.', attachment = '', peer_id=req['message']['peer_id'])
    elif rule == 'reboot':
            session = False