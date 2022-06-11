import random

class Object:
    name = 'CanaryBot basic plugin'
    only_chat = False
    commands = {
        'test': ['test'],
    }
    reply = {
        'test': [
            {
                'message': 'Hello world!',
                'attachment': ''
            },
        ],
    }


    def getReply(self, reply):
        if reply in self.reply:
            return random.choice(self.reply[reply]) 
        else:
            return {
                'message': reply, 'attachment': ''
            }

    def parse(self, tools, message):
        result = {
            'lim': [], 'rules': []
        }
        
        #tools.api = vk.com/dev/methods
        #tools.*** = юзабельные инструменты от автора

        command = ''
        
        for key, arr in self.commands.items():
            for cmd in arr:
                if message['text'].startswith(cmd):
                    command = key

                    # if len(message['text']) > len(cmd)+1 and message['text'][len(cmd)] == ' ':
                    #     args = message['text'][len(cmd)+1:]    

        if command == 'test':
            result['lim'].append(self.getReply('test'))

        return result