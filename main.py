import buildDictionaries
import testEditDistance

tableOfCosts = {'Copy': 0, 'Replace': 1, 'Swap': 1, 'Delete': 1, 'Insert': 1}

dictionaryPath = 'dizionari/95000_parole_italiane_con_nomi_propri.txt'
dictionary = []
buildDictionaries.buildDictionary(dictionary, dictionaryPath)

nGrams = [2, 3, 4]
gramDictionaries = []
buildDictionaries.buildGramDictionaries(dictionary, gramDictionaries, nGrams)

nWords = 100
nCharacterToBeModified = [1, 2, 3, 4, 5]
jaccardTresholds = [0.2, 0.4, 0.8]

randomWords = testEditDistance.randomWordsForTest(dictionary, nWords, nCharacterToBeModified)

risultati_ED_Completa = 'risultatiTXT/risultati_ED_Completa.txt'
risultati_nGram = 'risultatiTXT/risultatiNgram.txt'

testEditDistance.testEditDistance_Completa(risultati_ED_Completa, dictionary, randomWords, tableOfCosts,
                                           nCharacterToBeModified)

testEditDistance.testEditDistance_nGram(risultati_nGram, dictionary, nGrams, randomWords, jaccardTresholds,
                                        gramDictionaries, tableOfCosts, nCharacterToBeModified)
