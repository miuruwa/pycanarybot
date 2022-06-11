import random
import wikipedia

class Object():
    def __init__(self):
        wikipedia.set_lang('ru')
        self.args = {
                'name': 'Википедия (016)',
                'author': 'andrew prokofieff',
                'type': 'user',
                'commands': {
                    'wikia': [
                            'поиск',
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
        args = dict['args']

        if cmd_class == 'wikia':
            lim.append({
                'message': self.search(args), 
                'media': ''
            })
        else:
            rules = 'unknown'
        
        return {
                'rules': rules,
                'lim': lim,
            }

    def search(self, req):
        try:
            return "{}\nИсточник {}".format(wikipedia.summary(req, sentences=5), wikipedia.page(req).url)
        except:
            return "Ошибка."

if __name__ == "__main__":
    test = Object()
    print(test.getReply('test'))