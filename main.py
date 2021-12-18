import buildDictionaries
import testEditDistance

dictionaryPath = 'dizionari/95000_parole_italiane_con_nomi_propri.txt'
dictionary = []
buildDictionaries.buildDictionary(dictionary, dictionaryPath)

nGrams = [2, 3, 4]
gramDictionaries = []
buildDictionaries.buildGramDictionaries(dictionary, gramDictionaries, nGrams)

nWords = 5
nCharacterToBeModified = [1, 2, 3, 4, 5]
jaccardTresholds = [0.2, 0.4, 0.8]

randomWords = testEditDistance.randomWordsForTest(dictionary, nWords, nCharacterToBeModified)

risultati_ED_Completa = 'risultatiTXT/risultati_ED_Completa.txt'
risultati_nGram = 'risultatiTXT/risultatiNgram.txt'

testEditDistance.testEditDistance_Completa(risultati_ED_Completa, dictionary, randomWords, nCharacterToBeModified)

testEditDistance.testEditDistance_nGram(risultati_nGram, dictionary, nGrams, randomWords, jaccardTresholds,
                                        gramDictionaries, nCharacterToBeModified)
