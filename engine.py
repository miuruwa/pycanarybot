import random, vk_api, requests, sqlite3, datetime
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType, VkBotMessageEvent, VkBotEvent
# pylint: disable=C0321
usrnames = ['канари', 'канарейка', 'кеня', 'каня', 'ка', 'к', 'ри']
admnames = ['админ', 'адм', 'ад', 'а', '[club195675828|@canarybot]']
admid = [1,0]
def get_connection():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect('database.db')
    return __connection
__connection = None
conn = get_connection()
c = conn.cursor()
def init(t, i):
    vk_session = vk_api.VkApi(token=t)
    global vk
    longpoll, vk = VkBotLongPoll(vk_session, i), vk_session.get_api()
    initWork, force = True, False
    print('VK Bot started succesfully')
    if force:
        c.execute('DROP TABLE IF EXISTS usrlist')
        c.execute('DROP TABLE IF EXISTS admlist')
        c.execute('DROP TABLE IF EXISTS banlist')
        print('dropped')
    conn.commit()
    if force:
        print('Data base have just dropped\n')
    else:
        print('Data base have just connected\n')
    while initWork:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.object['message']['peer_id'] > 2000000000:
                chat_id, user_id, text= event.object['message']['peer_id'], event.object['message']['from_id'], event.object['message']['text']
                call, trigger = text[0:text.find(" ")].lower(), text[text.find(" ")+1:len(text)] 
                banstatus = banch(chat_id, user_id) 
                if banstatus['rule'] == False:
                    if nc(call) == '':
                        pass
                    else:
                        result = react(chat_id, user_id, trigger, nc(call))
                        if result['rule'] == 'send':
                            vk_messageSend(result['messageText'], result['messageAttachment'], chat_id, user_id,event.object['message']['text'])
                        #elif result['rule'] == 'ban':
                        #    vk_removeChatUser(chat_id, user_id)
                        #    vk_messageSend(result['messageText'], result['messageAttachment'], chat_id, user_id,event.object['message']['text'])            
                elif banstatus['attempt'] > 0:
                    #vk_messageDelete(chat_id, user_id,event.object['message']['conversation_message_id']-13)
                    vk_messageSend(nickname(user_id)+' попытался нарушить табу беседы "' + vk_getChat(chat_id)['chat_settings']['title'] + '", осталось '+str(banstatus['attempt']) +' попыток.\nПричина бана: ' + banstatus['reason']+'.', 'null', chat_id, user_id,event.object['message']['text'])
                    c.execute('UPDATE banlist SET attempts = ? WHERE chat_id = ? AND user_id = ?', (banstatus['attempt']-1, chat_id, user_id))
                else:
                    #vk_messageDelete(chat_id, user_id,event.object['message']['conversation_message_id']-13)
                    vk_messageSend(nickname(user_id)+' попытался нарушить табу беседы "' + vk_getChat(chat_id)['chat_settings']['title'] + '", за что был исключен. \n Причина бана: ' + banstatus['reason']+'.', 'photo517114114_457255570', chat_id, user_id,event.object['message']['text'])
                    vk_removeChatUser(chat_id, user_id)
                        

def nc(callstr):
    ch = ''
    n = 0
    for n in range(len(admnames)):
        if callstr == admnames[n]:
            ch = 'adm'
    for n in range(len(usrnames)):
        if callstr == usrnames[n]:
            ch = 'usr'
    return ch
def vk_removeChatUser(chat_id: int, user_id: int):
    try:
        vk.messages.removeChatUser(chat_id = chat_id-2000000000, user_id = user_id)
    except:
        vk.messages.send(random_id=random.randint(0,999999), message= 'Не удалось исключить '+nickname(user_id)+' из беседы "' + vk_getChat(chat_id)['chat_settings']['title'] + '".\nНаверное сообщество или админ беседы', attachment='null', peer_id = chat_id)
def vk_messageSend(mess, att, peer, user, trigg):
    vk.messages.send(random_id=random.randint(0, 999999), message=mess, attachment = att, peer_id=peer)
    print('{}\n{}-{}: {} \nreaction: {} (with attachment \'{}\')\n'.format(str(datetime.datetime.now()),peer,user,trigg,mess,att))
def vk_getUsers(id:int):
    return vk.users.get(user_ids = id)[0]
def vk_getChat(id:int):
    return vk.messages.getConversationsById(peer_ids = id)['items'][0]
def vk_messageDelete(user_id:int, chat_id:int, id:int):
    try:
        vk.messages.delete(message_ids = id, delete_for_all = True)
    except:
        vk.messages.send(random_id=random.randint(0,999999), message= 'Не удалось удалить сообщение '+nickname(user_id)+' в вашей беседе.\nНаверное админ беседы', attachment='null', peer_id = chat_id)



def banch(chat_id: int, user_id: int):
    ch = False
    attempt,reason = 0,''
    c.execute('SELECT user_id, attempts, reason FROM banlist WHERE chat_id = ?', (chat_id,))
    res = c.fetchall()
    for i in range(len(res)):
        (usr, attempt, reason) = res[i]
        if (user_id, attempt, reason) == res[i]:
            ch = True
    return {'rule': ch, 'attempt': attempt, 'reason': reason }

def addban(chat_id: int, user_id: int, reason:str):
    try:
        c.execute("INSERT INTO banlist VALUES(?, ?, 3, ?)", (chat_id, user_id, reason))
        vk.messages.send(random_id=random.randint(0,999999), peer_id = chat_id, message=nickname(user_id)+' успешно занесён в чс беседы ' + getChatInfo(chat_id)['name'] + '. Пользователю дан шанс в виде 3 попыток уговорить админов вынести из ЧС')
    except:
        vk.messages.send(random_id=random.randint(0,999999), peer_id = chat_id, message=nickname(user_id)+' уже в чёрном списке беседы ' + getChatInfo(chat_id)['name'])
