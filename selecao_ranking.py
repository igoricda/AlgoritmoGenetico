def selecao_ranking(population, n_individuos, n_elitism):
    ranked_pop = sorted(population, key=lambda ind: ind.fitness) #Ordena a população em lista baseado no fitness
    rankings = np.arange(1, len(population) + 1) #Cria a representação dos rankings de cada individuo
    probabilidade_selecao = rankings / np.sum(rankings) #Calcula a probabilidade de seleção de cada indivíduo
    probabilidade_acumulada = np.cumsum(probabilidade_selecao) #Calcula a soma acumulada das probabilidades
    n_individuos *= 2 #multiplica o tamanho da população por 2
    selecionados = []
    #Gera a quantidade de pais necessários para chegar ao tamanho da população
    for _ in range(n_individuos - 2*n_elitism): #
        r = np.random.rand()
        idx = np.searchsorted(probabilidade_acumulada, r)
        if _ > 0 and selecionados[-1] == ranked_pop[idx]: #Se for sorteado o mesmo pai 2 vezes seguidas, sortear novamente até ser diferente
            while selecionados[-1] == ranked_pop[idx]:
              r = np.random.rand()
              idx = np.searchsorted(probabilidade_acumulada, r)
        selecionados.append(ranked_pop[idx]) #Coloca os selecionados aleatoriamente na lista
    return selecionados
