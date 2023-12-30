import redis
from bot.config import Config
from uuid import uuid4
from redis.exceptions import RedisError

class Redis:

    def __init__(self, ttl=60) -> None:
        self.client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASS,
        )
        self.ttl = ttl

    def conn(self):
        try:
            self.client.ping()
        except RedisError as e:
            print(f"Error connecting to Redis: {e}")

    def gen_token(self, user_id: int) -> str:
        try:
            token = f"{str(uuid4())[0:6]}"
            self.client.set(user_id, token, ex=self.ttl)
            print(token)
            return token
        except RedisError as e:
            print(f"Error generating token: {e}")
            return ""

    def check_access(self, user_id: int) -> bool:
        try:
            return self.client.get(user_id) is not None
        except RedisError as e:
            print(f"Error checking access: {e}")
            return False

    def got_key(self, user_id):
        try:
            return self.client.get(f"acc^{user_id}").decode('utf-8') == '1'
        except RedisError as e:
            print(f"Error checking key: {e}")
            return False

    def accessed(self, user_id: int, key: str) -> bool:
        try:
            if self.client.get(user_id).decode('utf-8') == key:
                self.client.set(f"acc^{user_id}", 1, self.ttl)
                return True
            return False
        except RedisError as e:
            print(f"Error accessing: {e}")
            return False

# Example usage
myDb = Redis(Config.TIMEOUT)
myDb.conn() # Call this method to check connection change in this code 

# This line should be executed in the client side, for example when a user enters their key.
myDb.accessed(12345, '123456')
