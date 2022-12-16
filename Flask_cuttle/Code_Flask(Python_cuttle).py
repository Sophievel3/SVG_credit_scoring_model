
from flask import Flask
from flask import request
app = Flask(__name__)

#Importer les modules:

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
import colorama
from colorama import Fore
from colorama import Style
import os, sys
import matplotlib
from matplotlib import cm
from matplotlib.patches import Circle, Wedge, Rectangle
from math import log10
import gc
import time
from contextlib import contextmanager
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, f1_score, precision_score, recall_score 
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from xgboost import XGBClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import classification_report

from imblearn.over_sampling import SMOTE 
from imblearn.over_sampling import SMOTENC

import scipy.stats as stats
import shap
import lime
from lime import lime_tabular
import random

import statsmodels.api as sm
from statsmodels.formula.api import ols


import ast
import scipy.stats as stats
import re
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import fbeta_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import confusion_matrix
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn import metrics
from sklearn.inspection import permutation_importance
import math
from datetime import datetime
from datetime import timedelta, date

from functools import reduce
from sklearn.preprocessing import MinMaxScaler

import pickle

#----------------------------------------------------------------------------------------------------------------------
#D. Ce que l'on veut mettre sur flask.

#Je veux la base de données entière suite à tous ces traitements (train+test) pour avoir tous le clients.
#Je veux les bases qui ont servi pour entraîner et tester le modèle. (Celles ré-équilibrées avec SMOTE).
#Je veux le meilleure modèle entraîné (il ne faut pas le ré-entraîner à chaque fois).
#Je veux le rajout de la fonction coût métier.
#Je veux le 'training_data'= 'X_train_req', pour pouvoir avoir la fonction 'explainer' de lime.
#Je veux obtenir le score final donné (Défaut:1, Sain:0), la probabilité associée et l'explication.

#D.1 Base de données entière suite à tous ces traînements.

Base_complete=pd.read_csv('Base_complete.csv', sep=',', low_memory=False) 

#D.2 Bases qui ont servi pour entraîner et tester le modèle. (Celles ré-équilibrées avec SMOTE)

X_train_req_saved=pd.read_csv('X_train_req_saved.csv', sep=',', low_memory=False)

X_test_req_saved=pd.read_csv('X_test_req_saved.csv', sep=',', low_memory=False)

y_train_req_saved=pd.read_csv('y_train_req_saved.csv', sep=',', low_memory=False)

y_test_req_saved=pd.read_csv('y_test_req_saved.csv', sep=',', low_memory=False)

#D.3 Meilleur modèle entraîné.

# Load le pickled model
with open('model_pkl' , 'rb') as f:
     saved_model_from_pickle= pickle.load(f)

@app.route('/api/score', methods=['GET'])
def get__api_score():
    #cuttle-environment-set-config score route=/api/score methods=POST response=output2
    saved_model_from_pickle.predict(Base_complete)
    return output2

Proba= pd.DataFrame({'SK_ID_CURR': Base_complete.SK_ID_CURR, 'Proba': saved_model_from_pickle.predict_proba(Base_complete)[:,1]})
Proba

#D.4 Rajout de la fonction coût métier.

defaut_CM = []

for row in Proba['Proba']:
    if row > 0.091 :defaut_CM.append(1)
    else:defaut_CM.append(0)

Proba['Predict_Defaut_Avec_CM']=defaut_CM
Proba

#D.5 La partie 'Lime' ('explainer' et 'trainind_data')

explainer = lime_tabular.LimeTabularExplainer(training_data= X_train_req_saved.values, feature_names=X_train_req_saved.columns, class_names=['Not Default','Default'], mode='classification')

#ATTENTION:
#Les explications des 'features importances' avec LIME sont le résultat d'un processus d'échantillonnage aléatoire, 
#on ne dois donc pas obtenir exactement la même explication à chaque fois, à moins qu'on définisse le 'random seed' 
#avant chaque exécution de l''explain_instance'.

#Faisons une fonction qui le fasse:

def explain(data_row, predict_fn):
    np.random.seed(16)
    return explainer.explain_instance(data_row, predict_fn)

#D.6 Obtention des résultats.

n = float(input('What is your SK_ID_CURR?'))
s=Base_complete[Base_complete['SK_ID_CURR']==n].index[0]
status=Proba.loc[s, 'Predict_Defaut_Avec_CM']
if status==1:
    stat='Default'
else: 
    stat='Not Default'

probability=Proba.loc[s, 'Proba']
#exp_s=explain(Base_complete.iloc[s],saved_model_from_pickle.predict_proba)

o1=stat
o2=probability

output1=str(o1) 
output2=str(o2) 
#exp_s.show_in_notebook(show_table=True) 

#print("Status:", output1)
print("Probability:", output2)











if __name__ == '__main__':
    app.run()