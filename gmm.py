# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 15:38:08 2017

@author: shana
"""

import numpy as np

from sklearn.datasets import make_classification
from sklearn.mixture import GMM

from fun_StdFilter import getFunctional
import scipy
from sklearn.datasets import load_files
import jieba
import gensim
from gensim import corpora, models
import joblib
import numpy as np
import os.path

from sklearn.svm import LinearSVC
from sklearn.metrics import recall_score

train_X=[]
train_Y=[]

def getw2v(model_w2v,jieout):
    cn_w2v=[]
    for art in range(len(jieout)):
        this_score=np.zeros(shape=(size_w2,1)).flatten()
    
        A=[]
        for words in jieout[art]:
    
            A.append(model_w2v[words])
            
        cn_w2v.append(A)
    return cn_w2v
###############################################################################
def jiebacut(alltext):
    jieout=[]
    print('cutting')
    for i in range(0,len(alltext)):    
        tmp=[]
        this=alltext[i]
        this = jieba.cut(this, cut_all=False)
        for word in this:
            tmp.append(word)
        jieout.append(tmp)
    return jieout
###############################################################################
def eli(jieout):    
    punc='，。！？：／」「()（）％、１２３４５６７８９０0123456789'+' '
#    punc = punc.decode("utf-8")
    stop_word=set(['，','。','！','？','：','／','〔','．','；', '．','〕'])
    stop_words=set(punc)|stop_word
    final=[]
    print('clean')
    for j in range(0,len(jieout)):
        filtered_sentence=[]
        for ind,w in enumerate(jieout[j]):
            wrong=0
            for in_w in w:
                if in_w in  stop_words:
                    wrong=1
                    break
            if wrong==0:    
                filtered_sentence.append(w)
        final.append(filtered_sentence)
    return final
###############################################################################
def get_fisher_list(train_data):
    testX=[]
    testY=[]
    
    
    for chosen in range(0, 67, 1):
        testX = train_data[chosen:chosen+1]
        testY = train_Y[chosen:chosen+1]
        if(chosen == 0 or chosen == 66):
            if(chosen == 0):
                trainX = train_data[chosen+1:67]
            if(chosen == 66):
                trainX = train_data[0:chosen]
        else:
            nptx1=np.array(train_data[0:chosen])        
            nptx2=np.array(train_data[chosen+1:67])
            nptx12=np.concatenate((nptx1,nptx2),axis=0)
            trainX = nptx12
        #trainY=np.concatenate((np.array(train_Y[0:chosen]),np.array(train_Y[chosen+1:67])),axis=0)
        gmm = GMM(n_components=2, covariance_type='diag')
        gmm.fit(trainX)
        fv = fisher_vector(testX, gmm)
        fisher_list.append(fv)
###############################################################################        
def cross_validation(train_data, c, classiflication = ''):
    testX=[]
    testY=[]
    
    ACU_sum = 0
    
    predict=[]
    for chosen in range(0, 67, 1):
        testX = train_data[chosen:chosen+1]
        testY = train_Y[chosen:chosen+1]
        if(chosen == 0 or chosen == 66):
            if(chosen == 0):
                trainX = train_data[chosen+1:67]
            if(chosen == 66):
                trainX = train_data[0:chosen]
        else:
            nptx1=np.array(train_data[0:chosen])        
            nptx2=np.array(train_data[chosen+1:67])
            nptx12=np.concatenate((nptx1,nptx2),axis=0)
            trainX = nptx12
        trainY=np.concatenate((np.array(train_Y[0:chosen]),np.array(train_Y[chosen+1:67])),axis=0)
        
        from sklearn import feature_selection
        best_C= c #10 # 10 5 1 0.5 0.1 0.01
        best_percent=0.7 #feature留幾趴
        machine=LinearSVC(C=best_C, penalty="l1", dual=False,class_weight = 'balanced');
        fs=feature_selection.SelectPercentile(feature_selection.f_classif, percentile = best_percent).fit(trainX, trainY)            
        #trainX=fs.transform(trainX)
        
        machine.fit(trainX, trainY) #讓machine找線性規劃
        
        #testX =fs.transform(testX) 
        y_predicted = machine.predict(testX)
        ACU=np.mean(y_predicted == testY)
        predict.append(y_predicted)
        ACU_sum = ACU_sum + ACU
    print('########################')        
    print(classiflication)
    print('recall score:', recall_score(train_Y, predict, average='macro'))
    print('acu:',ACU_sum/67)
    a.append(ACU_sum/67)
###############################################################################
def fisher_vector(xx, gmm):
    """Computes the Fisher vector on a set of descriptors.
    Parameters
    ----------
    xx: array_like, shape (N, D) or (D, )
        The set of descriptors
    gmm: instance of sklearn mixture.GMM object
        Gauassian mixture model of the descriptors.
    Returns
    -------