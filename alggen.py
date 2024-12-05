import numpy as np
import random
import matplotlib.pyplot as plt
from statistics import mean
from PIL import Image
import os

#Individuos tem genes x e y e fitness
class Individuo:
    def __init__(self, x: str, y: str, fitness: float = 0):
        self.x = x
        self.y = y
        self.fitness = fitness

#Funcao para converter de ponto flutuante para binario
def float_to_bin(num, int_bits=5, frac_bits=10):
    #Separar inteiro de fracionario
    integer_part = int(num)
    fractional_part = abs(num - integer_part)

    #Checar caso de exceder limites
    if not (-2**(int_bits - 1) <= integer_part < 2**(int_bits - 1)):
        raise ValueError(f"Parte inteira fora do intervalo permitido para {int_bits} bits.")

    #Conversao para binario
    integer_bin = bin(integer_part & ((1 << int_bits) - 1))[2:].zfill(int_bits)
    fractional_bin = []
    for _ in range(frac_bits):
        fractional_part *= 2
        fractional_bin.append(str(int(fractional_part)))
        fractional_part -= int(fractional_part)

    return integer_bin + '.' + ''.join(fractional_bin)

#Conversao de binario para ponto flutuante
def bin_to_float(binstr):
    #String de 15 caracteres - 1 para sinal, 4 para parte inteira e 10 para fracionarios
    inteiro = int(binstr[1:5], 2)
    frac = int(binstr[6:16], 2)/1000
    x = inteiro + frac
    #Checa o bit de sinal
    if (binstr[0] == '1'):
        x *= -1
    return x

def generate_random_gene(bits=15, precision=3):
    value = random.uniform(-10, 10)  # Gera um número aleatório no intervalo [-10, 10]
    return float_to_bin(value)

#Calcula o fitness baseado na função de maximização pedida
def fitness(gene_x, gene_y):
    x = bin_to_float(gene_x)
    y = bin_to_float(gene_y)
    return (5 + 3 * x - 4 * y - x**2 + x * y - y**2) + 365

#Checa se gene está dentro dos limites estabelecidos de [-10, 10]
def check_boundaries(gene):

  if int(gene[1:5], 2) >= 10: #Se a parte inteira for maior que 10
    return gene[0] + "1010.0000000000" #truncar em 10.0
  else:
    integ = gene[1:5]

  if int(gene[6:16], 2) > 999: #Se a parte fracionario exceder a representação decimal
    frac = "1111100111" #999 em binario
  else:
    frac = gene[6:16]

  return gene[0] + integ + "." + frac


#Funcao para criação de população inicial, gerando genes aleatoriamente
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


def executar_algoritmo_genetico(pop_size, max_gen, prob_cruzamento, prob_mutacao, elitism=0.01):
    # Calcula o numero do elitismo para ser passado para as funcoes, mantendo o mesmo comportamento
    num_elitismo = (round(pop_size * elitism))
    population = create_population(pop_size)  # Cria populacao inicial
    
    # Instancia de listas usadas nos graficos
    gen_x = []
    gen_y = []
    media_fitness = []
    melhor_ind = population[0]  # Inicializa marcador de melhor individuo
    melhor_fitness = []  # Marca o fitness do melhor individuo para grafico de cada geracao
    
    for i in range(0, len(population)):  # Calcula melhor fitness da população inicial e cria listas com os genes x e y de todos os individuos
        gen_x.append(bin_to_float(population[i].x))
        gen_y.append(bin_to_float(population[i].y))
        if population[i].fitness > melhor_ind.fitness:
            melhor_ind = population[i]
    
    # Salva o gráfico da população inicial
    plt.scatter(gen_x, gen_y, label="Indivíduos", color="blue")  # Cria grafico de dispersao com os genes x e y de todos os individuos
    plt.scatter(bin_to_float(melhor_ind.x), bin_to_float(melhor_ind.y), label="Melhor Indivíduo", color="red")  # Coloca o melhor individuo em vermelho
    plt.title(f"População inicial")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend(loc="best")
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])
    plt.savefig("temp_inicial.png")  # Salva o gráfico como um arquivo PNG
    plt.close()  # Fecha o gráfico para não sobrescrever
    
    melhor_fitness.append(melhor_ind.fitness)  # Lista para mostrar evolução de melhor fitness gerado
    aux = elitismo(population, pop_size, num_elitismo)  # Recebe os individuos do elitismo em lista auxiliar
    
    # Lista para armazenar os nomes dos arquivos das imagens temporárias
    imagem_paths = ["temp_inicial.png"]
    
    for gen in range(max_gen):  # Gera cada geração pedida
        population = selecao_ranking(population, pop_size, num_elitismo)  # Gera lista de pais selecionados para cruzamento
        population = cruzamento_uniforme(population, prob_cruzamento, prob_mutacao)  # A partir dessa lista, faz os cruzamentos
        gen_x = []
        gen_y = []
        for ind in aux:  # Acrescenta os individuos do elitismo a população
            population.append(ind)
        for i in range(0, len(population)):  # Calcula melhor fitness da população inicial e cria listas com os genes x e y de todos os individuos
            gen_x.append(bin_to_float(population[i].x))
            gen_y.append(bin_to_float(population[i].y))
            if population[i].fitness > melhor_ind.fitness:
                melhor_ind = population[i]
        
        melhor_fitness.append(melhor_ind.fitness)
        media_fitness.append(mean(ind.fitness for ind in population))  # Calcula a media de fitness por geração
        aux = elitismo(population, pop_size, num_elitismo)
        
        # Salva o gráfico para cada geração como uma imagem temporária
        plt.scatter(gen_x, gen_y, label="Indivíduos", color="blue")
        plt.scatter(bin_to_float(melhor_ind.x), bin_to_float(melhor_ind.y), label="Melhor Indivíduo", color="red")
        plt.title(f"Geração {gen + 1}")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend(loc="best")
        plt.xlim([-10, 10])
        plt.ylim([-10, 10])
        imagem_path = f"temp_{gen + 1}.png"
        plt.savefig(imagem_path)  # Salva o gráfico como um arquivo PNG
        plt.close()  # Fecha o gráfico para não sobrescrever
        imagem_paths.append(imagem_path)  # Adiciona o nome da imagem à lista
    
    # Cria o GIF a partir das imagens salvas
    images = [Image.open(imagem_path) for imagem_path in imagem_paths]  # Abre as imagens temporárias
    images[0].save('evolucao.gif', save_all=True, append_images=images[1:], optimize=False, duration=500, loop=0)  # Cria o GIF
    
    # Exclui as imagens temporárias
    for imagem_path in imagem_paths:
        os.remove(imagem_path)

    return population, media_fitness, melhor_fitness

# Executar o algoritmo
pop_size = int(input("Tamanho da população: "))
max_gen = int(input("Quantidade de gerações: "))
prob_cruzamento = float(input("Taxa de cruzamento: "))
prob_mutacao = float(input("Taxa de mutação: "))
pop_final, fitness_evolucao, melhor_fitness = executar_algoritmo_genetico(pop_size, max_gen, prob_cruzamento, prob_mutacao)

plt.plot(fitness_evolucao, label = "Média por geração")
plt.plot(melhor_fitness, label = "Melhor individuo", color = "red")
plt.title("Evolução da Média do Fitness")
plt.xlabel("Gerações")
plt.ylabel("Fitness")
plt.legend(loc="best")
plt.savefig("evolucao_fitness.png") #Salva a evolucao das medias em uma imagem
plt.close()
