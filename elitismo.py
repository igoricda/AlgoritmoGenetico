def elitismo(population, n_individuos, num_elitismo):
    elit = []
    #Escolhe os n melhores individuos para serem passados para a próxima geração
    for _ in range(num_elitismo):
        melhor_indice = 0
        melhor_fitness = population[0].fitness
        for i in range(1, len(population)):
            if population[i].fitness > melhor_fitness:
                melhor_indice = i
                melhor_fitness = population[i].fitness
        elit.append((population.pop(melhor_indice))) #Tira os individuos da lista para que não sejam selecionados novamente
    for ind in elit:
          population.append(ind) #Retorna os individuos a lista
    return elit
