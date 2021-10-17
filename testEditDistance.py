import math
import random
import editDistance


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


def randomWordsForTest(dizionarioParole, numTestingWords):
    wordsTest = []
    twistedWordsTest = []
    for i in range(numTestingWords):
        rndWord = random.choice(dizionarioParole)
        while len(rndWord) == 1:
            rndWord = random.choice(dizionarioParole)
        wordsTest.append(rndWord)
    for i in range(len(wordsTest)):
        numOfChanges = random.randint(1, math.floor(len(wordsTest[i]) / 2))
        originalWord = wordsTest[i]
        originalWordAsList = list(originalWord)
        for i in range(numOfChanges):
            possiblePositions = [i for i in range(len(originalWordAsList))]
            randomPosition = random.choice(possiblePositions)
            while possiblePositions[randomPosition] == '#':
                randomPosition = random.choice(possiblePositions)
            possiblePositions[randomPosition] = '#'
            originalWordAsList = modifyCharacter(originalWordAsList, randomPosition)
        twistedWord = "".join(originalWordAsList)
        twistedWordsTest.append(twistedWord)
    randomWords = [wordsTest, twistedWordsTest]
    return randomWords


def testWords_nGram(risultati, wordsTest, twistedWordsTest, jaccardTreshold, tempi, gramDictionaries, tableOfCosts,
                    maxLengthWord):
    for i in range(len(wordsTest)):
        wrongWord = twistedWordsTest[i]
        orderedSW = editDistance.editDistanceNGram(wrongWord, gramDictionaries, jaccardTreshold, tempi,
                                                   tableOfCosts, maxLengthWord)  # solo ordered SW
        for y in range(len(risultati)):
            risultatiParola = []
            tmpSW = orderedSW.copy()
            tmpSW = editDistance.returnNSimilarWords(tmpSW, y + 1)
            for j in range(len(tmpSW)):
                found = 'no'
                for k in range(len(tmpSW[j])):
                    if wordsTest[i] == tmpSW[j][k][0]:
                        found = 'yes'
                risultatiParola.append(found)
            risultati[y].append(risultatiParola)
    return risultati


def testEditDistance_nGram(filesOfResult, dizionari, randomWords, numTestingWord, jaccardTresholds, gramDictionarie,
                           tableOfCosts, maxLengthWord):  # gramDictionarie contiene i dizionari gram

    for z in range(len(filesOfResult)):
        if z == 0:
            str00 = 'EditDistance considerato di successo se la parola cercata risulta quella con distanza minore. \n\n'
        else:
            str00 = 'EditDistance considerato di successo se la parola cercata è presente tra le PRIME ' + str(
                z + 1) + ' parole con distanza minore. \n\n'
        File_object = open(filesOfResult[z], "w")
        File_object.write(str00)

    for dizionarioIterator in range(len(dizionari)):
        for j in range(len(jaccardTresholds)):
            str0 = "Test edit distance su " + str(numTestingWord) + " parole, Jaccard Treshold = " + str(
                jaccardTresholds[j]) + ", dizionario con: " + str(len(dizionari[dizionarioIterator])) + " parole \n"
            tempi = []
            risultati = []
            for y in range(len(filesOfResult)):
                risultati.append([])
            risultati = testWords_nGram(risultati, randomWords[dizionarioIterator][0],
                                        randomWords[dizionarioIterator][1], jaccardTresholds[j], tempi,
                                        gramDictionarie[dizionarioIterator], tableOfCosts, maxLengthWord)

            for t in range(len(filesOfResult)):

                risNGRAM2, risNGRAM3, risNGRAM4 = 0, 0, 0
                timeNGRAM2, timeNGRAM3, timeNGRAM4 = 0, 0, 0
                for k in range(len(risultati[t])):
                    if risultati[t][k][0] == 'yes':
                        risNGRAM2 = risNGRAM2 + 1
                    if risultati[t][k][1] == 'yes':
                        risNGRAM3 = risNGRAM3 + 1
                    if risultati[t][k][2] == 'yes':
                        risNGRAM4 = risNGRAM4 + 1

                    timeNGRAM2 = timeNGRAM2 + tempi[k][0]
                    timeNGRAM3 = timeNGRAM3 + tempi[k][1]
                    timeNGRAM4 = timeNGRAM4 + tempi[k][2]

                str1 = 'HitRate ngram2 = ' + str("{:.2f}".format(risNGRAM2 / numTestingWord)) + "\n"
                str2 = 'HitRate ngram3 = ' + str("{:.2f}".format(risNGRAM3 / numTestingWord)) + "\n"
                str3 = 'HitRate ngram4 = ' + str("{:.2f}".format(risNGRAM4 / numTestingWord)) + "\n"
                str4 = 'Tempo edit distance ngram2 = ' + str("{:.2f}".format(timeNGRAM2 / numTestingWord)) + "\n"
                str5 = 'Tempo edit distance ngram3 = ' + str("{:.2f}".format(timeNGRAM3 / numTestingWord)) + "\n"
                str6 = 'Tempo edit distance ngram4 = ' + str("{:.2f}".format(timeNGRAM4 / numTestingWord)) + "\n\n"

                strList = [str0, str1, str2, str3, str4, str5, str6]
                File_object = open(filesOfResult[t], "a")
                File_object.writelines(strList)
                File_object.close()


