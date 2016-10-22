from sklearn.datasets import load_iris 
from sklearn import cross_validation 
from operator import itemgetter
from collections import Counter
from sklearn.metrics import classification_report, accuracy_score
import numpy as np
import math


#calculate euclidean distance
def get_distance(data1, data2):
    points = zip(data1, data2)
    diffs_squared_distance = [pow(a-b, 2) for (a,b) in points]
    return math.sqrt(sum(diffs_squared_distance))

def get_neighbours(training_set, test_instance, k):
    distances = [_get_tuple_distance(training_instance, test_instance) for training_instance in training_set]
#index 1: calculated distance between training_instance and test_instance
    sorted_distances = sorted(distances, key=itemgetter(1))
    #extract only training instances
    sorted_training_instances = [tuple[0] for tuple in sorted_distances]			
    #select first k elements
    return sorted_training_instances[:k]

def _get_tuple_distance(training_instance, test_instance):
    return (training_instance, get_distance(test_instance, training_instance[0]))

#unpack function
#given an array of nearest neighbours for a test case, tally up classes
def get_majority_vote(neighbours):
    #index 1
    classes = [neighbour[1] for neighbour in neighbours]
    count = Counter(classes)
    return count.most_common()[0][0]

#setting up main function
def main():
    #load dataset and partition in training and testing sets
    iris=load_iris()
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(iris.data, iris.target, test_size=0.4, random_state=1)
    #reformat train/test datasets for convenience
    train=np.array(zip(X_train, y_train))
    test = np.array(zip(X_test, y_test))
    #generate prediction
    predictions = []
    #number of clusters, could be predetermined according to optimized value
    k = 5
    
    #get NN & majority vote on predicted class
    for x in range(len(X_test)):
        print 'Classifying test instance number ' + str(x) + ":",
        neighbours = get_neighbours(training_set=train, test_instance=test[x][0], k=5)
        majority_vote = get_majority_vote(neighbours)
        predictions.append(majority_vote)
        print 'Predicted label=' + str(majority_vote) + ', Actual label=' + str(test[x][1])
    
    #summarize performance of the classification
    print '\nThe overall accuracy of the model is: ' + str(accuracy_score(y_test, predictions)) + "\n"
    report = classification_report(y_test, predictions, target_names = iris.target_names)
    print 'A detailed classification report: \n\n' + report
    
    if _name_=="_main_":
        main()