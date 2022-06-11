class Data():
    def __init__(self):
        self.token = "d7c3e40e8e9ab15257e03d54c002da4c44e87403725c4daa9ff1acd85a0b051d94042f776d2625f71aff6"
        self.gid = "196752424"
        self.version = "016"
        self.commands = ['#', '?', '%']
        print('Запуск бота...\n')

    def isCommand(self, ment):
        return ment in self.commands
