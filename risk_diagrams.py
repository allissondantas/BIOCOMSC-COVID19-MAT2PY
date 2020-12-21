import sys
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from crear_excel_brasil import run_crear_excel_brasil
from crear_excel_brasil_para import run_crear_excel_brasil_para
from crear_excel_recife import run_crear_excel_recife
from crear_excel_malawi import run_crear_excel_malawi
from crear_excel_by_ourworldindata import run_crear_excel_ourworldindata
from pandas import ExcelWriter
import colormap
import plotly.graph_objects as go   
from risk_animated import run_animation
from PIL import Image


matplotlib.use('tkagg')


def plotly_html(a_14_days, p_seven, dia, bra_title, save_path):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=a_14_days,
                             y=p_seven,
                             text=dia,
                             mode='lines+markers',
                             marker=dict(
                                 #color=a_14_days,
                                 color = 'rgba(255, 255, 255, 0.3)',
                                 showscale=False,
                                 size=10,
                                 line=dict(
                                     color='Black',
                                     width=0.8)),
                             line=dict(
                                 color="Black",
                                 width=0.5,
                                 dash="dot"),
                             ))
    fig.add_shape(type="line",
                  x0=1,
                  y0=1,
                  x1=max(a_14_days),
                  y1=1,
                  line=dict(
                      color="Black",
                      width=1,
                      dash="dot",
                  ))
   
    
    fig.update_layout(plot_bgcolor='rgb(255,255,255)',
                      title=bra_title,
                      width=1488,
                      height=1108,
                      xaxis_title='Taxa de ataque por 10^5 hab. (últimos 14 dias)',
                      yaxis_title='\u03C1 (média dos últimos 7 dias)',

                      )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', ticks="outside", tickwidth=2,
                     tickcolor='black', ticklen=0, mirror=True, automargin=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', ticks="outside", tickwidth=2,
                     tickcolor='black', ticklen=0, mirror=True, automargin=True)

    fig.write_html(save_path + 'html/' + bra_title + '.html')

