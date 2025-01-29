import math

def strategie1(n, s):
    """Recherche dichotomique pour trouver la première assiette mortelle, O(log2(n))"""
    left, right = 1, n + 1
    cpt = 0
    deaths = 0
    plates_eaten = 0
    while left < right:
        mid = (left + right) // 2
        cpt += 1
        plates_eaten = mid
        if mid < s:
            left = mid + 1
        else:
            right = mid
            deaths += 1
    return left, cpt, deaths, plates_eaten

def strategie2(n, k, s):
    """Hypothèse : k < log2(n), approche en O(k + n/(2k-1))"""
    block_size = max(1, (n // (2 * k - 1)))
    current = 0
    cpt = 0
    deaths = 0
    plates_eaten = 0
    while current < n:
        next_step = min(current + block_size, n)
        cpt += 1
        plates_eaten = next_step
        if next_step < s:
            current = next_step
        else:
            for x in range(current + 1, next_step + 1):
                cpt += 1
                deaths += 1
                plates_eaten = x
                if x == s:
                    return x, cpt, deaths, plates_eaten
            return n + 1, cpt, deaths, plates_eaten
    return n + 1, cpt, deaths, plates_eaten

def strategie3(n, s):
    """Hypothèse : k = 2, approche en O(sqrt(n))"""
    r = int(math.ceil((-1 + math.sqrt(1 + 8 * n)) / 2))
    start = 0
    step = r
    cpt = 0
    deaths = 0
    plates_eaten = 0
    while start < n:
        if step > n:
            step = n
        cpt += 1
        plates_eaten = step
        if step < s:
            start = step
            step += r - 1
            r -= 1
        else:
            for x in range(start + 1, step + 1):
                cpt += 1
                deaths += 1
                plates_eaten = x
                if x == s:
                    return x, cpt, deaths, plates_eaten
            return step + 1, cpt, deaths, plates_eaten
    return n + 1, cpt, deaths, plates_eaten

if __name__ == "__main__":
    n = 100  # Nombre total d'assiettes possibles
    s = 64  # Seuil mortel
    k = 6 # Nombre d'élèves

    result_1, iterations_1, deaths_1, plates_1 = strategie1(n, s)
    result_2, iterations_2, deaths_2, plates_2 = strategie2(n, k, s)
    result_3, iterations_3, deaths_3, plates_3 = strategie3(n, s)

    print("=== Résultats ===")
    print(f"Stratégie 1 (k >= log2(n)) : Seuil trouvé = {result_1}, Itérations = {iterations_1}, Élèves morts = {deaths_1}, Assiettes mangées = {plates_1}")
    print(f"Stratégie 2 (k < log2(n)) : Seuil trouvé = {result_2}, Itérations = {iterations_2}, Élèves morts = {deaths_2}, Assiettes mangées = {plates_2}")
    print(f"Stratégie 3 (k = 2) : Seuil trouvé = {result_3}, Itérations = {iterations_3}, Élèves morts = {deaths_3}, Assiettes mangées = {plates_3}")
