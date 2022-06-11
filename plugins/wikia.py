import wikipedia

class Object:
    def __init__(self):
        self.cmd = {'wiki': 'вики'}
        wikipedia.set_lang('ru')

    def getCMD(self):
        return self.cmd

    def search(self, req):
        try:
            return "{}\nИсточник {}".format(wikipedia.summary(req, sentences=5), wikipedia.page(req).url)
        except:
            return "Ошибка."

    def init(self, plugin_cmd, string):
        if plugin_cmd == 'wiki':
            text = self.search(string)
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