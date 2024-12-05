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
