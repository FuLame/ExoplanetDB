import numpy as np
from sklearn.preprocessing import scale
from random import random

def normalize(X):
    x = np.array(X[:])
    mu= np.mean(x,0)
    print mu
    scale = np.amax(x,0) - np.amin(x,0)
    print scale
    return (x - mu)/scale


def planet_eval(features):
    '''
        Input: list of features: mass, rad, eqTemp, star index, dens
        Output: 1 if planet is habitable, 0 otherwise.
    '''
    if features[0]<0.2 or features[0]>10.0: return 0
    elif features[1]<0.2 or features[1]>3.0: return 0
    elif features[2]<200 or features[2]>600: return 0
    elif features[3]<3.0 or features[3]>6.0: return 0
    elif features[4]<2.0 or features[4]>7.0: return 0
    else: return 1
        
def split_set(X,Y,t,cv):
    '''Splits given set into train set, cross validation set,
        and test set with corresponding label vector.
        Input: X - feature matrix, Y - label vector
              t - factor of test items, cv - factor of
              crossvalidation items
        Output: numpy arrays - train_f, train_l,
                crossval_f, crossval_l, test_f, test_l'''
    test_features = list()
    test_labels = list()
    cv_features = list()
    cv_labels = list()
    train_features = list()
    train_labels = list()
    
    for idx,item in enumerate(X):
        a = random()      
        if a < t:
            test_labels.append(Y[idx])
            test_features.append(item)
        elif a < t+cv:
            cv_labels.append(Y[idx])
            cv_features.append(item)
        else:
            train_labels.append(Y[idx])
            train_features.append(item)

    return np.array(train_features), np.array(train_labels),\
           np.array(cv_features), np.array(cv_labels),\
           np.array(test_features), np.array(test_labels)


def feature_vector(featureList):
    #features:
    #name, mass, radius, pl_temp, st_sp, st_spstr
    #eccent, orb per, orb a
    #st_temp, st_rad, st_mass, pl_insol
    features = list()
    labels = list()
    pl_id = list()
    for item in featureList:
        result = [float(x) for x in item[1:4]]
        if item[5] != None:
            if "M" in item[5]: result.append(6.0)
            elif "K" in item[5]: result.append(5.0)
            elif "G" in item[5]: result.append(4.0)
            elif "F" in item[5]: result.append(3.0)
            elif "O" in item[5]: result.append(2.0)
            elif "B" in item[5]: result.append(1.0)
            elif "A" in item[5]: result.append(0.0)
            else: result.append(8.0)
        else:
            if item[9] < 3700: result.append(6.0)
            elif item[9] < 5200: result.append(5.0)
            elif item[9] < 6000: result.append(4.0)
            elif item[9] < 7500: result.append(3.0)
            elif item[9] < 10000: result.append(2.0)
            elif item[9] < 30000: result.append(1.0)
            elif item[9] > 30000: result.append(0.0)
        result.append(5.31*item[1]/(item[2]**3))        #Density g/cm^3
        features.append(result)
        labels.append(planet_eval(result))
        pl_id.append(item[0])
    
    return np.array(features), np.array(labels), pl_id
