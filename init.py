import importlib
i = input('\n\n\n\u0009Write a version: ')

token = "fead8551c4e6b575ebd39dc6e347c0a660afbd91041ff47041ddcbc0d2edce3858efcfeb58b62fd63de1c"
identificator = "195675828"

while i != 'exit':
    engine = importlib.import_module('engine_'+i)
    importlib.reload(engine)
    engine.init(token, identificator) #старый движок, и типа ах ах кончи
    
    engine = ''
    i = input('\n\u0009Write a type: ')

