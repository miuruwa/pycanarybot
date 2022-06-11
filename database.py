import sqlite3
class Database:
    def __init__(self, file, drop = False):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()
        if drop:
            self.drop()
    #user
    def getUserExists(self, user_id = 1):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchall()
            return bool(len(result))
    
    def UserAdd(self, user_id = 1, name = '{first_name}'):
        if not self.getUserExists(user_id):
            with self.connection:
                return self.cursor.execute("INSERT INTO users (id, name) VALUES (?, ?)", (user_id, name))

    def getUserName(self, user_id = 1): 
        with self.connection:
            (name, ) = self.cursor.execute("SELECT name FROM users WHERE id = ?", (user_id,)).fetchall()[0]
            return name
    def changeUserName(self, user_id = 1, name = '{first_name}'):
        with self.connection:
            return self.cursor.execute("UPDATE users SET name = '[id{}|{}]' WHERE id = {}".format(user_id, name, user_id))
    
    def getUserMoney(self, user_id = 1):
        with self.connection:
            (money,) = self.cursor.execute("SELECT money FROM users WHERE id = ?", (user_id,)).fetchall()[0]
            return money
    def getUserBan(self, user_id = 1, peer_id = 2000000001):
        bl = self.getChatBL(peer_id)
        if (user_id, ) in bl:
            return 1
        else:
            return 0
    def getUserAdm(self, user_id = 1):
        with self.connection:
            return (1, ) in self.cursor.execute("SELECT admin FROM users WHERE id = ?", (user_id,)).fetchall()[0]
    def getUserVIP(self, user_id = 1):
        with self.connection:
            return (1, ) in self.cursor.execute("SELECT vip FROM users WHERE id = ?", (user_id,)).fetchall()[0]

    def changeUserMoney(self, user_id = 1, count = 150):
        with self.connection:
            return self.cursor.execute("UPDATE users SET money = ? WHERE id = ?", (count,user_id))
    
    def updUserAdm(self, user_id = 1):
        with self.connection:
            if self.getUserAdm(user_id):
                return self.cursor.execute("UPDATE users SET admin = 0 WHERE id = ?", (user_id,))
            else:
                return self.cursor.execute("UPDATE users SET admin = 1 WHERE id = ?", (user_id,))
    
    def updUserVIP(self, user_id = 1):
        with self.connection:
            if self.getUserVIP(user_id):
                return self.cursor.execute("UPDATE users SET vip = 0 WHERE id = ?", (user_id,))
            else:
                return self.cursor.execute("UPDATE users SET vip = 1 WHERE id = ?", (user_id,))
    
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
            return self.cursor.execute("SELECT user_id FROM banlist WHERE peer_id = ?", (peer_id,)).fetchall()
    
    def changeChatName(self, peer_id = 2000000001, name = 'chat'):
        with self.connection:
            return self.cursor.execute("UPDATE chats SET peer_name = ? WHERE peer_id = ?", (name, peer_id))

    def addtoChatBL(self, peer_id = 2000000001, user_id = 1, reason = ''):
        with self.connection:
            return self.cursor.execute("INSERT INTO banlist (peer_id, member_id, reason) VALUES(?, ?, ?)", (peer_id, user_id, reason)) 

    def delfrChatBL(self, peer_id = 2000000001, user_id = 1):
        with self.connection:
            return self.cursor.execute("DELETE FROM banlist WHERE peer_id = ? AND member_id = ?", (peer_id, user_id)) 

    def drop(self):
        with self.connection:
            self.cursor.execute("DROP TABLE chats IF EXISTS")
            self.cursor.execute("DROP TABLE users IF EXISTS")
            self.cursor.execute("DROP TABLE banlist IF EXISTS")
            self.cursor.execute("""
            CREATE TABLE "users" (
                "id"	INTEGER,
                "name"	INTEGER DEFAULT '{first_name}',
                "money"	INTEGER DEFAULT 0,
                "admin"	INTEGER DEFAULT 0,
	            "vip"	INTEGER DEFAULT 0,
                PRIMARY KEY("id")
            );
            """)
            self.cursor.execute("""
            CREATE TABLE "chats" (
                "peer_id"	INTEGER DEFAULT 2000000000,
                "peer_name"	TEXT DEFAULT 'chat_name',
                "peer_descr"	TEXT DEFAULT 'chat_description',
                "rule_autokick"	INTEGER DEFAULT 0,
                "rule_botnews"	INTEGER DEFAULT 0,
                PRIMARY KEY("peer_id")
            );
            """)
            self.cursor.execute("""
            CREATE TABLE "banlist" (
                "peer_id"	INTEGER NOT NULL DEFAULT 2000000000,
                "member_id"	INTEGER DEFAULT 1,
                "reason"	TEXT DEFAULT 'ban.reason',
                PRIMARY KEY("member_id")
            );
            """)
