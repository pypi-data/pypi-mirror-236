import base64
import sqlite3
from typing import Union


class Database:
    """
    This class is used to store the API keys and other sensitive information.
    """
    __instance = None
    @staticmethod
    def get_instance():
        if Database.__instance is None:
            Database()
        return Database.__instance
    def __init__(self):
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self
            #default values loaded
            self.index = {
                0:'openai_api_key',
                1:'powerwritingaid_api_key',
                2:'username',
                3:'password',
                4:'stealthgpt_api_key',
                5:'gptzero_api_key',
                6:'originality',
                7:'gpt_hero_api_key',
            }
            self.db = sqlite3.connect('database.db',check_same_thread=False)
            self.cursor = self.db.cursor()
            self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings(
                id INTEGER PRIMARY KEY,
                key INTEGER,
                value TEXT
            )
        ''')
        self.db.commit()
        self.cursor.execute('''
            SELECT * FROM user_settings WHERE key = 1
        ''')
        if len(self.cursor.fetchall()) == 0:
            self.cursor.execute('''
                INSERT INTO user_settings(
                    key,
                    value
                ) VALUES(?,?)
            ''', (
                1,
                'CC17F59E-1F6F-43EF-ACF4-A2B4B8E52401'
            ))
            self.db.commit()
        
    def get_settings(self, key: int) -> Union[str, bool]:
        """
            returns auth credintials matching the key value provided or False if no key is found
        """
        #check if user entered the special password for any key
        self.cursor.execute(''' SELECT value FROM user_settings WHERE key = ?''', (key,))
        dbKeys = self.cursor.fetchone()
        if dbKeys != None:
            if dbKeys[0] != '':
                return dbKeys[0]
        
        return False
    def set_settings(self, key: int, value: str) -> bool:
        """
            input: key to be used to get value from self.keys
            output: decrypted text
        """
        #check if user entered the special password for any key
        self.cursor.execute(''' SELECT * FROM user_settings''')
        dbKeys = self.cursor.fetchall()
        if len(dbKeys) > 0:
            for i in dbKeys:
                if i[1] == key:
                    self.cursor.execute('''
                        UPDATE user_settings SET value = ? WHERE key = ?
                    ''', (value, key))
                    self.db.commit()
                    return True
        self.cursor.execute('''
            INSERT INTO user_settings(
                key,
                value
            ) VALUES(?,?)
        ''', (
            key,
            value
        ))
        self.db.commit()
        return True
    def key_lable(self, key: int) -> str:
        name = self.index[key]
        #name to lowercase
        name = name.lower()
        #replace _ with space
        name = name.replace('_', ' ')
        #capitalize first letter
        name = name.capitalize()
        return name
