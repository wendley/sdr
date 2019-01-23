import numpy as np
import pandas as pd
import datetime

from sklearn import svm
from sklearn import linear_model as lin
from sklearn.neighbors import KNeighborsRegressor as knn
from sklearn import tree as dt
from sklearn.neural_network import MLPRegressor as nnet
from sklearn.ensemble import GradientBoostingRegressor as gbe

from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score, ShuffleSplit
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, explained_variance_score

ifile="traces-Cen1a4.csv"
df=pd.read_csv(ifile,header=0)

colunas=['rssi','prr','snr']

# TODO: Adicionar RMSE em todos os algoritmos,
# TODO: organizar saída para melhor coleta (copiar e colar)
# TODO: mais casas decimais na acurácia dos cross validation

# err=np.abs(estim-y_test)

# Embaralhar:
arq=df.sample(frac=1).reset_index(drop=True)

Xc=arq.loc[:,colunas] # Xc - X completo
yc=arq.loc[:,'txentrega']

X=arq.loc[1:20000,colunas] # X amostra de tamanho reduzido
y=arq.loc[1:20000,'txentrega']

X_test=arq.loc[8001:10000,colunas]
y_test=arq.loc[8001:10000,'txentrega']

clf1 = lin.LinearRegression();
clf2 = svm.SVR()
clf3 = svm.LinearSVR(random_state=0);
clf4 = svm.NuSVR(C=1.0, nu=0.1);
clf5 = knn(n_neighbors=2);
clf6 = dt.DecisionTreeRegressor();
clf7 = nnet(max_iter=100000);
clf8 = gbe();

X = Xc
y = yc

print "Em execucao, aguarde..."


# print "\n------------------------------\n"
# print "Cross validation com shuffle split"
#
# ##### CROSS VALIDATION 1 - LinearRegression
# t1 = datetime.datetime.now()
# cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf1, X, y, cv=5) # shuffle split
# # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
# diff = datetime.datetime.now() - t1
#
# print "\n------------------------------\n"
# print "Scores 1 - LinearRegression: "
# print scores
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
# print "Tempo de cross validation:"
# print diff
# print "\n------------------------------\n"
# ##### CROSS VALIDATION - END
#
#
# ##### CROSS VALIDATION 2 - SVR
# t1 = datetime.datetime.now()
# cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf2, X, y, cv=5) # shuffle split
# # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
# diff = datetime.datetime.now() - t1
#
# print "Scores 2 - SVR: "
# print scores
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
# print "Tempo de cross validation: "
# print diff
# print "\n------------------------------\n"
# ##### CROSS VALIDATION - END
#
#
# ##### CROSS VALIDATION 3 - LinearSVR
# t1 = datetime.datetime.now()
# cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf3, X, y, cv=5) # shuffle split
# # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
# diff = datetime.datetime.now() - t1
#
# print "Scores 3 - LinearSVR: "
# print scores
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
# print "Tempo de cross validation: "
# print diff
# print "\n------------------------------\n"
# ##### CROSS VALIDATION - END
#
#
#
# ##### CROSS VALIDATION 4 - NuSVR
# t1 = datetime.datetime.now()
# cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf4, X, y, cv=5) # shuffle split
# # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
# diff = datetime.datetime.now() - t1
#
# print "Scores 4 - NuSVR: "
# print scores
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
# print "Tempo de cross validation: "
# print diff
# print "\n------------------------------\n"
# ##### CROSS VALIDATION - END
#
#
#
# ##### CROSS VALIDATION 5 - KNN
# t1 = datetime.datetime.now()
# cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf5, X, y, cv=5) # shuffle split
# # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
# diff = datetime.datetime.now() - t1
#
# print "Scores 5 - KNN: "
# print scores
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
# print "Tempo de cross validation: "
# print diff
# print "\n------------------------------\n"
# ##### CROSS VALIDATION - END
#
#
#
#
# ##### CROSS VALIDATION 6 - DecisionTreeRegressor
# t1 = datetime.datetime.now()
# cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf6, X, y, cv=5) # shuffle split
# # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
# diff = datetime.datetime.now() - t1
#
# print "Scores 6 - DecisionTreeRegressor: "
# print scores
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
# print "Tempo de cross validation: "
# print diff
# print "\n------------------------------\n"
# ##### CROSS VALIDATION - END
#
#
# ##### CROSS VALIDATION 7 - NNet
# t1 = datetime.datetime.now()
# cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf7, X, y, cv=5) # shuffle split
# # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
# diff = datetime.datetime.now() - t1
#
# print "Scores 7 - NNet: "
# print scores
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
# print "Tempo de cross validation: "
# print diff
# print "\n------------------------------\n"
# ##### CROSS VALIDATION - END
#
#
# ##### CROSS VALIDATION 8 - GBE
# t1 = datetime.datetime.now()
# cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf8, X, y, cv=5) # shuffle split
# # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
# diff = datetime.datetime.now() - t1
#
# print "Scores 8 - GBE: "
# print scores
# print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
# print "Tempo de cross validation: "
# print diff
# print "\n------------------------------\n"
# ##### CROSS VALIDATION - END

