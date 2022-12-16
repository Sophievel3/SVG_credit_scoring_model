#Importer les modules:
import json

import requests
import streamlit as st
import streamlit.components.v1 as components

# -------------
#D. Ce que l'on veut mettre sur Streamlit.

#Je veux rentrer le Id du client et obtenir:
    #- Son Id, sa probabilité de défaut, son score et son statut.
    #- Ses feature importantes locales.
    #- Les feature importances globales.
    
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
        
        #Appel aux url de Flask.
        data_c= requests.get("http://192.168.43.52:81/app/scoring_cust/?SK_ID_CURR="+input_text).json()
        #data_c2= requests.get("http://192.168.43.52:81/app/feat_imp_local/?SK_ID_CURR=" + input_text)
        data_c3= requests.get("http://192.168.43.52:81/app/feat_imp_global").json()
        
        #Affichage du score du client.
        st.write(data_c)
        
        #Affichage des features importances globales.
        st.write(data_c3)

        #Affichage des features importances locales pour le client.
        components.iframe("http://192.168.43.52:81/app/feat_imp_local/?SK_ID_CURR=" + input_text, width=800, height=800, scrolling=True)

