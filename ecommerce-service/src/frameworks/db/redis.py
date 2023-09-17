import os

import redis

# Función para crear una conexión con Redis
# según las variables de entorno definidas.

def create_redis_client():

    host = os.environ["REDIS_HOST"]
    port = os.environ["REDIS_PORT"]

    return redis.StrictRedis(host = host, port = port)