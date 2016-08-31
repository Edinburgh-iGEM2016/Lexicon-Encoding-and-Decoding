# program to encode a lexicon in babblebrick format
# babbled - edinburgh ug igem 2016
# freddie starkey 

from operator import add

def encode(readName, writeName, gBlockFile):
    # takes the filename of the lexicon word doc and creates the dna equivalent of the text lexicon
    with open(readName) as f:
        vocab = f.read().splitlines()
    decimalCodes = list(range(len(vocab)))
    dnaCodes = map(toDNA, decimalCodes)
    paddedDNAcodes = map(wordPad, dnaCodes)
    restrictionGapped = map(restrictionGap, paddedDNAcodes)
    paddedWithStop = map(addStops, restrictionGapped)
    orc = map(addOrc, paddedDNAcodes)
    minusHangs = map(add, paddedWithStop, orc)
    abForms = map(hangAB, minusHangs)
    baForms = map(hangBA, minusHangs)
    lexicon = zip(vocab, abForms, baForms)
    codeRecord = open(writeName, "rw+")
    gBlocks = open(gBlockFile, "rw+")
    codeRecord.truncate()
    gBlocks.truncate()
    for eachCode in lexicon:
        codeRecord.write("%s\n" % str(eachCode))
        gBlocks.write("%s\n" % str(eachCode[0] +  ": " + "CTCG" + eachCode[1] +
                                   "TGAG CTCG" +
                                   eachCode[2] + "TGAG"))
    codeRecord.close()
    gBlocks.close()
    return lexicon

def toQuat(decimal):
    # changes base 10 to base 4
    quat = []
    while decimal != 0:
        quat.append(decimal % 4)
        decimal = decimal // 4
    return quat[::-1]

def toDNA(decimal):
    # converts a base 10 number into its DNA analogue using quaternary conversion function
    quat = toQuat(decimal)
    quatStr = str(quat)
    baseSeq = ""
    for digit in quatStr:
        if digit == '0':
            baseSeq = baseSeq + 'A'
        elif digit == '1':
            baseSeq = baseSeq + 'T'
        elif digit == '2':
            baseSeq = baseSeq + 'G'
        elif digit == '3':
            baseSeq = baseSeq + 'C'
    return baseSeq

def wordPad(unpaddedDNA):
    # increases the size of a dna code up to 5 bases
    return ('A' * (5 - len(unpaddedDNA))) + unpaddedDNA

def addStops(paddedDNAcode):
    # adds the stop region to a dna strand
    return paddedDNAcode + "TAGCTAATCACTTATGA"

def addOrc(paddedDNAcode):
    # adds the optimal rectangular code sequence to a dna strand
    firstCol = paddedDNAcode[:3]
    secondCol = paddedDNAcode[3:] + 'A'
    firstRow = paddedDNAcode[0] + paddedDNAcode[3]
    secondRow = paddedDNAcode[1] + paddedDNAcode[4]
    thirdRow = paddedDNAcode[2] + 'A'
    orcList = [firstCol, secondCol, firstRow, secondRow, thirdRow]
    orcNums = map(dnaToNum, orcList)
    orcSeq = map(toDNA, orcNums)
    orcSeq = map(orcPad, orcSeq)
    return orcSeq[0] + "GG" + orcSeq[1] + "TT" + orcSeq[2] + "GG" + orcSeq[3] + "TT" + orcSeq[4]

def dnaToNum(dnaCode):
    # converts dna sequence to equivalent number for use in orc
    num = ""
    for eachBase in dnaCode:
        if eachBase == 'A':
            num = num + '0'
        elif eachBase == 'T':
            num = num + '1'
        elif eachBase == 'G':
            num = num + '2'
        elif eachBase == 'C':
            num = num + '3'
    return sum(map(int, num))

def orcPad(unpaddedOrc):
    # increases the size of an orc code up to 2 bases
    return ('A' * (2 - len(unpaddedOrc))) + unpaddedOrc

def hangAB(word):
    # adds the hangs to create an AB form BabbleBrick
    return "GGAG" + word + "CGCT"

def hangBA(word):
    # adds the hangs to create an BA form BabbleBrick
    return "CGCT" + word + "GGAG"

def restrictionGap(word):
    # adds a gap sequence in the word coding region to prevent the formation of illegal restriction sites
    return word[0] + 'TT' + word[1:]
