class parser():
    calls = ['/', '%', '#', 'betabot '] #, 'канарейка ', 'канари ', 'каня ', '[club195675828|@canarybot]'

    def __init__(self, connection, api, tools, longpoll, plugins):
        self.connection = connection
        self.api = api
        self.tools = tools
        self.longpoll = longpoll
        
        self.plugins = plugins


    def listen(self):
        for event in self.longpoll.check():
            if event['type'] == 'message_new':
                self.parse(event['object']['message'])

    
    def mentions(self, text):
        for call in self.calls:
            if text.lower().startswith(call):
                return text[len(call):]
        else:
            if text == 'Привет, я подсяду?':
                return '$$$fool1'
                

    def paramscheck(self, keys):
        return bool(set(keys) & set(['action', 'payload', 'text']))


    def parse(self, message):
        # наличие action --> реакция на действия по типу выхода, киков, переименования, и тд.
        # наличие payload --> реакция на клавиатуру
        # наличие text --> реакция на остальные команды

        # если что-то из этого существует, то обязательно парсится client_info

        if self.paramscheck(message.keys()):
            
            if 'action' in message:
                pass

            elif 'payload' in message:
                pass
            
            elif 'text' in message:
                message['text'] = self.mentions(message['text'])
                lim, rules = [], []

                for plugin in self.plugins.values():
                    res = plugin.parse(self.tools, message)
                    
                    lim.extend(res['lim'])
                    rules.extend(res['rules'])

                if len(lim) == 0:
                    lim.append(self.plugins['basic'].getReply('unknown'))

                for m in lim:
                    self.tools.send(peer_id = message['peer_id'], message = m['message'], attachment = m['attachment'])
    