##############################################

##############################################

##############################################

##############################################

##############################################

print "\n------------------------------\n"
print "Cross validation com KFold = 5"

##### CROSS VALIDATION 1 - LinearRegression
t1 = datetime.datetime.now()
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf1, X, y, cv=5) # shuffle split
scores = cross_val_score(clf1, Xc, yc, cv=5) # KFold
diff = datetime.datetime.now() - t1

print "\n------------------------------\n"
print "Scores 1 - LinearRegression: "
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print "Tempo de cross validation:"
print diff
print "\n------------------------------\n"
##### CROSS VALIDATION - END


##### CROSS VALIDATION 2 - SVR
t1 = datetime.datetime.now()
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf2, X, y, cv=5) # shuffle split
scores = cross_val_score(clf2, Xc, yc, cv=5) # KFold
diff = datetime.datetime.now() - t1

print "Scores 2 - SVR: "
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print "Tempo de cross validation: "
print diff
print "\n------------------------------\n"
##### CROSS VALIDATION - END


##### CROSS VALIDATION 3 - LinearSVR
t1 = datetime.datetime.now()
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf3, X, y, cv=5) # shuffle split
scores = cross_val_score(clf3, Xc, yc, cv=5) # KFold
diff = datetime.datetime.now() - t1

print "Scores 3 - LinearSVR: "
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print "Tempo de cross validation: "
print diff
print "\n------------------------------\n"
##### CROSS VALIDATION - END



##### CROSS VALIDATION 4 - NuSVR
t1 = datetime.datetime.now()
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf4, X, y, cv=5) # shuffle split
scores = cross_val_score(clf4, Xc, yc, cv=5) # KFold
diff = datetime.datetime.now() - t1

print "Scores 4 - NuSVR: "
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print "Tempo de cross validation: "
print diff
print "\n------------------------------\n"
##### CROSS VALIDATION - END



##### CROSS VALIDATION 5 - KNN
t1 = datetime.datetime.now()
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf5, X, y, cv=5) # shuffle split
scores = cross_val_score(clf5, Xc, yc, cv=5) # KFold
diff = datetime.datetime.now() - t1

print "Scores 5 - KNN: "
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print "Tempo de cross validation: "
print diff
print "\n------------------------------\n"
##### CROSS VALIDATION - END




##### CROSS VALIDATION 6 - DecisionTreeRegressor
t1 = datetime.datetime.now()
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf6, X, y, cv=5) # shuffle split
scores = cross_val_score(clf6, Xc, yc, cv=5) # KFold
diff = datetime.datetime.now() - t1

print "Scores 6 - DecisionTreeRegressor: "
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print "Tempo de cross validation: "
print diff
print "\n------------------------------\n"
##### CROSS VALIDATION - END


##### CROSS VALIDATION 7 - NNet
t1 = datetime.datetime.now()
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf7, X, y, cv=5) # shuffle split
scores = cross_val_score(clf7, Xc, yc, cv=5) # KFold
diff = datetime.datetime.now() - t1

