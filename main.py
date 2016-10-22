import logging
from FileOps import readExcelFile
import classifier

TRAINING_DATA_FILE = '../data/training_exp.xlsx'
#C:\Users\AspireV5\Desktop\prototype_pn\UNSUPERVISED ALGORITHM - PYTHON\data
TEST_DATA_FILE = '../data/testing_exp.xlsx'
#C:\Users\AspireV5\Desktop\prototype_pn\UNSUPERVISED ALGORITHM - PYTHON\data

def word_feats(words):
	return dict([(word, True) for word in words])
		
if _name_ == '_main_':#create instance of classifier
	nbClassifier = Classifier.NBClassifier()
	#knn
	
	#TODO: add logging everywhere, add function decorators to capture the time taken, add multi-threading, and add more classifiers
	
	#call file ops to read input file
	training_tweets = readExcelFile(TRAINING_DATA_FILE, 'name', 'train') + readExcelFile(TRAINING_DATA_FILE, 'name', 'train')
	training_feats = nbClassifier.get_feats(word_Feats, training_tweets)
	
	#call get_feats for test tweets
	test_tweets = readExcelFile(TEST_DATA_FILE, 'name', 'test') + readExcelFile(TEST_DATA_FILE, 'name', 'test')
	test_feats = nbClassifier.get_feats(word_feats, test_tweets)
	
	#train the feature sets using naive baiyes classifier, e.g. other algorithm
	nbClassifier.train(training_feats, test_feats)

	#calculate the accuracy
	nbClassifier.accuracy()
	
	#calculate precision, recallm and f-score of positive, negative, neutral, and mixed sentiment tweets
	nbClassifier.stats()
	
	#print the confusion matrix
	nbClassifier.confusion_matrix()
	