import requests


class longpoll():
    def __init__(self, vk, wait=25):
        self.vk = vk
        self.group_id = vk.gid
        self.wait = wait

        self.url = None
        self.key = None
        self.server = None
        self.ts = None

        self.session = requests.Session()

        self.update_longpoll_server()


    def update_longpoll_server(self, update_ts=True):
        values = {
            'group_id': self.group_id
        }
        response = self.vk.method('groups.getLongPollServer', values)

        self.key = response['key']
        self.server = response['server']

        self.url = self.server

        if update_ts:
            self.ts = response['ts']


    def check(self):
        values = {
            'act': 'a_check',
            'key': self.key,
            'ts': self.ts,
            'wait': self.wait,
        }

        response = self.session.get(
            self.url,
            params=values,
            timeout=self.wait + 10
        ).json()

        if 'failed' not in response:
            self.ts = response['ts']
            return [
                raw_event
                for raw_event in response['updates']
            ]

        elif response['failed'] == 1:
            self.ts = response['ts']

        elif response['failed'] == 2:
            self.update_longpoll_server(update_ts=False)

        elif response['failed'] == 3:
            self.update_longpoll_server()

        return []