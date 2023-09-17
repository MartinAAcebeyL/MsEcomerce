# Implementación con Redis del caché utilizado por la sección de saludos.

class RedisGreetingCache():

    def __init__(self, redis_client):

        self.COUNTER_KEY = "greeting_counter"
        self.redis_client = redis_client

    def get_greeting_counter(self):

        return self.redis_client.incr(self.COUNTER_KEY, 1)
