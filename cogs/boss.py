# boss.py
import random

class Boss:
    def __init__(self, nome, saude, dano):
        self.nome = nome
        self.saude = saude
        self.dano = dano

    def atacar(self):
        return self.dano

# Lista de bosses com mensagens temáticas
bosses = [
    Boss("Zumbi Mutante", 300, 50),
    Boss("Chefe Zumbi", 500, 80),
    Boss("Líder do Culto", 1000, 100),
    Boss("Criatura das Sombras", 700, 70),
    Boss("Andarilho Enlouquecido", 400, 60)
]

def mensagem_boss(boss):
    return f"Você se deparou com **{boss.nome}**! Prepare-se para a batalha! Saúde: {boss.saude}"
