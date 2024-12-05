def cruzamento_uniforme(parents, prob_cruzamento, prob_mutacao ):
    nova_populacao = [] #Instância lista de nova populacao
    for i in range(0, len(parents), 2): #Separa os genes de pai a e pai b
        pai_a = parents[i]
        pai_b = parents[(i + 1) % len(parents)]

        if random.random() < prob_cruzamento: #Faz o cruzamento baseado na probabilidade de cruzar
            mask = np.random.randint(2, size=len(pai_a.x) + len(pai_a.y)) #Gera máscara aleatoriamente para cruzamento e gera os genes X e Y dos filhos
            filho_x = ''.join(pai_a.x[j] if mask[j] else pai_b.x[j] for j in range(len(pai_a.x)))
            filho_y = ''.join(pai_a.y[j] if mask[j] else pai_b.y[j] for j in range(len(pai_a.y)))
            #Calcula mutações nos genes
            if random.random() < prob_mutacao:
                filho_x = mutacao(filho_x)
            if random.random() < prob_mutacao:
                filho_y = mutacao(filho_y)
        else:
            filho_x, filho_y = pai_a.x, pai_a.y

        #checar limites
        filho_x = check_boundaries(filho_x)
        filho_y = check_boundaries(filho_y)
        fit_value = fitness(filho_x, filho_y)
        nova_populacao.append(Individuo(filho_x, filho_y, fit_value))
    return nova_populacao
