import streamlit as st
import pandas as pd
import numpy as np

import random


DICT_VALUE_OBESITY_TRANSLATION = {
    "Feminino": "Female",
    "Masculino": "Male",
    "Transporte público": "Public_Transportation",
    "Caminhada": "Walking",
    "Automóvel": "Automobile",
    "Motocicleta": "Motorbike",
    "Bicicleta": "Bike"
}

DICT_RESULT = {
    "Overweight_Level_I": "Sobrepeso Nível I",
    "Overweight_Level_II": "Sobrepeso Nível II",
    "Obesity_Type_I": "Obesidade Tipo I",
    "Obesity_Type_II": "Obesidade Tipo II",
    "Obesity_Type_III": "Obesidade Tipo III",
    "Insufficient_Weight": "Peso insuficiente"
}

DICT_FREQUENCY_OBESITY = {
  'Não': 0,
  'Nunca': 0,
  'Às vezes': 1,
  'Frequentemente': 2,
  'Sempre': 3
}

DICT_YES_NO_TO_BOOL = {
  'Sim': True,
  'Não': False
}

apptitle = 'Postech Obesity Predictor'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

st.title('Obesity Predictor')

def process_data_from_user(dict_values_user):
    dict_processed = {}

    dict_processed['gender'] = DICT_VALUE_OBESITY_TRANSLATION[dict_values_user['gender']]
    dict_processed['age'] = dict_values_user['age']
    dict_processed['height'] = dict_values_user['height']
    dict_processed['weight'] = dict_values_user['weight']
    dict_processed['family_history'] = dict_values_user['family_history']
    dict_processed['favc'] = dict_values_user['favc']
    dict_processed['fcvc'] = dict_values_user['fcvc']
    dict_processed['ncp'] = dict_values_user['ncp']
    dict_processed['caec'] = DICT_FREQUENCY_OBESITY[dict_values_user['caec']]
    dict_processed['smoke'] = dict_values_user['smoke']
    dict_processed['ch2o'] = dict_values_user['ch2o']
    dict_processed['scc'] = dict_values_user['scc']
    dict_processed['faf'] = dict_values_user['faf']
    dict_processed['tue'] = dict_values_user['tue']
    dict_processed['calc'] = DICT_FREQUENCY_OBESITY[dict_values_user['calc']]
    dict_processed['mtrans'] = DICT_VALUE_OBESITY_TRANSLATION[dict_values_user['mtrans']]

    return dict_processed


def generate_prediction():

    dict_processed = process_data_from_user(dict_values_user)
    
    print(dict_processed)
    
    predict = random.choice(list(DICT_RESULT.values()))
    
    print(f'A previsão é: {predict}')

    st.write(f'A previsão é: {predict}')


with st.sidebar.form(key='obesity_predictor'):

    dict_values_user = {}

    dict_values_user['gender'] = st.sidebar.selectbox(
            'Selecione um gênero',
            ['Masculino', 'Feminino']
        )

    dict_values_user['age'] = st.sidebar.number_input('Idade', placeholder=25, min_value=1, max_value=120, step=1)

    dict_values_user['height'] = st.sidebar.number_input('Altura (Metros)', placeholder=1.80, min_value=0.0, max_value=5.0, step=0.01)
    dict_values_user['weight'] = st.sidebar.number_input('Peso (KG)', placeholder=90, min_value=0, max_value=200, step=1)

    dict_values_user['family_history'] = st.sidebar.checkbox('Algum membro da família sofreu ou sofre de excesso de peso?')

    dict_values_user['favc'] = st.sidebar.checkbox('Você come alimentos altamente calóricos com frequência?')

    dict_values_user['fcvc'] = st.sidebar.slider('Você costuma comer vegetais nas suas refeições?', 1.0, 3.0, 1.0, 0.1)

    dict_values_user['ncp'] = st.sidebar.slider('Quantas refeições principais você faz diariamente?', 1.0, 4.0, 1.0, 0.1)

    dict_values_user['caec'] = st.sidebar.selectbox(
            'Você come alguma coisa entre as refeições?',
            ["Não", "Às vezes", "Frequentemente", "Sempre"]
        )

    dict_values_user['smoke'] = st.sidebar.checkbox('Você fuma?')

    dict_values_user['ch2o'] = st.sidebar.slider('Quanta água você bebe diariamente?', 1.0, 3.0, 1.0, 0.1)

    dict_values_user['scc'] = st.sidebar.checkbox('Você monitora as calorias que ingere diariamente?')

    dict_values_user['faf'] = st.sidebar.slider('Com que frequência você pratica atividade física?', 1.0, 3.0, 1.0, 0.1)

    dict_values_user['tue'] = st.sidebar.slider('Quanto tempo você usa dispositivos tecnológicos como celular, videogame, televisão, computador e outros?', 1.0, 2.0, 1.0, 0.1)

    dict_values_user['calc'] = st.sidebar.selectbox(
            'Com que frequência você bebe álcool?',
            ["Nunca", "Às vezes", "Frequentemente", "Sempre"]
        )

    dict_values_user['mtrans'] = st.sidebar.selectbox(
            'Qual meio de transporte você costuma usar?',
            ["Transporte público","Caminhada","Automóvel","Motocicleta","Bicicleta"]
        )

    st.sidebar.button('Predict', on_click=generate_prediction)

# with st.expander("See notes"):

#     st.markdown("""
# A Q-transform plot shows how a signal’s frequency changes with time.

#  * The x-axis shows time
#  * The y-axis shows frequency

# The color scale shows the amount of “energy” or “signal power” in each time-frequency pixel.

# A parameter called “Q” refers to the quality factor.  A higher quality factor corresponds to a larger number of cycles in each time-frequency pixel.  

# For gravitational-wave signals, binary black holes are most clear with lower Q values (Q = 5-20), where binary neutron star mergers work better with higher Q values (Q = 80 - 120).

# See also:

#  * [GWpy q-transform](https://gwpy.github.io/docs/latest/examples/timeseries/qscan/)
#  * [Reading Time-frequency plots](https://labcit.ligo.caltech.edu/~jkanner/aapt/web/math.html#tfplot)
#  * [Shourov Chatterji PhD Thesis](https://dspace.mit.edu/handle/1721.1/34388)
# """)