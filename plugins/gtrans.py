from googletrans import Translator

class Object():
    def __init__(self):
        self.LANGUAGES = {
            'af': 'бурский',
            'sq': 'албанский',
            'am': 'амхарский',
            'ar': 'арабский',
            'hy': 'армянский',
            'az': 'азербайджанский',
            'eu': 'баскский',
            'be': 'белорусский',
            'bn': 'бенгальский',
            'bs': 'боснийски',
            'bg': 'болгарский',
            'ca': 'каталонский',
            'ceb': 'кебуано',
            'ny': 'чичева',
            'zh-cn': 'китайский',
            'co': 'корсиканcкий',
            'hr': 'хорватский',
            'cs': 'чешский',
            'da': 'датский',
            'nl': 'нидерландский',
            'en': 'английский',
            'eo': 'эсперанто',
            'et': 'эстонский',
            'tl': 'филиппинский',
            'fi': 'финский',
            'fr': 'французский',
            'fy': 'фризский',
            'gl': 'галисийский',
            'ka': 'грузинский',
            'de': 'немецкий',
            'el': 'греческий',
            'gu': 'гуджарати',
            'ht': 'гаитянский креольский',
            'ha': 'хауса',
            'haw': 'гавайский',
            'iw': 'иврит',
            'hi': 'хинди',
            'hmn': 'мяо',
            'hu': 'венгерский',
            'is': 'исландский',
            'ig': 'игбо',
            'id': 'индонезийский',
            'ga': 'ирландский',
            'it': 'итальянский',
            'ja': 'японский',
            'jw': 'яванский',
            'kn': 'каннада',
            'kk': 'казах',
            'km': 'кхмерский',
            'ko': 'корейский',
            'ku': 'курдский',
            'ky': 'киргизский',
            'lo': 'лао',
            'la': 'латинский',
            'lv': 'латышский',
            'lt': 'литовский',
            'lb': 'люксембургский',
            'mk': 'македонский',
            'mg': 'малагасийский',
            'ms': 'малайский',
            'ml': 'малаяла',
            'mt': 'мальтийский',
            'mi': 'маори',
            'mr': 'маратхи',
            'mn': 'монгольский',
            'my': 'бирманский',
            'ne': 'непальский',
            'no': 'норвежский',
            'ps': 'пушту',
            'fa': 'персидский',
            'pl': 'польский',
            'pt': 'португальский',
            'pa': 'панджаби',
            'ro': 'румынский',
            'ru': 'русский',
            'sm': 'самоанский',
            'gd': 'гэльский',
            'sr': 'сербский',
            'st': 'сесото',
            'sn': 'шона',
            'sd': 'синдхи',
            'si': 'сингалезский',
            'sk': 'словацкий',
            'sl': 'словенский',
            'so': 'сомалийский',
            'es': 'испанский',
            'su': 'суданский',
            'sw': 'суахили',
            'sv': 'шведский',
            'tg': 'таджикский',
            'ta': 'тамильский',
            'te': 'телугу',
            'th': 'тайский',
            'tr': 'турецкий',
            'uk': 'украинский',
            'ur': 'урду',
            'uz': 'узбекский',
            'vi': 'вьетнамский',
            'cy': 'уэльский',
            'xh': 'кос',
            'yi': 'идиш',
            'yo': 'йоруба',
            'zu': 'зулу',
            'fil': 'филиппинский',
            'he': 'иврит'
        }
        self.cmd = {'translate': 'переведи', 'langs': 'языки'}

    def getCMD(self):
        return self.cmd

    def init(self, plugin_cmd, string):
        if plugin_cmd == 'translate':
            text = self.translate(string[0:string.rfind('на')], self.getLangByStr(string[string.rfind('на')+3:len(string)]))
        elif plugin_cmd == 'langs':
            text = self.getLanguages()
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

    def translate(self, request, to='en'):
        if self.getLangEx(to):
            return Translator().translate(request, dest=to).text
        else:
            return 'Язык не определён'

    def getLanguages(self):
        result = 'Хорошо, вот все языки, доступные в Google Translate:\n'
        for lang in self.LANGUAGES.values():
            result += lang + ', '
        result = result[0:len(result)-2]+'.'
        return result
    
    def getLangEx(self, lang):
        return lang in self.LANGUAGES.keys()
    def getLangByStr(self, lang):
        for key, value in self.LANGUAGES.items():
            if value == lang:
                return key
        else:
            return 'unknown'
