import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from crear_excel_brasil import run_crear_excel_brasil
from crear_excel_recife import run_crear_excel_recife
from pandas import ExcelWriter

import plotly.graph_objects as go


def gradient_image(ax, extent, direction=0.3, cmap_range=(0, 1), **kwargs):
    """
    Draw a gradient image based on a colormap.

    Parameters
    ----------
    ax : Axes
        The axes to draw on.
    extent
        The extent of the image as (xmin, xmax, ymin, ymax).
        By default, this is in Axes coordinates but may be
        changed using the *transform* kwarg.
    direction : float
        The direction of the gradient. This is a number in
        range 0 (=vertical) to 1 (=horizontal).
    cmap_range : float, float
        The fraction (cmin, cmax) of the colormap that should be
        used for the gradient, where the complete colormap is (0, 1).
    **kwargs
        Other parameters are passed on to `.Axes.imshow()`.
        In particular useful is *cmap*.
    """
    phi = direction * np.pi / 2
    v = np.array([np.cos(phi), np.sin(phi)])
    X = np.array([[v @ [1, 0], v @ [1, 1]],
                  [v @ [0, 0], v @ [0, 1]]])
    a, b = cmap_range
    X = a + (b - a) / X.max() * X
    im = ax.imshow(X, extent=extent, alpha=0.45, interpolation='bicubic',
                   vmin=0, vmax=1, **kwargs)
    return im


