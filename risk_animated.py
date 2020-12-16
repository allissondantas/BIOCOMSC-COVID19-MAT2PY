import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import colormap

def update_line(num, data, line):
    line.set_data(data[..., :num])
    #print(num)
    return line,

def run_animation(a_14_days, p_seven, lim, bra_title, last_day, brasil):
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='IRRDPE'), bitrate=5000)

    temp = [a_14_days.tolist(),  p_seven.tolist()]

    DPI = 240
    fig1 = plt.figure(dpi=DPI)
    ax1 = fig1.add_subplot(111)

    data = np.array(temp)
    l, = ax1.plot([], [], 'ko--', fillstyle='none', linewidth=0.5)
    x = np.ones(lim)
    ax1.plot(x, 'k--', fillstyle='none', linewidth=0.5)
    ax1.set_xlim(0, lim)
    ax1.set_ylim(0, 4)

    if brasil:
        #ax1.set_ylabel('\u03C1 (média de '+ cases_deaths +' dos últimos 7 dias)')
        ax1.set_ylabel('\u03C1 (média dos últimos 7 dias)')
        ax1.set_xlabel('Taxa de ataque por $10^5$ hab. (últimos 14 dias)')
    else:
        ax1.set_ylabel('$\u03C1$ (mean of the last 7 days)')
        ax1.set_xlabel('Attack rate per $10^5$ inh. (last 14 days)')
    #ax1.set_xlabel('Taxa de ataque por $10^5$ hab. (últimos 14 dias)')
    #ax1.set_ylabel('\u03C1 (média dos últimos 7 dias')
    ax1.set_title(bra_title)

    '''
    plt.subplots_adjust(bottom=0.2)
    text_annotate = (
        "*A zona vermelha representa alto risco de infecção, enquanto a zona verde representa baixo risco.\n Valores calculados baseados na incidência diária de casos e população. "
        "IRRD/PE. \n Fonte: SES-PE. Dados atualizados em "+last_day+".")

    plt.text(0, -1, text_annotate, fontsize=7, wrap=True)
    '''
    ax1.set_aspect('auto')

    rh = np.arange(0,lim,1)
    ar = np.linspace(0,4,400)
        
    RH, AR = np.meshgrid(rh, ar)

    EPG = RH * AR

    for i in range(len(EPG)):
        for j in range(len(EPG[i])):
            if EPG[i][j] > 100:
                EPG[i][j] = 100
    c = colormap.Colormap()
    mycmap = c.cmap_linear('green(w3c)', 'yellow', 'red')
    ax1.pcolorfast([0, lim], [0, 4],EPG, cmap=mycmap, alpha=0.6)

    '''
    ax1.annotate(last_day,
                            xy=(a_14_days[len(a_14_days) - 1], p_seven[len(p_seven) - 1]), xycoords='data',
                            xytext=(len(x) - abs(len(x) / 3), 3.5), textcoords='data',
                            arrowprops=dict(arrowstyle="->",
                                            connectionstyle="arc3", linewidth=0.4),
    
                            )
                            '''
    


    line_ani = animation.FuncAnimation(fig1, update_line, len(data[1]) + 20, fargs=(data, l),
                                    interval=50, blit=True)
    line_ani.save('video/'+last_day + '-' + bra_title +'.mp4', writer=writer)

    print("Video saved!!!")