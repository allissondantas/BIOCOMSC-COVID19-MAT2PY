from informe import generate_data
from crear_excel_brasil import run_crear_excel_brasil
from crear_excel_recife import run_crear_excel_recife
from progress.bar import IncrementalBar
from datetime import datetime
import pandas as pd
import numpy as np
import sys
import time

"""
For ALL      Usage example python3 crear_informe.py  data/Data_Spain_v2.xlsx 
For Brasil   Usage example python3 crear_informe.py  brasil 
"""


def main():
    try:
        filename = sys.argv[1]
        brasil = False
    except:
        print("\n\nFatal error!!!!!!!!!!\n\n",
              "For ALL      Usage example python3 crear_informe.py  data/Data_Spain_v2.xlsx\n",
              "For Brasil   Usage example python3 crear_informe.py  brasil")
        sys.exit()

    if filename == 'brasil' or filename == 'recife':
        if filename == 'brasil':
            try:
                run_crear_excel_brasil()
                filename = 'data/Data_Brasil.xlsx'
                filename_population = 'data/pop_Brasil_v2.xlsx'

            except AttributeError:
                print('Error! Not found file or could not download!')

        elif filename == 'recife':
            try:
                run_crear_excel_recife()
                filename = 'data/cases-recife.xlsx'
                filename_population = 'data/pop_recife.xlsx'

            except AttributeError:
                print('Error! Not found file or could not download!')

        DATA = pd.read_excel(filename, sheet_name='Cases')
        DEATHS = pd.read_excel(filename, sheet_name='Deaths')
        POP = pd.read_excel(filename_population)
        DIA = pd.to_datetime(DATA['date']).dt.strftime('%d/%m/%Y')
        brasil = True
    else:
        DATA = pd.read_excel(filename, sheet_name='Cases')
        DEATHS = pd.read_excel(filename, sheet_name='Deaths')
        POP = pd.read_excel(filename, sheet_name='Population')
        DIA = pd.to_datetime(DATA['Dia']).dt.strftime('%d/%m/%Y')

    region = POP.columns
    Population = POP.loc[0]

    A = np.zeros((len(DIA), 1))

    for i in range(len(DIA)):
        d = datetime.strptime(DIA[i], '%d/%m/%Y').date()
        dateNum = d.toordinal()
        A[i] = dateNum

    bar = IncrementalBar('Processing', max=len(region))
    start_time = time.time()
    for ID in range(len(region)):
        data = DATA[region[ID]]
        data = data.to_numpy()
        deaths = DEATHS[region[ID]]
        deaths = deaths.to_numpy()
        generate_data(A, data, deaths, region[ID], Population[ID], brasil)
        bar.next()

    bar.finish()
    end_time = time.time()
    print(end_time - start_time)


if __name__ == "__main__":
    sys.argv.append('brasil')
    #sys.argv.append('recife')
    # sys.argv.append('covid19/data/Data_Spain_v2.xlsx')
    main()
