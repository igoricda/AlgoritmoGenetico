def mutacao(gene):
        # Escolhe um índice aleatório no gene
        gene_list = list(gene)  # Converte a string binária em lista para alteração
        index = random.randint(0, len(gene_list) - 1)
        # Inverte o bit no índice escolhido
        if gene_list[index] == '0':
            gene_list[index] = '1'
        elif gene_list[index] == '1':
            gene_list[index] = '0'

        return ''.join(gene_list)  # Retorna o gene mutado como string binária