print "Scores 7 - NNet: "
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print "Tempo de cross validation: "
print diff
print "\n------------------------------\n"
##### CROSS VALIDATION - END


##### CROSS VALIDATION 8 - GBE
t1 = datetime.datetime.now()
cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
# scores = cross_val_score(clf8, X, y, cv=5) # shuffle split
scores = cross_val_score(clf8, Xc, yc, cv=5) # KFold
diff = datetime.datetime.now() - t1

print "Scores 8 - GBE: "
print scores
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
print "Tempo de cross validation: "
print diff
print "\n------------------------------\n"
##### CROSS VALIDATION - END


##############################################

##############################################

##############################################

##############################################

##############################################

# clf1 = lin.LinearRegression();
# clf2 = svm.SVR()
# clf3 = svm.LinearSVR(random_state=0);
# clf4 = svm.NuSVR(C=1.0, nu=0.1);
# clf5 = knn(n_neighbors=2);
# clf6 = dt.DecisionTreeRegressor();
# clf7 = nnet(max_iter=100000);
# clf8 = gbe();

# Amostra de 80%/20% (de 71472) 20% = 14294
Xc = arq.loc[1:57177,colunas] # X amostra de tamanho reduzido
yc = arq.loc[1:57177,'txentrega']
X_test = arq.loc[57178:71472,colunas]
y_test = arq.loc[57178:71472,'txentrega']



print "\n------------------------------\n"
print "Treino com 80% e teste com 20%"
print "\n------------------------------\n"
print "LinearRegression \n"
t1 = datetime.datetime.now()
clf1.fit(Xc,yc)
#clf = joblib.load('trainSVR.joblib')
diff = datetime.datetime.now() - t1
joblib.dump(clf1,'train1.joblib')
print "Tempo de treinamento/carregamento: "
print diff

t2  = datetime.datetime.now()
estim2=clf1.predict(X_test)
diff = datetime.datetime.now() - t2

print "Tempo de predicao: "
print diff

print "r2 score: %f" % r2_score(y_test, estim2)
print "mse: %f" % mean_squared_error(y_test, estim2)
print "rmse: %f" % sqrt(mean_squared_error(y_test, estim2))
print "mae: %f" % mean_absolute_error(y_test, estim2)
print "explained variance score: %f" % explained_variance_score(y_test, estim2)
print "\n------------------------------\n"


print "\n------------------------------\n"
print "SVR ----- \n"
t1 = datetime.datetime.now()
clf2.fit(Xc,yc)
#clf = joblib.load('trainSVR.joblib')
diff = datetime.datetime.now() - t1
joblib.dump(clf2,'train2.joblib')
print "Tempo de treinamento/carregamento: "
print diff

t2  = datetime.datetime.now()
estim2=clf2.predict(X_test)
diff = datetime.datetime.now() - t2

print "Tempo de predicao: "
print diff

print "r2 score: %f" % r2_score(y_test, estim2)
print "mse: %f" % mean_squared_error(y_test, estim2)
print "mae: %f" % mean_absolute_error(y_test, estim2)
print "explained variance score: %f" % explained_variance_score(y_test, estim2)
print "\n------------------------------\n"



print "\n------------------------------\n"
print "Linear SVR ----- \n"
t1 = datetime.datetime.now()
clf3.fit(Xc,yc)
#clf = joblib.load('trainSVR.joblib')
diff = datetime.datetime.now() - t1
joblib.dump(clf3,'train3.joblib')
print "Tempo de treinamento/carregamento: "
print diff

t2  = datetime.datetime.now()
estim2=clf3.predict(X_test)
diff = datetime.datetime.now() - t2

print "Tempo de predicao: "
print diff

print "r2 score: %f" % r2_score(y_test, estim2)
print "mse: %f" % mean_squared_error(y_test, estim2)
print "mae: %f" % mean_absolute_error(y_test, estim2)
print "explained variance score: %f" % explained_variance_score(y_test, estim2)
print "\n------------------------------\n"




