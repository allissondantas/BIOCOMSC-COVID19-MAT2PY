import pandas as pd
from pandas import ExcelWriter
import sys

pathToMalawi = "data/data-malawi.csv"


def run_crear_excel_malawi():
    try:
        data = pd.read_csv(pathToMalawi, sep=',')
        print('Data obtained from: ', pathToMalawi)
    except:
        print('Error! can\'t load data from web')
        sys.exit()

    data = data.rename(columns={'Date': 'date'})
    data = data.rename(columns={'District': 'district'})
    data = data.rename(columns={'Confirmed-total': 'totalcases'})
    data['date'] = pd.to_datetime(data['date']).dt.strftime("%Y-%m-%d") 
    data.set_index('date',  inplace=True)

    unique_dates = data.index.get_level_values('date').unique()
    unique_district = data['district'].unique()
    dfByTotalCases = dataFramePorColuna('totalcases', unique_dates, unique_district, data)

    with ExcelWriter('data/cases-malawi.xlsx') as writer:

        dfByTotalCases.to_excel(writer, sheet_name='Cases')

def dataFramePorColuna(coluna, unique_dates, unique_district, data):
    
    resul = pd.DataFrame(index=unique_dates, columns=unique_district)
    
    for district_ in unique_district:
        test = data.query('district == @district_')
        test = test[~test.index.duplicated()]
        resul[district_] = test[coluna]
   
    resul.fillna(0, inplace=True)
    resul['TOTAL'] = resul.sum(axis=1)
    
    return resul