
# Casos de uso para realizar el saludo utilizando un contador en el caché.
# Recibe en el constructor el caché a utilizar.

class GreetingUsecase:

    def __init__(self, greeting_cache):
        self.greeting_cache = greeting_cache

    def make_greeting(self):

        # Retorna un saludo indicando el contador obtenido desde el caché.

        value = self.greeting_cache.get_greeting_counter()
        return "Hello, you're the visitor N°%s." % value