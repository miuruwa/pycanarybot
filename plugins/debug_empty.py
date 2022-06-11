import random

class Object():
    def __init__(self):
        self.args = {
                'name': 'CanaryBot 016 Plugin Example',
                'author': 'andrew prokofieff',
                'type': 'chat',
                'commands': {
                    'test': [
                            'команда',
                        ]
                },
                'replies': {
                    'test': [
                            'Привет, мир!',
                        ],
                }
            }

    def getCommandDict(self):
        return {
            'cmd': self.args['commands'],
            'type': self.args['type']
        }
    def getReply(self, req):
        return random.choice(self.args['replies'][req])

    def response(self, dict, vk = None, database = None):
        lim = []
        rules = ''

        cmd_class = dict['cmd_class']
        # args = dict['args']
        # на случай если надо будет вспомогательные аргументы :D

        if cmd_class == 'test':
            lim.append({
                'message': self.getReply('test'), 
                'media': ''
            })
        else:
            rules = 'unknown'
        
        return {
                'rules': rules,
                'lim': lim,
            }

if __name__ == "__main__":
    test = Object()
    print(test.getReply('test'))