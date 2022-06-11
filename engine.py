import vk_api, sqlite3, random, datetime, math, sys
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent, VkBotEvent
__connection = None

def get_connection(baseName: str):
    global __connection
    if __connection is None:
        __connection = sqlite3.connect(baseName)
    return __connection
    conn = get_connection()
    c = conn.cursor()

def init(t, i):
    vk_session = vk_api.VkApi(token=t)
    global vk, conn, c
    longpoll, vk = VkBotLongPoll(vk_session, i), vk_session.get_api()
    initWork = True
    print('VK API connected')
    
    conn = get_connection('database.db')
    c = conn.cursor()
    print('DB connected')
    while initWork:
        for event in longpoll.listen():
            print(event)
            if event.type == VkBotEventType.MESSAGE_NEW and event.object['message']['peer_id'] > 2000000000:
                chat_id, user_id, message = event.object['message']['peer_id'], event.object['message']['from_id'], event.object['message']['text']
                result = react(chat_id, user_id, message)
                if result['messageRule'] != '':
                    vk_messageSend(chat_id, user_id, result['messageText'], result['messageAttachment'], message)
                if result['messageRule'] == 'kick':
                    try:
                        vk_removeChatUser(chat_id, result['test'])
                    except:
                         vk_messageSend(chat_id, user_id, 'Ошибка, пользователь является админом или уже исключён', 'photo-195675828_457239175', message)
                elif result['messageRule'] == 'ban':
                    vk_messageDelete(event.object['message']['conversation_message_id'])
                    vk_removeChatUser(chat_id, user_id)
                elif result['messageRule'] == 'banUpdate':
                    vk_messageDelete(event.object['message']['conversation_message_id'])
                    c.execute("UPDATE banlist SET try = ? WHERE chat_id = ? AND user_id = ?", (banch(chat_id, user_id)['try']-1, chat_id, user_id))
                elif result['messageRule'] == 'close':
                    quit() 
                    

def banch(chat_id: int, user_id: int):
    ch, reason, tryin = False, '', 0
    c.execute('SELECT user_id, reason, try FROM banlist WHERE chat_id = ?', (chat_id,))
    res = c.fetchall()
    for i in range(len(res)):
        if ch == False:
            (usr, reason, tryin) = res[i]
            if user_id == usr:
                ch = True
    return {'rule': ch, 'try': tryin, 'reason': reason }
def vipch(user_id):
    getName(user_id)
    c.execute('SELECT viprole FROM usrlist WHERE id = ?', (user_id,))
    (res,) = c.fetchall()[0]
    return res
def admch(user_id):
    getName(user_id)
    c.execute('SELECT admrole FROM usrlist WHERE id = ?', (user_id,))
    (res,) = c.fetchall()[0]
    return res
def modch(chat_id, user_id):
    ch = False
    conv = vk_getChat(chat_id)['chat_settings']
    if conv['owner_id'] == user_id:
        ch = True
    else: 
        for i in conv['admin_ids']:
            if user_id == i:
                ch = True
    return ch
def namech(name: str):
    c.execute('SELECT type FROM names WHERE name = ?', (name,))
    try:
        (res,) = c.fetchall()[0]
        return res
    except:
        return 3

def getName(user_id: int):
    if user_id > 0:
        c.execute("INSERT INTO usrlist SELECT "+str(user_id)+", '[id"+str(user_id)+"|"+vk_getUsers(user_id)['first_name']+"]', 0, 0 WHERE NOT EXISTS(SELECT 1 FROM usrlist WHERE id = "+str(user_id)+")")
        conn.commit()
        c.execute("SELECT name FROM usrlist WHERE id = ?", (user_id,))
        (res,) = c.fetchall()[0]
    else: 
        res = '[club'+str(vk.groups.getById(group_id=str(math.fabs(user_id)))[0]['id'])+'|'+vk.groups.getById(group_id=str(math.fabs(user_id)))[0]['name']+']'
    return res
def updName(user_id: int, newName: str):
    if len(newName) > 30:
        newName = newName[0:29]
    old = getName(user_id)
    if newName == 'admin':
        res = old
        t = 0
    else:
        c.execute("UPDATE usrlist SET name = '[id{}|{}]' WHERE id = {}".format(user_id, newName, user_id))
        conn.commit()
        c.execute("SELECT name FROM usrlist WHERE id = ?", (user_id,))
        (res,) = c.fetchall()[0]
        t = 1
    return {'old': old, 'new': res, 'result': t}

