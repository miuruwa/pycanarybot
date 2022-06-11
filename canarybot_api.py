import vk_api, traceback
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

class CanaryBot:
    def __init__(**args):
        try:
            self.id = vk_ID
            self.session = vk_api.VkApi(token=args['vk_Token'])
            self.longpoll = VkBotLongPoll(self.session, args['vk_ID'])
            self.api = self.session.get_api()
            self.media = args['media']
            return print('Canary bot v009\nСделано Андреем Прокофьевым')
        except:
            return print(traceback.format_exc())
    def check(**args):
        try:
            for event in self.longpoll.check():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    self.request(event.object['message'])
        except:
            return print(traceback.format_exc())
    def request(message)
        kind, rule, arg, ids, lom = 'null','null','',[],[]
        
        #обработка с помощью

