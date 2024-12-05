#Individuos tem genes x e y e fitness
class Individuo:
    def __init__(self, x: str, y: str, fitness: float = 0):
        self.x = x
        self.y = y
        self.fitness = fitness
