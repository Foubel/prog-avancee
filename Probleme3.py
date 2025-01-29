'''
Pour démontrer que le code du professeur effectue des appels récursifs inutiles, on peut utiliser un compteur d'appels
On remarque que beaucoup d'appels sont identiques.


import random

cpt = 0

calls = {}

def trouveExpr(v, valeurs):
    global cpt, calls
    
    cpt += 1
    
    etat = (v, tuple(valeurs))
    
    if etat in calls:
        calls[etat] += 1
    else:
        calls[etat] = 1

    if len(valeurs) == 1 :
        if (v == valeurs[0]):
            return (True, str(v))
        else:
            return (False, "")
    else:
        if v in valeurs:
            return (True, str(v))
        else:
            for x in valeurs:
                valeurs2 = valeurs[:]
                valeurs2.remove(x)
                
                (t, ch) = trouveExpr(v + x, valeurs2)
                if t: return (t, ch + " - " + str(x))
                
                if (v >= x):
                    (t, ch) = trouveExpr(v - x, valeurs2)
                    if t: return (t, str(x) + " + (" + ch + ") ")
                
                if (v <= x):
                    (t, ch) = trouveExpr(x - v, valeurs2)
                    if t: return (t, str(x) + " + (" + ch + ") ")
                
                if (v >= x) and v % x == 0:
                    (t, ch) = trouveExpr(v // x, valeurs2)
                    if t: return (t, "(" + ch + ") * " + str(x))
                
                if (v <= x) and x % v == 0:
                    (t, ch) = trouveExpr(x // v, valeurs2)
                    if t: return (t, str(x) + " / (" + ch + ") ")
                
                (t, ch) = trouveExpr(v * x, valeurs2)
                if t: return (t, "(" + ch + ") / " + str(x))
            
            return (False, "")

# Cas de test
test_cases = [
    (813, [6, 5, 10, 9, 8, 3]),
    (184, [50, 10, 2, 9, 10, 25]),
    (799, [4, 8, 5, 6, 6, 2])
]

# Exécution et affichage des résultats
for cible, nombres in test_cases:
    cpt = 0  # Reset global counter
    calls = {}  # Reset memoization

    trouveExpr(cible, nombres)
    redondances = sum((nb_appels - 1) for nb_appels in calls.values())

    print(f"Exemple ({cible}, {nombres}) :")
    print(f"  Nombre total d'appels : {cpt}")
    print(f"  Nombre de redondances : {redondances}\n")


'''

# Version optimisée

import random

# Compteur pour suivre le nombre d'appels (facultatif)
cpt = 0

# Dictionnaire pour mémoriser les résultats déjà calculés (évite les recalculs inutiles)
memo = {}

def trouveExpr(cible, valeurs):
    """
    Trouve une expression qui permet d'obtenir la valeur cible en utilisant les nombres donnés.
        
    :param cible: La valeur cible à atteindre.
    :param valeurs: Liste des nombres disponibles.
    :return: Un tuple (booléen, expression). True si une solution existe, sinon False.
    """
    global cpt, memo
    cpt += 1

    # Clé unique pour mémoriser ce cas (ordre des valeurs non important, donc frozenset)
    cle_memo = (cible, frozenset(valeurs))

    # Vérification si le cas a déjà été calculé
    if cle_memo in memo:
        return memo[cle_memo]

    # Cas de base : un seul nombre dans la liste
    if len(valeurs) == 1:
        if cible == valeurs[0]:
            resultat = (True, str(cible))
        else:
            resultat = (False, "")
        memo[cle_memo] = resultat
        return resultat

    # Optimisation : si la cible est directement dans les valeurs
    if cible in valeurs:
        memo[cle_memo] = (True, str(cible))
        return (True, str(cible))

    # Exploration des différentes opérations possibles
    for x in valeurs:
        valeurs_restantes = valeurs[:]
        valeurs_restantes.remove(x)

        operations = [
            (cible + x, "-", x),  # (v + x) - x = v
            (cible - x, "+", x) if cible >= x else None,
            (x - cible, "+", cible) if x >= cible else None,
            (cible // x, "*", x) if x != 0 and cible % x == 0 else None,
            (x // cible, "/", cible) if cible != 0 and x % cible == 0 else None,
            (cible * x, "/", x),  # (v * x) / x = v
        ]

        for operation in operations:
            if operation:  # Vérifie que l'opération est valide
                new_cible, op, operand = operation
                trouve, expr = trouveExpr(new_cible, valeurs_restantes)
                if trouve:
                    memo[cle_memo] = (True, f"({expr}) {op} {operand}")
                    return memo[cle_memo]

    # Si aucune combinaison ne fonctionne
    memo[cle_memo] = (False, "")
    return (False, "")


def generer_nombres(n=6):
    """
    Génère une liste aléatoire de 6 nombres parmi les petits nombres (1-10) et les grands nombres (25, 50, 75, 100).
    """
    operandes = list(range(1, 11)) * 2 + [25, 50, 75, 100]
    return random.sample(operandes, n)


if __name__ == "__main__":
    # Génération aléatoire de la cible et des nombres
    nombres = [4, 8, 5, 6, 6, 2]
    cible = 799

    # Recherche d'une solution exacte
    res = trouveExpr(cible, nombres)
    print(f"Cible: {cible}, Nombres: {nombres}, Résultat: {res}, Nombre d'appels: {cpt}")

    # Si aucune solution exacte n'est trouvée, on cherche la plus proche
    if not res[0]:
        for i in range(1, cible):  # Recherche progressive autour de la cible
            for ecart in [cible + i, cible - i]:
                memo.clear()
                cpt = 0
                res = trouveExpr(ecart, nombres)
                if res[0]:
                    print(f"Approximation trouvée à {ecart} ({'+' if ecart > cible else '-'}{i}) : {res}, Nombre d'appels: {cpt}")
                    exit()