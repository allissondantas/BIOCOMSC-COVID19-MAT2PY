from risk_diagrams import run_risk_diagrams
import os, sys

if __name__ == "__main__":
    try:
        run_risk_diagrams('recife', 'False', None, None)
        run_risk_diagrams('brasil', 'False', None, None)
    except:
        print('Error!!!!!!')
    sys.exit()
