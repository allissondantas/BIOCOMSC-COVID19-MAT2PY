from datetime import date
from scipy.stats.distributions import t
from scipy.optimize import curve_fit
from matplotlib.ticker import AutoMinorLocator
from matplotlib import pyplot as plot
from matplotlib.backends.backend_pdf import PdfPages
import scipy.stats
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys

np.seterr(all='ignore')

xx_ = 0
yy_ = 0
time = []


def model_ml(x, k, a):
    return k * np.exp(- np.log(k / yy_[0]) * np.exp(- a * (x - xx_[0])))


def mat_numpy_logical(t, j):
    aux = []
    for i in range(len(t)):
        if t[i]:
            aux.append(j[i])
    np.asarray(aux)
    return aux

def simple_confint(yy, popt, pcov):
    alpha = 0.05
    n = len(yy)
    p = len(popt)

    dof = max(0, n - p)

    tval = t.ppf(1.0-alpha/2., dof)
    cf = np.zeros((2, 2))

    for i, p, var in zip(range(n), popt, np.diag(pcov)):
        sigma = var**0.5
        cf[i, 0] = p - sigma*tval
        cf[i, 1] = p + sigma*tval
        
        '''print('p{0}: {1} [{2}  {3}]' .format(i, p,
                                                p - sigma*tval,
                                                p + sigma*tval))
                                                '''
        
    return cf
    
''' predband by https://apmonitor.com/che263/index.php/Main/PythonRegressionStatistics'''
def predband(x, xd, yd, p, func, conf=0.95):

    alpha = 1.0 - conf    # significance
    N = xd.size        # data sample size
    var_n = len(p)  # number of parameters
    # Quantile of Student's t distribution for p=(1-alpha/2)
    q = scipy.stats.t.ppf(1.0 - alpha / 2.0, N - var_n)
    # Stdev of an individual measurement
    se = np.sqrt(1. / (N - var_n) *
                 np.sum((yd - func(xd, *p)) ** 2))
    # Auxiliary definitions
    sx = (x - xd.mean()) ** 2
    sxd = np.sum((xd - xd.mean()) ** 2)
    # Predicted values (best-fit model)
    yp = func(x, *p)
    for i in range(len(yp)):
        yp[i] = round(yp[i], 1)
    # Prediction band
    dy = q * se * np.sqrt(1.0 + (1.0/N) + (sx/sxd))
    # Upper & lower prediction bands.
    lpb, upb = yp - dy, yp + dy
    return yp, lpb, upb


