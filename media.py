import random
class Media:
    def __init__():
        self.args = {
            'version': 'preview',
            'names': [
                'канарейка','канари','каня','[club196752424|@canarybot]'
            ],
            'kind': {
                'help': {
                    'cmd': [
                        'помощь', 'начать'
                        ],
                    'rule': 'null',
                    'maxid': 0,
                    'boolstr': 0,
                    'replycount': 'cycle',
                    'reply': [
                        {
                            'messageText': '{from_id_name}, вся нужная информация есть в этой статье: vk.com/@canarybot-rules',
                            'messageAttachment': ''
                        },
                    ],
                },
                'ping': {
                    'cmd': [
                        'пинг', 'мяу', 'мрр', 'как ты', 'ты кто'
                    ],
                    'rule': 'null',
                    'maxid': 0,
                    'boolstr': 0,
                    'replycount': 'random',
                    'reply': [
                        {
                            'messageText': 'Мяу',
                            'messageAttachment': ''
                        },
                        {
                            'messageText': 'Мур',
                            'messageAttachment': ''
                        },
                        {
                            'messageText': 'Ась?',
                            'messageAttachment': ''
                        },
                        {
                            'messageText': 'Что такое, {from_id_name}?',
                            'messageAttachment': ''
                        },
                        {
                            'messageText': 'Ай авэ у.',
                            'messageAttachment': ''
                        },
                    ],
                },
                'chat_review': {
                    'cmd': [
                        'инфа о беседе', 'чат инфо'
                    ],
                    'rule': 'chat_info',
                    'maxid': 0,
                    'boolstr': 0,
                    'replycount': 'cycle',
                    'reply': [
                        {
                            'messageText': 'Информация о беседе {chat_name}:',
                            'messageAttachment': ''
                        },
                        {
                            'messageText': 'Описание: {descr};\nКоличество участников: {member_count};\nКоличество участников в чёрном списке: {member_count_bl}',
                            'messageAttachment': ''
                        },
                    ],
                },
                'chat_blacklist': {
                    'cmd': [
                        'инфа о чс', 'кто в чс', 'чс'
                    ],
                    'rule': 'chat_bl',
                    'maxid': 0,
                    'boolstr': 0,
                    'replycount': 'cycle',
                    'reply': [
                        {
                            'messageText': 'Чёрный список беседы "{chat_name}":',
                            'messageAttachment': ''
                        },
                        {
                            'messageText': '{black_list}',
                            'messageAttachment': ''
                        },
                    ],
                },
                'chat_adminlist': {
                    'cmd': [
                        'инфа об админах', 'кто админ', 'чат админы', 'админы'
                    ],
                    'rule': 'chat_al',
                    'maxid': 0,
                    'boolstr': 0,
                    'replycount': 'cycle',
                    'reply':[
                        {
                            'messageText': 'Администраторы беседы "{chat_name}":',
                            'messageAttachment': ''
                        },
                        {
                            'messageText': '{admin_list}',
                            'messageAttachment': ''
                        },
                    ],
                }, 
                'chat_online': {
                    'cmd': [
                        'кто онлайн', 'онлайн', 'кто в сети'
                    ], 
                    'rule': 'chat_online',
                    'maxid': 0,
                    'boolstr': 0,
                    'replycount': 'cycle',
                    'reply':[
                        {
                            'messageText': 'Вот пользователи в сети, {from_id_name}:',
                            'messageAttachment': ''
                        },
                        {
                            'messageText': '{online}',
                            'messageAttachment': ''
                        },
                    ],
                },
                'chat_kick': {
                    'cmd': [
                        'кик'
                    ], 
                    'rule': 'chat_kick',
                    'maxid': -1,
                    'boolstr': 0,
                    'replycount': 'random',
                    'reply':[
                        {
                            'messageText': 'Исключаю пользователя...',
                            'messageAttachment': ''
                        },
                    ],
                },
                'chat_ban': {
                    'cmd': [
                        'кик'
                    ], 
                    'rule': 'chat_ban',
                    'maxid': -1,
                    'boolstr': 0,
                    'replycount': 'random',
                    'reply':[
                        {
                            'messageText': 'Пользователь в чёрном списке. Нигадяй.',
                            'messageAttachment': ''
                        },
                    ],
                },
                'chat_unban': {
                    'cmd': [
                        'кик'
                    ], 
                    'rule': 'chat_unban',
                    'maxid': -1,
                    'boolstr': 0,
                    'replycount': 'random',
                    'reply':[
                        {
                            'messageText': 'Выношу пользователя из списка. Неужели есть добрые люди...',
                            'messageAttachment': ''
                        },
                    ],
                },
                'unknown': {
                    'cmd': [
                        '$$$ dont required $$$'
                    ], 
                    'rule': 'null',
                    'maxid': 0,
                    'boolstr': 0,
                    'replycount': 'random',
                    'reply':[
                        {
                            'messageText':'{from_id_name}, я тебя не поняла',
                            'messageAttachment': ''
                        },
                        {
                            'messageText':'{from_id_name}, БИП БОП БУП. БУП БИП?',
                            'messageAttachment': ''
                        },
                    ]
                },
                """
                'empty': {
                    'cmd': [
                        'empty'
                    ], 
                    'rule': 'null',
                    'maxid': 0,
                    'boolstr': 0,
                    'reply':[
                        {
                            'messageText':'',
                            'messageAttachment': ''
                        }
                    ]
                },
                {from_id_name}, {second_id_name}
                {chat_name}, {descr}, {member_count}, {member_count_bl}
                {admin_list}, {black_list}, {ban_reason}, {online}
                {your_text}
                """
            }
        }

    def define(self, **kwargs):
        text, cmd, rule, maxid, string = kwargs['text'], '', 'null', 0, ''
        for i in self.args.names:
            #проверка на обращение к боту
            if text[0:len(i)+1] == i + ' ':
                #это точно обращение, значит прерываем функцию и обрабатываем тип команды
                text = text[len(i)+1:len(text)]
                break
        else:
            rule = 'unknown'
            for cmd_key, cmd_value in self.args.cmd.items():
                #смотрим типы команд
                for cmd_string in cmd_value['cmd']:
                    #сравнение текста с массивом типа
                    #нужный тип, если текст равен ячейке массива
                    if cmd_value['boolstr'] == 0 and text == cmd_string:
                        break
                    elif cmd_value['boolstr'] == 1 and text[0:len(cmd_string)] == cmd_string:
                        string = text[len(string)+2]
                        break
                    else:
                        pass
                else:
                    #rule - правка для обработчика, по сути для вставок по типу "{online}"
                    #maxid - максимально допустимое число прикреплённых пользователей
                    #-1 - неограниченное
                    #0 - без вложений
                    #остальные числа влияют как длина массива
                    cmd, rule, maxid = cmd_key, cmd_value['rule'], cmd_value['maxid']
                    break
        return {
            'cmd': cmd, 'rule': rule, 'maxids': maxid, 'string': string
        }
    def get(self, cmdkind, formatt):
        if self.args['kind'][cmdkind]['replycount'] == 'random':
            lim.append(self.args['kind'][cmdkind]['reply'][random.randint(0,len(setstr))].format(**formatt))
        elif self.args['kind'][cmdkind]['replycount'] == 'cycle':
            lim = []
            for i in self.args['kind'][cmdkind]['reply']:
                lim.append(i)
        return lim

    """

    name начать / null
    name помощь / null
    name кто я / user_info
    name кто это + юзер / user_info
    name кто админ / chat_al
    name кто в чс / chat_bl
    name кто онлайн / chat_online
    name чат / chat_review
    name чат название / chat_name
    name чат описание / chat_descr
    name кик / chat_kick
    name разбан / chat_unban
    name бан / chat_ban
    name ник / user_nickname
    {standalone.name} -- для использования standalone
    """