def buildDictionary(dictionary, pathDizionari):
    with open(pathDizionari, encoding="utf8", errors='ignore') as fip:
        for word in fip:
            dictionary.append(word.rstrip())


def nGram(word, n):
    wordnGrams = []
    if word is not None:
        for i in range(len(word) - n + 1):  # RANGE va da 0 a n ESCLUSO
            wordnGrams.append(word[i:i + n])
    return wordnGrams


def buildGramDictionaries(dictionary, gramDictionaries, nGrams):
    for i in range(len(nGrams)):
        gramDictionaries.append({})

    for word in dictionary:
        i = 0
        while i < len(gramDictionaries):
            gramDictionaries[i].update({word: nGram(word, nGrams[i])})
            i = i + 1
