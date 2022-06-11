import random

class Object():
    def __init__(self):
        self.args = {
                'name': 'Ролевые игры',
                'author': 'andrew prokofieff',
                'type': 'chat',
                'all': [
                    '@all', '@everyone', 'всех'
                ],
                'commands': {
                    'hug': [
                            'обнять', 'обняв', 'обнял', 'обням', 'обнимашки', 
                        ],
                    'kiss': [
                            'чмаф', 'поцеловать', 'чмокнуть', 'поцелуй' 
                        ],
                    'fuck': [
                            'пригласить в постель', 'трахнуть', 'пометить', 'трах', 'фак', 
                        ]
                },
                'replies': {
                    'hug': [
                            '{from_id_name} обнял {sub_id}', 'Ого, {from_id_name} обнял {sub_id}', '{from_id_name} спрятал {sub_id} в своих обнимашках.', '{from_id_name}, {sub_id}. Ну вы поняли.',
                        ],
                    'fuck': [
                            '{from_id_name} трахнул {sub_id}', 'А дети будут?', '{from_id_name} принудил {sub_id} к сексуальным действиям', 'Может вы в другую комнату пойдёте?'
                        ],
                    'test': [
                        'roleplay'
                    ]
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
        args = dict['args']
        uids = dict['uids']

        if '[' in args:
            uids.append(args[args.find('[')+1:args.find('|')])

        if cmd_class in self.args['commands'].keys():
            if args in self.args['all']:
                lim.append({
                    'message': self.getReply(cmd_class).format(from_id_name = vk.getUserInfo(dict['from_id'])['mention'], sub_id = "всех"), 
                    'media': ''
                })
                
            elif len(uids) > 0:
                lim.append({
                    'message': self.getReply(cmd_class).format(from_id_name = vk.getUserInfo(dict['from_id'])['mention'], sub_id = vk.getUserInfo(uids[0], 'acc')['mention']), 
                    'media': ''
                })

            else:
                lim.append({
                        'message': 'А кого?', 
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