import random

class Object():
    def __init__(self):
        self.args = {
                'name': 'Движок CanaryBot',
                'author': 'andrew prokofieff',
                'type': 'user',
                'commands': {
                    'help': [
                            'помощь', 'начать',
                        ],
                    'info': [
                            'инфо', 'бот',
                        ],
                    'plugins': [
                            'плагины', 'модули',
                        ],
                },
                'replies': {
                    'test': [
                            'Привет, мир!',
                        ],
                    'info': [
                        'Канарейка | Чат-бот ВКонтакте, версия 016. Сделано Прокофьевым Андреем, 2020'
                    ],
                    'err': [
                            'Неизвестная ошибка', 'Аннаун ерро', 'Ты видишь что печатаешь?'
                        ],
                }
            }

    def getCommandDict(self):
        return {
            'cmd': self.args['commands'],
            'type': self.args['type']
        }
    def getReply(self, req):
        try:
            return random.choice(self.args['replies'][req])
        except:
            return req

    def response(self, dict, vk = None, database = None):
        lim = []
        rules = ''

        cmd_class = dict['cmd_class']

        if cmd_class == 'help':
            lim.append({
                'message': self.getReply('help'), 
                'media': ''
            })

            lim.append({
                'message': self.getReply('helpcommands'), 
                'media': ''
            })

        elif cmd_class == 'err':
            lim.append({
                'message': self.getReply('err'), 
                'media': 'photo-195675828_457241068'
            })

        elif cmd_class == 'info':
            lim.append({
                'message': self.getReply('info'), 
                'media': ''
            })

        elif cmd_class == 'plugins':
            rules = 'plugins'

        else:
            rules = 'unknown'
        
        return {
                'rules': rules,
                'lim': lim,
            }

if __name__ == "__main__":
    test = Object()
    print(test.getReply('test'))