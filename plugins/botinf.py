class Object:
    def __init__(self):
        self.cmd = {'help': 'помощь', 'plugins': 'плагины_инфо'}
        self.args = {
            'noch': 'Пользователь не в чате.',
            'adm': 'Администраторов нельзя исключать',
            'noadm': 'У меня нет прав',
            'selfkick': 'Если тебе это так надо, то кикни меня самостоятельно.',
            'unknown': 'Неизвестная ошибка',
        }

    def getCMD(self):
        return self.cmd

    def get(self, req):
        return self.args[req]

    def compress(self, string):
        uids = []
        for i in string.split():
            if i[0] == '[':
                uids.append(i[1:i.find('|')])
            elif i[0:7] == 'vk.com/':
                if i.count('/') == 1:
                    uids.append(i[i.rfind('/')+1:len(i)])
            elif i[0:14] == 'http://vk.com/' or i[0:15] == 'https://vk.com/':
                uids.append(i[i.rfind('/')+1:len(i)])
        return uids

    def init(self, plugin_cmd, string):
        lim, uids, rule, args = [], [], '', ''
        if plugin_cmd == 'help':
            lim.append({
                'messageText': 'Канарейка | Чат-бот ВКонтакте, версия {}. Сделано [club195953234|Прокофьевым Андреем], 2020', 
                'messageAttachment': ''
            })
        elif plugin_cmd == 'plugins':
            rule = 'plugins'
            uids
        elif plugin_cmd == 'kick':
            rule = 'kick'
        elif plugin_cmd == 'unknown':
            lim.append({
                'messageText': 'Неизвестная команда, отправьте "[club195675828|@canarybot] помощь" для получения списка.', 
                'messageAttachment': ''
            })
        else:
            lim.append({
                'messageText': 'where\'s a command?', 
                'messageAttachment': ''
            })
            
        return {
                'rule': rule,
                'string': args,
                'lim': lim,
                'uids': uids,
            }