def main():
    try:
        filename = sys.argv[1]
        deaths = sys.argv[2]
    except:
        print('Error! Usage: python3 risk_diagrams.py brasil')
        sys.exit()

    if filename == 'brasil' or filename == 'recife':
        brasil = True
        pt = True

        dataTable = []
        

        if filename == 'brasil' and deaths == 'False':
            try:
                run_crear_excel_brasil()
                filename = 'data/Data_Brasil.xlsx'
                filename_population = 'data/pop_Brasil_v3.xlsx'
                sheet_name = 'Cases'
            except AttributeError:
                print('Error! Not found file or could not download!')
        elif filename == 'brasil' and deaths == 'True':
            try:
                run_crear_excel_brasil()
                filename = 'data/Data_Brasil.xlsx'
                filename_population = 'data/pop_Brasil_v3.xlsx'
                sheet_name = 'Deaths'

            except AttributeError:
                print('Error! Not found file or could not download!')
        elif filename == 'recife':
            try:
                run_crear_excel_recife()
                filename = 'data/cases-recife.xlsx'
                filename_population = 'data/pop_recife.xlsx'
                sheet_name = 'Cases'

            except AttributeError:
                print('Error! Not found file or could not download!')

        data = pd.read_excel(filename, sheet_name= sheet_name)
        population = pd.read_excel(filename_population)
        dia = pd.to_datetime(data['date']).dt.strftime('%d/%m/%Y')
        dia = dia.to_numpy()
        region = population.columns

        if sheet_name == 'Cases':
            cases_deaths = 'casos'
            ataque_densidade = 'Taxa de ataque'
        else:
            cases_deaths = 'óbitos'
            ataque_densidade = 'Densidade de óbitos'

        for ID in range(len(region)):
            cumulative_cases = data[region[ID]]  
            cumulative_cases = cumulative_cases.to_numpy()
            new_cases = np.zeros((len(cumulative_cases)), dtype=np.int)
            for i in range(len(cumulative_cases)):
                if i != 0: new_cases[i] = cumulative_cases[i] - cumulative_cases[i - 1]

            p = np.zeros((len(new_cases)), dtype=np.float)
            for i in range(7, len(new_cases)):
                div = 0
                aux = new_cases[i - 5] + new_cases[i - 6] + new_cases[i - 7]
                if aux == 0:
                    div = 1
                else:
                    div = aux
                p[i] = min((new_cases[i] + new_cases[i - 1] + new_cases[i - 2]) / div, 4)

            p_seven = np.zeros((len(new_cases)), dtype=np.float)
            n_14_days = np.zeros((len(new_cases)), dtype=np.float)
            a_14_days = np.zeros((len(new_cases)), dtype=np.float)
            risk = np.zeros((len(new_cases)), dtype=np.float)
            risk_per_10 = np.zeros((len(new_cases)), dtype=np.float)
            for i in range(13, len(new_cases)):
                p_seven[i] = np.average(p[i - 6:i + 1])
                n_14_days[i] = np.sum(new_cases[i - 13: i + 1])
                pop = population[region[ID]] 
                a_14_days[i] = n_14_days[i] / pop * 100000
                risk[i] = n_14_days[i] * p_seven[i]
                risk_per_10[i] = a_14_days[i] * p_seven[i]
            first_day = dia[13]
            last_day = dia[len(dia) - 1]
            first_day = first_day.replace('/', '-')
            last_day = last_day.replace('/', '-')
            if brasil and not pt:
                save_path = 'reports_pdf/brasil/risk/' + last_day + '-' + region[ID] + '.pdf'
            elif brasil and pt:
                save_path = 'reports_pdf/brasil/risk-pt/'+sheet_name+'/'+ last_day + '-' + region[ID] + '.pdf'
            else:
                save_path = 'reports_pdf/risk/' + last_day + '-' + region[ID] + '.pdf'

            for i in a_14_days:
                    if sheet_name == 'Cases':
                        if i < 30:
                            c_min = 0.6
                            c_max = 0.89
                            green = [0, 'rgb(0, 255, 0)']
                            yellow = [0.9,'rgb(255, 255, 0)']
                            red = [1, 'rgb(255, 0, 0)']
                            red_ = [1, 'rgb(255, 0, 0)']

                        elif 30 > i < 100:
                            c_min = 0.65
                            c_max = 0.95
                            green = [0, 'rgb(0, 255, 0)']
                            yellow = [0.5,'rgb(255, 255, 0)']
                            red = [1, 'rgb(255, 0, 0)']
                            red_ = [1, 'rgb(255, 0, 0)']
                        elif 100 > i < 200:
                            c_min = 0.65
                            c_max = 1.1
                            green = [0, 'rgb(0, 255, 0)']
                            yellow = [0.3,'rgb(255, 255, 0)']
                            red = [1, 'rgb(255, 0, 0)']
                            red_ = [1, 'rgb(255, 0, 0)']
                        else:
                            c_min = 0.65
                            c_max = 1.3
                            green = [0, 'rgb(0, 255, 0)']
                            yellow = [0.2,'rgb(255, 255, 0)']
                            red = [0.5, 'rgb(255, 0, 0)']
                            red_ = [1, 'rgb(255, 0, 0)']
                    elif sheet_name == 'Deaths': 
                        if i < 10:
                            c_min = 0.6
                            c_max = 0.89
                            green = [0, 'rgb(0, 255, 0)']
                            yellow = [0.9,'rgb(255, 255, 0)']
                            red = [1, 'rgb(255, 0, 0)']
                            red_ = [1, 'rgb(255, 0, 0)']
                        elif i > 10:
                            c_min = 0.65
                            c_max = 1.3
                            green = [0, 'rgb(0, 255, 0)']
                            yellow = [0.2,'rgb(255, 255, 0)']
                            red = [0.5, 'rgb(255, 0, 0)']
                            red_ = [1, 'rgb(255, 0, 0)']

            with PdfPages(save_path) as pdf:
                fig1, ax1 = plt.subplots(sharex=True)
                ax1.plot(a_14_days, p_seven, 'ko--', fillstyle='none', linewidth=0.5)
                lim = ax1.get_xlim()
                x = np.ones(int(lim[1]))
                ax1.plot(x, 'k-', fillstyle='none', linewidth=0.5)
                ax1.set_ylim(0, 4)
                if brasil and pt:
                    ax1.set_ylabel('\u03C1 (média de '+ cases_deaths +' dos últimos 7 dias)')
                    ax1.set_xlabel(ataque_densidade +' por $10^5$ hab. (últimos 14 dias)')
                else:
                    ax1.set_ylabel('$\u03C1$ (mean of the last 7 days)')
                    ax1.set_xlabel('Attack rate per $10^5$ inh. (last 14 days)')
                ax1.annotate(first_day,
                             xy=(a_14_days[13], p_seven[13]), xycoords='data',
                             xytext=(len(x) - abs(len(x) / 2), 3), textcoords='data',
                             arrowprops=dict(arrowstyle="->",
                                             connectionstyle="arc3", linewidth=0.4),
                             )
                ax1.annotate(last_day,
                             xy=(a_14_days[len(a_14_days) - 1], p_seven[len(p_seven) - 1]), xycoords='data',
                             xytext=(len(x) - abs(len(x) / 3), 3.5), textcoords='data',
                             arrowprops=dict(arrowstyle="->",
                                             connectionstyle="arc3", linewidth=0.4),
                             )
                 
                
                
                if brasil:
                    bra_title = region[ID] + ' - Brasil'
                    plt.title(bra_title)
                else:
                    plt.title(region[ID])
                color_map = plt.cm.hsv
                cmap = color_map.reversed()
               
                gradient_image(ax1, direction=0.6, extent=(0, 1, 0, 1), transform=ax1.transAxes,
                               cmap=cmap, cmap_range=(c_min, c_max))
               
                
                
                if region[ID] == "Pernambuco" or sys.argv[1] == 'recife':
                   
                    plt.subplots_adjust(bottom=0.2)
                    text_annotate = (
                        "*A zona vermelha representa alto risco de infecção, enquanto a zona verde representa baixo risco.\n Valores calculados baseados na incidência diária de "+ cases_deaths +" e população. "
                        "IRRD/PE. \n Fonte: SES-PE. Dados atualizados em "+ str(last_day) +".")
                    
                    plt.text(0, -1, text_annotate, fontsize=7, wrap=True)
                ax1.set_aspect('auto')
                

                #plt.show()
                #break

                if brasil and pt:
                    save_path_img = 'reports_pdf/brasil/risk-pt/'+sheet_name+'/'+ last_day + '-' + region[ID] + '.png'
                    plt.savefig(save_path_img, bbox_inches='tight', dpi=300)

                    siglasEstados = ["AC", "AL", "AP", "AM", "BA", "CE",
                    "DF", "ES", "GO", "MA", "MT", "MS",
                    "MG", "PA", "PB", "PR", "PE", "PI", "RJ",
                    "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO", "TOTAL"]

                    save_path_img_site = 'reports_pdf/brasil/risk-pt/'+sheet_name+'/IRRD/'+ siglasEstados[ID] + '.png'
                    plt.savefig(save_path_img_site, bbox_inches='tight', dpi=300)
                try:
                    pdf.savefig(fig1)
                    plt.close('all')
                    print(
                        "\n\nPrediction for the region of " + region[
                            ID] + " performed successfully!\nPath:" + save_path)
                except:
                    print("An exception occurred")
            
            dataTable.append([region[ID], cumulative_cases[len(cumulative_cases) - 1], new_cases[len(new_cases) - 1], p[len(p) - 1], p_seven[len(p_seven)  - 1], n_14_days[len(n_14_days) - 1], a_14_days[len(a_14_days) - 1], risk[len(risk) - 1], risk_per_10[len(risk_per_10) - 1]])    
            #break

    df = pd.DataFrame(dataTable, columns=['State', 'Cumulative cases', 'New cases', 'ρ', 'ρ7', 'New cases last 14 days (N14)', 'New cases last 14 days per 105 inhabitants (A14)', 'Risk (N14*ρ7)',  'Risk per 10^5 (A14*ρ7)' ])       
        
    with ExcelWriter('reports_pdf/brasil/risk-pt/'+sheet_name+'/IRRD/BRASIL.xlsx') as writer:
        df.to_excel(writer, sheet_name='Alt_Urgell')

            

if __name__ == "__main__":
    sys.argv.append('brasil')
    #sys.argv.append('recife')
    sys.argv.append('False') # True -> Deaths False -> Cases
    main()
