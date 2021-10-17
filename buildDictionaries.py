def buildDictionaries(dizionari, pathDizionari):
    maxLength = 0
    i = 0
    while i < len(dizionari):
        with open(pathDizionari[i], encoding="utf8", errors='ignore') as fip:
            for word in fip:
                dizionari[i].append(word.rstrip())
                if len(word) > maxLength:
                    maxLength = len(word)
        i = i + 1
    return maxLength


def nGram(word, n):
    nGrams = []
    if word is not None:
        for i in range(len(word) - n + 1):  # RANGE va da 0 a n ESCLUSO
            nGrams.append(word[i:i + n])
    return nGrams


def buildGramDictionaries(dizionari, dizionariGram):
    for j in range(len(dizionari)):
        for word in dizionari[j]:
            i = 0
            while i < len(dizionariGram[j]):
                dizionariGram[j][i].update({word: nGram(word, i + 2)})
                i = i + 1
