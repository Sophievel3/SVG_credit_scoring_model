#Importer les modules:
import json

import requests
import streamlit as st
import streamlit.components.v1 as components

# -------------
#D. Ce que l'on veut mettre sur Streamlit.

#Je veux rentrer le Id du client et obtenir:
    #- Son Id, sa probabilité de défaut, son score et son statut.
    #- Ses features importances locales.
    #- Les features importances globales.
    
#Tout cela en appelant les URL de Flask.
# -------------



#---------------------------------------------------------
#                    S T R E A M L I T
#---------------------------------------------------------



# Construction du Dashboard.
title_text = "Analysis of a client's status"
subheader_text = 'Default or not Default'

st.markdown(f"<h2 style='text-align: center;'><b>{title_text}</b></h2>", unsafe_allow_html=True)
st.markdown(f"<h5 style='text-align: center;'>{subheader_text}</h5>", unsafe_allow_html=True)
st.text("")
input_text = st.text_input('Enter the ID of the client:', "")



if st.button("Explain Results"):
    with st.spinner('Calculating...'):
        
        
        #Affichage du score du client.
        components.iframe("https://svg-crsm-flask.herokuapp.com/app/id/")
        
        #Affichage des features importances globales.
        components.iframe("https://svg-crsm-flask.herokuapp.com/app/feat_imp_global/")

        #Affichage des features importances locales pour le client.
        components.iframe("https://svg-crsm-flask.herokuapp.com/app/id/", width=800, height=800, scrolling=True)

