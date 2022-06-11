import vk_api, plugins
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import importlib, random, traceback
class Main():
    def __init__(self, token = None, gid = None):
        if token and gid:
            self.session = vk_api.VkApi(token = token)
            self.api = self.session.get_api()

            self.longpoll = VkBotLongPoll(self.session, gid)

            self.v = '017'
            self.commands = ['#', '?', '%']
            
        else:
            raise print('Token and group id need!')

        self.allPlugins = self.replug()

    def listen(self):
        for event in self.longpoll.check():
            if event.type == VkBotEventType.MESSAGE_NEW and len(event.object['message']['text']) > 1:
                if self.isCommand(event.object['message']['text'][0]):
                    self.response(event.object['message'])

    def replug(self):
        pl = {}

        for plugin in plugins.__all__:
            pluginObj = getattr(importlib.import_module("plugins."+ plugin), 'Object')()

            if pluginObj.v == self.v:
                pl[plugin] = pluginObj
                print(f"{pluginObj.name} загружен")

            else:
                print(f"{pluginObj.name} устарел")
        
        return pl
    def kind(self, peer_id, pltype):
        return pltype == 'user' or peer_id > 2000000000 and pltype == 'chat'
    def pluginlist(self):
        listtext = 'Вот список установленных модулей: '
        
        for plugin in self.allPlugins:
            try:
                listtext += f"\n\u2022 {self.allPlugins[plugin].name}"
            except:
                continue
        
        return listtext
    def response(self, message):
        command =  {
            'plugin': 'cb_core',
            'peer_id': message['peer_id'],
            'from_id': message['from_id'],
            'cmd_class': 'unknown',
            'args': '',
            'uids': [], 'attachments': []
        }
        for name, plugin in self.allPlugins.items():
            for key, item in plugin.define.items():
                for word in item:
                    if message['text'][1:].startswith(word) and self.kind(message['peer_id'], plugin.type):
                        command['plugin'] = name
                        command['cmd_class'] = key

                        if len(message['text'][1:]) > len(word + ' ') and message['text'][1:][len(word)] == ' ':
                            command['args'] = message['text'][1:][len(word)+1:]

                        if 'reply_message' in message:
                            command['uids'].append(message['reply_message']['from_id'])

                            if 'attachments' in message['reply_message']:
                                command['attachments'].extend(message['reply_message']['attachments'])

                        elif 'fwd_messages' in message:
                            for mes in message['fwd_messages']:
                                command['uids'].append(mes['from_id'])

                                if 'attachments' in mes:
                                    command['attachments'].extend(mes['attachments'])
                        break
        try:
            result = self.allPlugins[command['plugin']].response(command, vk = self.api)

            if 'messages' in result:
                for m in result['messages']:
                    self.api.messages.send(random_id = random.randint(0, 999999), peer_id = message['peer_id'], message = m['message'], attachment = m['attachment'])
            if 'rules' in result:
                for m in result['rules']:
                    if m == 'unknown':
                        res = self.allPlugins[command['plugin']].getReply('unknown')
                        self.api.messages.send(random_id = random.randint(0, 999999), peer_id = message['peer_id'], message = res['message'], attachment = res['attachment'])
                    elif m == 'plugins':
                        self.api.messages.send(random_id = random.randint(0, 999999), peer_id = message['peer_id'], message = self.pluginlist(), attachment = 'photo-195675828_457239072')

        except:
            print(traceback.format_exc())

    def isCommand(self, ment):
        return ment in self.commands
                        
        
            