import pandas as pd
from pandas import ExcelWriter
import sys

pathToBrasil = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-cities-time.csv"
#pathToBrasil = "data/cases-brazil-cities-time.csv"


def run_crear_excel_brasil_para():
    try:
        dados = pd.read_csv(pathToBrasil)
        print('Data obtained from: ', pathToBrasil)
        dados_semTotal = dados[dados['state'] != 'TOTAL']
    except:
        print('Error! can\'t load data from web')
        sys.exit()
    dados_para = dados_semTotal[dados_semTotal['state'] == 'PA']
    dados_para.set_index('date', 'state', inplace=True)
    unique_dates = dados_para.index.get_level_values('date').unique()
    dados_para['city'] = dados_para['city'].str.replace(u"/PA", "")
    unique_city = dados_para['city'].unique()

    dfByTotalCases = dataFramePorColuna('totalCases', unique_dates, unique_city, dados_para)
    
    #dfByTotalCases.columns = nameEstados
    #print(dfByTotalCases)
    with ExcelWriter('data/cases-para.xlsx') as writer:

        dfByTotalCases.to_excel(writer, sheet_name='Cases')

def dataFramePorColuna(coluna, unique_dates, siglasEstados, dados_semTotal):
    
    resul = pd.DataFrame(index=unique_dates, columns=siglasEstados)

    for city in siglasEstados:
        test = dados_semTotal.query('city == @city ')
        resul[city] = test[coluna]

    resul.fillna(0, inplace=True)
    resul['TOTAL'] = resul.sum(axis=1)
    return resul

#run_crear_excel_brasil_para()