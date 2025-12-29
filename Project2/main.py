import sys
import math

def ler_entrada():
    # Leio a entrada toda de uma vez
    data = list(map(int, sys.stdin.read().split()))

    # As informações sobre a parte 1 estão da posição 0 até 1+N
    N = data[0]
    muros = data[1:1 + N]

    # As informações da parte 2 estão no resto do vetor
    Z = data[1 + N]
    coordenadas = []

    i = N + 2
    for idx in range(Z):
        x = data[i]
        y = data[i + 1]
        coordenadas.append((x, y, idx + 1))  # guarda índice original
        i += 2

    return muros, coordenadas

def parte_1(muros):
    # Para a parte 1 vou passar pelo vetor e conferir a altura máxima de cada posição olhando para os n/2 vizinhos

    total_muros = len(muros)

    if total_muros == 0:
        return 0

    # Os vetores esquerda e direita irão armazenar a altura máxima possível indo pela esquerda ou pela direita
    esquerda = [0] * total_muros
    direita = [0] * total_muros

    # Os vetores são preenchidos e analisados
    esquerda[0] = 1
    for i in range(1, total_muros):
        esquerda[i] = min(muros[i], esquerda[i - 1] + 1)

    direita[-1] = 1
    for i in range(total_muros - 2, -1, -1):
        direita[i] = min(muros[i], direita[i + 1] + 1)

    # Para cada posição, a altura máxima é o menor daquela posição entre os 2 vetores
    alturas_maximas = [min(esquerda[i], direita[i]) for i in range(total_muros)]
    return max(alturas_maximas)

# Função para calcular distância entre pontos no plano cartesiano 
def distancia(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx*dx + dy*dy)

# Perimetro do triangulo é a distancia entre cada um dos pontos 
def perimetro(p1, p2, p3):
    return distancia(p1, p2) + distancia(p2, p3) + distancia(p1, p3)

def menor_triangulo(pontos):
    n = len(pontos)

    # Enquanto não tivermos os 3 pontos continuamos a chamar a função recursivamente
    if n < 3:
        return float('inf'), None
    if n == 3:
        return perimetro(pontos[0], pontos[1], pontos[2]), (pontos[0], pontos[1], pontos[2])

    meio = n // 2
    ponto_medio = pontos[meio][0]

    # Divido os pontos em 2 porções iguais e faço o cálculo do menor triangulo para as duas
    esquerda = pontos[:meio]
    direita = pontos[meio:]

    per_esq, tri_esq = menor_triangulo(esquerda)
    per_dir, tri_dir = menor_triangulo(direita)

    delta = min(per_esq, per_dir)
    melhor_triangulo = tri_esq if per_esq <= per_dir else tri_dir

    # A partir o delta (menor perimetro encontrado) utilizamos uma faixa para delimitar os possíveis candidatos
    faixa = [p for p in pontos if abs(p[0] - ponto_medio) < delta]
    faixa.sort(key=lambda p: p[1])

    L = len(faixa)
    for i in range(L):
        for j in range(i + 1, min(i + 7, L)):
            for k in range(j + 1, min(i + 7, L)):
                p1, p2, p3 = faixa[i], faixa[j], faixa[k]
                per = perimetro(p1, p2, p3)
                if per < delta:
                    delta = per
                    melhor_triangulo = (p1, p2, p3)

    return delta, melhor_triangulo

def parte_2(coordenadas):
    # ordenar por x mas manter índices originais
    pontos = sorted(coordenadas, key=lambda p: p[0])
    menor_perimetro, tri = menor_triangulo(pontos)

    indices = sorted([tri[0][2], tri[1][2], tri[2][2]])
    return menor_perimetro, indices

def main():
    muros, coordenadas = ler_entrada()
    max_altura = parte_1(muros)
    print(f"Parte 1: {max_altura}")

    menor_perimetro, indices = parte_2(coordenadas)
    print(f"Parte 2: {menor_perimetro:.4f} {indices[0]} {indices[1]} {indices[2]}")

if __name__ == "__main__":
    main()