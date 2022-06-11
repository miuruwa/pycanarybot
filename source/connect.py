import requests


import threading
import logging
import time


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