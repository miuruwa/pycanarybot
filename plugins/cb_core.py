import random

class Object():
    def __init__(self):
        self.name = 'Плагин CanaryBot'
        self.type = 'user'
        self.v = '017'
        
        self.define = {
            'test': [
                'привет',
            ],
            'plugins': [
                'модули',
            ],
        }

        self.reply = {
            'test': [
                {
                    'message': 'Привет, мир!',
                    'attachment': ''
                }
            ],
            'unknown': [
                {
                    'message': '{from_id},',
                    'attachment': 'photo-195675828_457241068'
                }
            ]
        }

    def getReply(self, reply):
        return random.choice(self.reply[reply]) or reply

    def response(self, cmd, vk):
        lim, rules = [], []
        
        #обработка args если требуется
        if cmd['cmd_class'] == 'plugins':
            rules.append('plugins')
        elif cmd['cmd_class'] in self.define.keys():
            lim.append(self.getReply(cmd['cmd_class']))
        else:
            lim.append(self.getReply('unknown'))

        return {
            'messages': lim, 'rules': rules
        }