def getChatInfo(chat_id: int):
    c.execute("INSERT INTO chtlist SELECT "+str(chat_id)+", '"+vk_getChat(chat_id)['chat_settings']['title']+"', '"+ str(vk_getChat(chat_id)['chat_settings']['members_count'])+" участников', 'photo517114114_457255420' WHERE NOT EXISTS(SELECT 1 FROM chtlist WHERE chat_id = "+str(chat_id)+")")
    conn.commit()
    c.execute("SELECT name, description, attachment FROM chtlist WHERE chat_id = ?", (chat_id,))
    (name, description, attachment) = c.fetchall()[0]
    return {'name': name, 
            'description': description, 
            'attachment': attachment}
def getChatAdm(chat_id: int):
    conv = vk_getChat(chat_id)['chat_settings']
    text = 'Создатель беседы: ' + getName(conv['owner_id']) + '\nАдмины: '
    for i in conv['admin_ids']:
        text = text + '\n\u2022 ' + getName(i) + ' ('+kind(i)+')'
    return text
def getChatBan(chat_id: int):
    text = ''
    c.execute("SELECT user_id, reason, try FROM banlist WHERE chat_id = ?", (chat_id,))
    for i in c.fetchall():
        (user_id, reason, att) = i
        text = text + '\n\u2022 ' + getName(user_id) + ' ('+str(att)+')'
    return text

def updChatInfo_name(chat_id: int, chatName: str):
    getChatInfo(chat_id)
    c.execute("UPDATE chtlist SET name = ? WHERE chat_id = ?", (chatName, chat_id))
    conn.commit()
def updChatInfo_description(chat_id: int, chatDescr: str):
    getChatInfo(chat_id)
    c.execute("UPDATE chtlist SET description = ? WHERE chat_id = ?", (chatDescr, chat_id))
    conn.commit()
def updChatInfo_attachment(chat_id: int, chatAtt: str):
    getChatInfo(chat_id)
    c.execute("UPDATE chtlist SET attachment = ? WHERE chat_id = ?", (chatAtt, chat_id))
    conn.commit()
def vk_getUsers(user_id: int):
    return vk.users.get(user_ids = user_id)[0]
def vk_getChat(chat_id):
    return vk.messages.getConversationsById(peer_ids = chat_id)['items'][0]
def vk_removeChatUser(chat_id: int, user_id: int):
    vk.messages.removeChatUser(chat_id = chat_id-2000000000, user_id = user_id)
def vk_messageSend(chat_id: int, user_id: int, message: str, attachment: str,trigg):
    vk.messages.send(random_id=random.randint(0, 999999), message=message, attachment = attachment, peer_id=chat_id)
    print('{}\n{}-{}: {} \nreaction: {} (with attachment \'{}\')\n'.format(str(datetime.datetime.now()),chat_id,user_id,trigg,message,attachment))
def vk_messageDelete(id: int):
    vk.messages.delete(message_ids=[id], delete_for_all=1)

