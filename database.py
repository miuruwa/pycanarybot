class Database:
    def __init__(self, file, drop = False):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()
        if drop:
            self.drop()
    #user
    def getUserExists(self, user_id = 1):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))
    
    def UserAdd(self, user_id = 1, name = 'user'):
        if not self.getUserExists(user_id):
            with self.connection:
                return self.cursor.execute("INSERT INTO users (user_id, name) VALUES (?, ?)", (user_id, name))

    def getUserName(self, user_id = 1): 
        with self.connection:
            (name, ) = self.cursor.execute("SELECT name FROM users WHERE user_id = ?", (user_id,)).fetchall()[0]
            return name
    def changeUserName(self, user_id = 1, name = 'user'):
        with self.connection:
            return self.cursor.execute("UPDATE users SET name = '[id{}|{}]' WHERE user_id = {}".format(user_id, name, user_id))
    
    def getUserMoney(self, user_id = 1):
        with self.connection:
            (money,) = self.cursor.execute("SELECT money FROM users WHERE user_id = ?", (user_id,)).fetchall()[0]
            return money
    def getUserBan(self, user_id = 1, peer_id = 2000000001):
        bl = getChatBL(peer_id)
        for key, value in bl:
            if key == str(user_id):
                break
        else:
            return 1
        return 0
    def getUserAdm(self, user_id = 1):
        with self.connection:
            (admin,) = self.cursor.execute("SELECT admin FROM users WHERE user_id = ?", (user_id,)).fetchall()[0]
            return admin
    def getUserVIP(self, user_id = 1):
        with self.connection:
            (vip,) = self.cursor.execute("SELECT vip FROM users WHERE user_id = ?", (user_id,)).fetchall()[0]
            return vip

    def changeUserMoney(self, user_id = 1, count = 150):
        with self.connection:
            return self.cursor.execute("UPDATE users SET money = ? WHERE user_id = ?", (count,user_id))
    
    def updUserAdm(self, user_id = 1):
        with self.connection:
            if self.getUserAdm(user_id) = 0:
                return self.cursor.execute("UPDATE users SET admin = 1 WHERE user_id = ?", (user_id,))
            else:
                return self.cursor.execute("UPDATE users SET admin = 0 WHERE user_id = ?", (user_id,))
    
    def updUserVIP(self, user_id = 1):
        with self.connection:
            if self.getUserVIP(user_id) = 0:
                return self.cursor.execute("UPDATE users SET vip = 1 WHERE user_id = ?", (user_id,))
            else:
                return self.cursor.execute("UPDATE users SET vip = 0 WHERE user_id = ?", (user_id,))
    
    #chat
    def getChatExists(self, peer_id = 2000000001):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM chats WHERE peer_id = ?", (peer_id,)).fetchall()
            return bool(len(result))
    def ChatAdd(self, peer_id = 2000000001, name = 'chat'):
        if not self.getChatExists(peer_id):
            with self.connection:
                return self.cursor.execute("INSERT INTO chats (peer_id, peer_name) VALUES (?, ?)", (peer_id, name))

    def getChatName(self, peer_id = 2000000001):
        with self.connection:
            (name, ) = self.cursor.execute("SELECT peer_name FROM chats WHERE peer_id = ?", (peer_id,)).fetchall()[0]
            return name
    def getChatBL(self, peer_id = 2000000001):
        with self.connection:
            (bl, ) = self.cursor.execute("SELECT peer_bl FROM chats WHERE peer_id = ?", (peer_id,)).fetchall()[0]
            return eval(bl)
    
    def changeChatName(self, peer_id = 2000000001, name = 'chat'):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET peer_name = ? WHERE peer_id = ?".format(name, user_id))
    def updChatBL(self, peer_id = 2000000001, cell = {}):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET peer_bl = ? WHERE peer_id = ?".format(getChatBL(peer_id).update(cell), user_id))


    def drop(self):
        with self.connection:
            self.cursor.execute("DROP TABLE chats IF EXISTS")
            self.cursor.execute("DROP TABLE users IF EXISTS")
            self.cursor.execute("""
            CREATE TABLE "users" (
                "id"	INTEGER DEFAULT 1,
                "user_id"	INTEGER DEFAULT 1,
                "name"	TEXT DEFAULT 'name',
                "vip"	INTEGER DEFAULT 0,
                "admin"	INTEGER DEFAULT 0,
                "money"	INTEGER DEFAULT 150,
                PRIMARY KEY("id","user_id")
            );
            """)
            self.cursor.execute("""
            CREATE TABLE "chats" (
                "id"	INTEGER DEFAULT 1,
                "peer_id"	INTEGER DEFAULT 2000000001,
                "peer_name"	TEXT DEFAULT 'name',
                "peer_bl"	TEXT DEFAULT '{}',
                PRIMARY KEY("id","peer_id")
            );
            """)
