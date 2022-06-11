import importlib
import canarybot.connect
import canarybot.tools
import canarybot.parser

group_token = 'fead8551c4e6b575ebd39dc6e347c0a660afbd91041ff47041ddcbc0d2edce3858efcfeb58b62fd63de1c'
group_id = '195675828'
debug = 1

session = canarybot.connect.session(group_token, group_id)
longpoll = canarybot.connect.longpoll(session, group_id)

plugins = canarybot.tools.connectLibrary(canarybot.tools.directory(__file__))

# объявление парсера