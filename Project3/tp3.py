import sys

def ler_entrada():
    # sys.stdin para maior eficiência
    input_data = sys.stdin.read().split()
    
    if not input_data: 
        return 0, []
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return 0, []

    # Utilizando uma lista de inteiros (bits) pois com a matriz estava muito demorado
    # Se o bit j de brigas[i] for 1 então i e j brigam
    brigas = [0] * N
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        
        # Marca o bit de conflito entre os dois duendes nas duas posições referentes a eles
        brigas[u] |= (1 << v)
        brigas[v] |= (1 << u)
        
    return N, brigas

def analisa_particao(tamanho, offset_indice, brigas):
    combinacoes_validas = []
    total_combinacoes = 1 << tamanho

    for subset in range(total_combinacoes):
        eh_independente = True
        
        # Percorre os bits do subset para ver se brigam entre si
        temp_mask = subset
        index = 0
        while temp_mask > 0:
            # Se o bit final for 1 então o duende i está na solução
            if temp_mask & 1:
                # O índice real do duende atual é indice + offset
                duende_atual = index + offset_indice
                # brigas[duende_atual] armazena com quem o duende atual briga
                # subset << offset são os duendes que já estão na solução 
                # confere se tem algum conflito entre o duende atual e os os duendes da solução
                mask_global_atual = subset << offset_indice
                
                if (brigas[duende_atual] & mask_global_atual):
                    eh_independente = False
                    break # Se achou uma briga então esse subset não é válido

            # Avança para o próximo duende 
            temp_mask >>= 1
            index += 1

        # Caso todos os vértices sejam independetes salva a solução
        if eh_independente:
            mask_global = subset << offset_indice
            quantidade_duendes = bin(subset).count('1')
            combinacoes_validas.append((mask_global, quantidade_duendes))

    return combinacoes_validas

def combinacao_sem_brigas(grupoA_mask, grupoB_mask, brigas, N):
    # Verifica se alguém do grupo A briga com alguém do grupo B
    
    # Itera pelos duendes do Grupo A
    for i in range(N):
        if (grupoA_mask >> i) & 1: # Verifica se o duende i está no grupo A
            # Verifica se o duende i briga com alguém do grupo B
            if brigas[i] & grupoB_mask:
                return False
    return True

def verifica_particao(combinacoes_possiveis_1, combinacoes_possiveis_2, brigas, N):
    melhor_tam = -1
    melhor_mask = 0

    # Ordenar o segundo conjunto por tamanho (decrescente) ajuda a minimizar o loop
    combinacoes_possiveis_2.sort(key=lambda x: x[1], reverse=True)
    
    combinacoes_possiveis_1.sort(key=lambda x: x[1], reverse=True)

    for grupoA, tamA in combinacoes_possiveis_1:
        for grupoB, tamB in combinacoes_possiveis_2:
            
            # Se essa soma não ganha do melhor atual já vai pro próximo
            if tamA + tamB < melhor_tam:
                break # E como combinações_2 estão ordenadas, os próximos serão menores ainda
            
            # Se for empate, verificamos lexicograficamente
            if tamA + tamB == melhor_tam:
               nova_mask_potencial = grupoA | grupoB
               # Compara com melhor_mask atual
               diff = nova_mask_potencial ^ melhor_mask
               if diff != 0:
                   lsb = diff & -diff
                   # Se a melhor_mask já tem o bit menor ela é melhor que a nova mask
                   if melhor_mask & lsb:
                       continue

            if combinacao_sem_brigas(grupoA, grupoB, brigas, N):
                melhor_tam = tamA + tamB
                melhor_mask = grupoA | grupoB

    return melhor_tam, melhor_mask

def main():
    N, brigas = ler_entrada()
    if N == 0: 
        return

    # Divide os N duendes em 2 porções para reduzir a complexidade
    metade1 = N // 2
    metade2 = N - metade1

    # Encontra as combinações válidas em cada partição
    possiveis_solucoes_1 = analisa_particao(metade1, 0, brigas)
    possiveis_solucoes_2 = analisa_particao(metade2, metade1, brigas)

    # Verifica a combinação
    tamanho_final, resultado_mask = verifica_particao(possiveis_solucoes_1, possiveis_solucoes_2, brigas, N)

    print(tamanho_final)
    
    # Converte a máscara final para índices
    indices = []
    for i in range(N):
        if (resultado_mask >> i) & 1:
            indices.append(str(i))
    print(" ".join(indices))

if __name__ == "__main__":
    main()