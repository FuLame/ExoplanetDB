from PlanetaryDB.planetarydb import *
import numpy as np
from sklearn.preprocessing import scale
from sklearn.svm import SVC

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

a = select_habitable()

trf,trl,cvf,cvl,tf,tl = split_set(x,y,0.2,0.2)

clf = SVC()
clf.fit(trf,trl)

print clf.score(trf,trl)
print clf.score(cvf,cvl)
print clf.score(tf,tl)
print clf.score(X,Y)

