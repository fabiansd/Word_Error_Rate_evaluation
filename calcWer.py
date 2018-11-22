#!/usr/bin/env python
# coding=utf-8

import sys

def wer(r, h):
    """
    Calculation of WER with Levenshtein distance.

    Works only for iterables up to 254 elements (uint8).
    O(nm) time ans space complexity.

    Parameters
    ----------
    r : list
    h : list

    Returns
    -------
    int

    Examples
    --------
    >>> wer("who is there".split(), "is there".split())
    1
    >>> wer("who is there".split(), "".split())
    3
    >>> wer("".split(), "who is there".split())
    3
    """
    # initialisation
    import numpy
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint16)
    d = d.reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i

    # computation
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitution = d[i-1][j-1] + 1
                insertion    = d[i][j-1] + 1
                deletion     = d[i-1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    ErrorsTotal = float(d[len(r)][len(h)])
    WordsTotal = float(len(r))
    WordErrorRate = ErrorsTotal / WordsTotal
    print("substitution", substitution)
    print("insertion", insertion)
    print("deletion", deletion)
    print("Amount of errors:",ErrorsTotal)
    print("Amount of words: ", WordsTotal)
    return WordErrorRate

filename1 = sys.argv[1]
filename2 = sys.argv[2]
fasit = open(filename1).read()
hypotese = open(filename2).read()
WER = wer(fasit.split(), hypotese.split())
print("Word Error Rate [%]: ",round(WER*100,3))