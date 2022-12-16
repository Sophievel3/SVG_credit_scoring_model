#Importer les modules:
import pandas as pd
import numpy as np

from lime import lime_tabular

import json
import joblib
from flask import Flask, request, jsonify, render_template


import zipfile
import dill

# -------------
#D. Ce que l'on veut mettre sur flask.

#Je veux la base de données entière suite à tous ces traitements (train+test) pour avoir tous le clients.

#Je veux le meilleure modèle entraîné (il ne faut pas le ré-entraîner à chaque fois).

#Je veux le rajout de la fonction coût métier.

#Je veux obtenir le score final donné (Défaut:1, Sain:0), la probabilité associée et l'explication.

#Je veux les "Features importances locales" sauvegardées en "pickle" pour ne pas avoir à loader la baser de "training".

#Je veux le "explainer" de "LIME" sauvegardé en "pickle" pour ne pas avoir à loader la baser de "training".
# -------------


#D.1 Base de données entière suite à tous ces traînements.

zf=zipfile.ZipFile('Base_test.zip')
Base_complete=pd.read_csv(zf.open('Base_test.csv'), sep=',', low_memory=False)



#D.2 Meilleur modèle entraîné(Load le pickled model).
saved_model_from_pickle = joblib.load('model_pkl')



#D.3 Fonction coût métier.
def CM(row):
    if row > 0.091: sc=1
    else: sc=0
    return sc



#D.4 État du client (Défaut ou Non Défaut).
def Et(k):
    if k==1: etat='Default'
    else: etat='Non Default'
    return etat


#D.5 Features importances locales (Sauvegardées en "pickle").
with open('global_pkl', 'rb') as files:
    glob= dill.load(files)


#D.6 Partie 'Lime' (Explainer en "pickle" et Fonction auxiliaire 'explainer').

#"Explainer" de "LIME" sauvegardé en "pickle" (Load le pickled model).
with open('expl_pkl', 'rb') as files:
    explainer_pickle = dill.load(files)

#Fonction auxiliaire.
def explain(data_row, predict_fn):
    np.random.seed(16)
    return explainer_pickle.explain_instance(data_row, predict_fn,num_features=20)


#---------------------------------------------------------
#                        F L A S K
#---------------------------------------------------------
#Initions Flask.
app = Flask(__name__)

#Index Déployé en local sur: http://192.168.43.52:81/
@app.route("/")
def index():
    return render_template("home.html")
    #return "APP loaded, modèle et data loaded............"



#Liste des 'SK_ID_CURR'.
#Liste des ID déployée en local sur: http://192.168.43.52:81/app/id/
@app.route('/app/id/')
def ids_list():
    # Extraction des'SK_ID_CURR' dans Base_complete.
    customers_id_list = pd.Series(list(Base_complete['SK_ID_CURR']))
    # Conversion de la pd.Series a JSON.
    customers_id_list_json = json.loads(customers_id_list.to_json())
    #Retour de la  liste des ID.
    return jsonify({'List of IDs': customers_id_list_json})
 
    

# Sélection d'un client.
#Par exemple, la ligne du client ayant le 'SK_ID_CURR'= 165690 dans le dataset sera déployée en local dans:
#http://192.168.43.52:81/app/client/?SK_ID_CURR=165690
@app.route('/app/client/')  
def selected_cust_data():  
    #Parse demande http pour obtenir le client.
    selected_id_customer = int(request.args.get('SK_ID_CURR'))
    X_cust = Base_complete.loc[Base_complete['SK_ID_CURR']==selected_id_customer]
    #Conversion de la pd.Series à JSON.
    data_x_json = json.loads(X_cust.to_json())
    #Retour de la  ligne client.
    return jsonify({'Ligne client': data_x_json})



#Statut du client.
#Statut déployé en local sur: http://192.168.43.52:81/app/scoring_cust/?SK_ID_CURR=165690
@app.route('/app/scoring_cust/')
def scoring_cust():
    #Parse demande http pour obtenir le client.
    selected_id_customer = int(request.args.get('SK_ID_CURR'))
    #Obtention de la data du client.
    X_cust = Base_complete.loc[Base_complete['SK_ID_CURR']==selected_id_customer]
    #Probabilité de défaut associée au client.
    proba = saved_model_from_pickle.predict_proba(X_cust)[:, 1][0]
    proba_round=round(proba, 2)
    #Application de la fonction coût métier.
    score = CM(proba)
    #État du client:
    F = Et(score)    
    # Retour du score du client.
    return jsonify({'SK_ID_CURR': selected_id_customer,
                    'Probability': proba_round,
                    'score': score,
                    'Etat': F})



#Déploiement des features importance globale.
#Features importance globale déployée en local sur:
#http://192.168.43.52:81/app/feat_imp_global
@app.route('/app/feat_imp_global/')
def send_feat_imp():
    
    feat_imp_glb=glob

    # Conversion de la pd.Series en JSON.
    feat_imp_json = json.loads(feat_imp_glb.to_json())
    # Retour de la data comme un objet json.
    return jsonify({'10 Most important global features': feat_imp_json})




#Déploiement des features importance locale.
#Features importance globale déployée en local sur:
#http://192.168.43.52:81/app/feat_imp_local/?SK_ID_CURR=165690
@app.route('/app/feat_imp_local/')
def lime_results():
    exp = ""
    print("toto1")
    
    #Parse demande http pour obtenir le client.
    selected_id_customer = int(request.args.get('SK_ID_CURR'))
    print("toto2")
   
    #Obtention de l'index associé au client.
    r = Base_complete[Base_complete['SK_ID_CURR']==selected_id_customer].index[0]
    #s=str(r)
    print("toto3")
    
    #Calculs de l'explainer associée au client.
    exp = explain(Base_complete.iloc[r],saved_model_from_pickle.predict_proba)
    
    print("toto4")
    exp = exp.as_html()
    
    return render_template('index.html', exp=exp)
    
 

    
@app.route('/results/', methods=['POST'])
def render_results():
    selected_id_customer=request.form['SK_ID_CURR']
    return 'ID: '+ selected_id_customer
    

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port=81)
