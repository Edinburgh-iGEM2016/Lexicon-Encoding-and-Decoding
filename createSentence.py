# program to encode a passage of text in dna
# babbled - edinburgh ug igem 2016
# freddie starkey 

import lexEncode
import re

def storeInSeq(filepath, lexicon):
    print lexicon
    sentences = readIn(filepath)  # list of sentences
    print sentences
    dnaSentences = [wordSeqs(sentence, lexicon) for sentence in sentences]
    print dnaSentences
    filterDnaSentences = filter(None, dnaSentences)  # list of lists of sentences with possible dna conversions
    checked = [checksum(filterDnaSentence, lexicon) for filterDnaSentence in filterDnaSentences]
    addressedDnaSentences = addAddresses(checked, lexicon)
    print "check"
    print addressedDnaSentences
    print list(set([val for sublist in addressedDnaSentences for val in sublist]))
    sentenceSeqs = map(completeStrand, addressedDnaSentences)
    return sentenceSeqs

def readIn(filepath):
    with open(filepath) as f:
        text = f.read()
    f.close()
    return re.split(r' *[\.\?!][\'"\)\]]* *', text)

def wordSeqs(sentence, lexicon):
    sentenceList = re.sub("[^\w]", " ",  sentence).split()
    sentenceListLower = [word.lower() for word in sentenceList]
    print sentenceListLower
    words = [i[0] for i in lexicon]
    eachWordIndex = 0
    for eachWord in sentenceListLower:
        try:
            lexIndex = words.index(eachWord)
        except ValueError:
            print "word: " + eachWord + " not in ogdan."
        else:
            if eachWordIndex % 2 == 0:
                sentenceListLower[eachWordIndex] = lexicon[lexIndex][1]
            else:
                sentenceListLower[eachWordIndex] = lexicon[lexIndex][2]
        eachWordIndex = eachWordIndex + 1
    return sentenceListLower

def addAddresses(sentences, lexicon):
    index = 0
    addressOffset = [word[0] for word in lexicon].index('address00')
    for eachSentence in sentences:
        if (len(eachSentence) % 2) == 0:
            eachSentence.append(lexicon[addressOffset + index][1])
        else:
            eachSentence.append(lexicon[addressOffset + index][2])
        index = index + 1
    return sentences

def checksum(dnaSentence, lexicon):
    checkPerWord = map(dnaToNum, dnaSentence)
    intCheckPerWord = map(int, checkPerWord)
    check = padChecksum(str(sum(intCheckPerWord)))
    finalCheck = []
    offset = 0
    for eachDigit in check:
        if (len(dnaSentence) + offset) % 2 == 0:
            finalCheck.append(lexicon[int(eachDigit)][1])
        else:
            finalCheck.append(lexicon[int(eachDigit)][2])
        offset = offset + 1
    checked = list(dnaSentence) + finalCheck
    return checked

def dnaToNum(dnaWord):
    total = 0
    for eachBase in dnaWord[4] + dnaWord[7:11]:
        if eachBase == 'A':
            total = total + 0
        elif eachBase == 'T':
            total = total + 1
        elif eachBase == 'G':
            total = total + 2
        elif eachBase == 'C':
            total = total + 3
    return str(total)

def padChecksum(check):
    return ('0' * (4 - len(check))) + check

def completeStrand(dnaSentence):
    toJoin = [word[4:] for word in dnaSentence[1:]]
    toJoin.insert(0, dnaSentence[0])
    return ''.join(toJoin)
    
