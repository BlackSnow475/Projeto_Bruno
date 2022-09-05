import string
import random

class GeradorID:
    @staticmethod
    def gerar_id():
        id = ''.join(random.choices(string.digits, k=8))
        return id
