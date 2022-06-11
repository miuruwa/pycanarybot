import requests


import threading
import logging
import time
import six
import random


class session():
    def __init__(self, token, gid):
        if token and gid:
            self.token = token
            self.gid = gid

            self.http = requests.session()
            self.http.headers.update({
                'User-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"})

            self.last_request = 0.0
            self.RPS_DELAY = 1 / 20.0
            self.lock = threading.Lock()
        
        else:
            raise print('You forgot a token and/or a gid!')


    def method(self, method, values, raw = False):
        values = values.copy() if values else {}
        
        if 'v' not in values:
            values['v'] = '5.130'
        if 'access_token' not in values:
            values['access_token'] = self.token

        with self.lock:
            delay = self.RPS_DELAY - (time.time() - self.last_request)

            if delay > 0:
                time.sleep(delay)

            response = self.http.post(
                'https://api.vk.com/method/' + method,
                values)
                
            self.last_request = time.time()

        if response.ok:
            response = response.json()

        else:
            response = {'error': {
                        'error_code': response.status_code,
                        'error_msg': response.reason}}
        if 'error' in response:
            print(f"[{response['error']['error_code']}] {response['error']['error_msg']}")

            if response is not None:
                return response

        return response if raw else response['response']

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
        
class get_api(object):
    __slots__ = ('_vk', '_method')
    def __init__(self, vk, method=None):
        self._vk = vk
        self._method = method


    def __getattr__(self, method):
        if '_' in method:
            m = method.split('_')
            method = m[0] + ''.join(i.title() for i in m[1:])

        return get_api(self._vk, (self._method + '.' if self._method else '') + method)


    def __call__(self, **kwargs):
        for k, v in six.iteritems(kwargs):
            if isinstance(v, (list, tuple)):
                kwargs[k] = ','.join(str(x) for x in v)

        return self._vk.method(self._method, kwargs)