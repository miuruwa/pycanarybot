import importlib, traceback
token = 'fead8551c4e6b575ebd39dc6e347c0a660afbd91041ff47041ddcbc0d2edce3858efcfeb58b62fd63de1c'
identificator = "195675828"

while True:
    try:
        import engine
        importlib.reload(engine)
        engine.init(token, identificator)
    except:
        print(traceback.format_exc())

