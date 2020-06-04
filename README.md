# BIOCOMSC-COVID19-MAT2PY
This is a translation Matlab to Python code for the Analysis and prediction of COVID-19 created by (BIOCOMSC) and avalaible in https://biocomsc.upc.edu/en/covid-19/situation-and-prediction .

### Project Description:
We employ an empirical model, verified with the evolution of the number of confirmed cases in previous countries where the epidemic is close to conclude, including all provinces of China. The model does not pretend to interpret the causes of the evolution of the cases but to permit the evaluation of the quality of control measures made in each state and a short-term prediction of tendencies. Note, however, that the effects of the measures’ control that start on a given day are not observed until approximately 5-7 days later.

Project authors: Martí Català, MD; Pere-Joan Cardona, PhD; Clara Prats, PhD; Sergio Alonso, PhD; Daniel López, PhD.

### Usage 
Run in command line:
```sh
$python3 crear_informe.py  youdata.xlsx 
$python3 risk_diagrams.py youdata.xlsx  
```

To Brazil use:
```sh
$python3 crear_informe.py  brasil 
$python3 risk_diagrams.py brasil 
```
The data is retrieved automatically from: https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv



License
---- 

MIT License

Copyright (c) 2020.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
