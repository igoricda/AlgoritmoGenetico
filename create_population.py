#Funcao para criação de populaçplt.savefig("evolucao_fitness.png")ão inicial, gerando genes aleatoriamente
def create_population(pop_size, bits_x=15, bits_y=15):
    population = []
    for _ in range(pop_size):
        gene_x = generate_random_gene(bits_x)
        gene_y = generate_random_gene(bits_y)
        gene_x = check_boundaries(gene_x) #Checa se o gene gerado está nos limites e trata se não estiver
        gene_y = check_boundaries(gene_y)
        fit_value = fitness(gene_x, gene_y) #Calcula o fitness a ser atribuido ao individuo
        population.append(Individuo(gene_x, gene_y, fit_value)) #Coloca o individuo na lista de população
    return population #Retorna a lista
