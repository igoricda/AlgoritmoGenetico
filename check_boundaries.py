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
