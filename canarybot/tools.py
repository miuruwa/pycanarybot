import random
import glob
import importlib

from os.path import dirname
from os.path import basename
from os.path import isfile
from os.path import join

def directory(file):
    return dirname(file)

def connectLibrary(directory):
    a = glob.glob(join(directory + '\\library\\', "*.py"))
    b, c = [basename(f)[:-3] for f in a if isfile(f)], {}
    for obj in b:
        c[obj] = getattr(importlib.import_module('library.' + obj), 'Object')()
    return c

class tools(object):
    def __init__(self, api):
        self.api = api


    def send(self, peer_id, message, attachment):
        self.api.messages.send(random_id = random.randint(0,999999), peer_id = peer_id, message = message, attachment = attachment)


    def getchat(self, chat_id):
        pass


    def getmembers(self, chat_id):
        pass


    def isadmin(self, chat_id, user_id):
        pass


    def isowner(self, chat_id, user_id):
        pass


    def getmention(self, user_id):
        return f'[id{user_id}|id1]'


    def kick(self, chat_id, user_id):
        result = self.api.messages.removeChatUser(chat_id = chat_id - 2000000000, member_id = user_id)
        if 'error' in result:
            e = result['error']['error_code']
            if e == 925:
                return 1
                # self.send(chat_id, 'Не удалось исключить пользователя: нет прав администратора.')
            elif e == 935:
                return 2
                # self.send(chat_id, 'Не удалось исключить пользователя: такого профиля нет в чате.')
            elif e == 15:
                return 3
                # self.send(chat_id, 'Не удалось исключить пользователя: нельзя исключать администраторов.')


    def loadPhoto(self, file):
        pass
