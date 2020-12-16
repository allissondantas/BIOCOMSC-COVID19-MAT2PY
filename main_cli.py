from risk_diagrams import run_risk_diagrams
import os, sys

if __name__ == "__main__":
    try:
        # 0 None | 1 last_days | 2 html | 3 animation
        radio_valor = 0
        run_risk_diagrams('recife', 'False', None, None, radio_valor)
        #run_risk_diagrams('brasil', 'False', None, None, radio_valor)
        #run_risk_diagrams('malawi', 'False', None, None, radio_valor)
        #run_risk_diagrams('ourworldindata', 'False', None, None, radio_valor)
        
    except ValueError:
        print('Error!!!!!!')
    sys.exit()
