import random
import editDistance
import matplotlib.pyplot as plt


def modifyCharacter(originalWordAsList, randomPosition):
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']
    randomFloat = random.random()
    parola = []
    if randomFloat < 0.25:  # Aggiungi carattere
        for i in range(len(originalWordAsList)):
            if i == randomPosition:
                parola.append(random.choice(letters))
            parola.append(originalWordAsList[i])
    elif randomFloat < 0.5:  # Rimuovi caratere
        for i in range(len(originalWordAsList)):
            if i != randomPosition:
                parola.append(originalWordAsList[i])
    elif randomFloat < 0.75:  # Sostituisci carattere
        for i in range(len(originalWordAsList)):
            if i != randomPosition:
                parola.append(originalWordAsList[i])
            else:
                parola.append(random.choice(letters))
    else:  # Scambia caratteri
        parola = originalWordAsList
        if randomPosition == 0 and len(originalWordAsList) > 1:
            parola[0] = originalWordAsList[1]
            parola[1] = originalWordAsList[0]
        elif len(originalWordAsList) > 1:
            parola[randomPosition - 1] = originalWordAsList[randomPosition]
            parola[randomPosition] = originalWordAsList[randomPosition - 1]

    originalWordAsList = parola
    return originalWordAsList


def randomWordsForTest(dizionarioParole, numTestingWords, nCharacterToBeModified):
    wordsTest = []
    twistedWordsTest = []
    # scegli parole
    for i in range(numTestingWords):
        rndWord = random.choice(dizionarioParole)
        while len(rndWord) == 1:
            rndWord = random.choice(dizionarioParole)
        wordsTest.append(rndWord)
    # modifica parole
    for i in range(len(nCharacterToBeModified)):
        tmpTwistedWordsTest = []
        numOfChanges = nCharacterToBeModified[i]
        for j in range(len(wordsTest)):
            originalWord = wordsTest[j]
            originalWordAsList = list(originalWord)
            for k in range(numOfChanges):
                if len(originalWordAsList) > k:
                    possiblePositions = [t for t in range(len(originalWordAsList))]
                    randomPosition = random.choice(possiblePositions)
                    while possiblePositions[randomPosition] == '#':
                        randomPosition = random.choice(possiblePositions)
                    possiblePositions[randomPosition] = '#'
                    originalWordAsList = modifyCharacter(originalWordAsList, randomPosition)
            twistedWord = "".join(originalWordAsList)
            tmpTwistedWordsTest.append(twistedWord)
        twistedWordsTest.append(tmpTwistedWordsTest)
    return wordsTest, twistedWordsTest


def testWords_nGram(wordsTest, twistedWordsTest, jaccardTreshold, tempi, nGrams, gramDictionaries):
    risultati = []
    for i in range(len(wordsTest)):
        wrongWord = twistedWordsTest[i]
        similarWords = editDistance.editDistanceNGram(wrongWord, nGrams, gramDictionaries, jaccardTreshold, tempi)
        risultatiParola = []
        for ngrams in range(len(similarWords)):
            found = 'no'
            for k in range(len(similarWords[ngrams])):
                if wordsTest[i] == similarWords[ngrams][k]:  # similarWords[ngram][lista di parole vicine]
                    found = 'yes'
            risultatiParola.append(found)
        risultati.append(risultatiParola)
    return risultati


def testEditDistance_nGram(resultFile, dizionari, nGrams, randomWords, jaccardTresholds, gramDictionarie, nCharacterToBeModified):
    numTestingWord = len(randomWords[0])
    str00 = 'EditDistance considerato di successo se la parola cercata risulta tra quelle con distanza minore. \n\n'
    File_object = open(resultFile, "w")
    File_object.write(str00)
    File_object.close()

    # Per Plot Grafico
    ngramHitRate = []
    for nGramterator in range(len(gramDictionarie)):
        ngramHitRate.append([])
        for jIterator in range(len(jaccardTresholds)):
            ngramHitRate[nGramterator].append([])

    # Test Edit Distance nGram
    for n in range(len(nCharacterToBeModified)):
        for j in range(len(jaccardTresholds)):
            str0 = "Test edit distance su " + str(numTestingWord) + " parole, ogni parola ha " + str(
                nCharacterToBeModified[n]) + " caratteri modificati, Jaccard Treshold = " + str(
                jaccardTresholds[j]) + ", dizionario con: " + str(len(dizionari)) + " parole \n"
            tempi = []
            risultati = testWords_nGram(randomWords[0], randomWords[1][n], jaccardTresholds[j], tempi, nGrams,
                                        gramDictionarie)

            risNGRAM = []
            timeNGRAM = []
            for nGramIterator in range(len(nGrams)):
                risNGRAM.append(0)
                timeNGRAM.append(0)

            for k in range(len(risultati)):  # per ogni parola
                for nGramIterator in range(len(nGrams)):
                    if risultati[k][nGramIterator] == 'yes':
                        risNGRAM[nGramIterator] = risNGRAM[nGramIterator] + 1
                    timeNGRAM[nGramIterator] = timeNGRAM[nGramIterator] + tempi[k][nGramIterator]

            list_HitRateResult = []
            list_TimeResult = []
            for nGramIterator in range(len(nGrams)):
                hitRateNgram = risNGRAM[nGramIterator] / numTestingWord
                str1 = 'HitRate ngram' + str(nGrams[nGramIterator]) + ' = ' + str("{:.2f}".format(hitRateNgram)) + "\n"
                str2 = 'Tempo edit distance ngram' + str(nGrams[nGramIterator]) + ' = ' + str(
                    "{:.2f}".format(timeNGRAM[nGramIterator] / numTestingWord)) + "\n"
                list_HitRateResult.append(str1)
                list_TimeResult.append(str2)
                ngramHitRate[nGramIterator][j].append(hitRateNgram)  # Per PLOT Grafico

            strList = [str0] + list_HitRateResult + list_TimeResult + ['\n']
            File_object = open(resultFile, "a")
            File_object.writelines(strList)
            File_object.close()

    draw_nGramPlot(ngramHitRate, nCharacterToBeModified)


