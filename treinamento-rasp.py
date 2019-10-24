# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import datetime
import time
import os

from sklearn import tree as dt
from sklearn import model_selection

from sklearn.externals import joblib
from sklearn.model_selection import cross_val_score, ShuffleSplit
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error, explained_variance_score

ifile="/home/sdr-data/traces/traces5.csv"
df=pd.read_csv(ifile,header=0,index_col=0)

matr=[]
linha=[]

for c in range(0,1):

    colunas=['rssi','prr','snr','latencia-ms','relacao'] # inputs

    if c == 0 :
        target=['prr2']
        print "\n============================="
        print "\n\nEm execucao, aguarde..."
        print "TARGET -- prr2..."
        print target
    elif c == 1 :
        target=['diff-txentrega']
        print "\n============================="
        print "\n\nEm execucao, aguarde..."
        print "TARGET -- diff tx entrega..."
        print target

    # TODO: Adicionar RMSE em todos os algoritmos,
    # TODO: organizar saida para melhor coleta (copiar e colar)

    # err=np.abs(estim-y_test)

    # Embaralhar:
    # arq=df.sample(frac=1).reset_index(drop=True)

    Xc=arq.loc[:,colunas] # Xc - X completo
    yc=arq.loc[:,target]

    # prepare models

    models = []

    # models.append(('LinearR', lin.LinearRegression()))
    # models.append(('SVR', svm.SVR()))
    # models.append(('LinSVR', svm.LinearSVR(random_state=0)))
    # models.append(('NuSVR', svm.NuSVR(C=1.0, nu=0.1)))
    # models.append(('KNN', knn(n_neighbors=2)))
    models.append(('DecTreeReg', dt.DecisionTreeRegressor()))
    # models.append(('NNET', nnet(max_iter=100000)))
    # models.append(('GBE', gbe()))



    # evaluate each model in turn
    results = []
    names = []
    tempos = []
    met1 = []
    met2 = []
    met3= []
    met4 = []
    metStd1 = []
    metStd2 = []
    metStd3= []
    metStd4 = []



    # scor = 'neg_mean_squared_error'
    scor = ('r2','neg_mean_squared_error','neg_mean_absolute_error','explained_variance')

    cross_ss = 1 # cross shuffle split
    cross_sk = 0 # cross shuffle k fold
    proporcao = 0 # proporcao -- melhor usar cross validation
    salvarJoblib = 1


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
        print "\n------------------------------\n"

        for name, model in models:

            ##### CROSS VALIDATION 1 - LinearRegression

            if salvarJoblib == 1:
                t1 = datetime.datetime.now()
                model.fit(Xc,yc)
                #clf = joblib.load('trainSVR.joblib')
                diff = datetime.datetime.now() - t1
                timestr = time.strftime("%Y%m%d-%H%M%S")
                filename = "/home/sdr-data/joblib/train-"+timestr+".joblib"
                joblib.dump(model,filename)
                print "Tempo de treinamento/carregamento: "
                print diff

            else:
                t1 = datetime.datetime.now()
                cv = model_selection.ShuffleSplit(n_splits=5, test_size=0.3, random_state=0) # shuffle split
                scores = model_selection.cross_validate(model, Xc, yc, cv=cv, scoring=scor) # shuffle split OLD: r2, scoring='mean_squared_error'
                # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
                diff = datetime.datetime.now() - t1

                linha=[]
                linha.append(name)
                linha.append(target)
                linha.append('mean')
                results.append(scores)
                linha.append(scores['test_r2'].mean())
                linha.append(scores['test_neg_mean_squared_error'].mean())
                linha.append(scores['test_neg_mean_absolute_error'].mean())
                linha.append(scores['test_explained_variance'].mean())
                
                matr.append(linha)

                linha=[]
                linha.append(name)
                linha.append(target)
                linha.append('std')
                linha.append(scores['test_r2'].std())
                linha.append(scores['test_neg_mean_squared_error'].std())
                linha.append(scores['test_neg_mean_absolute_error'].std())
                linha.append(scores['test_explained_variance'].std())

                matr.append(linha)

                names.append(name)

            # msg = "%s: %0.2f (+/- %0.2f)" % (name, scores.mean(), scores.std()*2)
            print (name)
            print "Trainning time:"
            print diff
            print "\n------------------------------\n"
            
            ##### CROSS VALIDATION - END





    # print results
    
    print names



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
        print "\n------------------------------\n"

        for name, model in models:

            ##### CROSS VALIDATION 1 - LinearRegression
            t1 = datetime.datetime.now()
            cv = model_selection.ShuffleSplit(n_splits=5, test_size=0.3, random_state=0)
            scores = model_selection.cross_validate(model, Xc, yc, cv=5, scoring=scor)# shuffle split OLD: scoring = 'mean_squared_error
            # scores = cross_val_score(clf, Xc, yc, cv=5) # KFold
            diff = datetime.datetime.now() - t1

            results.append(scores)
            names.append(name)

            # msg = "%s: %f (+/- %2f)" % (name, scores.mean(), scores.std()*2)
            print (name)
            print "Trainning time:"
            print diff
            print "\n------------------------------\n"
            
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

# GERA CSV FILE

if salvarJoblib == 0:

    df2=pd.DataFrame(matr,columns=['name','target','calc','r2', 'mse', 'msa','expl-var'])

    # if file does not exist write header
    ifile='report2.csv'
    if not os.path.isfile(ifile):
       df2.to_csv(ifile,mode='a')
    else: # else it exists so append without writing the header
       df2.to_csv(ifile,mode='a', header=False)




# apt-get update ;
# apt-get install git ;
# git clone https://github.com/wendley/sdr.git ;
# apt-get install python-scipy ; 
# apt-get install python-pandas ;

# pip install --upgrade pip ;
# pip install -U scikit-learn==0.20.0 ;

# Optionally:
# pip install numpy==1.10.4
# pip install pandas==0.23.1
# pip show numpy