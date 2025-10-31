
def lire_fichier(nom_fichier):
    
    with open(nom_fichier, 'r') as f:
        return f.read().lower()

def compter_frequences(mots):
    frequences = {}
    for mot in mots:
        if mot in frequences:
            frequences[mot] += 1
        else:
            frequences[mot] = 1
    return frequences


def statistiques_mots(mots):
    tot_mots = len(mots)
    tot_longueur = sum(len(m) for m in mots)
    longueur_moy = tot_longueur / tot_mots 
    return tot_mots, longueur_moy

def mots_extremes(frequences):
    if not frequences:
        return [], []
    freq_max = max(frequences.values())
    freq_min = min(frequences.values())
    mots_max = [m for m, f in frequences.items() if f == freq_max]
    mots_min = [m for m, f in frequences.items() if f == freq_min]
    return mots_max, mots_min

def fpalindromes(mots):
    return [m for m in mots if len(m) > 1 and m == m[::-1]]

def extraire_phrases(texte):
    phrases = []
    phrase = ""
    for c in texte:
        phrase += c
        if c in ".!?":
            phrases.append(phrase.strip())
            phrase = ""
    if phrase.strip():
        phrases.append(phrase.strip())
    return phrases

def statistiques_phrases(phrases):
    nb = len(phrases)
    tot_mots = sum(len(p.split()) for p in phrases)
    longueur_moy = tot_mots / nb 
    return nb, longueur_moy

def vocabulaire(mots):
    if not mots:
        return 0
    return len(set(mots)) / len(mots)

def analyser_texte(fichier):
    texte = lire_fichier(fichier)
    mots = texte.split()

    frequences = compter_frequences(mots)
    tot_mots, longueur_moy = statistiques_mots(mots)
    mots_max, mots_min = mots_extremes(frequences)
    palindromes = fpalindromes(frequences.keys())

    phrases = extraire_phrases(texte)
    nb_phrases, longueur_moy_phrase = statistiques_phrases(phrases)
    diversite = vocabulaire(mots)

    print(" ANALYSE LEXICALE ")
    print("Nombre total de mots :", tot_mots)
    print("Longueur moyenne des mots :", longueur_moy)
    print("Mots les plus utilisés :", mots_max)
    print("Mots les moins utilisés :", mots_min)
    print("Palindromes :", palindromes)

    print("\n ANALYSE GRAMMATICALE ")
    print("Nombre de phrases :", nb_phrases)
    print("Longueur moyenne des phrases :", longueur_moy_phrase)
    print("Diversité du vocabulaire :", diversite)

