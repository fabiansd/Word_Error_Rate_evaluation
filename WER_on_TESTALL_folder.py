# coding=utf-8
from os import listdir
import codecs
import os
import pandas as pd
import numpy as np

#!/usr/bin/env python

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
    return [WordErrorRate, ErrorsTotal]

#If word contains ,.!?, remove last character of word
def removePeriodOrComma(word):
    if word[-1:] in ',.!?':
        word = word[:-1]
    return word.lower()


def returnOnelineHypotese(filepath):
    # Read file as utf-8, which handles øæå
    oneline = codecs.open(filepath, encoding='utf-8').read().split()


    # Create a list of word, strip each word of ,.!? and rejoin to string
    oneline_stripped_list = []
    for word in oneline:
        oneline_stripped_list.append(removePeriodOrComma(word))

    return oneline_stripped_list

def createLists(hypothesisFolderPath,solutionFilePath):

    fasit = returnOnelineHypotese(solutionFilePath)

    filenameList = []
    werList = []
    errorList = []
    Nhyp_list = []
    Nfasit = len(fasit)
    #Iterate through all files in given folder. If no folderPath given in argument, use 'txt-files'
    #WER for all hypoteses in folderPath is calcualted up to 'fasit'
    for filename in listdir(hypothesisFolderPath):
        print('Name of file: {}'.format(filename))

        #Hypotese in clean text on one line
        hypoteseOneline = returnOnelineHypotese(filepath=os.path.join(hypothesisFolderPath,filename))

        #Calculate WER on current hypoteses to ground truth
        Nhyp = len(hypoteseOneline)
        print('#words fasit: {} #words hyp: {}\n'.format(Nfasit,Nhyp))
        werResult = wer(fasit, hypoteseOneline)


        #Store iteration information in lists
        filenameList.append(filename)
        werList.append(round(werResult[0] * 100, 3))
        errorList.append(werResult[1])
        Nhyp_list.append(Nhyp)
    return [filenameList, werList, errorList, Nhyp_list], Nhyp


#Prints results of createList()
def printLists(lists, Nsol):
    print('{:<0} {:>15} {:>10} {:>10} {:>15}'.format('WER','ACCURACY','ERRORS','#Words','FILENAME'))
    for i in range(len(lists[0])):
        #print('{} \t\t {} \t\t {} \t\t {}'.format(round(lists[1][i],2), round(100-lists[1][i],2), lists[2][i], lists[0][i]))
        print('{:0.2f} {:10.2f} {:10d} {:10d} {:<0}'.format(lists[1][i], 100-lists[1][i], int(lists[2][i]),lists[3][i], '\t\t' + lists[0][i]))

#Save results visually in txt file and in pandas cav file for later visualization
def save_results(result, resultName, Nsol):
    #Save in txt file in the folder
    with open(os.path.join(resultName, 'WER_results.txt'),'w') as resultTXT:
        resultTXT.write('Results for: {}. #words in solution: {}\n'.format(resultName, Nsol))
        resultTXT.write('{:<0} {:>15} {:>10} {:>10} {:>15}\n'.format('WER','ACCURACY','ERRORS','#Words','FILENAME'))
        for i in range(len(result[0])):
            resultTXT.write('{:0.2f} {:10.2f} {:10d} {:10d} {:<0}\n'.format(result[1][i], 100-result[1][i], int(result[2][i]),result[3][i], '\t\t' + result[0][i]))
            #resultTXT.write('{} \t\t {} \t\t {} \t\t {}\n'.format(round(result[1][i],2), round(100-result[1][i],2), int(result[2][i]), result[0][i]))

    result = np.transpose(np.array([result[1],[100-x for x in result[1]],result[2],result[3],result[0]]))

    dataframe = pd.DataFrame(data = result,columns = ['WER','ACCURACY','ERRORS','#words','FILENAME'])
    dataframe.to_csv(path_or_buf = os.path.join(resultName, 'WER_results.csv'))


def initialiseFolderStructure(solutionName, hypothesisFoldeName, testFolderName):
    #Check for validating folder structure
    if not os.path.exists(testFolderName):
        os.mkdir(testFolderName)

    hypothesisFolderPath = os.path.join(testFolderName, hypothesisFoldeName)
    if not os.path.exists(hypothesisFolderPath):
        os.mkdir(hypothesisFolderPath)

    solutionFilePath = os.path.join(testFolderName,solutionName)
    if (not os.path.exists(solutionFilePath)):
        solution_txt_file  = open(solutionFilePath, 'w')
        solution_txt_file.close()
        print('\nFill in the solution file named: ' + solutionName + ' in the folder: '+testFolderName + ' before proceeding\n')
        exit(0)

    if (len(os.listdir(hypothesisFolderPath)) == 0):
        print('\nPlace at least one hypothesis (.txt files only) in the folder: ' + hypothesisFolderPath + ' before proceeding\n')
        exit(0)

    return hypothesisFolderPath, solutionFilePath

if __name__ == '__main__':


    ################# Define folder structure ######################################
    solutionName = 'solution.txt'
    hypothesisFoldeName = 'Hypotheses'
    try:
        testFolderName = sys.argv[1]
    except:
        testFolderName = 'TestAllDefault'

    hypothesisFolderPath, solutionFilePath = initialiseFolderStructure(solutionName, hypothesisFoldeName, testFolderName)
    #################################################################################

    #Run functions to perform WER on folder
    result_matrix, Nsol = createLists(hypothesisFolderPath,solutionFilePath)

    printLists(result_matrix, Nsol)
    save_results(result = result_matrix,Nsol=Nsol,resultName=testFolderName)