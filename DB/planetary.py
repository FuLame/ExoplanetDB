from PlanetaryDB.planetarydb import *
from PlanetaryDB.dataProcess import *
import numpy as np
from sklearn.preprocessing import scale
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


#from planetaryClass import *

#db_init("PlanetaryDB/planets_short.tab")
#db_fill("planets.tab")
#data = db_grab("Kepler-11 b", ["pl_hostname", "pl_name", "pl_orbper", "pl_masse", "pl_massj", "pl_disc", "pl_rade", "pl_radj", "pl_dens"])
#print data
#Planetx = BasicPlanet()
#Planetx.setPlanetaryProperties(data)
#print Planet

x, y, pl_id = feature_vector(select_all())
X, Y, pl_id2 = feature_vector(select_habitable())


x, mu, variance = normalize(x)
X = normalize(X, mu, variance)

trf,trl,cvf,cvl,tf,tl = split_set(x,y,0.4,0.0)


#clf = DecisionTreeClassifier()
#clf.fit(trf,trl)


def evaluate(clf, top_score, top_clf):
    score = clf.score(features_test, labels_test)
    if  score > top_score:
        return clf, score
    else:
        return top_clf, top_score

print "Decision Tree"
features_train = trf
labels_train = trl
features_test = x
labels_test = y

top_score = 0.0
top_clf = None
for criterion in ['gini', 'entropy']:
    print "Criterion:", criterion
    for splitter in ['best', 'random']:
        for min_samples_split in range(2,10):##########
            for min_samples_leaf in range(1,10):############
                clf_tree = DecisionTreeClassifier(criterion=criterion, splitter=splitter, \
                                                  min_samples_split=min_samples_split, \
                                                  min_samples_leaf=min_samples_leaf)
                clf_tree.fit(features_train, labels_train)
                top_clf, top_score  = evaluate(clf_tree, top_score, top_clf)            
                


print "Top tree classifier is:"
print top_clf.get_params()
print "With the score of:", top_score,"for crossvalidation set"
print "and:",top_clf.score(features_test, labels_test),"for test set."
print "----------------------------------------------"


'''
print clf.score(trf,trl)
print clf.score(cvf,cvl)
print clf.score(tf,tl)
print clf.score(X,Y)
'''
