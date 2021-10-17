import time
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


def editDistanceN(str1, dizionario, tempi, tableOfCosts, maxLengthWord, N):
    similarWords = []  # è solo un container per uniformare le funzioni per la ricerca di parole vicine.
    sw = []
    startTime = time.time()
    lun = len(str1)
    numSimilarWords = 0
    for word in dizionario:
        if abs(lun - len(word)) <= N:
            d = editDistance(str1, word, tableOfCosts)
            if d <= 2:
                sw.append((word, d))
                numSimilarWords = numSimilarWords + 1
    endTime = time.time()
    tempi.append(endTime - startTime)
    similarWords.append(sw)
    return orderedSimilarWords(similarWords, maxLengthWord)


def editDistanceCompleta(str1, dizionario, tempi, tableOfCosts, maxLengthWord):
    similarWords = []  # è solo un container per uniformare le funzioni per la ricerca di parole vicine.
    sw = []
    startTime = time.time()
    for word in dizionario:
        d = editDistance(str1, word, tableOfCosts)
        sw.append((word, d))
    endTime = time.time()
    tempi.append(endTime - startTime)
    similarWords.append(sw)
    return orderedSimilarWords(similarWords, maxLengthWord)


def editDistanceNGram(parola, gramDictionaries, jaccardTreshold, tempi, tableOfCosts, maxLengthWord):
    similarWords = []
    timeGram = []
    minDistance = 26
    i = 0
    while i < len(gramDictionaries):
        parolaGram = buildDictionaries.nGram(parola, i + 2)
        startTime = time.time()
        sw = []
        for word in gramDictionaries[i].keys():
            wordGram = gramDictionaries[i][word]
            jac = jaccard(parolaGram, wordGram)
            if jac >= jaccardTreshold:
                d = editDistance(parola, word, tableOfCosts)
                if d <= minDistance:
                    sw.append((word, d))
        endTime = time.time()
        timeGram.append(endTime - startTime)
        similarWords.append(sw)
        i = i + 1
    tempi.append(timeGram)
    return orderedSimilarWords(similarWords, maxLengthWord)


def orderedSimilarWords(similarWords, k):
    i = 0
    while i < len(similarWords):
        sw = similarWords[i]
        swOrdered = countingSort(sw, k)
        similarWords[i] = swOrdered
        i = i + 1
    return similarWords


def returnNSimilarWords(sW, N):
    i = 0
    similarWords = []
    while i < len(sW):
        tmp = []
        if len(sW[i]) != 0:
            j = 0
            while j < N and j < len(sW[i]):
                tmp.append(sW[i][j])
                j = j + 1
        similarWords.append(tmp)
        i = i + 1
    sW = similarWords
    return sW


def jaccard(strGram1, strGram2):
    num = [gram for gram in strGram1 if gram in strGram2]
    den = strGram1 + [gram for gram in strGram2 if gram not in strGram1]
    if len(num) == 0:
        return 0
    else:
        return float(len(num) / len(den))


def countingSort(a, k):
    size = len(a)
    b = [('', 0)] * size
    c = [0 for i in range(k + 1)]

    for j in range(0, size):
        c[a[j][1]] = c[a[j][1]] + 1
    for i in range(1, k + 1):
        c[i] = c[i] + c[i - 1]
    j = size - 1
    while j >= 0:
        b[c[a[j][1]] - 1] = (a[j][0], a[j][1])
        c[a[j][1]] = c[a[j][1]] - 1
        j = j - 1
    return b
