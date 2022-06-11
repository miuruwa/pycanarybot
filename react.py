import plugins, importlib
pluginsList, pluginsDict = plugins.__all__, {}

for module in pluginsList:
    pluginsDict[module] = getattr(importlib.import_module("plugins."+ module), 'Object')()
    print('PLUGIN ' + module.upper() + '\u0009LOADED')

print('PLUGINS LOADED.')
 
def getPLuginByResponses(string):
    for plugin_name, plugin_class in pluginsDict.items():
        for cmd, response in plugin_class.getCMD().items():
            if string == response:
                return {'plugin_name': plugin_name, 'plugin_cmd': cmd}
    else:
        return {'plugin_name': 'botinf', 'plugin_cmd': 'unknown'}
    
def getPlugin(plugin_name):
    return pluginsDict[plugin_name]

def installed():
    text = 'Installed plugins for Canarybot (015):'
    for module in pluginsList:
        text += "\n\u2022 {}".format(module)
    return text