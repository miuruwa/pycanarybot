class Database:
    def __init__(self, file, drop):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()
        if drop:
            self.drop()
    def user_exist(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def user_add(self, user_id):
        if not self.user_exist(user_id):
            with self.connection:
                return self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id))

    def chat_exist(self, peer_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM chats WHERE peer_id = ?", (peer_id,)).fetchall()
            return bool(len(result))
    
    def chat_add(self, peer_id):
        if not self.user_exist(user_id):
            with self.connection:
                return self.cursor.execute("INSERT INTO chats (peer_id) VALUES (?)", (peer_id))
    def userInfoGet():
        pass
    class ban:
        def get(peer_id, user_id):
            with self.connection:
                self.cursor.execute()
            return True
        def delete(peer_id, user_id):
            pass
        def add(peer_id, user_id, reason):
            pass
    class admin:
        def get(user_id):
            return True
    class vip:
        def get(user_id):
            return True
        def delete(user_id):
            pass
        def add(user_id):
            pass

    def drop(self):
        with self.connection:
            self.cursor.execute("DROP TABLE chats IF EXISTS")
            self.cursor.execute("DROP TABLE users IF EXISTS")
            self.cursor.execute("""CREATE TABLE chats (
                id	INTEGER DEFAULT 1,
                "peer_id	INTEGER DEFAULT 1,
                character	TEXT,
                PRIMARY KEY(id,peer_id)
            );""")
            self.cursor.execute("""CREATE TABLE "users" (
                "id"	INTEGER DEFAULT 1,
                "user_id"	INTEGER DEFAULT 1,
                "name"	TEXT DEFAULT 'user_nickname',
                "character"	TEXT,
                "money"	INTEGER DEFAULT 0,
                PRIMARY KEY("user_id","id")
            );""")

        """
        character
        chat 
        {
            'blacklist'
        }
        user
        {
            'vip': 0,
            'admin': 0,
        }
        """


    def close(self):
        self.connection.close()