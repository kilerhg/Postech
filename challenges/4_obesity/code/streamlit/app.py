import os

import streamlit as st
import pandas as pd
import numpy as np
import joblib


DICT_VALUE_OBESITY_TRANSLATION = {
    "Feminino": 0,
    "Masculino": 1,
    "Transporte público": "Public_Transportation",
    "Caminhada": "Walking",
    "Automóvel": "Automobile",
    "Motocicleta": "Motorbike",
    "Bicicleta": "Bike"
}

DICT_RESULT = {
    0: "Peso insuficiente",
    1: "Peso Ideal",
    2: "Sobrepeso Nível I",
    3: "Sobrepeso Nível II",
    4: "Obesidade Tipo I",
    5: "Obesidade Tipo II",
    6: "Obesidade Tipo III",   
}


DICT_FREQUENCY_FCVC = {
  'Nunca': 1,
  'Às vezes': 2,
  'Sempre': 3
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

DICT_GENDER = {
    'Male'
}

apptitle = 'Postech Obesity Predictor'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")


# header = st.container()
st.title('Obesity Predictor')
body = st.container()
with st.expander('Veja Mais'):
    extra = st.container()


def process_data_from_user(dict_values_user):
    dict_processed = {}

    dict_processed['mtrans_Automóvel'] = 0.0
    dict_processed['mtrans_Bicicleta'] = 0.0
    dict_processed['mtrans_Caminhada'] = 0.0
    dict_processed['mtrans_Motocicleta'] = 0.0
    dict_processed['mtrans_Transporte público'] = 0.0
    key_mtrans = f'mtrans_{dict_values_user['mtrans']}'
    if key_mtrans in dict_processed:
        dict_processed[key_mtrans] = 1.0
    else:
        print(f'not found: {key_mtrans}')

    dict_processed['gender'] = DICT_VALUE_OBESITY_TRANSLATION[dict_values_user['gender']]
    dict_processed['age'] = dict_values_user['age']
    dict_processed['height'] = dict_values_user['height']
    dict_processed['weight'] = dict_values_user['weight']
    dict_processed['family_history'] = dict_values_user['family_history']
    dict_processed['favc'] = dict_values_user['favc']
    dict_processed['fcvc'] = DICT_FREQUENCY_FCVC[dict_values_user['fcvc']]
    dict_processed['ncp'] = dict_values_user['ncp']
    dict_processed['caec'] = DICT_FREQUENCY_OBESITY[dict_values_user['caec']]
    dict_processed['smoke'] = dict_values_user['smoke']
    dict_processed['ch2o'] = dict_values_user['ch2o']
    dict_processed['scc'] = dict_values_user['scc']
    dict_processed['faf'] = dict_values_user['faf']
    dict_processed['tue'] = dict_values_user['tue']
    dict_processed['calc'] = DICT_FREQUENCY_OBESITY[dict_values_user['calc']]

    return dict_processed


## IMC, Quantidade de agua

## Sinais de alerta: QTD: Exercicio fisico, Quantidade Agua, IMC, Alimentos caloricos, Historico familiar.  

def calculate_bmi(dict_processed): # BMI == IMC
    weight = dict_processed['weight']
    height = dict_processed['height']
    
    bmi = round(weight/(height**2),2)
    return bmi


def calculate_water_intake(dict_processed):
    weight = dict_processed['weight']
    ideal_water_intake_lt = round(weight*0.033,2)
    return ideal_water_intake_lt


def calculate_personal_insights(dict_processed):

    dict_personal_insights = {}
    dict_personal_insights['bmi'] = calculate_bmi(dict_processed)
    dict_personal_insights['ideal_water_intake'] = calculate_water_intake(dict_processed)
    dict_personal_insights['suggestion'] = []

    if dict_processed['favc']:
        dict_personal_insights['suggestion'].append('Ingestão de alimentos altamente calóricos podem ter alto impacto na obesidade')
    if dict_personal_insights['ideal_water_intake'] > dict_processed['ch2o']:
        dict_personal_insights['suggestion'].append(f'Ingestão de Agua menor do que deveria para o seu peso - atual: {dict_processed['ch2o']}L - deveria ser: {dict_personal_insights['ideal_water_intake']}L')


    return dict_personal_insights


def generate_prediction():

    dict_processed = process_data_from_user(dict_values_user)

    dict_personal_insights = calculate_personal_insights(dict_processed)

    dir_path = os.path.dirname(os.path.realpath(__file__))

    full_path_joblib = os.path.join(dir_path, 'model.joblib')
    
    model = joblib.load(full_path_joblib)

    df = pd.DataFrame.from_records([dict_processed])

    result = model.predict(df)

    if result[0] in DICT_RESULT:
        predict = DICT_RESULT[result[0]]

    print(f'dict_personal_insights: {dict_personal_insights}')
    print(result, predict)

    body.write(f'A previsão é: {predict}')
    body.write(f'Seu IMC Atual é de: {dict_personal_insights["bmi"]}')
    body.write(f'Seu consumo ideal de agua é de: {dict_personal_insights["ideal_water_intake"]}')
    body.write(f'Insights:')
    for insight in dict_personal_insights['suggestion']:
        body.write(f'Atenção: {insight}')
    extra.write(df)


with st.sidebar.form(key='obesity_predictor'):

    dict_values_user = {}

    dict_values_user['gender'] = st.sidebar.selectbox(
            'Selecione um gênero',
            ['Masculino', 'Feminino']
        )

    dict_values_user['age'] = st.sidebar.number_input('Idade', placeholder=25, min_value=1, max_value=120, step=1, value=25)

    dict_values_user['height'] = st.sidebar.number_input('Altura (Metros)', placeholder=1.80, min_value=1.0, max_value=5.0, step=0.01, value=1.80)
    dict_values_user['weight'] = st.sidebar.number_input('Peso (KG)', placeholder=90, min_value=1, max_value=200, step=1, value=90)

    dict_values_user['family_history'] = st.sidebar.checkbox('Algum membro da família sofreu ou sofre de excesso de peso?')

    dict_values_user['favc'] = st.sidebar.checkbox('Você come alimentos altamente calóricos com frequência?')

    dict_values_user['fcvc'] = st.sidebar.selectbox(
            'Você costuma comer vegetais nas suas refeições?',
            ["Nunca", "Às vezes","Sempre"]
        )

    dict_values_user['ncp'] = st.sidebar.slider('Quantas refeições principais você faz diariamente?', 1.0, 8.0, 3.0, 1.0)

    dict_values_user['caec'] = st.sidebar.selectbox(
            'Você come alguma coisa entre as refeições?',
            ["Não", "Às vezes", "Frequentemente", "Sempre"]
        )

    dict_values_user['smoke'] = st.sidebar.checkbox('Você fuma?')

    dict_values_user['ch2o'] = st.sidebar.slider('Quantos Litros de água você bebe diariamente?', 1.0, 6.0, 2.0, 0.1)

    dict_values_user['scc'] = st.sidebar.checkbox('Você monitora as calorias que ingere diariamente?')

    dict_values_user['faf'] = st.sidebar.slider('Quantos dias da semana você pratica atividade física?', 0.0, 5.0, 2.0, 1.0)

    dict_values_user['tue'] = st.sidebar.slider('Quantas horas você usa dispositivos tecnológicos como celular, videogame, televisão, computador e outros?', 1.0, 8.0, 1.0, 0.5)

    dict_values_user['calc'] = st.sidebar.selectbox(
            'Com que frequência você bebe álcool?',
            ["Nunca", "Às vezes", "Frequentemente", "Sempre"]
        )

    dict_values_user['mtrans'] = st.sidebar.selectbox(
            'Qual meio de transporte você costuma usar?',
            ["Transporte público","Caminhada","Automóvel","Motocicleta","Bicicleta"]
        )

    st.sidebar.button('Predict', on_click=generate_prediction)