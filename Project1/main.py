import sys
import heapq

# Função para facilitar a leitura dos parâmetros
def ler_entrada():
    # Pega o número de vértices e arestas
    N, M = map(int, sys.stdin.readline().split()) 
    
    # Gera um grafo com os dados anteriores
    grafo = [[] for _ in range(N + 1)]
    
    # Adiciona as arestas ao grafo, 
    # como são bidirecionais adicionamos tanto em u como em v
    for i in range(1, M + 1):
        u, v, w = map(int, sys.stdin.readline().split())
        grafo[u].append((v, w, i))
        grafo[v].append((u, w, i))
    return N, M, grafo

# Busca em profundidade, baseado no algoritmo de tarjan para detectar pontes
def dfs(u, pai, subgrafo, visitado, disc, low, tempo, ruas_criticas):
    # disc[u] : tempo que o nó foi descoberto na DFS
    # low[u] : menor tempo alcançavel a partir de u 
    visitado[u] = True
    disc[u] = low[u] = tempo[0]
    tempo[0] += 1

    for v, idx, in subgrafo[u]:
        if not visitado[v]:
            dfs(v, u, subgrafo, visitado, disc, low, tempo, ruas_criticas)
            low[u] = min(low[u], low[v])
            if low[v] > disc[u]:
                ruas_criticas.append(idx) # Toda idx (aresta) que for para pontes é uma rua critica
        elif v != pai:
            low[u] = min(low[u], disc[v])


# Algoritmo Dijkstra para encontrar menor caminho 
def dijkstra(N, grafo, origem):
    INF = float('inf') 
    dist = [INF] * (N + 1)
    dist[origem] = 0
    pq = [(0, origem)] # Cria min heap, cada item é formado por (distancia, nó)
    
    # Enquanto existir nós que ainda não foram englobados
    while pq:
        d, u = heapq.heappop(pq) # Pegamos o nó com a menor dist acumulada até agora
        if d > dist[u]:
            continue
        for v, w, idx in grafo[u]:
            # Verifica se passar por u até v é melhor do que o caminho conhecido
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist

def parte1(N, grafo):
    dist1 = dijkstra(N, grafo, 1)
    menor_dist = dist1[N]
    print("Parte 1:", int(menor_dist))
    return menor_dist, dist1

# Para a parte 2 apliquei dijkstra da origem para o destino e o inverso
# As arestas que estiverem presentes nas 2 soluções são importantes
def parte2(N, grafo, dist1, menor_dist):

    dist_init = dijkstra(N, grafo, 1)
    dist_fin = dijkstra(N, grafo, N)

    arestas_importantes = []
    
    for u in range(1, N + 1):
        for v, w, idx in grafo[u]:
            if dist_init[u] + w + dist_fin[v] == menor_dist or dist_init[v] + w + dist_fin[u] == menor_dist:
                arestas_importantes.append(idx)

    arestas_importantes = sorted(set(arestas_importantes))
    print("Parte 2:", *arestas_importantes)
    return arestas_importantes

# Para a parte 3 apliquei uma dfs no subgrafo que tem todas as arestas do caminho mínimo
# Uma rua é crítica caso não exista outro caminho entre u e v que não passe por ela
def parte3(N, grafo, ruas_min):
    
    subgrafo = [[] for _ in range(N + 1)]
    for u in range(1, N + 1):
        for v, w, idx in grafo[u]:
            if idx in ruas_min:
                subgrafo[u].append((v, idx))

    visitado = [False] * (N + 1)
    disc = [0] * (N + 1)
    low = [0] * (N + 1)
    tempo = [0]
    ruas_criticas = []

    # Executamos dfs a partir do primeiro nó
    dfs(1, -1, subgrafo, visitado, disc, low, tempo, ruas_criticas)

    if ruas_criticas: 
        print("Parte 3:", *sorted(ruas_criticas))
    else:
        print("Parte 3: -1")
    

def main():
    N, M, grafo = ler_entrada()
    menor_dist, dist1 = parte1(N, grafo)
    ruas_min = parte2(N, grafo, dist1, menor_dist)
    parte3(N, grafo, ruas_min)
    
if __name__ == "__main__":
    main()