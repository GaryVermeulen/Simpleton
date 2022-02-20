#
# Grammar testing
#
import nltk
from nltk import word_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag
import re
import random as rd


# CFG file
#
fCFG = 'simp2a.cfg'

#testSentence = 'Mary saw Pookie in the park with a telescope'
#testSentence = 'with a telescope Mary saw Pookie in the park'
#testSentence = 'the cat saw Mary in the park with a telescope'
#testSentence = 'with a telescope Mary saw Pookie in the park'
testSentence = 'with a cat park saw Pookie in the telescope'

def chkGrammar(s, traceLevel):

    simpleGrammar = nltk.data.load('file:' + str(fCFG))

    rd_parser = nltk.RecursiveDescentParser(simpleGrammar, traceLevel) #, trace=2)
    treesFound = []

    slist = s.split()

    try:
        for tree in rd_parser.parse(slist):
            treesFound.append(tree)
            print('>' + str(tree) + '<')

        if len(treesFound) == 0:
            print('IF; Input: ' + str(s) + ' - did not produce a tree:\n')
            tok_s = word_tokenize(s)
            pos_s = nltk.pos_tag(tok_s)
            print('Simple tokenizer: ' + str(pos_s) + '\n')
            retCode = 0
        else:
            print('ELSE; Input: ' + str(s) + ' - produced:\n')
            for t in treesFound:
                print('t: ' + str(t) + '\n')

            tok_s = word_tokenize(s)
            pos_s = nltk.pos_tag(tok_s)
            print('Simple tokenizer: ' + str(pos_s) + '\n')
            
            retCode = treesFound
    
    except ValueError as err:
#        print('Problem with input not covered by grammar')
#        print('ValueError: {0}'.format(err))
#        myErrHandler(err)        
#        retCode = -1
        retCode = err
        
##    fl.close()
    
    return retCode

print('Start with: ' + str(testSentence))
print('-------------------------------')

traceLevel = 2
ret = chkGrammar(testSentence, traceLevel)

print('-------------------------------')
print(ret)
