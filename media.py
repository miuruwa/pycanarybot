import random
class media:
    def __init__():
        self.args = {
            'version': 'preview',
            'names': ['канарейка','канари','каня','[club196752424|@canarybot]'],
            'reply': {
                'help': [
                    {
                        'messageText': '{from_id_name}, вся нужная информация есть в этой статье: vk.com/@canarybot-rules',
                        'messageAttachment': ''
                    },
                ],
                'ping': [
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
                'chat_review': [
                    {
                        'messageText': 'Информация о беседе {chat_name}: \n\nОписание: {descr};\nКоличество участников: {member_count};\nКоличество участников в чёрном списке: {member_count_bl};\n\nАдминистраторы чата: {admin_list}',
                        'messageAttachment': ''
                    },
                ],
                'chat_blacklist': [
                    {
                        'messageText': 'Чёрный список беседы {chat_name}: {black_list}',
                        'messageAttachment': ''
                    },
                ],
                'chat_adminlist': [
                    {
                        'messageText': 'Администраторы беседы {chat_name}: {admin_list}',
                        'messageAttachment': ''
                    },
                ],
                'chat_online': [
                    {
                        'messageText': 'Пользователи в сети: {online}',
                        'messageAttachment': ''
                    },
                ],
                'empty': [
                    {
                        'messageText': '',
                        'messageAttachment': ''
                    },
                ],
            }
            #'': '',
        }

    def get(self, **args):
        setstr = self.args[args['name']]
        return setstr[random.randint(0,len(setstr))]

    """

    name начать
    name помощь
    name кто я
    name кто это + юзеры
    name кто админ
    name кто в чс
    name кто онлайн
    name чат
    name чат название
    name чат описание
    name кик
    name разбан
    name бан
    name ник
    {standalone.name} -- для использования standalone
    """