print "\n------------------------------\n"
print "NuSVR ----- \n"
t1 = datetime.datetime.now()
clf4.fit(Xc,yc)
#clf = joblib.load('trainSVR.joblib')
diff = datetime.datetime.now() - t1
joblib.dump(clf4,'train4.joblib')
print "Tempo de treinamento/carregamento: "
print diff

t2  = datetime.datetime.now()
estim2=clf4.predict(X_test)
diff = datetime.datetime.now() - t2

print "Tempo de predicao: "
print diff

print "r2 score: %f" % r2_score(y_test, estim2)
print "mse: %f" % mean_squared_error(y_test, estim2)
print "mae: %f" % mean_absolute_error(y_test, estim2)
print "explained variance score: %f" % explained_variance_score(y_test, estim2)
print "\n------------------------------\n"




print "\n------------------------------\n"
print "5 ----- \n"
t1 = datetime.datetime.now()
clf5.fit(Xc,yc)
#clf = joblib.load('trainSVR.joblib')
diff = datetime.datetime.now() - t1
joblib.dump(clf5,'train5.joblib')
print "Tempo de treinamento/carregamento: "
print diff

t2  = datetime.datetime.now()
estim2=clf5.predict(X_test)
diff = datetime.datetime.now() - t2

print "Tempo de predicao: "
print diff

print "r2 score: %f" % r2_score(y_test, estim2)
print "mse: %f" % mean_squared_error(y_test, estim2)
print "mae: %f" % mean_absolute_error(y_test, estim2)
print "explained variance score: %f" % explained_variance_score(y_test, estim2)
print "\n------------------------------\n"




print "\n------------------------------\n"
print "6 ----- \n"
t1 = datetime.datetime.now()
clf6.fit(Xc,yc)
#clf = joblib.load('trainSVR.joblib')
diff = datetime.datetime.now() - t1
joblib.dump(clf6,'train6.joblib')
print "Tempo de treinamento/carregamento: "
print diff

t2  = datetime.datetime.now()
estim2=clf6.predict(X_test)
diff = datetime.datetime.now() - t2

print "Tempo de predicao: "
print diff

print "r2 score: %f" % r2_score(y_test, estim2)
print "mse: %f" % mean_squared_error(y_test, estim2)
print "mae: %f" % mean_absolute_error(y_test, estim2)
print "explained variance score: %f" % explained_variance_score(y_test, estim2)
print "\n------------------------------\n"




print "\n------------------------------\n"
print "7 ----- \n"
t1 = datetime.datetime.now()
clf7.fit(Xc,yc)
#clf = joblib.load('trainSVR.joblib')
diff = datetime.datetime.now() - t1
joblib.dump(clf7,'train7.joblib')
print "Tempo de treinamento/carregamento: "
print diff

t2  = datetime.datetime.now()
estim2=clf7.predict(X_test)
diff = datetime.datetime.now() - t2

print "Tempo de predicao: "
print diff

print "r2 score: %f" % r2_score(y_test, estim2)
print "mse: %f" % mean_squared_error(y_test, estim2)
print "mae: %f" % mean_absolute_error(y_test, estim2)
print "explained variance score: %f" % explained_variance_score(y_test, estim2)
print "\n------------------------------\n"





print "\n------------------------------\n"
print "8 ----- \n"
t1 = datetime.datetime.now()
clf8.fit(Xc,yc)
#clf = joblib.load('trainSVR.joblib')
diff = datetime.datetime.now() - t1
joblib.dump(clf8,'train8.joblib')
print "Tempo de treinamento/carregamento: "
print diff

t2  = datetime.datetime.now()
estim2=clf8.predict(X_test)
diff = datetime.datetime.now() - t2

print "Tempo de predicao: "
print diff

print "r2 score: %f" % r2_score(y_test, estim2)
print "mse: %f" % mean_squared_error(y_test, estim2)
print "mae: %f" % mean_absolute_error(y_test, estim2)
print "explained variance score: %f" % explained_variance_score(y_test, estim2)
print "\n------------------------------\n"