def react(chat_id: int, user_id: int, message: str):
    messageText, messageAttachment, messageRule, identify_user = '', '', '', 0
    banch_res = banch(chat_id, user_id)
    if banch_res['rule'] == False:
        name, text = message[0:message.find(" ")].lower(), message[message.find(" ")+1:len(message)]
        namech_res = namech(name)
        if namech_res == 0:
            if text.lower() == 'начать':
                messageText = 'Приветствую вас, {}! Для начала пропишите "@canarybot помощь" и ознакомьтесь с командами!'.format(getName(user_id))
                messageAttachment = 'photo-195675828_457239172'
                messageRule = 'send'
            elif text.lower() == 'инфо чат':
                messageText = 'Информация о беседе "'+getChatInfo(chat_id)['name']+'"\n\n'+getChatAdm(chat_id)+'\n\nОписание: '+getChatInfo(chat_id)['description']
                messageAttachment = getChatInfo(chat_id)['attachment']
                messageRule = 'send'
            elif text[0:text.find(' ')].lower() == 'ник':
                nick = updName(user_id, text[text.find(' ')+1:len(text)])
                if nick['result'] == 0:
                    messageText = '{},'.format(getName(user_id))
                    messageAttachment = 'photo-195675828_457239169'
                    messageRule = 'send'
                else: 
                    messageText = 'Поздравляем, вы сменили ник с {} на {}'.format(nick['old'], nick['new'])
                    messageAttachment = 'photo517114114_457253882'
                    messageRule = 'send'
            elif text[0:text.find(' ')].lower() == 'кик':
                if modch(chat_id, user_id) and text.count('[id') == 1 and text.count('|') == 1 and text.count(']') == 1:
                    identify_user = int(text[text.find('[id')+3:text.find('|')])
                    messageText = '{} исключил {} из беседы.'.format(getName(user_id), getName(identify_user))
                    messageAttachment = ''
                    messageRule = 'kick'
                else:
                    messageText = '{} попытался кикнуть {}, но у него нет прав. нигадяй'.format(getName(user_id), getName(identify_user))
                    messageAttachment = ''
                    messageRule = 'kick'
            elif text[0:text.find(' ')].lower() == 'бан':
                if modch(chat_id, user_id) and text.count('[id') == 1 and text.count('|') == 1 and text.count(']') == 1:
                    identify_user = int(text[text.find('[id')+3:text.find('|')])
                    try:
                        c.execute("INSERT INTO banlist VALUES(?,?,?,3)", (chat_id, identify_user, text[text.find(']')+2:len(text)]))
                        conn.commit()
                        messageText = '{} забанил {}. нигадяй'.format(getName(user_id), getName(identify_user))
                        messageAttachment = 'photo-195675828_457239170'
                        messageRule = 'send'
                    except:
                        messageText = '{} уже забанен'.format(getName(identify_user))
                        messageAttachment = ''
                        messageRule = 'send'
                else:
                    messageText = '{} попытался забанить {}, но у него нет прав. нигадяй'.format(getName(user_id), getName(identify_user))
                    messageAttachment = ''
                    messageRule = 'send'
                pass
            elif text[0:text.find(' ')].lower() == 'разбан':
                if modch(chat_id, user_id) and text.count('[id') == 1 and text.count('|') == 1 and text.count(']') == 1:
                    identify_user = int(text[text.find('[id')+3:text.find('|')])
                    c.execute("DELETE FROM banlist WHERE chat_id = ? AND user_id = ?", (chat_id, identify_user))
                    conn.commit()
                    messageText = '{} разбанил {}. Неужли есть добрые люди..'.format(getName(user_id), getName(identify_user))
                    messageAttachment = 'photo-195675828_457239173'
                    messageRule = 'send'
                else:
                    messageText = '{} попытался забанить {}, но у него нет прав. нигадяй'.format(getName(user_id), getName(identify_user))
                    messageAttachment = ''
                    messageRule = 'send'
            elif text == 'инфо чс':
                if modch(chat_id, user_id):
                    messageText = '{}, вот чёрный список беседы: '.format(getName(user_id))+getChatBan(chat_id)
                    messageAttachment = ''
                    messageRule = 'send'
                else:
                    messageText = 'У тебя нет прав, {}, спроси администраторов для выполнения этой функции.'.format(getName(user_id))
                    messageAttachment = ''
                    messageRule = 'send'
        elif namech_res == 1:
            vipch_res = vipch(user_id)
            if vipch_res == 0:
                messageText = '{},'.format(getName(user_id))
                messageAttachment = 'photo-195675828_457239178'
                messageRule = 'send'
            else:
                if text.lower() == 'чек':
                    messageText = '{}, ваши вип права успешно установлены, для ознакомления с командами прочтите статью: vk.com/@canarybot-rules'.format(getName(user_id))
                    messageAttachment = 'photo-195675828_457239176'
                    messageRule = 'send'
                elif text.lower() == 'помощь':
                    messageText = 'vip.help'.format(getName(user_id))
                    messageAttachment = ''
                    messageRule = 'send'
                else:
                    pass
        elif namech_res == 2:
            admch_res = admch(user_id)
            if admch_res == 0:
                messageText = '{},'.format(getName(user_id))
                messageAttachment = 'photo-195675828_457239169'
                messageRule = 'send'
            else:
                if text == 'чек':
                    messageText = '{},'.format(getName(user_id))
                    messageAttachment = 'photo-195675828_457239179'
                    messageRule = 'send'
                elif text == 'помощь':
                    messageText = 'Лучше посмотри вот это:'
                    messageAttachment = 'video-193595427_456239018'
                    messageRule = 'send'
                elif text == 'закройся' or text == 'захлопнись' or text == 'пошла нахуй':
                    messageText = 'Ладно, пойду посплю..'
                    messageAttachment = ' '
                    messageRule = 'close'
                else:
                    pass
        else:
            pass
    elif banch_res['try'] > 1:
        messageText = '{} попытался нарушить табу беседы, осталось {} попыток.\nПричина блокировки: {}'.format(getName(user_id), banch_res['try']-1, banch_res['reason'])
        messageAttachment = 'null'
        messageRule = 'banUpdate'
    else: 
        messageText = '{} попытался нарушить табу беседы, за что был кикнут из беседы.\nПричина блокировки: {}'.format(getName(user_id), banch_res['reason'])
        messageAttachment = 'photo-195675828_457239183'
        messageRule = 'ban'
    return {'messageText': messageText,
            'messageAttachment': messageAttachment,
            'messageRule': messageRule,
            'test':identify_user}
        
def kind(user_id):
    if user_id > 0:
        return 'пользователь'
    else:
        return 'сообщество'