def run_risk_diagrams(argv_1, deaths, file_others_cases, file_others_pop, radio_valor):

    if argv_1:
        last_days_time = 30
        brasil = False
        pt = False
        html = False
        last_days = False
        animation = False 

        if radio_valor == 1:
            last_days = True
        elif radio_valor == 2:
            html = True
        elif radio_valor == 3:
            animation = True
        else:
            pass


        dataTable = []
        dataTable_EPG = []
        
        if argv_1 == 'brasil' and deaths == 'False':
            try:
                run_crear_excel_brasil()
                filename = 'data/Data_Brasil.xlsx'
                filename_population = 'data/pop_Brasil_v3.xlsx'
                sheet_name = 'Cases'
            except AttributeError:
                print('Error! Not found file or could not download!')
        elif argv_1 == 'brasil' and deaths == 'True':
            try:
                run_crear_excel_brasil()
                filename = 'data/Data_Brasil.xlsx'
                filename_population = 'data/pop_Brasil_v3.xlsx'
                sheet_name = 'Deaths'

            except AttributeError:
                print('Error! Not found file or could not download!')
        elif argv_1 == 'recife':
            try:
                run_crear_excel_recife()
                filename = 'data/cases-recife.xlsx'
                filename_population = 'data/pop_recife_v1.xlsx'
                sheet_name = 'Cases'

            except AttributeError:
                print('Error! Not found file or could not download!')

        elif argv_1 == 'alagoas':
            try:
                brasil = True
                pt = True
                filename = 'data/cases-alagoas.xlsx'
                filename_population = 'data/pop_alagoas_v1.xlsx'
                sheet_name = 'Cases'

            except AttributeError:
                print('Error! Not found file or could not download!')

        elif argv_1 == 'para':
            try:
                run_crear_excel_brasil_para()
                filename = 'data/cases-para.xlsx'
                filename_population = 'data/pop_para_v1.xlsx'
                sheet_name = 'Cases'

            except AttributeError:
                print('Error! Not found file or could not download!')

        elif argv_1 == 'malawi' and deaths == 'False':
            try:
                run_crear_excel_malawi()
                filename = 'data/cases-malawi.xlsx'
                filename_population = 'data/pop_malawi_v1.xlsx'
                sheet_name = 'Cases'

            except AttributeError:
                print('Error! Not found file or could not download!')
        
        elif argv_1 == 'ourworldindata' and deaths == 'False':
            try:
                country = 'Canada'
                run_crear_excel_ourworldindata(country)
                filename = 'data/ourworldindata.xlsx'
                filename_population = 'data/pop_ourworldindata_v1.xlsx'
                sheet_name = 'Cases'

            except AttributeError:
                print('Error! Not found file or could not download!')

        elif argv_1 == 'others' and deaths == 'False':
            try:
                filename = file_others_cases
                filename_population = file_others_pop
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

            day13 = 13


            for i in range(day13, len(new_cases)):
                p_seven[i] = np.average(p[i - 6:i + 1])
                n_14_days[i] = np.sum(new_cases[i - day13: i + 1])
                pop = population[region[ID]] 
                a_14_days[i] = n_14_days[i] / pop * 100000
                risk[i] = n_14_days[i] * p_seven[i]
                risk_per_10[i] = a_14_days[i] * p_seven[i]
            
            first_day = dia[day13]
            last_day = dia[len(dia) - 1]
            first_day = first_day.replace('/', '-')
            last_day = last_day.replace('/', '-')
        
            #For last 15 days
            if last_days:
                a_14_days_solo = []
                day13 = len(a_14_days) - last_days_time
                first_day = dia[day13]
                for i in range(len(a_14_days)):
                    if i >= len(a_14_days) - last_days_time:
                        a_14_days_solo.append(a_14_days[i])
                    else:
                        a_14_days_solo.append(None)
            
            if brasil and pt:
                save_path = 'reports_pdf/brasil/risk-pt/'+sheet_name+'/'+ last_day + '-' + region[ID]
                save_path_xlsx = 'reports_pdf/brasil/risk-pt/'+sheet_name+'/'
            else:
                save_path = 'reports_pdf/brasil/risk-en/'+sheet_name+'/'+ last_day + '-' + region[ID]
                save_path_xlsx = 'reports_pdf/brasil/risk-en/'+sheet_name+'/'
           
            #with PdfPages(save_path + '.pdf') as pdf:
            fig1, ax1 = plt.subplots(sharex=True)
            if last_days: 
                ax1.plot(a_14_days,  p_seven, 'ko--', fillstyle='none', linewidth=0.5, color = (0,0,0,0.15))
                ax1.plot(a_14_days_solo,  p_seven, 'ko--', fillstyle='none', linewidth=0.5) #For last 15 days
                ax1.plot(a_14_days_solo[len(a_14_days_solo) - 1],  p_seven[len(p_seven) - 1], 'bo')
            else: 
                ax1.plot(a_14_days,  p_seven, 'ko--', fillstyle='none', linewidth=0.5)
                ax1.plot(a_14_days[len(a_14_days) - 1],  p_seven[len(p_seven) - 1], 'bo')
            lim = ax1.get_xlim()
            x = np.ones(int(lim[1]))
            ax1.plot(x, 'k--', fillstyle='none', linewidth=0.5)
            ax1.set_ylim(0, 4)
            ax1.set_xlim(0, int(lim[1]))

            if brasil and pt:
                #ax1.set_ylabel('\u03C1 (média de '+ cases_deaths +' dos últimos 7 dias)')
                ax1.set_ylabel('\u03C1 (média dos últimos 7 dias)')
                ax1.set_xlabel(ataque_densidade +' por $10^5$ hab. (últimos 14 dias)')
            else:
                ax1.set_ylabel('$\u03C1$ (mean of the last 7 days)')
                ax1.set_xlabel('Attack rate per $10^5$ inh. (last 14 days)')
            ax1.annotate(first_day,
                            xy=(a_14_days[day13], p_seven[day13]), xycoords='data',
                            xytext=(len(x) - abs(len(x) / 1.5), 2.7), textcoords='data',
                            arrowprops=dict(arrowstyle="->",
                                            connectionstyle="arc3", linewidth=0.4),
                            )
            ax1.annotate(last_day,
                            xy=(a_14_days[len(a_14_days) - 1], p_seven[len(p_seven) - 1]), xycoords='data',
                            xytext=(len(x) - abs(len(x) / 2), 3), textcoords='data',
                            arrowprops=dict(arrowstyle="->",
                                            connectionstyle="arc3", linewidth=0.4),
                            )

            if brasil:
                bra_title = region[ID] + ' - Brasil'
                plt.title(bra_title)
                plt.annotate(
                ' EPG > 100: Alto', xy=(len(x) - abs(len(x) / 3.5), 3.8), color=(0,0,0), 
                ha='left', va='center', fontsize='6', 
                bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))
                plt.annotate(
                " 70 < EPG < 100: Moderado-alto\n"
                " 30 < EPG < 70 : Moderado", xy=(len(x) - abs(len(x) / 3.5), 3.55), color=(0,0,0), 
                ha='left', va='center', fontsize='6', 
                bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))
                plt.annotate(
                ' EPG < 30: Baixo', xy=(len(x) - abs(len(x) / 3.5), 3.3), color=(0,0,0), 
                ha='left', va='center', fontsize='6', 
                bbox=dict(fc=(0, 0, 0, 0), lw=0, pad=2))

                plt.annotate(
                '  ', xy=(len(x) - abs(len(x) / 3.3), 3.8), color=(0,0,0), 
                ha='left', va='center', fontsize='6', 
                bbox=dict(fc=(1, 0, 0, .5), lw=0, pad=2))
                plt.annotate(
                "  \n", xy=(len(x) - abs(len(x) / 3.3), 3.55), color=(0,0,0), 
                ha='left', va='center', fontsize='6', 
                bbox=dict(fc=(1, 1, 0, .5), lw=0, pad=2))
                plt.annotate(
                '  ', xy=(len(x) - abs(len(x) / 3.3), 3.3), color=(0,0,0), 
                ha='left', va='center', fontsize='6', 
                bbox=dict(fc=(0, 1, 0, .5), lw=0, pad=2))
            else:
                bra_title = region[ID]
                plt.title(region[ID])
            
            rh = np.arange(0,int(lim[1]),1)
            ar = np.linspace(0,4,400)
            
            RH, AR = np.meshgrid(rh, ar)

            EPG = RH * AR

            for i in range(len(EPG)):
                for j in range(len(EPG[i])):
                    if EPG[i][j] > 100:
                        EPG[i][j] = 100
            c = colormap.Colormap()
            mycmap = c.cmap_linear('green(w3c)', 'yellow', 'red')
            ax1.pcolorfast([0, int(lim[1])], [0, 4],EPG, cmap=mycmap, alpha=0.6)


            if region[ID] == "Pernambuco" or argv_1 == 'recife':
                bra_title = region[ID] + ' - PE'
                plt.title(bra_title)
                brasil = True
                pt = True
                plt.subplots_adjust(bottom=0.2)
                text_annotate = (
                    "*A zona vermelha representa alto risco de infecção, enquanto a zona verde representa baixo risco.\n Valores calculados baseados na incidência diária de "+ cases_deaths +" e população. "
                    "IRRD/PE. \n Fonte: SES-PE. Dados atualizados em "+ str(last_day) +".")
                
                plt.text(0, -1, text_annotate, fontsize=7, wrap=False)

              
                
            
            ax1.set_aspect('auto')


            if(animation):
                run_animation(a_14_days, p_seven, int(lim[1]), bra_title, last_day, False)


            #plt.show()
            #break

            if brasil and pt:
                if last_days: 
                    save_path_img = 'reports_pdf/brasil/risk-pt/'+sheet_name+'/last15days/'+ last_day + '-' + region[ID] + '_last15days.png'
                    plt.savefig(save_path_img, bbox_inches='tight', dpi=300)
                else:
                    save_path_img = 'reports_pdf/brasil/risk-pt/'+sheet_name+'/'+ last_day + '-' + region[ID] + '.png'
                    plt.savefig(save_path_img, bbox_inches='tight', dpi=300)

                if argv_1 == 'brasil' and last_days == False:
                    siglasEstados = ["AC", "AL", "AP", "AM", "BA", "CE",
                    "DF", "ES", "GO", "MA", "MT", "MS",
                    "MG", "PA", "PB", "PR", "PE", "PI", "RJ",
                    "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO", "TOTAL"]

                    save_path_img_site = 'reports_pdf/brasil/risk-pt/'+sheet_name+'/IRRD/'+ siglasEstados[ID] + '.png'
                    plt.savefig(save_path_img_site, bbox_inches='tight', dpi=300)
                elif argv_1 == 'recife' and last_days == False:
                    save_path_img = 'reports_pdf/brasil/risk-pt/'+sheet_name+'/IRRD/PERNAMBUCO/'+ region[ID] + '.png'
                    plt.savefig(save_path_img, bbox_inches='tight', dpi=300)
            else:
                plt.savefig(save_path + '.png', bbox_inches='tight', dpi=300)

            #try:
                #pdf.savefig(fig1)
            plt.close('all')
            print(
                "\n\nPrediction for the region of " + region[
                        ID] + " performed successfully!\nPath:" + save_path +'.png')
            #except:
                #print("An exception occurred")
            if html: 
                plotly_html(a_14_days, p_seven, dia, bra_title, save_path_xlsx)

        
            dataTable.append([region[ID], cumulative_cases[len(cumulative_cases) - 1], new_cases[len(new_cases) - 1], p[len(p) - 1], p_seven[len(p_seven)  - 1], n_14_days[len(n_14_days) - 1], a_14_days[len(a_14_days) - 1], risk[len(risk) - 1], risk_per_10[len(risk_per_10) - 1]])    
            
            for i in range(len(dia)): dataTable_EPG.append([dia[i], region[ID], risk_per_10[i]])
    
    df = pd.DataFrame(dataTable, columns=['State', 'Cumulative cases', 'New cases', 'ρ', 'ρ7', 'New cases last 14 days (N14)', 'New cases last 14 days per 105 inhabitants (A14)', 'Risk (N14*ρ7)',  'Risk per 10^5 (A14*ρ7)' ])       
    df_EPG = pd.DataFrame(dataTable_EPG, columns=['DATE', 'CITY', 'EPG']) 

    with ExcelWriter(save_path_xlsx + last_day + '_'+ argv_1 + '_report.xlsx') as writer:
        df.to_excel(writer, sheet_name='Alt_Urgell')
    with ExcelWriter(save_path_xlsx + last_day + '_'+ argv_1 + '_report_EPG.xlsx') as writer:
        df_EPG.to_excel(writer, sheet_name='Alt_Urgell')
