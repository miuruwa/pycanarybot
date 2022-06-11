import random

class Object():
    def __init__(self):
        self.args = {
                'name': 'Обработчик ГС',
                'author': 'andrew prokofieff',
                'type': 'user',
                'commands': {
                    'response': [
                            'распознать', 'гс'
                        ],
                    'link': [
                            'распознать_ссылка', 'гс_ссылка'
                        ]
                },
                'replies': {
                    'response': [
                            'Выделите голосовые сообщения!',
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
        args = dict['attachments']

        if cmd_class == 'response':
            if len(args) > 0:
                e = 'Голосовые сообщения: \n'
                for i in args:
                    if i['type'] == 'audio_message':
                        e+= f"\n{vk.getUserInfo(i['audio_message']['owner_id'])['mention']}: {i['audio_message']['transcript']}"
                lim.append({
                    'message': e, 
                    'media': ''
                })
            else:
                lim.append({
                    'message': self.getReply('response'), 
                    'media': ''
                })
        if cmd_class == 'link':
            if len(args) > 0:
                e = 'Голосовые сообщения: \n'
                for i in args:
                    if i['type'] == 'audio_message':
                        e+= f"\n[id{dict['from_id']}|{vk.getUserInfo(i['audio_message']['owner_id'])['first_name']}]: {i['audio_message']['link_mp3']}"
                lim.append({
                    'message': e, 
                    'media': ''
                })
            else:
                lim.append({
                    'message': self.getReply('response'), 
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
    [
        {
            'type': 'audio_message', 
            'audio_message': 
            {
                'id': 558786531, 
                'owner_id': 455357451, 
                'duration': 19,
                'transcript': 'Я хотела проситься на ночевку, но в итоге мне зачитали такому ради жизни папе. Просто пихал друг. Так говорит, ты еще много чего.', 
'transcript_state': 'done'}}]