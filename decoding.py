# program to decode dna babble bricks to text
# freddie starkey for edinburgh igem 2016

#import lexEncode
import numpy
import orcDecode
from operator import itemgetter

#lexicon = lexEncode.encode("/home/freddie/PycharmProjects/iGEM/ogdan",
                           #"/home/freddie/PycharmProjects/iGEM/codeRecord",
                           #"/home/freddie/PycharmProjects/iGEM/gBlocks")

#lexicon = lexEncode.encode("/home/freddie/PycharmProjects/iGEM/maryLex",
                           #"/home/freddie/PycharmProjects/iGEM/mary letter encoding",
                           #"/home/freddie/PycharmProjects/iGEM/gBlocks")

def readIn(filepath):
    with open(filepath) as f:
            sequences = f.readlines()
    f.close()
    return sequences

def decodeControl(filepath, lexicon):
    sequences = readIn(filepath) # file containing sequences for each sentence
    print sequences
    sequencesFilter = map(filterNonDna, sequences)
    print sequencesFilter
    sequencesEmptyFilter = filter(None, sequencesFilter)
    print sequencesEmptyFilter
    sentences = map(splitToWords, sequencesEmptyFilter) # split each sentence into a list of words with appropriate hangs
    print sentences
    #encodedChecksums = map(checkEncodedCheck, sentences) # check the checksum value from the strand itself
    encodedChecksums = [checkEncodedCheck(checksum, lexicon) for checksum in sentences]
    checksumInSeq = map(checkSeqSum, sentences) # check the checksum value in the checksum words
    checkCompare = zip(encodedChecksums, checksumInSeq) # get tuples of the checksum values
    print checkCompare
    for eachCheck in checkCompare:
        if eachCheck[0] != eachCheck[1]:
           #orcCorrected = map(orcDecode.orcCorrect, sentences[checkCompare.index(eachCheck)])
           orcCorrected = [orcDecode.orcCorrect(toCompare, lexicon) for toCompare in sentences[checkCompare.index(eachCheck)]]
           sentences[checkCompare.index(eachCheck)] = orcCorrected
    print [wordList[:len(wordList)-5] for wordList in sentences]
    #decoded = [(map(lookUp, wordList[:len(wordList)-5]), getAddress(wordList)) for wordList in sentences]
    decoded = [([lookUp(wordCoding, lexicon) for wordCoding in wordList[:len(wordList)-5]], getAddress(wordList)) for wordList in sentences]
    print decoded
    return sorted(decoded, key=itemgetter(1))

def filterNonDna(sequence):
    return filter(lambda x: x == 'A' or x == 'T' or x == 'C' or x == 'G', sequence)

# split each sentence into a list of words with appropriate hangs
def splitToWords(sequence):
    return [sequence[i * 46:i * 46 + 50] for i in xrange(0, (len(sequence)/46))]

# check the checksum value from the strand itself
def checkEncodedCheck(wordList, lexicon):
    checkWords = wordList[len(wordList)-5: len(wordList)-1]
    #checkVals = map(lookUp, checkWords)
    checkVals = [lookUp(checkWord, lexicon) for checkWord in checkWords]
    strCheckVals = map(str, checkVals)
    numberStr = ''.join(strCheckVals)
    return int(numberStr)

# check the checksum value in the checksum words
def checkSeqSum(wordList):
    return sum(map(wordSum, wordList[:len(wordList)-5]))

def wordSum(word):
    total = 0
    for eachChar in word[4] + word[7:11]:
        if eachChar == 'A':
            total = total + 0
        elif eachChar == 'T':
            total = total + 1
        elif eachChar == 'G':
            total = total + 2
        elif eachChar == 'C':
            total = total + 3
    return total

def getAddress(wordList):
    return toWordCode(wordList[len(wordList)-1][4] + wordList[len(wordList)-1][7:11])

# returns text from sequence
def lookUp(word, lexicon):
    wordCode = word[4] + word[7:11]
    wordIndex = toWordCode(wordCode)
    return lexicon[wordIndex][0]

# returns base 10 word no. given dna sequence
def toWordCode(wordCode):
    quatCode = ""
    for eachChar in wordCode:
        if eachChar == 'A':
            quatCode = quatCode + '0'
        elif eachChar == 'T':
            quatCode = quatCode + '1'
        elif eachChar == 'G':
            quatCode = quatCode + '2'
        elif eachChar == 'C':
            quatCode = quatCode + '3'
    return int(numpy.base_repr(int(quatCode, base=4), 10))

def universalLookup(sequence, lexicon):
    words = splitToWords(sequence)
    print map(lambda x: x[4] + x[7:11], words)
    #return map(lookUp, words)
    return [lookUp(word, lexicon) for word in words]

#decoded = decodeControl("/home/freddie/PycharmProjects/iGEM/storedSequences")
#print decoded