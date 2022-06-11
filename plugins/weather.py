import random, pyowm

class Object():
    def __init__(self):
        self.owm = pyowm.OWM('115fe76805a81b92ea81a3a280763fda')
        self.mgr = self.owm.weather_manager()
        self.args = {
                'name': 'Open Weather Map (016)',
                'author': 'andrew prokofieff',
                'type': 'user',
                'commands': {
                    'weather': [
                            'погода',
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

        if cmd_class == 'weather':
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
            
    def search(self, city):
            try:
                observation = self.mgr.weather_at_place(city)
                w = observation.weather
                temp = w.temperature('celsius')

                result = 'Погода в городе {}\n\nВетер: {} м/с,\nВлажность: {}%,\nТемпература: {}°С'.format(
                    city.title(), w.wind()['speed'], w.humidity, temp['temp'])
                return result
            except:
                return 'Ничего не найдено, возможно произошла ошибка, повторите позже.'

if __name__ == "__main__":
    test = Object()
    print(test.getReply('test'))