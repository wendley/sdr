# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import datetime
import time
#import seaborn as sns
#import matplotlib.pyplot as plt

from sklearn import svm
from sklearn import linear_model as lin
from sklearn.neighbors import KNeighborsRegressor as knn
from sklearn import tree as dt
from sklearn.neural_network import MLPRegressor as nnet
from sklearn.ensemble import GradientBoostingRegressor as gbe

from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score, ShuffleSplit
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, explained_variance_score

ifile="../sdr-data/traces/traces-03112018-Cen1a4.csv"
df=pd.read_csv(ifile,header=0)


for c in range(0,2):

    colunas=['rssi','prr','snr']

    if c == 0 :
        target=['txentrega']
        print "\n\n\nEm execucao, aguarde..."
        print "TARGET -- tx entrega..."
        print target
    elif c == 1 :
        target=['relacao']
        print "\n\n\nEm execucao, aguarde..."
        print "TARGET -- relacao..."
        print target

    # TODO: Adicionar RMSE em todos os algoritmos,
    # TODO: organizar saida para melhor coleta (copiar e colar)

    # err=np.abs(estim-y_test)

    # Embaralhar:
    arq=df.sample(frac=1).reset_index(drop=True)

    Xc=arq.loc[:,colunas] # Xc - X completo
    yc=arq.loc[:,target]

    clf1 = lin.LinearRegression();
    clf2 = svm.SVR()
    clf3 = svm.LinearSVR(random_state=0);
    clf4 = svm.NuSVR(C=1.0, nu=0.1);
    clf5 = knn(n_neighbors=2);
    clf6 = dt.DecisionTreeRegressor();
    clf7 = nnet(max_iter=100000);
    clf8 = gbe();



    cross_ss = 1 # cross shuffle split
    cross_sk = 0 # cross shuffle k fold
    proporcao = 0 # proporcao


    if cross_ss == 1 :

        #############################################
        #                                           #
        #   Cross validation com shuffle split      #
        #                                           #
        #############################################

        print "\n------------------------------\n"
        print "Cross validation com shuffle split"
        print "Target: "
        print target

        ##### CROSS VALIDATION 1 - LinearRegression
        t1 = datetime.datetime.now()
        cv = ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
        scores = cross_val_score(clf1, Xc, yc, cv=5, scoring='mean_squared_error') # shuffle split
        # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
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
        scores = cross_val_score(clf2, Xc, yc, cv=5) # shuffle split
        # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
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
        scores = cross_val_score(clf3, Xc, yc, cv=5) # shuffle split
        # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
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
        scores = cross_val_score(clf4, Xc, yc, cv=5) # shuffle split
        # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
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
        scores = cross_val_score(clf5, Xc, yc, cv=5) # shuffle split
        # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
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
        scores = cross_val_score(clf6, Xc, yc, cv=5) # shuffle split
        # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
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
        scores = cross_val_score(clf7, Xc, yc, cv=5) # shuffle split
        # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
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
        scores = cross_val_score(clf8, Xc, yc, cv=5) # shuffle split
        # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
        diff = datetime.datetime.now() - t1

        print "Scores 8 - GBE: "
        print scores
        print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
        print "Tempo de cross validation: "
        print diff
        print "\n------------------------------\n\n\n\n"
        ##### CROSS VALIDATION - END


    if cross_sk == 1 :

        #############################################
        #                                           #
        #  Cross validation com shuffle kFold = 5   #
        #                                           #
        #############################################


        print "\n------------------------------\n"
        print "Cross validation com KFold = 5"
        print "Target: "
        print target

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
        print "\n------------------------------\n\n\n\n"
        ##### CROSS VALIDATION - END


    if proporcao == 1 : # proporcao

        #############################################
        #                                           #
        #   Treino 80% / teste 20%                  #
        #                                           #
        #############################################



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
        yc = arq.loc[1:57177,target]
        X_test = arq.loc[57178:71472,colunas]
        y_test = arq.loc[57178:71472,target]



        print "\n------------------------------\n"
        print "Treino com 80% e teste com 20%"
        print "\n------------------------------\n"
        print "Target: "
        print target

        print "LinearRegression \n"
        t1 = datetime.datetime.now()
        clf1.fit(Xc,yc)
        #clf = joblib.load('trainSVR.joblib')
        diff = datetime.datetime.now() - t1
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "../sdr-data/joblib/train1-"+timestr+".joblib"
        joblib.dump(clf1,filename)
        print "Tempo de treinamento/carregamento: "
        print diff

        t2  = datetime.datetime.now()
        estim2=clf1.predict(X_test)
        diff = datetime.datetime.now() - t2

        print "Tempo de predicao: "
        print diff

        print "r2 score: %f" % r2_score(y_test, estim2)
        print "mse: %f" % mean_squared_error(y_test, estim2)
        print "rmse: %f" % np.sqrt(mean_squared_error(y_test, estim2))
        print "mae: %f" % mean_absolute_error(y_test, estim2)
        print "explained variance score: %f" % explained_variance_score(y_test, estim2)
        print "\n------------------------------\n"


        print "\n------------------------------\n"
        print "SVR ----- \n"
        t1 = datetime.datetime.now()
        clf2.fit(Xc,yc)
        #clf = joblib.load('trainSVR.joblib')
        diff = datetime.datetime.now() - t1
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "../sdr-data/joblib/train2-"+timestr+".joblib"
        joblib.dump(clf1,filename)
        print "Tempo de treinamento/carregamento: "
        print diff

        t2  = datetime.datetime.now()
        estim2=clf2.predict(X_test)
        diff = datetime.datetime.now() - t2

        print "Tempo de predicao: "
        print diff

        print "r2 score: %f" % r2_score(y_test, estim2)
        print "mse: %f" % mean_squared_error(y_test, estim2)
        print "rmse: %f" % np.sqrt(mean_squared_error(y_test, estim2))
        print "mae: %f" % mean_absolute_error(y_test, estim2)
        print "explained variance score: %f" % explained_variance_score(y_test, estim2)
        print "\n------------------------------\n"



        print "\n------------------------------\n"
        print "Linear SVR ----- \n"
        t1 = datetime.datetime.now()
        clf3.fit(Xc,yc)
        #clf = joblib.load('trainSVR.joblib')
        diff = datetime.datetime.now() - t1
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "../sdr-data/joblib/train3-"+timestr+".joblib"
        joblib.dump(clf1,filename)
        print "Tempo de treinamento/carregamento: "
        print diff

        t2  = datetime.datetime.now()
        estim2=clf3.predict(X_test)
        diff = datetime.datetime.now() - t2

        print "Tempo de predicao: "
        print diff

        print "r2 score: %f" % r2_score(y_test, estim2)
        print "mse: %f" % mean_squared_error(y_test, estim2)
        print "rmse: %f" % np.sqrt(mean_squared_error(y_test, estim2))
        print "mae: %f" % mean_absolute_error(y_test, estim2)
        print "explained variance score: %f" % explained_variance_score(y_test, estim2)
        print "\n------------------------------\n"




        print "\n------------------------------\n"
        print "NuSVR ----- \n"
        t1 = datetime.datetime.now()
        clf4.fit(Xc,yc)
        #clf = joblib.load('trainSVR.joblib')
        diff = datetime.datetime.now() - t1
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "../sdr-data/joblib/train4-"+timestr+".joblib"
        joblib.dump(clf1,filename)
        print "Tempo de treinamento/carregamento: "
        print diff

        t2  = datetime.datetime.now()
        estim2=clf4.predict(X_test)
        diff = datetime.datetime.now() - t2

        print "Tempo de predicao: "
        print diff

        print "r2 score: %f" % r2_score(y_test, estim2)
        print "mse: %f" % mean_squared_error(y_test, estim2)
        print "rmse: %f" % np.sqrt(mean_squared_error(y_test, estim2))
        print "mae: %f" % mean_absolute_error(y_test, estim2)
        print "explained variance score: %f" % explained_variance_score(y_test, estim2)
        print "\n------------------------------\n"



        print "\n------------------------------\n"
        print "5 ----- \n"
        t1 = datetime.datetime.now()
        clf5.fit(Xc,yc)
        #clf = joblib.load('trainSVR.joblib')
        diff = datetime.datetime.now() - t1
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "../sdr-data/joblib/train5-"+timestr+".joblib"
        joblib.dump(clf1,filename)
        print "Tempo de treinamento/carregamento: "
        print diff

        t2  = datetime.datetime.now()
        estim2=clf5.predict(X_test)
        diff = datetime.datetime.now() - t2

        print "Tempo de predicao: "
        print diff

        print "r2 score: %f" % r2_score(y_test, estim2)
        print "mse: %f" % mean_squared_error(y_test, estim2)
        print "rmse: %f" % np.sqrt(mean_squared_error(y_test, estim2))
        print "mae: %f" % mean_absolute_error(y_test, estim2)
        print "explained variance score: %f" % explained_variance_score(y_test, estim2)
        print "\n------------------------------\n"




        print "\n------------------------------\n"
        print "6 ----- \n"
        t1 = datetime.datetime.now()
        clf6.fit(Xc,yc)
        #clf = joblib.load('trainSVR.joblib')
        diff = datetime.datetime.now() - t1
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "../sdr-data/joblib/train6-"+timestr+".joblib"
        joblib.dump(clf1,filename)
        print "Tempo de treinamento/carregamento: "
        print diff

        t2  = datetime.datetime.now()
        estim2=clf6.predict(X_test)
        diff = datetime.datetime.now() - t2

        print "Tempo de predicao: "
        print diff

        print "r2 score: %f" % r2_score(y_test, estim2)
        print "mse: %f" % mean_squared_error(y_test, estim2)
        print "rmse: %f" % np.sqrt(mean_squared_error(y_test, estim2))
        print "mae: %f" % mean_absolute_error(y_test, estim2)
        print "explained variance score: %f" % explained_variance_score(y_test, estim2)
        print "\n------------------------------\n"




        print "\n------------------------------\n"
        print "7 ----- \n"
        t1 = datetime.datetime.now()
        clf7.fit(Xc,yc)
        #clf = joblib.load('trainSVR.joblib')
        diff = datetime.datetime.now() - t1
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "../sdr-data/joblib/train7-"+timestr+".joblib"
        joblib.dump(clf1,filename)
        print "Tempo de treinamento/carregamento: "
        print diff

        t2  = datetime.datetime.now()
        estim2=clf7.predict(X_test)
        diff = datetime.datetime.now() - t2

        print "Tempo de predicao: "
        print diff

        print "r2 score: %f" % r2_score(y_test, estim2)
        print "mse: %f" % mean_squared_error(y_test, estim2)
        print "rmse: %f" % np.sqrt(mean_squared_error(y_test, estim2))
        print "mae: %f" % mean_absolute_error(y_test, estim2)
        print "explained variance score: %f" % explained_variance_score(y_test, estim2)
        print "\n------------------------------\n"





        print "\n------------------------------\n"
        print "8 ----- \n"
        t1 = datetime.datetime.now()
        clf8.fit(Xc,yc)
        #clf = joblib.load('trainSVR.joblib')
        diff = datetime.datetime.now() - t1
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "../sdr-data/joblib/train8-"+timestr+".joblib"
        joblib.dump(clf1,filename)
        print "Tempo de treinamento/carregamento: "
        print diff

        t2  = datetime.datetime.now()
        estim2=clf8.predict(X_test)
        diff = datetime.datetime.now() - t2

        print "Tempo de predicao: "
        print diff

        print "r2 score: %f" % r2_score(y_test, estim2)
        print "mse: %f" % mean_squared_error(y_test, estim2)
        print "rmse: %f" % np.sqrt(mean_squared_error(y_test, estim2))
        print "mae: %f" % mean_absolute_error(y_test, estim2)
        print "explained variance score: %f" % explained_variance_score(y_test, estim2)
        print "\n------------------------------\n"


        print "Fim da rodada numero ----------- "
        print c

    ########################