def generate_data(dateData, data, deaths, name, pop, brasil):

    x = np.arange(start=0, stop=len(data), step=1)
    y = data
    z = deaths
    

    if sum(y > 100) > 3 and max(y) > 200:
        temp_x_y = np.logical_or(y > 100, None)
        xx = mat_numpy_logical(temp_x_y, x)
        yy = mat_numpy_logical(temp_x_y, y)
        temp_t0 = np.where(y > 50)
        T0 = np.asarray(temp_t0)
        T0 = (T0.item(0) + 1) - 10

        if len(xx) > 15:
            xx = xx[len(xx) - 15:len(xx)]
            yy = yy[len(yy) - 15:len(yy)]

        global xx_, yy_, time
        xx_, yy_ = xx, yy

        for i in range(len(xx)):
            time.append(i)

        x0 = np.array([max(yy[(len(yy) - 1)], 1000), 0.2])

        popt, pcov = curve_fit(model_ml, xx, yy, x0, method='lm', maxfev = 10000)

        cf = simple_confint(yy, popt, pcov)
        #print('confidence interval\n', cf)
        
        xp = [len(x)]

        if len(xx) > 6:
            xp.append((len(x) - 1) + 2)
            if len(xx) > 9:
                xp.append((len(x) - 1) + 3)
                if len(xx) > 12:
                    xp.append((len(x) - 1) + 4)
                    if len(xx) > 15:
                        xp.append((len(x) - 1) + 5)
        Npred = len(xp)
        dateNum = []
        dateNumComplete = []
        dateNumPred = []
        dateNumPredComplete = []

        for i in range(len(dateData)):
            convertData = date.fromordinal(int(dateData[i]))
            dateNum.append(convertData.strftime("%d-%m"))
            dateNumComplete.append(convertData.strftime("%d-%m-%Y"))
            if i == len(dateData) - 1:
                convertDataLast = convertData
        #convertDataLast = date.fromordinal(int(dateData[len(dateData) - 1]))

        for k in range(Npred):
            convertDataLast += datetime.timedelta(days=1)
            dateNumPred.append(convertDataLast.strftime("%d-%m"))
            dateNumPredComplete.append(convertDataLast.strftime("%d-%m-%Y"))
        
        dateTotal = dateNum + dateNumPred 
            
        xx_nd = np.asarray(xx)
        yy_nd = np.asarray(yy)
        yp, lep, uep = predband(xp, xx_nd, yy_nd, popt, model_ml, conf=.998018)
        #print('yp_pre = ', yp)
        for i in range(len(yp)):
            yp[i] = max(yp[i], y[len(y) - 1])
        np_ = [yp[0] - yy[len(yy) - 1]]
        en = [uep[0] - yp[0]]
        for i in range(len(lep)):
            lep[i] = round(lep[i], 1)
            uep[i] = round(uep[i], 1)
        #print('ep_low = ', lep, '\nep_upp = ', uep)
        for ii in range(1, len(xp)):
            np_.append(yp[ii] - yp[ii - 1])
            en = np.append(en, np.sqrt(
                (uep[ii] - yp[ii])**2+(uep[ii - 1]-yp[ii - 1])**2))
        #print('np = ', np_)
        
        en = [en, en]
        en = np.transpose(en)
        
        for i in range(len(en)): en[i][0] = min(en[i][0], np_[i])
        #print(en)
        for i in range(len(lep)): lep[i] = max(lep[i], y[len(y) - 1])
        for i in range(len(lep)): lep[i] = yp[i] - lep[i]
        for i in range(len(uep)): uep[i] = max(uep[i], y[len(y) - 1])
        for i in range(len(uep)): uep[i] = uep[i] - yp[i]
        Nvect = len(x[y > 100 ])- 5 
        tvect = x[y>100]
        
        if Nvect > 0:
            tvect = tvect[5:len(tvect)]
        else:
            sys.exit('\n\nError!!! It was not possible to make a prediction for '+name+'. Check the data. \n\nError information:  Nvect < 0')
        
        
        Kvect = np.zeros((Nvect, 3))
        avect = np.zeros((Nvect, 3))
        
        FR = popt
        
        for k in range(0, Nvect):
            xx = x[y>100]
            yy = y[y>100]
            x1 = xx[0:(5+(k+1))]
            y1 = yy[0:(5+(k+1))]
            if len(x1) > 16:
                x1 = x1[(len(x1) - 15): len(x1)]
                y1 = y1[(len(y1) - 15): len(y1)]
            
            popt1, pcov1 = curve_fit(model_ml, x1, y1, x0, method='lm', maxfev = 10000)
            Kvect[k, 0] = popt1[0]
            avect[k, 0] = popt1[1]
            cf = simple_confint(y1, popt1, pcov1)
            cf = np.transpose(cf)
            #print('confidence interval\n', cf)
            
            cf[0,0] = max(cf[0,0], y1[len(y1) - 1])
            cf[0,1] = max(cf[0,1],0)
            Kvect[k, 1] = Kvect[k, 0] - cf[0, 0]
            Kvect[k, 2] = cf[1, 0] - Kvect[k, 0]
            avect[k, 1] = avect[k, 0] - cf[0, 1]
            avect[k, 1] = min(avect[k, 1], avect[k, 0])
            avect[k, 2] = cf[1, 1] - avect[k, 0]
        
        if max(z) > 10:
            nwd = z
            deathrate = 0.01
            i18 = 1/deathrate*nwd[1: len(nwd) - 1]
            i19 = 1/deathrate*nwd[2: len(nwd)]
            estimated = 0.5*(i18+i19)
        else:
            estimated = []
            
        t = np.arange(xx[0], 100, 0.1)
        pt = True
        if brasil and not pt:
            savePath = 'reports_pdf/brasil/'+dateNumComplete[len(dateNumComplete) - 1]+'-'+name+'.pdf'
        elif brasil and pt:
            savePath = 'reports_pdf/brasil/informe-pt/'+dateNumComplete[len(dateNumComplete) - 1]+'-'+name+'.pdf'
        else:
            savePath = 'reports_pdf/'+dateNumComplete[len(dateNumComplete) - 1]+name+'.pdf'
        with PdfPages(savePath) as pdf:
            #fig, axes = plt.subplots(nrows=4, ncols=2)
            #ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8 = axes.flatten()
            
            if brasil and pt:
                cases_label = 'Número de casos'
                cumulative_confirmed_label  = 'Casos confirmados acumulados'
                time_day_label = 'Tempo (dia)'
                cumulative_cases_per_label = 'Casos acumulados por $\mathregular{10^5}$'
                table_title_label = ['Dia', 'Predição', 'Intervalo']
                prediction_label = 'Predição'
                confirmed_cases_label = 'Casos confirmados'
                estimated_cases_label = 'Casos estimados'
                a_day_label = '$a (dia^-1)$'
                k_label = 'K (Número de casos final)'
                incident_observed_cases_label = 'Casos observados'
                confirmed_label = 'Confirmado'
                actual_label = 'Atual'
                cumulative_observed_deaths_label = 'Óbitos observados acumulados'
                cumulative_observed_deaths_per_label = 'Óbitos acumulados por $\mathregular{10^5}$ hab.'
                case_fatality_rate_label = 'Taxa de letalidade (%)'
                
            else: 
                cases_label = 'Number of cases'
                cumulative_confirmed_label  = 'Cumulative confirmed cases'
                time_day_label = 'Time (day)'
                cumulative_cases_per_label = 'Cumulative cases per $\mathregular{10^5}$'
                table_title_label = ['Day', 'Prediction', 'Interval']
                prediction_label = 'Prediction'
                confirmed_cases_label = 'Confirmed cases'
                estimated_cases_label = 'Estimated cases'
                a_day_label = '$a (day^-1)$'
                k_label = 'K (Final number of cases)'
                incident_observed_cases_label = 'Incident observed cases' 
                confirmed_label = 'Confirmed'
                actual_label = 'Actual'
                cumulative_observed_deaths_label = 'Cumulative observed deaths'
                cumulative_observed_deaths_per_label = 'Cumulative deaths per $\mathregular{10^5}$ inhabitants'
                case_fatality_rate_label = 'Case fatality rate (%)'
            
            fig1, ax1 = plt.subplots()

            xfit = np.arange(0.0, len(x) + len(xp), 0.01)
            yfit = model_ml(xfit, popt[0], popt[1])
            ax1.plot(xfit, yfit, 'r--')
            ax1.plot(dateNum, y, 'b. ', label= cases_label)
            ax1.errorbar(dateNumPred, yp, (lep, uep), 
                        fmt='r.',
                        elinewidth=0.5,
                        capsize=5,
                        capthick=0.5,
                        ecolor='xkcd:red',
                        label= prediction_label)
            ax1.set_ylabel(cumulative_confirmed_label)
            ax1.set_xlabel(time_day_label)
            ax1.set_xticks(np.arange(0,  len(dateTotal) - 1, 5))
            labels = []
            for i in ax1.get_xticks(): labels.append(dateTotal[i])
            ax1.set_xticklabels(labels, rotation = 45, ha="right")
            ax1.xaxis.set_minor_locator(AutoMinorLocator())
            ax1.legend()

            ax1_1 = ax1.twinx()
            ax1_1.set_ylabel(cumulative_cases_per_label)
            ax1_y_lim = ax1.get_ylim()
            limlim = ax1_y_lim[1]/pop*1e5
            ax1_1.set_ylim(0, limlim)
            

            ax1_2 = ax1.twinx()
            ax1_2.axis('off')
            table_data = []
        
            for i in range(len(xp)):
                if i == 0:
                    diference = yp[i] - yy[(len(yy) - 1)]
                    diference = round(diference)
                    table_data.append(
                        [dateNumPredComplete[i], "{} +({})".format(int(yp[i]), int(diference)), "{} - {}".format( int(yp[i] - lep[i]), int(yp[i] + uep[i]))])
                else:
                    diference = yp[i] - yp[i - 1]
                    diference = round(diference)
                    table_data.append(
                        [dateNumPredComplete[i], "{} +({})".format(int(yp[i]), int(diference)), "{} - {}".format( int(yp[i] - lep[i]), int(yp[i] + uep[i]))])
            table = ax1_2.table(cellText=table_data,
                            loc='center left',
                            zorder=3,
                            cellLoc='center',
                            bbox=[0.015, 0.5, 0.56, 0.3],
                            colWidths=[0.2, 0.2, 0.3],
                            colLabels= table_title_label)
            fig1.tight_layout()
            if brasil and pt:
                    savePathImg = 'reports_pdf/brasil/informe-pt/figures/'+dateNumComplete[len(dateNumComplete) - 1]+'-'+name+'_fig1.png'
                    plt.savefig(savePathImg, bbox_inches='tight', dpi=300) 
            
            
            fig2, ax2 = plt.subplots()
            
            if len(estimated) == 0:
                print("Not enough data")
            else:
                ax2.plot(dateNum, y, 'b.', label = confirmed_cases_label)
                ax2.plot(x[0:len(estimated)] - 18, estimated,'g.', label = estimated_cases_label)
                ax2.set_ylabel(cases_label)
                ax2.set_xlabel(time_day_label)
                ax2.set_xlim(T0, len(dateData)+Npred+1)
                ax2.set_xticks(np.arange(0,  len(dateTotal) - 1, 5))
                labels = []
                for i in ax2.get_xticks(): labels.append(dateTotal[i])
                ax2.set_xticklabels(labels, rotation = 45, ha="right")
                ax2.legend()
                ax2.xaxis.set_minor_locator(AutoMinorLocator())
                ax2_1 = ax2.twinx()
                ax2_1.set_ylabel(cumulative_cases_per_label)
                ax1_y_lim = ax2.get_ylim()
                limlim = ax1_y_lim[1]/pop*1e5
                ax2_1.set_ylim(0, limlim)
                
            fig2.tight_layout()
            if brasil and pt:
                    savePathImg = 'reports_pdf/brasil/informe-pt/figures/'+dateNumComplete[len(dateNumComplete) - 1]+'-'+name+'_fig2.png'
                    plt.savefig(savePathImg, bbox_inches='tight', dpi=300) 

            fig3, ax3 = plt.subplots()
            if Nvect > 0:
                dateNum_ax1 = []
                for i in tvect: dateNum_ax1.append(dateNum[i])
                ax3.errorbar(tvect, avect[:, 0], (avect[:, 1], avect[:, 2]), 
                        fmt='b.',
                        elinewidth=0.5,
                        capsize=5,
                        capthick=0.5,
                        ecolor='xkcd:blue',
                        label=prediction_label)
                
                ax3.plot(tvect, avect[:, 0], 'b--')
                ax3.set_xlabel(time_day_label)
                ax3.set_ylabel(a_day_label)
                ax3.set_xlim(T0, len(dateData)+Npred+1)
                ax3.set_ylim(0, 0.2)
                ax3.set_xticks(np.arange(0,  len(dateTotal) - 1, 5))
                labels = []
                for i in ax3.get_xticks(): labels.append(dateTotal[i])
                ax3.set_xticklabels(labels, rotation = 45, ha="right")
                ax3.xaxis.set_minor_locator(AutoMinorLocator())
            else:
                print("Not enough data")
    
            fig3.tight_layout()
            if brasil and pt:
                    savePathImg = 'reports_pdf/brasil/informe-pt/figures/'+dateNumComplete[len(dateNumComplete) - 1]+'-'+name+'_fig3.png'
                    plt.savefig(savePathImg, bbox_inches='tight', dpi=300) 
            
            fig4, ax4 = plt.subplots()
            if Nvect > 0:
                ax4.errorbar(tvect, Kvect[:, 0], (Kvect[:, 1], Kvect[:, 2]), 
                        fmt='b.',
                        elinewidth=0.5,
                        capsize=5,
                        capthick=0.5,
                        ecolor='xkcd:blue',
                        label=prediction_label)
                ax4.plot(tvect, Kvect[:, 0], 'b--')
                ax4.set_xlabel(time_day_label)
                ax4.set_ylabel(k_label)
                ax4.set_xlim(T0, len(dateData)+Npred+1)
                ax4.set_xticks(np.arange(0,  len(dateTotal) - 1, 5))
                labels = []
                for i in ax4.get_xticks(): labels.append(dateTotal[i])
                ax4.set_xticklabels(labels, rotation = 45, ha="right")
            else:
                print("Not enough data")
            
            if pop > 100e6:
                ax4.set_ylim(1e4, 1e7)
            else:
                ax4.set_ylim(1e3, 1e6)
            
            ax4.set_yscale('log')
            ax4.xaxis.set_minor_locator(AutoMinorLocator())
        
            fig4.tight_layout()
            if brasil and pt:
                    savePathImg = 'reports_pdf/brasil/informe-pt/figures/'+dateNumComplete[len(dateNumComplete) - 1]+'-'+name+'_fig4.png'
                    plt.savefig(savePathImg, bbox_inches='tight', dpi=300) 
            
            fig5, ax5 = plt.subplots()
            ax5.bar(x[2:len(x)], y[2:len(y)] - y[1:len(y)-1], label=confirmed_label)
            ax5.bar(xp, np_, color='red', label=prediction_label)
            ax5.set_xlabel(time_day_label)
            ax5.set_ylabel(incident_observed_cases_label)
            ax5.legend()
            ax5.set_xticks(np.arange(0,  len(dateTotal) - 1, 5))
            labels = []
            for i in ax5.get_xticks(): labels.append(dateTotal[i])
            ax5.set_xticklabels(labels, rotation = 45, ha="right")
            
            ax5_1 = ax5.twinx()
            ax5_1.set_ylabel(cumulative_cases_per_label)
            #ax1_y_lim = ax5.get_ylim()
            #limlim = ax1_y_lim[1]/pop*1e5
            #ax5_1.set_ylim(0, ax5.get_ylim())
            ax5.xaxis.set_minor_locator(AutoMinorLocator())
            
            fig5.tight_layout()
            if brasil and pt:
                    savePathImg = 'reports_pdf/brasil/informe-pt/figures/'+dateNumComplete[len(dateNumComplete) - 1]+'-'+name+'_fig5.png'
                    plt.savefig(savePathImg, bbox_inches='tight', dpi=300) 
            
            fig6, ax6 = plt.subplots()
            
            nw = y[1: len(y)] - y[0: len(y) - 1]
            id_ = np.arange(6, len(nw) - 1)
            rh = (nw[id_-1]+nw[id_]+nw[id_+1])//(nw[id_-6]+nw[id_-5]+nw[id_-4])
            ax6.plot(x[id_+1], rh, 'bh ')
            ax6.set_xlabel(time_day_label)
            ax6.set_ylabel('\u03C1')
            ax6.set_xlim(T0, len(dateData)+Npred+1)
            ax6.set_ylim(0, 12)
            ax6.set_xticks(np.arange(0,  len(dateTotal) - 1, 5))
            labels = []
            for i in ax6.get_xticks(): labels.append(dateTotal[i])
            ax6.set_xticklabels(labels, rotation = 45, ha="right")
            ax6.xaxis.set_minor_locator(AutoMinorLocator())
            ax6.set_title(actual_label+' \u03C1 = {:2.1f}'.format(rh[len(rh) - 1]))
            
            fig6.tight_layout()
            if brasil and pt:
                    savePathImg = 'reports_pdf/brasil/informe-pt/figures/'+dateNumComplete[len(dateNumComplete) - 1]+'-'+name+'_fig6.png'
                    plt.savefig(savePathImg, bbox_inches='tight', dpi=300) 
            
            fig7, ax7 = plt.subplots()
            
            ax7.plot(x, z, 'b.')        
            ax7.set_ylabel(cumulative_observed_deaths_label)
            ax7.set_xlabel(time_day_label)
            ax7.set_xlim(T0, len(dateData)+Npred+1)
            ax7.set_xticks(np.arange(0,  len(dateTotal) - 1, 5))
            labels = []
            for i in ax7.get_xticks(): labels.append(dateTotal[i])
            ax7.set_xticklabels(labels, rotation = 45, ha="right")        
            ax7_1 = ax7.twinx()
            ax7_1.set_ylabel(cumulative_observed_deaths_per_label)
            ax1_y_lim = ax7.get_ylim()
            limlim = ax1_y_lim[1]/pop*1e5
            ax7_1.set_ylim(0, limlim)
            ax7.xaxis.set_minor_locator(AutoMinorLocator())
            
            fig7.tight_layout()
            if brasil and pt:
                    savePathImg = 'reports_pdf/brasil/informe-pt/figures/'+dateNumComplete[len(dateNumComplete) - 1]+'-'+name+'_fig7.png'
                    plt.savefig(savePathImg, bbox_inches='tight', dpi=300) 
    
            fig8, ax8 = plt.subplots()
            
            ax8.plot(x,100*z/y, 'bh')        
            ax8.set_ylabel(case_fatality_rate_label)
            ax8.set_xlabel(time_day_label)
            ax8.set_xlim(T0, len(dateData)+Npred+1)
            ax8.set_xticks(np.arange(0,  len(dateTotal) - 1, 5))
            labels = []
            for i in ax8.get_xticks(): labels.append(dateTotal[i])
            ax8.set_xticklabels(labels, rotation = 45, ha="right")        
            ax8.xaxis.set_minor_locator(AutoMinorLocator())
            
            fig8.tight_layout()
            if brasil and pt:
                    savePathImg = 'reports_pdf/brasil/informe-pt/figures/'+dateNumComplete[len(dateNumComplete) - 1]+'-'+name+'_fig8.png'
                    plt.savefig(savePathImg, bbox_inches='tight', dpi=300) 
            #fig.tight_layout()
            plt.close()
            try:
                pdf.savefig(fig1)
                pdf.savefig(fig2)
                pdf.savefig(fig3)
                pdf.savefig(fig4)
                pdf.savefig(fig5)
                pdf.savefig(fig6)
                pdf.savefig(fig7)
                pdf.savefig(fig8)
                
                plt.close('all')
                
                print("\n\nPrediction for the region of "+ name+" performed successfully!\nPath:" + savePath)
            except:
                print("An exception occurred")
        
        
            #plt.show()
                
        
        
