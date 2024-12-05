def generate_random_gene(bits=15, precision=3):
    value = random.uniform(-10, 10)  # Gera um número aleatório no intervalo [-10, 10]
    return float_to_bin(value)
