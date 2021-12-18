import timeit as time
import numpy as np
import buildDictionaries

tableOfCosts = {'Copy': 0, 'Replace': 1, 'Swap': 1, 'Delete': 1, 'Insert': 1}
tableOfOperation = {'Null': 0, 'Copy': 1, 'Replace': 2, 'Swap': 3, 'Delete': 4, 'Insert': 5}


def editDistance(str1, str2):
    m = len(str1)
    n = len(str2)
    c = np.zeros((m + 1, n + 1))
    op = np.zeros((m + 1, n + 1))

    for i in range(m + 1):
        c[i, 0] = i * tableOfCosts['Delete']
        op[i, 0] = i * tableOfOperation['Delete']
    for j in range(n + 1):
        c[0, j] = j * tableOfCosts['Insert']
        op[0, j] = j * tableOfOperation['Insert']

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            c[i, j] = np.inf
            op[i, j] = tableOfOperation['Null']
            if str1[i - 1] == str2[j - 1]:
                c[i, j] = c[i - 1, j - 1] + tableOfCosts['Copy']
                op[i, j] = tableOfOperation['Copy']
            if str1[i - 1] != str2[j - 1] and c[i - 1, j - 1] + tableOfCosts['Replace'] < c[i, j]:
                c[i, j] = c[i - 1, j - 1] + tableOfCosts['Replace']
                op[i, j] = tableOfOperation['Replace']
            if i >= 2 and j >= 2 and str1[i - 1] == str2[j - 2] and str1[i - 2] == str2[j - 1] and c[i - 2, j - 2] + \
                    tableOfCosts['Swap'] < c[i, j]:
                c[i, j] = c[i - 2, j - 2] + tableOfCosts['Swap']
                op[i, j] = tableOfOperation['Swap']
            if c[i - 1, j] + tableOfCosts['Delete'] < c[i, j]:
                c[i, j] = c[i - 1, j] + tableOfCosts['Delete']
                op[i, j] = tableOfOperation['Delete']
            if c[i, j - 1] + tableOfCosts['Insert'] < c[i, j]:
                c[i, j] = c[i, j - 1] + tableOfCosts['Insert']
                op[i, j] = tableOfOperation['Insert']
    return c, op


def distance(str1, str2):
    result = editDistance(str1, str2)
    c = result[1]
    return c[len(str1), len(str2)]


def editDistanceCompleta(str1, dizionario, tempi):
    # data un parole trova le più vicine controllando l'intero dizionario.
    sw = []
    startTime = time.default_timer()
    minDistance = np.inf
    for word in dizionario:
        d = distance(str1, word)
        if d < minDistance:
            minDistance = d
            sw.clear()
            sw.append(word)
        elif d == minDistance:
            sw.append(word)
    endTime = time.default_timer()
    tempi.append(endTime - startTime)
    return sw


def editDistanceNGram(parola, nGrams, gramDictionaries, jaccardTreshold, tempi):
    # data un parola trova le più vicine per ogni dizionario nGram sfruttando la soglia di jaccard ricevuta.
    similarWords = []
    timeGram = []
    nGramIndex = 0
    while nGramIndex < len(gramDictionaries):
        startTime = time.default_timer()
        minDistance = np.inf
        parolaGram = buildDictionaries.nGram(parola, nGrams[nGramIndex])
        sw = []
        for word in gramDictionaries[nGramIndex].keys():
            wordGram = gramDictionaries[nGramIndex][word]
            jac = jaccard(parolaGram, wordGram)
            if jac >= jaccardTreshold:
                d = distance(parola, word)
                if d < minDistance:
                    minDistance = d
                    sw.clear()
                    sw.append(word)
                elif d == minDistance:
                    sw.append(word)
        endTime = time.default_timer()
        timeGram.append(endTime - startTime)
        similarWords.append(sw)
        nGramIndex = nGramIndex + 1
    tempi.append(timeGram)
    return similarWords


def jaccard(strGram1, strGram2):
    num = [gram for gram in strGram1 if gram in strGram2]
    den = strGram1 + [gram for gram in strGram2 if gram not in strGram1]
    if len(num) == 0:
        return 0
    else:
        return float(len(num) / len(den))
