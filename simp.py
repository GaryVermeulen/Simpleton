#
# Simpleton
#    Simple-Ton: A ton of simple things to do.
#
#

from datetime import datetime
from dataclasses import dataclass
import simpMod as sm
import nltk
from nltk import word_tokenize

flog = 'simpLog.txt'

@dataclass
class NP:
    # Class attribute
    species = "et al"

    name: str
    gender: str
    isA: str
    canDo: str

@dataclass
class Nouns:
    # Vauge since the lex is so small
    name: str
    isA: str
    canDo: str
    
myNames = []
myNouns = []

f = open(flog, 'a')
now = datetime.now()

print("Simple-Ton, A ton of simple things to do.")
print("Reading data, one moment please...")
dt = now.strftime("%m/%d/%Y %H:%M:%S")

f.write('\n=== START RUN AT: ' + str(dt) + ' ===\n')

# Build a list of nouns (NN) from cfg
cfgNouns = sm.getNouns()
print(str(len(cfgNouns)) + " Nouns (NN) read.")
f.write(str(len(cfgNouns)) + ' Nouns (NN) read.\n')

# Build a list of names (NP) from lex
cfgNames = sm.getNames()
print(str(len(cfgNames)) + " Proper Nouns (NNP) read.")
f.write(str(len(cfgNames)) + ' Proper Nouns (NNP) read.\n')

# Build an isA list from KB
isA = sm.getIsA()
print(str(len(isA)) + " isA relations read.")
f.write(str(len(isA)) + ' isA relations read.\n')

# Build an canDo list from KB
canDo = sm.getCanDo()
print(str(len(canDo)) + " canDo relations read.")
f.write(str(len(canDo)) + " canDo relations read.\n")

# Build a list of name (NP) objects with attributes from KBs
for name in cfgNames:
    name_isA = "UNK"
    name = name.replace('"', '')    
    for x in isA:
        if x[0] == name:
            if x[1] != '':
                name_isA = x[1]

    name_canDo = "UNK"
    for x in canDo:
        if x[0] == name:
            if x[0] != '':
                name_canDo = x[1]
    
    myNames.append(NP(name,"UNK",name_isA,name_canDo))

print("----------------------")
f.write("----------------------\n")

for obj in myNames:
    print(obj.name, obj.gender, obj.isA, obj.canDo, sep=' : ')
    f.write(obj.name + ' : ' + obj.gender + ' : ' + obj.isA + ' : ' + obj.canDo + '\n')

print("----------------------")
f.write("----------------------\n")

# Build a list of noun (NN) objects with attributes from KBs
for noun in cfgNouns:
    noun_isA = "UNK"
    noun = noun.replace('"', '')
    
    for x in isA:
        if x[0] == noun:
            if x[0] != '':
                noun_isA = x[1]

    noun_canDo = "UNK"
    for x in canDo:
        if x[0] == noun:
            if x[0] != '':
                noun_canDo = x[1]
                
    myNouns.append(Nouns(noun,noun_isA,noun_canDo))

for o in myNouns:
    print(o.name, o.isA, o.canDo, sep=' : ')
    f.write(o.name + ' : ' + o.isA + ' : ' + o.canDo + '\n')

print("----------------------")
f.write("----------------------\n")
f.close()

loop = True


while loop:

    speak = True
    
    while speak:
        response = input('Input or Output<I/O>?')

        if response in 'Oo':
            relationFound = False
            while not relationFound:
                s = sm.randomSpeak()
                relationFound = sm.searchMeaning(s, myNames, myNouns)
                print('relationFound: ' + str(relationFound))
            speak = True
        else:
            speak = False
    
    # Get user input
    #
    s = sm.getSentence()

    if len(s) > 0:

        # Parse input per grammar
        #
        retCode = sm.chkGrammar(s)

        # retCode will be either:
        # 1)
        #  retType: <class 'list'>
        #  [Tree('S', [Tree('NP', ['Mary']), Tree('VP', [Tree('V', ['walked']), Tree('NP', ['Pookie']), Tree('PP', [Tree('P', ['in']), Tree('NP', [Tree('Det', ['the']), Tree('N', ['park'])])])])])]
        # 2)
        #  retType: <class 'ValueError'>
        #  Grammar does not cover some of the input words: "'Harry'".
        # 3)
        #  retType: <class 'int'>
        #  0

        if retCode == 0:
            print('-->>Unable to find any productions in existing grammar')
            sm.searchMeaning(s, myNames, myNouns)
    
        elif isinstance(retCode, ValueError):
            print('-->>retCode returned a ValueError' + str(ValueError))

            if sm.myErrHandler(retCode):
                sm.learningMode(retCode)
                loop = False
    
        elif isinstance(retCode, list):
            print('-->>Input is grammatically correct per CFG')
            print('-->>Searching for relationships and/or meaning...')
            sm.searchMeaning(s, myNames, myNouns)
        else:
            print('-->>Something unexpected happened')
        
    else:
        loop = False
    
print('End Simple-Ton.')

# end simp.py