def deleteban(chat_id:int, user_id:int):
    try:
        c.execute("DELETE FROM banlist WHERE chat_id = ? AND user_id = ?", (chat_id, user_id))
        vk.messages.send(random_id=random.randint(0,999999), peer_id = chat_id, message=nickname(user_id)+' успешно вынесен из чс беседы ' + getChatInfo(chat_id)['name'] + '. Удачного общения :3')
    except:
        vk.messages.send(random_id=random.randint(0,999999), peer_id = chat_id, message=nickname(user_id)+' не состоял в чёрном списке беседы ' + getChatInfo(chat_id)['name'] + '.')

def nickname(user_id: int):
    c.execute("INSERT INTO usrlist SELECT "+str(user_id)+", '[id"+str(user_id)+"|"+vk_getUsers(user_id)['first_name']+"]', 0 WHERE NOT EXISTS(SELECT 1 FROM usrlist WHERE id = "+str(user_id)+")")
    conn.commit()
    c.execute("SELECT nickname FROM usrlist WHERE id = ?", (user_id,))
    (res,) = c.fetchall()[0]
    return res
def nickname_update(user_id: int, string:str):
    c.execute("INSERT INTO usrlist SELECT "+str(user_id)+", '[id"+str(user_id)+"|"+vk_getUsers(user_id)['first_name']+"]', 0 WHERE NOT EXISTS(SELECT 1 FROM usrlist WHERE id = "+str(user_id)+")")
    c.execute("SELECT nickname FROM usrlist WHERE id = ?", (user_id,))
    (old,) = c.fetchall()[0]
    c.execute("UPDATE usrlist SET nickname = '[id{}|{}]' WHERE id = {}".format(user_id,string,user_id))
    conn.commit()
    c.execute("SELECT nickname FROM usrlist WHERE id = ?", (user_id,))
    (res,) = c.fetchall()[0]
    return {'old': old, 'new': res,}
def admch(user_id: int):
    ch = False
    c.execute('SELECT id FROM admlist')
    res = c.fetchall()
    for i in res:
        if (user_id,) == i:
            ch = True
    return ch

def getChatInfo(chat_id):
    c.execute("INSERT INTO chtlist SELECT "+str(chat_id)+", '"+vk_getChat(chat_id)['chat_settings']['title']+"', '"+ str(vk_getChat(chat_id)['chat_settings']['members_count'])+" участников', 'photo517114114_457255420' WHERE NOT EXISTS(SELECT 1 FROM chtlist WHERE chat_id = "+str(chat_id)+")")
    conn.commit()
    c.execute("SELECT name, description, attachment FROM chtlist WHERE chat_id = ?", (chat_id,))
    (name, description, attachment) = c.fetchall()[0]
    return { 
        'name': name, 'description':description, 'attachment': attachment
    }

def react(chat_id:int, user_id:int, message:str, messageType: str):
    mess = 'check'
    att = 'photo517114114_457255027'
    rule = ''
    print("{}\n{}".format(user_id, message))
    if messageType == 'usr':
        if message[0:message.find(' ')].lower() == 'ник':
            nick = nickname_update(user_id, message[message.find(' ')+1:len(message)])
            mess = 'Поздравляем, вы сменили ник с {} на {}'.format(nick['old'], nick['new'])
            att = 'photo517114114_457253882'
            rule = 'send'
        elif message.lower() == 'банить не буш?' or message.lower() == 'банить не будешь?':
            mess = 'не буду'
            att = ''
            rule = 'send'
        elif message.lower() == 'инфо чат':
            info = getChatInfo(chat_id)
            mess = 'Информация о беседе "'+info['name']+'": \nОписание: '+info['description']
            att = info['attachment']
            rule = 'send'
        else:
            mess = 'Текст'
            att = 'photo517114114_457255552'
    #elif messageType == 'usr' and not banch(chat_id, user_id):
    #    mess = nickname(user_id)+' попытался нарушить табу беседы "' + vk_getChat(chat_id)['chat_settings']['title'] + '", за что был исключен из беседы'
    #    att = 'photo517114114_457255570'
    #    rule = 'ban'
    elif messageType == 'adm' and message.lower() == 'начать':
        mess = 'Привет, для начала работы прочтите статью: vk.com/@canarybot-rules001'
        att = 'photo517114114_457255420'
        rule = 'send'
    elif messageType == 'adm':
        if admch(user_id):
            if message.lower() == 'реакция':
                mess = 'О, привет, ' + nickname(user_id)
                att = 'photo517114114_457255552'
                rule = 'send'
                
            elif message[0:message.find(" ")].lower() == 'бан':
                addban(chat_id, message[message.find(" ")+1:len(message)][message.find['[id']:message.find["|"]],message[message.find(" ")+1:len(message)[message[message.find(" ")+1:len(message).find(" ")+1:len(message[message.find(" ")+1:len(message)])]]])
                
                rule = ''
            elif message[0:message.find(" ")].lower() == 'разбан':
                addban(chat_id, message[message.find(" ")+1:len(message)][message.find['[id']:message.find["|"]])
                rule = ''
            
            elif message == '':
                pass
        else:
            mess = nickname(user_id) + ', '
            att = 'photo517114114_457255443'
            rule = 'send'
    return {
        'messageText': mess,
        'messageAttachment': att,
        'rule': rule
        }

