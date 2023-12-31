from pymongo import MongoClient
from bot.config import Config
from uuid import uuid4

class MongoDB:

    def __init__(self, ttl=60) -> None:
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client[Config.MONGO_DB]
        self.ttl = ttl

    def conn(self):
        self.client.server_info()

    def gen_token(self, user_id: int) -> str:
        token = f"{str(uuid4())[0:6]}"
        self.db.tokens.insert_one({"_id": user_id, "token": token})
        print(token)
        return token

    def check_access(self, user_id: int) -> bool:
        return self.db.tokens.find_one({"_id": user_id}) is not None

    def got_key(self, user_id):
        try:
            return self.db.access.find_one({"_id": f"acc^{user_id}"})['value'] == '1'
        except:
            return False

    def accessed(self, user_id: int, key: str) -> bool:
        try:
            document = self.db.tokens.find_one({"_id": user_id, "token": key})
            if document:
                self.db.access.update_one({"_id": f"acc^{user_id}"}, {"$set": {"value": '1'}}, upsert=True)
                return True
            return False
        except:
            return False


myDb = MongoDB(Config.TIMEOUT)
