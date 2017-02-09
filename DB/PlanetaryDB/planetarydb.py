import sqlite3
import numpy as np
from sklearn.preprocessing import scale
from random import random

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
            
    
def select_habitable():
    '''
    Grabs the requested value from the database.
    '''       
    try:
        conn = sqlite3.connect('planets.sqlite')
    except:
        print "Connection to database failed."
        return None

    cur = conn.cursor()
    command = '''SELECT pl_name,pl_bmasse,pl_rade,
                pl_eqt,st_sp,st_spstr, 
                pl_orbeccen,pl_orbper,pl_orbsmax,           
                st_teff,st_rad,st_mass,pl_insol
                FROM PlanetsFull WHERE pl_name NOTNULL
                AND pl_bmasse>0.2 AND pl_bmasse<10.0 
                AND pl_rade>0.2 AND pl_rade<3.0
                AND ((st_sp > 3.0 AND st_sp < 6.0) OR st_teff NOTNULL 
                OR st_spstr LIKE "%M%" OR st_spstr LIKE "%K%" OR 
                st_spstr LIKE "%G%" OR st_spstr LIKE "%F%")
                AND pl_eqt > 200.0 AND pl_eqt < 600.0'''
    
    cur.execute(command)
    result = cur.fetchall()
    cur.close
    return result

def select_all():
    '''
    Grabs the requested value from the database.
    '''       
    try:
        conn = sqlite3.connect('planets.sqlite')
    except:
        print "Connection to database failed."
        return None

    cur = conn.cursor()
    command = '''SELECT pl_name,pl_bmasse,pl_rade,
                pl_eqt,st_sp,st_spstr, 
                pl_orbeccen,pl_orbper,pl_orbsmax,           
                st_teff,st_rad,st_mass,pl_insol
                FROM PlanetsFull WHERE pl_name NOTNULL
                AND pl_bmasse NOTNULL AND pl_rade NOTNULL
                AND (st_sp NOTNULL OR st_teff NOTNULL OR st_spstr NOTNULL)
                AND pl_eqt NOTNULL'''
    
    cur.execute(command)
    result = cur.fetchall()
    cur.close
    return result

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

def db_fetch():
    '''
    Grabs the requested value from the database.
    '''       
    try:
        conn = sqlite3.connect('planets.sqlite')
    except:
        print "Connection to database failed."
        return None

    cur = conn.cursor()
    command = "SELECT pl_name, pl_dens, pl_masse FROM Planets WHERE pl_dens > 2.0"
    cur.execute(command)
    result = cur.fetchall()
    cur.close
    return result

def db_grab(planet, data):
    '''
    Grabs the requested value from the database.
    '''       
    try:
        conn = sqlite3.connect('planets.sqlite')
    except:
        print "Connection to database failed."
        return None

    cur = conn.cursor()
    if type(data) != list:
        data = [data]
    command = "SELECT " + " , ".join(data) + " FROM Planets WHERE pl_name = ?"
    cur.execute(command, (planet,))
    result = cur.fetchone()
    cur.close()
    return dict(zip(data,result))
    
def db_init(fname='PlanetsFull.csv'):
    '''
    Initializes the database with column names from the file
    '''
    try:
        conn = sqlite3.connect('planets.sqlite')
        cur = conn.cursor()
        cur.executescript('''
        DROP TABLE IF EXISTS PlanetsFull;''')
        conn.commit()
    except:
        print "Could not connect to database"
        return None
    
    try:
        fh = open(fname)
        columns_designation = list()
        planet_properties = dict()
        command_init_DB = '''CREATE TABLE IF NOT EXISTS PlanetsFull (
                                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                '''
        for line in fh:
            if line.startswith("# COLUMN"):
                #Line example ['#', 'COLUMN', 'pl_hostname:', 'Host', 'Name']
                columns_designation.append(line.split()[2][:-1])
                planet_properties[line.split()[2][:-1]] = " ".join(line.split()[3:])
            elif line.startswith("#") or line.split(',')[0] == 'rowid' or line.split(',')[0] == 'id':
                continue  
            else:
                asd = line.split(',')[1:]
                print asd
                for ind,val in enumerate(asd):
                    if val == "":
                        val = 0.0
                    try:
                        print val
                        float(val)
                        command_init_DB = command_init_DB + columns_designation[ind] + " REAL, "
                    except:
                        command_init_DB = command_init_DB + columns_designation[ind] + " TEXT, "
                break
                    
        command_init_DB = command_init_DB[:-2] + ")"
        print command_init_DB
        cur.execute(command_init_DB)
        conn.commit()
        print "Database initiated."
                
    except IOError:
        print "File not found"
        return None
    except:
        print "Unknown Error"
        return None
    finally:
        cur.close()
        print "Database closed."
        fh.close()

    return columns_designation


        
#######################################################################
def db_fill(fname='planets.tab'):
    '''
    Initializes the database with column names from the file
    '''
    try:
        columns_designation = db_init(fname)
        conn = sqlite3.connect('planets.sqlite')
        cur = conn.cursor()
        conn.commit()
    except:
        print "Database error."
        return None
    
    try:
        fh = open(fname)      
        properties = list()
        for line in fh:
            if line.startswith("#"):
                continue
            
            line = line.split(",")
            if line[0] == "rowid":
                continue            
            
            planet_properties = list()
            planet_field = list()
            command_planets = "INSERT OR IGNORE INTO PlanetsFull ({}) VALUES ("

            for item in zip(columns_designation, line[1:]):
                if item[1] == "": value = None
                else: value = item[1]
                command_planets +=  "?,"
                planet_properties.append(value)
                planet_field.append(item[0])


            command_planets = command_planets[:-1] + ")" #one more for star_id           

            cur.execute(command_planets.format(", ".join(planet_field)), tuple(planet_properties))
       
        
        conn.commit()
        print "Database filled."
                
    except IOError:
        print "File not found"
        return None
    #except:
     #   print "Unknown Error"
      #  return None
    finally:
        cur.close()
        print "Database closed."
        fh.close()



