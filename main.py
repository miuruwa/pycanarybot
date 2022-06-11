import importlib

from source.connect import session
from source.longpoll import longpoll

from source.methods import getmethod
from source.methods import tools

from source.parse import parser

token = 'fead8551c4e6b575ebd39dc6e347c0a660afbd91041ff47041ddcbc0d2edce3858efcfeb58b62fd63de1c'
gid = '195675828'

debug = 1

import libs #библиотеки Канарейки

cnr = session(token, gid)
lpl = longpoll(cnr)
api = getmethod(cnr)
tls = tools(api)

plugin = {}

for obj in libs.__all__:
    if (debug == 1 and obj.startswith('debug.')):
        continue
    plugin[obj] = getattr(importlib.import_module('libs.' + obj), 'Object')()

parse = parser(cnr, api, tls, lpl, plugin)

while True:
    parse.listen()

input()