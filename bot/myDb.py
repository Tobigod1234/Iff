import redis
from bot.config import Config
from uuid import uuid4
from threading import Lock

class Redis:
    def __init__(self, ttl=60) -> None:
        self.redis_pool = redis.ConnectionPool(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            password=Config.REDIS_PASS,
        )
        self.ttl = ttl
        self.lock = Lock()

    def conn(self):
        redis_client = redis.StrictRedis(connection_pool=self.redis_pool)
        redis_client.ping()

    def gen_token(self, user_id: int) -> str:
        token = f"{str(uuid4())[0:6]}"
        with self.lock:
            redis_client = redis.StrictRedis(connection_pool=self.redis_pool)
            redis_client.set(user_id, token, ex=self.ttl)
        return token

    def check_access(self, user_id: int) -> bool:
        with self.lock:
            redis_client = redis.StrictRedis(connection_pool=self.redis_pool)
            return redis_client.get(user_id) is not None

    def got_key(self, user_id):
        try:
            with self.lock:
                redis_client = redis.StrictRedis(connection_pool=self.redis_pool)
                return redis_client.get(f"acc^{user_id}").decode('utf-8') == '1'
        except:
            return False

    def accessed(self, user_id: int, key: str) -> bool:
        try:
            with self.lock:
                redis_client = redis.StrictRedis(connection_pool=self.redis_pool)
                if redis_client.get(user_id).decode('utf-8') == key:
                    redis_client.set(f"acc^{user_id}", 1, self.ttl)
                    return True
                return False
        except:
            return False

myDb = Redis(Config.TIMEOUT)
myDb.conn()  
