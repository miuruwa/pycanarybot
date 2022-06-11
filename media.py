import random
class Media:
    def __init__(self):
        self.version = '015'
        self.adms = [517114114]
        self.args = {
            'mentions': {
                'release': ['[club195675828|@canarybot]'], 
                'beta': ['betabot'],
            },
            'commands': {
                'kick': ['кик', 'исключить', 'исключи', 'kick'],
                'ban': ['бан', 'забанить', 'заблокировать', 'ban'],
                'unban': ['разбан', 'разбанить', 'разблокировать', 'unban'],
                'chat': ['чат', 'chat', 'конфа'],
                'url': ['ссылка', 'сократи', 'link'],
                'ver': ['version', 'версия'],
                'search': ['поиск', 'search'],
                'trans': ['translate', 'переведи'],
                'weather': ['weather', 'погода'],
                'betahelp': ['помощь', 'help'],
                'adm': ['!адм'],
                'rule': ['!правило', '!rule'],
            },
            'cmdargs': {
                'chat_info': ['инфо', 'info', 'инфа'],
                'chat_admins': ['админы', 'admins', 'адм'],
                'chat_bl': ['bl', 'чс'],
                'reboot': ['reboot', 'ребут'],
                'updateadm': ['адм', 'adm'],
                'updatevip': ['вип', 'vip'],
                'rule_botnews': ['новости', 'news'],
            },
            'reactions': {
                'ban_noids': ['Выделите сообщения пользователей для бана или добавьте упоминание/ссылку на них'],
                'ban_one': ['Блокирую пользователя...'],
                'ban_more': ['Блокирую пользователей...'],
                'banadm': ['Не получится забанить, мне нельзя блокировать администраторов беседы'],
                'selfban': ['Нет я саму себя банить точно не буду.'],
                'selfkick': ['Если тебе это надо, то исключи самостоятельно :\'('],
                'unban_noids': ['Выделите сообщения пользователей для разбана или добавьте упоминание/ссылку на них'],
                'unban_one': ['Выношу пользователя из чёрного списка беседы...'],
                'unban_more': ['Выношу пользователей из чёрного списка беседы...'],
                'kick_noids': ['Выделите сообщения пользователей для кика или добавьте упоминание/ссылку на них'],
                'kick_one': ['Исключаю пользователя...'],
                'kick_more': ['Исключаю пользователей...'],
                'kickadm': ['Не получилось кикнуть пользователя (Администратор беседы или её создатель).'],
                'kicknoadm': ['Не получилось кикнуть пользователя (Сообществу не выдана роль администратора).'],
                'kickfalse': ['Не получилось кикнуть пользователя (Пользователь не в беседе).'],
                'unknown': ['Неизвестная команда, отправьте "[club195675828|@canarybot] помощь" для получения списка.'],
                'ver': ['Канарейка | Чат-бот ВКонтакте, версия {}. Сделано [club195953234|Прокофьевым Андреем], 2020'.format(self.version)],
                'result': ['Процедура завершена'],
                'rule_att': ['Правило для вашей беседы обновлено.'],
                'rule_empt': ['Такого правила не существует.'],
                'noadmrole': ['Ошибка: у вас нет прав адмнистратора'],
                'bannedURL': ['Ссылка заблокирована, обратитесь в Техподдержку, если вы владелец сайта.'],
                'processingURL': ['Ссылка в процессе проверки, повторите позже.'],
                'search': ['Результат поиска: '],
                'betahelp': ['betabot kick *\nbetabot ban *\nbetabot unban *\nbetabot search string\nbetabot weather city\nbetabot translate *lang in two letters* *string*'],
                'emp': [''],
                'startst1': ['Ой, привет, {name}, почему ты пишешь мне?'],
                'startst2': ['Нужно добавиться в беседу? Ох, тогда прочти статью: vk.com/@canarybot-rules'],
            }
        }

    def isCommand(self, command):
        for key, value in self.args['mentions'].items():
            if command in value:
                return key
        else:
            return ''

    def typeCommand(self, command):
        for key, value in self.args['commands'].items():
            if command in value:
                return key
        else:
            return 'unknown'

    def get(self, key):
        try:
            return self.args['reactions'][key][random.randint(0,len(self.args['reactions'][key])-1)]
        except:
            return key