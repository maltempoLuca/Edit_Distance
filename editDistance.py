import timeit as time
import numpy as np
import buildDictionaries


def editDistance(str1, str2, tableOfCosts):
    m = len(str1)
    n = len(str2)
    c = np.zeros((m + 1, n + 1), dtype=np.int16)

    for i in range(m + 1):
        c[i, 0] = i * tableOfCosts['Delete']
    for j in range(n + 1):
        c[0, j] = j * tableOfCosts['Insert']

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            c[i, j] = n * m + 1
            if str1[i - 1] == str2[j - 1]:
                c[i, j] = c[i - 1, j - 1] + tableOfCosts['Copy']
            if str1[i - 1] != str2[j - 1] and c[i - 1, j - 1] + tableOfCosts['Replace'] < c[i, j]:
                c[i, j] = c[i - 1, j - 1] + tableOfCosts['Replace']
            if i >= 2 and j >= 2 and str1[i - 1] == str2[j - 2] and str1[i - 2] == str2[j - 1] and c[i - 2, j - 2] + \
                    tableOfCosts['Swap'] < c[i, j]:
                c[i, j] = c[i - 2, j - 2] + tableOfCosts['Swap']
            if c[i - 1, j] + tableOfCosts['Delete'] < c[i, j]:
                c[i, j] = c[i - 1, j] + tableOfCosts['Delete']
            if c[i, j - 1] + tableOfCosts['Insert'] < c[i, j]:
                c[i, j] = c[i, j - 1] + tableOfCosts['Insert']
    return c[m, n]


def editDistanceCompleta(str1, dizionario, tempi, tableOfCosts):
    sw = []
    startTime = time.default_timer()
    minDistance = np.inf
    for word in dizionario:
        d = editDistance(str1, word, tableOfCosts)
        if d < minDistance:
            minDistance = d
            sw.clear()
            sw.append((word, d))
        elif d == minDistance:
            sw.append((word, d))
    endTime = time.default_timer()
    tempi.append(endTime - startTime)
    return sw


def editDistanceNGram(parola, nGrams, gramDictionaries, jaccardTreshold, tempi, tableOfCosts):
    similarWords = []
    timeGram = []
    i = 0
    while i < len(gramDictionaries):
        startTime = time.default_timer()
        minDistance = np.inf
        parolaGram = buildDictionaries.nGram(parola, nGrams[i])
        sw = []
        for word in gramDictionaries[i].keys():
            wordGram = gramDictionaries[i][word]
            jac = jaccard(parolaGram, wordGram)
            if jac >= jaccardTreshold:
                d = editDistance(parola, word, tableOfCosts)
                if d < minDistance:
                    minDistance = d
                    sw.clear()
                    sw.append((word, d))
                elif d == minDistance:
                    sw.append((word, d))
        endTime = time.default_timer()
        timeGram.append(endTime - startTime)
        similarWords.append(sw)
        i = i + 1
    tempi.append(timeGram)
    return similarWords


def jaccard(strGram1, strGram2):
    num = [gram for gram in strGram1 if gram in strGram2]
    den = strGram1 + [gram for gram in strGram2 if gram not in strGram1]
    if len(num) == 0:
        return 0
    else:
        return float(len(num) / len(den))
