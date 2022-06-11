from engine import * 
import random
import os
vktoken, vkid, session = 'd7c3e40e8e9ab15257e03d54c002da4c44e87403725c4daa9ff1acd85a0b051d94042f776d2625f71aff6', "196752424", True
randy = ['ксюша','ксюха','скинь сиськи','ну скинь','позязя']
bot = CanaryBot(vktoken, vkid, False)
for i in range(20):
    bot.send(peer_id=2000000002, message=randy[random.randint(0,2)], attachment='')
for i in range(5):
    bot.send(peer_id=2000000002, message=randy[random.randint(2,5)], attachment='')