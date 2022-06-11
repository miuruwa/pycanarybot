import random, traceback

class Object():
    def __init__(self):
        self.args = {
                'name': 'Методы для сообщений VK',
                'author': 'andrew prokofieff',
                'type': 'chat',
                'commands': {
                    'kick': [
                            'кик', 'исключить', 'кикнуть'
                        ],
                    'link': [
                            'ссылка', 'сократи', 'сократи'
                        ],
                },
                'replies': {
                    'test': [
                            'Привет, мир!',
                        ],
                    'kick_stt': [
                            'Исключаю пользователей.',
                        ],
                    'kick_err': [
                            'Не удалось исключить {} [{}]',
                        ],
                    'kick_fin': [
                            'Процедура завершена.',
                        ],
                    'short': [
                            'Результат: {}'
                        ]
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
        uids = dict['uids']

        
        if vk.isAdmin(dict['peer_id'], dict['from_id']) or vk.isOwner(dict['peer_id'], dict['from_id']):
            if cmd_class == 'kick':
                vk.send(dict['peer_id'],self.getReply('kick_stt'), '')

                if '[' in args:
                    uids.append(args[args.find('[')+1:args.find('|')])

                for uid in uids:
                    try:
                        res = vk.kick(dict['peer_id'] - 2000000000, vk.getUserInfo(uid)['id'])
                        if not res == '':
                            vk.send(dict['peer_id'], self.getReply('kick_err').format(vk.getUserInfo(uid, 'acc')['mention'], res), '')

                    except:
                        print(traceback.format_exc())
                        vk.send(dict['peer_id'], self.getReply('kick_err').format(vk.getUserInfo(uid, 'acc')['mention'], 'noid'), '')

                vk.send(dict['peer_id'], self.getReply('kick_fin'), '')

        if cmd_class == 'link':
            lim.append(
                {
                    'message': self.getReply('short').format(vk.getShortURL(dict['peer_id'], args)),
                    'media': ''
                }
            )

        elif not cmd_class in self.args['commands'].keys():
            rules = 'unknown'
        
        return {
                'rules': rules,
                'lim': lim,
            }

if __name__ == "__main__":
    test = Object()
    print(test.getReply('test'))