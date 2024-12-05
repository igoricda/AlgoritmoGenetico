#Calcula o fitness baseado na função de maximização pedida
def fitness(gene_x, gene_y):
    x = bin_to_float(gene_x)
    y = bin_to_float(gene_y)
    return (5 + 3 * x - 4 * y - x**2 + x * y - y**2) + 365
