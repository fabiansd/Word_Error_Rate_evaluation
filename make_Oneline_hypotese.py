import codecs
import sys

def removePeriodOrComma(word):
    if word[-1:] in ',.!?':
        word = word[:-1]
    return word

file1 = sys.argv[1]

with open(file1, 'r') as fasit:
    fasitString=fasit.read().replace('\n', ' ')

codecs.open("hypoteseOneline.txt", "w", "ISO-8859-1")

with open("hypoteseOneline.txt", "w") as text_file:
    #text_file.write("# coding=ISO-8859-1\n")
    for word in fasitString.split():
        text_file.write(removePeriodOrComma(word.lower()) + " ")
