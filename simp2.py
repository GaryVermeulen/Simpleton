#
# Simpleton
#    Simple-Ton: A ton of simple things to do.
#
#

from datetime import datetime
from dataclasses import dataclass
import simp2Mod as sm
import nltk
from nltk import word_tokenize

flog = 'simpLog.txt'

@dataclass
class NPP:
    # Class attribute
    species = "et al"

    name: str
    gender: str
    isA: str
    canDo: str

@dataclass
class NN:
    # Vauge since the lex is so small
    name: str
    isA: str
    canDo: str
    

myNames = []
myNouns = []

f = open(flog, 'a')
startTime = datetime.now()

print("Simple-Ton, A ton of simple things to do.")

st = startTime.strftime("%m/%d/%Y %H:%M:%S")

print('*** START RUN AT: ' + str(st) + ' ***')
f.write('\n*** START RUN AT: ' + str(st) + ' ***\n')

print("--- Reading data, one moment please ---")

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

# Build a list of name (NNP) objects with attributes from KBs
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
    
    myNames.append(NPP(name,"UNK",name_isA,name_canDo))

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
                
    myNouns.append(NN(noun,noun_isA,noun_canDo))

for o in myNouns:
    print(o.name, o.isA, o.canDo, sep=' : ')
    f.write(o.name + ' : ' + o.isA + ' : ' + o.canDo + '\n')

print("----------------------")
print("--- Reading of data completed ---\n")

endTime = datetime.now()
et = endTime.strftime("%m/%d/%Y %H:%M:%S")

elpTime = endTime - startTime

print("--- endTime: " + str(et) + "\n")
print(type(elpTime))
print(str(elpTime))


f.write("----------------------\n")
f.write("--- reading of data completed ---\n")
f.close()

loop = True

# Main loop
#
while loop:
   
   
    # Get user command input
    #
    cmd = sm.getInput()

    if cmd == 'c' or cmd == 'C': # Chat
        s = input("Enter a short sentence: ")

        
        
    elif cmd == 's' or cmd == 'S': # Speak
        # Randomly generates a sentence from the exiting CFG
        # 
        rules = sm.getRules()
        relationFound = False
        
        while not relationFound:
            s = sm.randomSpeak(rules)
            # This check also returns a list which is needed
            ccs = sm.correctCase(s, myNames)
            pos_s = sm.getTags(s)
            relationFound = sm.searchMeaning(ccs, pos_s, myNames, myNouns)
            print('relationFound: ' + str(relationFound))
        s = ''
            
    elif cmd == 't' or cmd == 'T': # Not yet
        print("TODO: Enter learningMode")
        s = ''
    #    sm.learningMode(retCode)
    else:
        print("else cmd = " + str(cmd))
        s = ''

    if len(s) > 0: # Now the fun begins

        f = open(flog, 'a')
        sLoopTime = datetime.now()
        slt = sLoopTime.strftime("%m/%d/%Y %H:%M:%S")

        print('=== START LOOP AT: ' + str(slt) + ' ===')
        f.write('\n=== START LOOP AT: ' + str(slt) + ' ===\n')
        f.close()

        # Check and correct case for NNPs 
        ccs = sm.correctCase(s, myNames)
        print(type(ccs))
        print(ccs)
        pos_s = sm.getTags(ccs)
        print(type(pos_s))
        print(pos_s)

        # Parse corrected case sentenance (input) per grammar
        #
        retCode = sm.chkGrammar(ccs)

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
            print('-->>Searching for relationships and/or meaning...')
            sm.searchMeaning(ccs, pos_s, myNames, myNouns)
    
        elif isinstance(retCode, ValueError):
            print('-->>retCode returned a ValueError' + str(ValueError))
            sm.myErrHandler(retCode)

# TODO           if sm.myErrHandler(retCode):
#                    sm.learningMode(retCode)
    
        elif isinstance(retCode, list):
            print('-->>Input is grammatically correct per CFG')
            print('-->>Searching for relationships and/or meaning...')

            print(retCode)
            print('- - - - - ')
            print(type(retCode))
            print('- - - - - ')
            
            sm.searchMeaning(ccs, pos_s, myNames, myNouns)
        else:
            print('-->>Something unexpected happened')
        
    else:
        loop = False

    now = datetime.now()
    dt = now.strftime("%m/%d/%Y %H:%M:%S")

    f = open(flog, 'a')
    print('=== END LOOP AT: ' + str(dt) + ' ===')
    f.write('\n=== END LOOP AT: ' + str(dt) + ' ===\n')
    f.close()
        

now = datetime.now()
dt = now.strftime("%m/%d/%Y %H:%M:%S")

f = open(flog, 'a')    

print('*** END RUN AT: ' + str(dt) + ' ***')
f.write('\n*** END RUN AT: ' + str(dt) + ' ***\n')
f.close()

print('End Simple-Ton.')

# end simp.py
