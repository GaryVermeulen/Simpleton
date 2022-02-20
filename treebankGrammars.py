#
# Treebanks and Grammars
#
import nltk
from nltk.corpus import treebank
from collections import defaultdict


def filter(tree):
    child_nodes = [child.label() for child in tree
                   if isinstance(child, nltk.Tree)]
    return  (tree.label() == 'VP') and ('S' in child_nodes)



t = treebank.parsed_sents('wsj_0001.mrg')[0]

print(t)

print('------------------------')

#[subtree for tree in treebank.parsed_sents()
#         for subtree in tree.subtrees(filter)]

entries = nltk.corpus.ppattach.attachments('training')
table = defaultdict(lambda: defaultdict(set))
for entry in entries:
    key = entry.noun1 + '-' + entry.prep + '-' + entry.noun2
    table[key][entry.attachment].add(entry.verb)

for key in sorted(table):
    if len(table[key]) > 1:
        print(key, 'N:', sorted(table[key]['N']), 'V:', sorted(table[key]['V']))

