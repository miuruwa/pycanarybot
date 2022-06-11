import six
import random


class getmethod(object):
    __slots__ = ('_vk', '_method')
    def __init__(self, vk, method=None):
        self._vk = vk
        self._method = method


    def __getattr__(self, method):
        if '_' in method:
            m = method.split('_')
            method = m[0] + ''.join(i.title() for i in m[1:])

        return getmethod(self._vk, (self._method + '.' if self._method else '') + method)


    def __call__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)

        return self._vk.method(self._method, kwargs)


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
