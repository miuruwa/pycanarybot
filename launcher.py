import vkdev, mention, traceback, config
import react

canarybot = vkdev.CanaryBot(config.token, config.gid)
m = mention.MentionPy()

def init():
    while True:
        for message in canarybot.check():
            cmd = message['text'].split(" ", 2)
            cmd.append('')
            if not m.getMent(cmd[0]):
                continue
            resource = react.getPLuginByResponses(cmd[1])
            result = react.getPlugin(resource['plugin_name']).init(resource['plugin_cmd'], cmd[2])

            for event in result['lim']:
                canarybot.send(message['peer_id'], event['messageText'], event['messageAttachment'])
            
            if result['rule'] == '':
                pass
            
            elif result['rule'] == 'plugins':
                canarybot.send(message['peer_id'], react.installed(), '')
            elif result['rule'] == 'kick':
                for uid in result['uids']:
                    usr = canarybot.getObjID(uid)
                    res = canarybot.kick(message['peer_id'], usr)
                    if res != 'noch':
                        canarybot.send(message['peer_id'], react.getPlugin(resource['botinf']).get(res), '')

init()
            