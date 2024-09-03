import pickle
import streamlit as st
import pandas as pd
import mysql.connector
from mysql.connector import Error

# Carregando a Máquina Preditiva
with open('maquina_preditiva_doenca_cardiaca.pkl', 'rb') as file:
    maquina_preditiva_doenca_cardiaca = pickle.load(file)

# Função para inserir a predição no banco de dados
def conectar_bd(dados, resultado):
    try:
        conexao = mysql.connector.connect(
            host='localhost',
            user="root",  
            password="1234",
            database='previsoes_cardio',
            port=3306     
        )
        cursor = conexao.cursor()
        
        sql = """
        INSERT INTO predições (Idade, Cholesterol, FrequenciaCardiaca, ConsumoAlcool,
                               NivelEstresse, IMC, Triglicerides, AtividadeFisica, Resultado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (*dados, resultado))
        
        conexao.commit()
        cursor.close()
        conexao.close()
    except Error as err:
        print(f"Erro: {err}")

# Função de predição usando os dados inseridos pelo usuário
def prediction(Idade, Cholesterol, FrequenciaCardiaca, ConsumoAlcool,
               NivelEstresse, IMC, Triglicerides, AtividadeFisica):   
    ConsumoAlcool = 0 if ConsumoAlcool == "Não" else 1

    # Criando um DataFrame para passar para o modelo
    parametro_df = pd.DataFrame([[
        Idade, Cholesterol, FrequenciaCardiaca, ConsumoAlcool,
        NivelEstresse, IMC, Triglicerides, AtividadeFisica
    ]], columns=[
        'Idade', 'Cholesterol', 'FrequenciaCardiaca', 'ConsumoAlcool',
        'NivelEstresse', 'IMC', 'Triglicerides', 'AtividadeFisica'
    ])

    # Fazendo a Predição
    fazendo_previsao = maquina_preditiva_doenca_cardiaca.predict(parametro_df)
   
    return int(fazendo_previsao[0])

# Função principal da aplicação
def main():  
    html_temp = """ 
    <div style ="background-color:blue;padding:13px"> 
    <h1 style ="color:white;text-align:center;">PROJETO PARA PREVER DOENÇA CARDÍACA</h1> 
    <h2 style ="color:white;text-align:center;">SISTEMA PARA PREVER DOENÇA CARDÍACA - by João Coimbra </h2> 
    </div> 
    """
    st.markdown(html_temp, unsafe_allow_html=True) 

    Idade = st.number_input("Idade") 
    Cholesterol = st.number_input("Cholesterol")
    FrequenciaCardiaca = st.number_input("Frequência Cardíaca")
    NivelEstresse = st.number_input("Nível De Estresse")
    ConsumoAlcool = st.selectbox('Consumo De Álcool', ("Sim", "Não"))
    IMC = st.number_input("Índice De Massa Corporal") 
    Triglicerides = st.number_input("Triglicerides") 
    AtividadeFisica = st.number_input("Horas De Atividade Física Semanais") 
 
    if st.button("Verificar"): 
        result = prediction(Idade, Cholesterol, FrequenciaCardiaca, ConsumoAlcool,
                            NivelEstresse, IMC, Triglicerides, AtividadeFisica) 
     
        if result == 0:
            st.success("Não possui risco de doença cardíaca")
        else:
            st.warning("Possui risco de doença cardíaca")

        dados = [Idade, Cholesterol, FrequenciaCardiaca, ConsumoAlcool,
                 NivelEstresse, IMC, Triglicerides, AtividadeFisica]
        conectar_bd(dados, result)

if __name__ == '__main__':
    main()
