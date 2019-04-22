import sys
import re
from collections import defaultdict


def build_lcs_matrix(X, Y):
    m = len(X)
    n = len(Y)
    b1 = [0 for x in range(n + 1)]
    c1 = [0 for x in range(n + 1)]
    b = [list(b1) for x in range(m + 1)]
    c = [list(c1) for x in range(m + 1)]
    X1 = X.lower()
    X2 = (''.join(str(e) for e in Y).lower())
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X1[i - 1] == X2[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = 'diag'
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = 'up'
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = 'left'
    lcs_len = c[i][j]
    return c, b, lcs_len


def parse_LCS_matrix(b, start_i, start_j, m, n, length, lcs_len, stack, vectorlist):
    for i in range(start_i, m + 1):
        for j in range(start_j, n + 1):
            if b[i][j] == 'diag':
                stack.append((i, j))
                if length == 1:
                    if len(stack) == lcs_len:
                        vector = build_vector(stack, n)
                        vectorlist.append(vector)
                    else:
                        continue
                else:
                    length = length - 1
                    parse_LCS_matrix(b, i + 1, j + 1, m, n, length, lcs_len, stack, vectorlist)
                    stack = []
    return


def build_vector(stack, n):
    v = [0] * n
    for i, j in stack:
        v[j - 1] = i
    return v


def vector_values(v, container):
    i = 1
    while i < len(v) and v[i] == 0:
        i = i + 1
    first = i
    i = len(v) - 1
    while i > 0 and v[i] == 0:
        i = i - 1
    last = i
    container['size'] = last - first
    container['distance'] = len(v) - last
    for i in range(first, last):
        if v[i] > 0 and types[i] == "s":
            container['stopcount'] = container['stopcount'] + 1
        elif v[i] == 0 and types[i] != "s" and (types[i] != "h" or types[i]!='H'):
            container['misses'] = container['misses'] + 1


def compare_vectors(A, B):
    values_a, values_b = defaultdict(int), defaultdict(int)
    vector_values(A, values_a)
    vector_values(B, values_b)
    if values_a['misses'] > values_b['misses']:
        return (B)
    elif values_a['misses'] < values_b['misses']:
        return (A)
    if values_a['stopcount'] > values_b['stopcount']:
        return (B)
    elif values_a['stopcount'] < values_b['stopcount']:
        return (A)
    if values_a['distance'] > values_b['distance']:
        return (B)
    elif values_a['distance'] < values_b['distance']:
        return (A)
    if values_a['size'] > values_b['size']:
        return (B)
    elif values_a['size'] < values_b['size']:
        return (A)
    return A


types = []


def acronym_finder(acr):
    global types
    for index, w in enumerate(document_words):
        if acr in w:
            current_window = document_words[index - (2 * len(acr)):index]
            leader = []
            fulltext = []
            for word in current_window:
                fulltext.append(word)
                leader.append(word[:1])
                if word in stop_words:
                    types.append('s')
                elif '-' in word:
                    hypen = word.split('-')
                    for indx, value in enumerate(hypen):
                        if indx == 0:
                            types.append('h')
                        else:
                            types.append('H')
                else:
                    types.append('w')
    c, b, lcs_len = build_lcs_matrix(acr, leader)
    stack = []
    vectorlist = []
    parse_LCS_matrix(b, 0, 0, len(acr), len(leader), lcs_len, lcs_len, stack, vectorlist)
    bvector = []
    bvector = vectorlist[0]
    for i in range(1, len(vectorlist)):
        bvector = compare_vectors(bvector, vectorlist[i])
    text = []
    for i in range(0, len(bvector)):
        if bvector[i] > 0:
            text.append(fulltext[i])
        elif types[i] == 'H' and bvector[i - 1] > 0:
            text.append(fulltext[i])
        elif types[i] == 's' and text != []:
            text.append(fulltext[i])
        else:
            continue
    types = []
    return ' '.join(text)


filename = sys.argv[1]
try:
    document = open(filename, 'r').read()
    document = open('test1.txt', 'r').read()
    document_words = document.split()
    acronyms = re.findall(r'\(([A-Z]{3,10})\)', document)
    stop_words = open('stop_words.txt', 'r').read().split()
    for acronym in acronyms:
        print(acronym + ': ' + acronym_finder(acronym))

except IOError:
    print('Cannot open this file')
