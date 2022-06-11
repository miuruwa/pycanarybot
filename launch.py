import configure
import core
import datetime

class Launcher():
    def __init__(self, debug = False):
        self.data = configure.Data()
        self.debug = debug
        self.plugin = core.Plugin(self.data.token, self.data.gid, self.data.version)

    def check(self):
        for message in self.plugin.bot.listen():
            try:
                if 'text' in message:
                    if self.data.isCommand(message['text'][0]):
                        self.plugin.getResponse(message)
            except:
                pass

if __name__ == "__main__":
    while True:
        try:
            start = Launcher()
            while True:
                start.check()
        except:
            print(f"{datetime.datetime.now()}: error, reloading.")