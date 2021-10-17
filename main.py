import buildDictionaries
import testEditDistance

tableOfCosts = {'Copy': 0, 'Replace': 1, 'Swap': 1, 'Delete': 1, 'Insert': 1}

generalPath = 'dizionari'
piccoloDizPath = generalPath + '/95000_parole_italiane_con_nomi_propri.txt'
grandeDizPath = generalPath + '/parole_uniche.txt'
pathDizionari = [piccoloDizPath, grandeDizPath]

dizionarioPiccolo = []
dizionarioGrande = []
dizionari = [dizionarioPiccolo]
maxLengthWord = buildDictionaries.buildDictionaries(dizionari, pathDizionari)

dizionario2GramPiccolo, dizionario3GramPiccolo, dizionario4GramPiccolo = {}, {}, {}
dizionario2GramGrande, dizionario3GramGrande, dizionario4GramGrande = {}, {}, {}

gramDictionariesPiccolo = [dizionario2GramPiccolo, dizionario3GramPiccolo, dizionario4GramPiccolo]
gramDictionariesGrande = [dizionario2GramGrande, dizionario3GramGrande, dizionario4GramGrande]
dizionariGram = [gramDictionariesPiccolo]

buildDictionaries.buildGramDictionaries(dizionari, dizionariGram)

nWords = 100
jaccardTresholds = [0.2, 0.4, 0.8]

randomWords = [testEditDistance.randomWordsForTest(dizionari[0], nWords)]   # ,testEditDistance.randomWordsForTest(dizionari[1], nWords)

risultati_ED_Completa = 'risultati_ED_Completa.txt'
risultati_ED_N = 'risultati_ED_N.txt'
risultati_nGram = ['risultati1.txt', 'risultati2.txt']

testEditDistance.testEditDistance_Completa(risultati_ED_Completa, dizionari, randomWords, nWords, tableOfCosts,
                                           maxLengthWord)
testEditDistance.testEditDistance_N(risultati_ED_N, dizionari, randomWords, nWords, tableOfCosts, maxLengthWord, 1)
testEditDistance.testEditDistance_nGram(risultati_nGram, dizionari, randomWords, nWords, jaccardTresholds,
                                        dizionariGram, tableOfCosts, maxLengthWord)
