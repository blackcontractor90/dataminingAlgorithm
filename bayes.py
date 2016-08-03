from numpy import *
import bayes

def loadDataSet():
	postingList = []
	classVec = [0, 1, 0, 1, 0, 1]
	#1 is abusive, o is not abusive
	return postingList, classVec

#creates an empty set
def  createVocabList(dataSet):
	vocabSet = set([])
	for document in dataSet:
		vocabSet = vocabSet | set(document)
		return list(vocabSet)

#create the set of 2 unions
def  setOfWords2Vec(vocabList, inputSet):
	returnVec = [0]*len(vocabList) #create a vector of all 0's
	for word in inputSet:
		if  word in vocabList:
			returnVec[vocabList.index(word)] = 1
		else: print "The word: %s is not in the Vocabulary list!" % word
	return returnVec

def trainNB0(trainMatrix, trainCategory):
	numTrainDocs = len(trainMatrix)
	numWords = len(trainMatrix[0])
	#initialize probabilities
	pAbusive = sum(trainCategory)/float(numTrainDocs)
	p0Num = zeros(numWords); p1Num = zeros(numWords) #change to p0Num = ones(numWords); p1Num=ones(numWords)
	p0Denom = 0.0; p1Denom = 0.0					 #change to p0Denom = 2.0; p1Denom = 2.0
	for i in range(numTrainDocs):
		if trainCategory[i] == 1:
			p1Num += trainMatrix[i]
			p1Denom += sum(trainMatrix[i])
		else:
			p0Num += trainMatrix[i]
			p0Denom += sum(trainMatrix[i])
	p1Vect = p1Num/p1Denom
	p0Vect = p0Num/p0Denom
	return p0Vect, p1Vect, pAbusive

#develop classifier
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1): #element wise manipulation
	p1 = sum(vec2Classify * p1Vec) + log(pClass1)
	p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
	if p1 > p0:
		return 1
	else:
		return 0

def testingNB():
	listOPosts, listClasses = loadDataSet()
	myVocabList = createVocabList(listOPosts)
	trainMat = []
	for postinDoc in listOPosts:
		trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
		p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
		testEntry = [] #fill with test entry words
		thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
		print testEntry, 'Classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
		testEntry = [] # fill with test entry words
		thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
		print testEntry, 'Classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