def draw_nGramPlot(ngramHitRate, nCharacterToBeModified):
    strPath = "risultatiGrafici/"
    zero = [0]
    uno = [1]
    for nGramIt in range(len(ngramHitRate)):
        plt.clf()
        plt.cla()
        plt.plot(zero + nCharacterToBeModified, uno + (ngramHitRate[nGramIt][0]))
        plt.plot(zero + nCharacterToBeModified, uno + (ngramHitRate[nGramIt][1]))
        plt.plot(zero + nCharacterToBeModified, uno + (ngramHitRate[nGramIt][2]))
        plt.legend(["j=0.2", "j=0.4", "j=0.8"])  # , bbox_to_anchor=(1.05, 0.6)
        str000 = 'HitRate al variare del numero di caratteri con nGram = ' + str(nGramIt + 2)
        plt.title(str000)
        plt.xticks(zero + nCharacterToBeModified)
        plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        plt.xlabel("Numero di caratteri modificati")
        plt.ylabel("HitRate")
        plt.grid()
        plt.savefig(strPath + 'plotHitRate_nGram' + str(nGramIt + 2))


def testWords_Completa(risultati, wordsTest, twistedWordsTest, dizionarioParole, tempi):
    for i in range(len(wordsTest)):
        wrongWord = twistedWordsTest[i]
        similarWords = editDistance.editDistanceCompleta(wrongWord, dizionarioParole, tempi)
        found = 'no'
        for j in range(len(similarWords)):
            if wordsTest[i] == similarWords[j]:  # similarWords[parola]
                found = 'yes'
        risultati.append(found)
    return risultati


def testEditDistance_Completa(fileOfResult, dictionary, randomWords, nCharacterToBeModified):
    numTestingWord = len(randomWords[0])
    str00 = 'EditDistance considerato di successo se la parola cercata risulta tra quelle con distanza minore. \n\n'
    File_object = open(fileOfResult, "w")
    File_object.write(str00)
    nHitRate = []
    for n in range(len(nCharacterToBeModified)):
        str0 = "Test edit distance di " + str(numTestingWord) + " parole, ogni parola ha " + str(
            nCharacterToBeModified[n]) + " carattere modificati, dizionario con: " + str(
            len(dictionary)) + " parole \n"
        tempi = []
        risultati = []
        risultati = testWords_Completa(risultati, randomWords[0], randomWords[1][n], dictionary, tempi)
        result = 0
        time = 0
        for k in range(len(risultati)):
            if risultati[k] == 'yes':
                result = result + 1
            time = time + tempi[k]
        hitRate = result / numTestingWord
        time = time / numTestingWord
        nHitRate.append(hitRate)
        str1 = 'HitRate = ' + str("{:.2f}".format(hitRate)) + "\n"
        str2 = 'Tempo edit distance = ' + str("{:.0f}".format(time)) + "\n\n"
        strList = [str0, str1, str2]
        File_object = open(fileOfResult, "a")
        File_object.writelines(strList)
        File_object.close()

    draw_nPlot(nCharacterToBeModified, nHitRate)


def draw_nPlot(nCharacterToBeModified, nHitRate):
    strPath = "risultatiGrafici/"
    zero = [0]
    uno = [1]
    plt.clf()
    plt.cla()
    plt.plot(zero + nCharacterToBeModified, uno + nHitRate)
    str000 = 'HitRate al variare del numero di caratteri, Edit distance completa.'
    plt.title(str000)
    plt.xticks(zero + nCharacterToBeModified)
    plt.yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    plt.xlabel("Numero di caratteri modificati")
    plt.ylabel("HitRate")
    plt.grid()
    plt.savefig(strPath + 'plotHitRate_ED_Completa')