def testWords_Completa(risultati, wordsTest, twistedWordsTest, dizionarioParole, tempi, tableOfCosts, maxLengthWord):
    for i in range(len(wordsTest)):
        wrongWord = twistedWordsTest[i]
        sW = editDistance.editDistanceCompleta(wrongWord, dizionarioParole, tempi, tableOfCosts,
                                               maxLengthWord)  # solo ordered SW
        tmpSW = sW.copy()
        tmpSW = editDistance.returnNSimilarWords(tmpSW, 1)
        for j in range(len(tmpSW)):
            found = 'no'
            for k in range(len(tmpSW[j])):
                if wordsTest[i] == tmpSW[j][k][0]:
                    found = 'yes'
        risultati.append(found)
    return risultati


def testEditDistance_Completa(fileOfResult, dizionarioParole, randomWords, numTestingWord, tableOfCosts, maxLengthWord):
    str00 = 'EditDistance considerato di successo se la parola cercata risulta quella con distanza minore. \n\n'
    File_object = open(fileOfResult, "w")
    File_object.write(str00)
    for i in range(len(dizionarioParole)):
        str0 = "Test edit distance di " + str(numTestingWord) + " parole, dizionario con: " + str(
            len(dizionarioParole[i])) + " parole \n"
        tempi = []
        risultati = []
        risultati = testWords_Completa(risultati, randomWords[i][0], randomWords[i][1], dizionarioParole[i], tempi,
                                       tableOfCosts, maxLengthWord)
        result = 0
        time = 0
        for k in range(len(risultati)):
            if risultati[k] == 'yes':
                result = result + 1
            time = time + tempi[k]
        str1 = 'HitRate = ' + str("{:.2f}".format(result / numTestingWord)) + "\n"
        str2 = 'Tempo edit distance = ' + str("{:.2f}".format(time / numTestingWord)) + "\n\n"
        strList = [str0, str1, str2]
        File_object = open(fileOfResult, "a")
        File_object.writelines(strList)
        File_object.close()


def testWords_N(risultati, wordsTest, twistedWordsTest, dizionarioParole, tempi, tableOfCosts, maxLengthWord, N):
    for i in range(len(wordsTest)):
        wrongWord = twistedWordsTest[i]
        orderedSW = editDistance.editDistanceN(wrongWord, dizionarioParole, tempi, tableOfCosts, maxLengthWord,
                                               N)  # solo ordered SW
        tmpSW = orderedSW.copy()
        tmpSW = editDistance.returnNSimilarWords(tmpSW, 1)
        for j in range(len(tmpSW)):
            found = 'no'
            for k in range(len(tmpSW[j])):
                if wordsTest[i] == tmpSW[j][k][0]:
                    found = 'yes'
        risultati.append(found)
    return risultati


def testEditDistance_N(fileOfResult, dizionarioParole, randomWords, numTestingWord, tableOfCosts, maxLengthWord, N):
    str000 = 'EditDistance eseguita solo se la differenza tra la lunghezza delle due parole è minore di ' + str(
        N) + '.\n'
    str00 = 'EditDistance considerato di successo se la parola cercata risulta quella con distanza minore. \n\n'
    File_object = open(fileOfResult, "w")
    File_object.writelines([str000, str00])
    for i in range(len(dizionarioParole)):
        str0 = "Test edit distance di " + str(numTestingWord) + " parole, dizionario con: " + str(
            len(dizionarioParole[i])) + " parole \n"
        tempi = []
        risultati = []
        risultati = testWords_N(risultati, randomWords[i][0], randomWords[i][1], dizionarioParole[i], tempi,
                                tableOfCosts, maxLengthWord, N)
        result = 0
        time = 0
        for k in range(len(risultati)):
            if risultati[k] == 'yes':
                result = result + 1
            time = time + tempi[k]
        str1 = 'HitRate = ' + str("{:.2f}".format(result / numTestingWord)) + "\n"
        str2 = 'Tempo edit distance = ' + str("{:.2f}".format(time / numTestingWord)) + "\n\n"
        strList = [str0, str1, str2]
        File_object = open(fileOfResult, "a")
        File_object.writelines(strList)
        File_object.close()
