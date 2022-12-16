SVG_credit_scoring_model
            
            
                         I M P L E M E N T A T I O N   D'U N   M O D E L E   D E   S C O R E.

<<Construire un modèle de scoring qui donnera une prédiction sur la probabilité de faillite d'un client de 
façon automatique>>.

On retrouve ici tous les codes pour:
- Permettre de visualiser le score et l’interprétation de ce score pour chaque client de façon intelligible 
- pour une personne non experte en data science.
- Permettre de visualiser des informations descriptives relatives à un client (via un système de filtre).
- Permettre de comparer les informations descriptives relatives à un client à l’ensemble des clients.

---------------------------------------------------------------------------------------------------------


INVENTAIRE DES FICHIERS PRESENTS:

1. Un dossier "templates"--> On y trouve le fichier "index.html" qui fut utilisé sur Flask pour afficher les résultats de LIME.

2. P7_Sofia_Velasco_1_Dashboard_Cloud --> Code utilisé pour faire le Dashboard sur Streamlit (version cloud). On utilise un code ".py" travaillé sur Spyder.

3. P7_Sofia_Velasco_1_Dashboard_Local --> Code utilisé pour faire le Dashboard sur Streamlit (version local). On utilise un code ".py" travaillé sur Spyder.

4. P7_Sofia_Velasco_1_Flask_Cloud --> Code utilisé pour passer le code de modélisation à Flask et l'uploader sur Heroku (version cloud). On utilise un code ".py" travaillé sur Spyder.

5. P7_Sofia_Velasco_1_Flask_Local --> Code utilisé pour passer le code de modélisation à Flask et le faire tourner en local (version local). On utilise un code ".py" travaillé sur Spyder.

6. P7_Sofia_Velasco_2_dossier_Code_Final --> Le code de modélisation (du prétraitement à la prédiction)

7. expl_pkl --> Le explainer résultant de l'analyse "LIME" de notre meilleur modèle.

8. global_pkl --> Les "Global Features Importances" de notre meilleur modèle.

9. model_pkl --> le meilleure modèle (LGBMClassifier), avec les meilleures hyperparamètres, entraîné et sauvegardé à l'aide du packaging "Pickle".



---------------------------------------------------------------------------------------------------------
Viennent ensuite, dans un dossier "Flask_cuttle", deux "essais" d'utilisation du packaging "cuttle" pour 
passer directement du notebook de Jupyter à Flask. Au final ce ne furent pas les solutions retenues car avec 
"cuttle" il est compliqué de traiter la partie des features importances locales obtenues avec LIME. Mais comme
c'est quand même intéressant voici les codes obtenus.

3. Code_Flask(cuttle_Jupyter) --> Code utilisé pour passer le code de modélisation fait sur Jupyter à 
                                 Flask, en utilisant le packaging "Cluttle" sur Jupyter.

4. Code_Flask(Python_cuttle) --> Code ".py" obtenu suite à l'utilisation de "Cuttle" 
                                                    (code+commandes sur le prompt d'Anaconda), qui quand 
                                                    on le lit avec Python nous donne la URL qui exécute 
                                                    notre code sur le port localhost.



---------------------------------------------------------------------------------------------------------
ATTENTION:

Compte tenue du fait que Heroku est devenu payant depuis le 28 novembre 2022 (500 euros le mois max selon 
le temps d'utilisation de leur serveur, mais on ne spécifie pas vraiment comment ils prennent en compte ce 
temps d'utilisation), le service gratuit étant limité à:

- une mémoire maximum utilisable du serveur de 512Mb et
- à l'exécution de taches qui prennent moins de 30s;



J'ai dû, dans la version du 'Dashboard cloud' (code: "P7_Sofia_Velasco_1_Dashboard_Cloud.py" et 
URL:https://sophievel3-svg-credit-p7-sofia-velasco-1-dashboard-cloud-49prj2.streamlit.app/):

- faire les tests sur une base de données bien réduite (que quelques lignes et uniquement de la base test, 
  afin d'éviter les erreurs de mémoire, erreur H12).
           --> Vous pouvez donc tester avec le ID: 100005 par exemple ou n'importe quel ID du fichier zippé 
               'base_test' disponible dans le repository 'SVG_credit_scoring_model_Flask'.


- lier le dashboard Streamlit, aux URL qui ne nécessitaient pas de chercher dans la base d'un client 
  spécifique. 
  En fait, même en réduisant énormément la base, cette tache prend plus de 30s à se faire sur leur serveur 
  et du coup elle génère un crash. Suite à en avoir discuté avec ma mentor, on a décidé donc de faire ainsi 
  dans le but de montrer que je sais bien lier un dashboard "Streamlit", à une app "Flask" mise dans le 
  cloud avec Heroku, comme il est demandé dans ce projet. Ce sachant bien sûr qur faisant tourner et l'app 
  Flask et le dashboard Streamlit en local, tout marche correctement et avec la base complète.
  (cf. Repository: 'SVG_credit_scoring_model_Dashboard_Local').


Ainsi dans ce repository vous trouverez tous les codes pour les versions "locale" et "cloud".