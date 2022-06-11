import vk_api, random

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

class CanaryBot:
    def __init__(self, token, gid):
        self.id = -int(gid)

        self.session = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.session, gid)
        self.api = self.session.get_api()
        

    def check(self):
        for event in self.longpoll.check():
            if event.type == VkBotEventType.MESSAGE_NEW:
                yield event.object['message']

    def send(self, chat_id, text, att):
        self.api.messages.send(random_id = random.randint(0,999999), peer_id = chat_id, message = text, attachment = att)

    def getChatInfo(self, chat_id):
        res = self.api.messages.getConversationsById(peer_ids = chat_id)['items'][0]['chat_settings']
        return {
            'owner_id': res['owner_id'],
            'admin_ids': res['admin_ids'],
            'active_ids': res['admin_ids'],
            'invite_link': res['see_invite_link'],
            'title': res['title']
            }
    
    def kick(self, chat_id, member_id):
        try:
            if member_id != self.id:
                self.api.messages.removeChatUser(chat_id = chat_id, member_id = member_id)
                return ''
            else:
                return 'selfkick'
        except:
            try:
                if not self.isInChat(chat_id, member_id):
                    return 'noch'
                elif self.isAdmin(chat_id, member_id) or self.isOwner(chat_id, member_id):
                    return 'adm'
                else:
                    return 'unkn'
            except:
                return 'noadm'

    def getMemberLists(self, chat_id):
        for i in self.api.messages.getConversationMembers(peer_id = chat_id)['items']:
            yield i['member_id']
        
    def isInChat(self, chat_id, member_id):
        return member_id in self.getMemberLists(chat_id)

    def isOwner(self, chat_id, member_id):
        return member_id == self.getChatInfo(chat_id)['owner_id']

    def isAdmin(self, chat_id, member_id):
        return member_id in self.getChatInfo(chat_id)['admin_ids']

    def getUserInfo(self, member_id):
        res = self.api.users.get(user_ids = member_id, fields='online, domain')
        return {
            'first_name': res['first_name'],
            'last_name': res['last_name'],
            'online': res['online'],
            'domain': res['domain'],
            }

    def getShortURL(self, chat_id, url):
        stat = self.api.utils.checkLink(url = url)['status']
        if stat == 'processing':
            return 'proc'
        elif stat == 'banned':
            return 'bann'
        else:
            return self.api.utils.getShortLink(url = url)['short_url']

    def getObjID(self, uid):
        try:
            if self.getObjKind(uid) == 'group' or self.getObjKind(uid) == 'page':
                return -self.api.utils.resolveScreenName(screen_name = uid)['object_id']
            elif self.getObjKind(uid) == 'user':
                return self.api.utils.resolveScreenName(screen_name = uid)['object_id']
            else:
                return 0
        except:
            return 0
    
    def getObjKind(self, uid):
        return self.api.utils.resolveScreenName(screen_name = uid)['type']
