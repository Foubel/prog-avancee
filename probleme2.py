import heapq
import copy

TROU = '0'

# Déplacements possibles
MOVES = {
    'Haut': (-1, 0),
    'Bas': (1, 0),
    'Gauche': (0, -1),
    'Droite': (0, 1)
}

# Affichage du taquin
def afficheJeu(jeu):
    for row in jeu:
        print(" ".join(row))
    print()

def initTaquin(nf):
    with open(nf, "r") as f:
        lignes = f.readlines()
    dim = len(lignes) // 2
    jeu = [lignes[i].split() for i in range(dim)]
    ref = [lignes[i].split() for i in range(dim, 2 * dim)]
    return jeu, ref, dim

# Recherche de la position d'une valeur
def chercher(val, jeu):
    for i, row in enumerate(jeu):
        if val in row:
            return i, row.index(val)

# Heuristique de Manhattan
def heuristique(jeu, ref):
    distance = 0
    for i in range(len(jeu)):
        for j in range(len(jeu[i])):
            if jeu[i][j] != TROU:
                y, x = chercher(jeu[i][j], ref)
                distance += abs(y - i) + abs(x - j)
    return distance

# Vérification de la résolubilité
def est_resoluble(jeu, dim):
    ligne_trou, _ = chercher(TROU, jeu)
    inv_count = 0
    flat_list = [num for row in jeu for num in row if num != TROU]
    for i in range(len(flat_list)):
        for j in range(i + 1, len(flat_list)):
            if flat_list[i] > flat_list[j]:
                inv_count += 1
    if dim % 2 == 1:
        return inv_count % 2 == 0
    else:
        return (inv_count + ligne_trou) % 2 == 1

# Génération des états voisins
def get_neighbors(jeu, dim):
    y, x = chercher(TROU, jeu)
    voisins = []
    for move, (dy, dx) in MOVES.items():
        ny, nx = y + dy, x + dx
        if 0 <= ny < dim and 0 <= nx < dim:
            new_jeu = copy.deepcopy(jeu)
            new_jeu[y][x], new_jeu[ny][nx] = new_jeu[ny][nx], new_jeu[y][x]
            voisins.append((new_jeu, move))
    return voisins

# Algorithme A* (A-star)
def a_star(jeu, ref, dim):
    open_set = []
    heapq.heappush(open_set, (heuristique(jeu, ref), 0, jeu, []))
    visited = set()
    
    while open_set:
        _, g, current, path = heapq.heappop(open_set)
        state_tuple = tuple(tuple(row) for row in current)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)
        
        if current == ref:
            return path
        
        for neighbor, move in get_neighbors(current, dim):
            if tuple(tuple(row) for row in neighbor) not in visited:
                heapq.heappush(open_set, (g + 1 + heuristique(neighbor, ref), g + 1, neighbor, path + [move]))
    return None

# Chargement du taquin
jeu, ref, dim = initTaquin("taquin4.txt")
print("État initial:")
afficheJeu(jeu)
print("État final:")
afficheJeu(ref)

if not est_resoluble(jeu, dim):
    print("Ce taquin n'est pas résoluble.")
else:
    solution = a_star(jeu, ref, dim)
    if solution:
        print("Solution trouvée en", len(solution), "coups:")
        print(" -> ".join(solution))
    else:
        print("Aucune solution trouvée.")
