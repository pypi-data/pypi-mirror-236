import redis


class History:
    unique_key: str = ""

    def __init__(self, unique_key: str = "", redis_url="redis://localhost:6379/0"):
        self.redis_url = redis_url
        self.unique_key = unique_key
        self.redis = redis.from_url(self.redis_url)

    def push(self, data):
        self.redis.lpush(self.unique_key, data)
        self.redis.ltrim(self.unique_key, 0, 9)

    def get_all(self):
        all_elements = self.redis.lrange(self.unique_key, 0, -1)
        if all_elements:
            all_elements = [element.decode() for element in all_elements]
            return all_elements
        else:
            return []

    def get(self, index=0):
        element = self.redis.lindex(self.unique_key, index)
        if element:
            return element.decode()
        else:
            return None

    def compare(self, index1=0, index2=1):
        return self.get(index1) == self.get(index2)

    def length(self):
        return len(self.get_all())

    def clear(self):
        self.redis.delete(self.unique_key)
