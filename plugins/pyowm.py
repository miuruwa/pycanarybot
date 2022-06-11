import pyowm
class Object:
    def __init__(self):
        self.owm = pyowm.OWM('115fe76805a81b92ea81a3a280763fda')
        self.mgr = self.owm.weather_manager()
        self.cmd = {'search': 'погода'}

    def getCMD(self):
        return self.cmd
    
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

    def init(self, plugin_cmd, string):
        if plugin_cmd == 'search':
            text = self.search(string)
        else:
            text = 'where\'s a command?'
            
        return {
                'rule': '',
                'string': '',
                'lim': [
                    {'messageText': text, 'messageAttachment': ''}
                ],
                'uids': [],
            }