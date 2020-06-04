# Authors: Edneide Ramalho and Allisson Dantas

# Regions and populations
Spain <- c('Andalucia', 'Aragon', 'Asturias', 'Baleares', 'Canarias', 'Cantabria',
                       'Castilla-La Mancha', 'Castilla y Leon', 'Catalunya', 'Ceuta', 'Comunitat Valenciana',
                       'Extremadura', 'Galicia', 'Madrid', 'Melilla', 'Murcia', 'Navarra', 'Euskadi', 'La Rioja', 'Total')
population <- c(8414240, 1319291, 1022800, 1149460, 2153389, 581078, 2032863, 2399548, 7675217, 84777,
                              5003769, 1067710, 2699499, 6663394, 86487, 1493898, 654214, 2207776, 316798, 47026208)

# Data base for Spain
library(readr)
DATA = read_delim("Data_Spain_v2.csv", ";", escape_double = FALSE, trim_ws = TRUE)
DEATHS = read_delim("Data_Spain_v2_deaths.csv", ";", escape_double = FALSE, trim_ws = TRUE)
library(dplyr)
DEATHS = DEATHS %>% dplyr::select(Dia:Total) 

# Writing the dates in the correct format
library(lubridate)
DATA$Dia = as.POSIXct(as.character(DATA$Dia), format = "%d/%m/%Y")
DATA$Dia = lubridate::as_date(DATA$Dia)

DEATHS$Dia = as.POSIXct(as.character(DEATHS$Dia), format = "%d/%m/%Y")
DEATHS$Dia = lubridate::as_date(DEATHS$Dia)

# Regions names
names = Spain

# Date
Avec = DATA$Dia

# Vector of zeros
# A = vector(mode = "numeric", length = length(Avec))
# for(i in 1:length(Avec)){
#   A[i] =  Avec[i] # Date in a number format 
# }

# Creating a matrix 
id = array(dim = c(length(Spain), 4), 0)

# Creating data base: this is the input to create the report
id = 1 # Only for Andalucia
data = pull(DATA[Spain[id]])
deaths = pull(DEATHS[Spain[id]])
name = rep(Spain[id], length(data))
time = seq(0, length(data)-1, by = 1)
# Creation of report
data_frame1 = data.frame(Avec, data, deaths, name, time) # Only Andalucia


#==================#
#Code to the Report#
#==================#

# Intial values
xx_ = 0 # It will receive the time
yy_ = 0 # It will receive the number of cases
time = NULL


# Function to fit
model_ml = function(x, k, a){
  return(k * exp(- log(k / yy_[1]) * exp(- a * x)))
}


# fitting <- nls(cases ~ K * exp(-log(K/115) * exp(-a * time)), 
#                data = data2,
#                start = list(K = K0, a = 0.2), trace = T)


#===================================================#
# Função Principal: Generate data                                  #
#===================================================#

# A - Date
# data - number of cases
# name - region name
# pop - population
# guardar - logical vector
# yF = ??? 

#generate_data = function(A, data, deaths, name, pop){}
  ##
  
#########
# Teste #
#########
# Inputs, function parameters
# Only Andalucia id = 1
A = data_frame1$Avec
data = data_frame1$data
deaths = data_frame1$deaths
name = Spain[id]
pop = population[id]

# Transformations
    
x = seq(0, length(data)-1, by = 1) # Time vector
y = data # Cases
z = deaths # Deaths
  
# Condition to start the fitting
if(sum(y > 100) > 3 & max(y) > 200){
    temp_x_y = if_else(y > 100, TRUE, FALSE)
    xx = x[which(temp_x_y==TRUE)]
    yy = y[which(temp_x_y==TRUE)]  
    temp_t0 = which(y>50)
    T0 = temp_t0
    T0 = (T0[1] + 1) - 10
  }
  
  if(length(xx) > 15){
    xx = xx[length(xx) - 15:length(xx)]
    yy = yy[length(yy) - 15:length(yy)]
  }

# The model will be fitted to these points
xx_ = xx
yy_ = yy
data_model = data.frame(xx_ = xx_, yy_ =yy, time = seq(0, length(xx_)-1,1))
    
for(i in 1:length(xx)){
  #intial guess for parameters 
  k0 = max(yy[length(yy)], 1000) 
  a = 0.2
  x0 = c(k0, a)

}

# Fitting the model
# fitting <- nls(cases ~ K * exp(-log(K/115) * exp(-a * time)), 
#                data = data2,
#                start = list(K = K0, a = 0.2), trace = T)

# Function to fit
fitting = nls(
  yy_ ~ model_ml(time, k, a), 
  data = data_model,
  start = list(k = x0[1], a = x0[2])
              )

#summary(fitting)


# Fitted Predictions
predictions = predict(fitting)

# Adding a column to the data frame
data_model = data_model %>% 
  mutate(predictions = round(predictions))

# Predicting for the next 3 days
new.time <- seq(data_model$time[length(data_model$time)] + 1,
                data_model$time[length(data_model$time)] + 3,
                by = 1)

library(propagate)
prediction_next = predictNLS(fitting, 
                             newdata = data.frame(time = new.time), 
                             interval = "prediction", alpha = 0.01)

# Creating a data base for the three days prediction
prediction_df <- data.frame(time = new.time,
                            prediction = round(prediction_next[[1]]$Prop.Mean.1),
                            pred_low = round(prediction_next[[1]]$`Sim.0.5%`),
                            pred_upp = round(prediction_next[[1]]$`Sim.99.5%`))


# Updating the data frame to do the plot

# Prediction Data base

# Include Date to prediction
prediction_df$Avec = seq(data_frame1$Avec[length(data_frame1$Avec)] + 1,
                         data_frame1$Avec[length(data_frame1$Avec)] + 3, 1)


# Including predictions into data_frame1
data_frame1$predictions = c(rep(NA, length(data_frame1$time) - length(data_model$xx_)),
                            round(predictions))


# General Data base
df_general = data_frame1 %>% 
  dplyr::select(Avec, data, predictions)

prediction_df2 = prediction_df %>%  
  dplyr::select(Avec, prediction) %>% 
  dplyr::mutate(data = NA) %>% 
  dplyr::rename(predictions = prediction)
prediction_df2 = prediction_df2 %>% 
  dplyr::select(Avec, data, predictions)


df_general = rbind(df_general, prediction_df2)
### Até aqui consigo gerar a figura1.

# Continuação

### Coeficientes do modelo ajustado
# linha 174 em Python
#FR <- coef(fitting)

# Linha 108 do python
#================================================#
# Continuação do código para gerar a figura 2
#================================================#
xp = length(x)


if(length(xx) > 6){
xp <- c(xp, (length(x) - 1) + 2)
}

if(length(xx) > 9){
    xp <- c(xp, (length(x) - 1) + 3)
  }

if(length(xx) > 15){
  xp <- c(xp, (length(x) - 1) + 4)
}

Npred <- length(xp)

# Creating vectors
# Transformação das datas
dateNum = NULL
dateNumComplete = NULL
dateNumPred = NULL
dateNumPredComplete = NULL

# A já é uma data convertida

# Linha 141
xx_nd = xx
yy_nd = yy
yp = prediction_df$prediction # Valores preditos
lep = prediction_df$pred_low
uep = prediction_df$pred_upp

# Linha 147
for(i in 2:length(yp)){
  yp[i] = max(yp[i], y[length(y)])
  np_1 = yp[1] - yy[length(yy)]
  en1 = uep[1] - yp[1]
}



# Linha 158:
# np_ é o acréscimo no número de casos
np_ = vector("numeric", length = 3)
np_[1] = np_1
en = vector("numeric", length = 3)
en[1] = en1

for(ii in 2:length(xp)){
  np_[ii] = yp[ii] - yp[ii-1]
  en[ii] = sqrt((uep[ii]-yp[ii])^2 + (uep[ii-1] - yp[ii-1])^2)
}

en2 = array(dim = c(2,3))
en2[1,] = en
en2[2,] = en
en2 = t(en2)

for(i in 1:dim(en2)[1]){
  en2[i, 1] = min(en2[i,1], np_[i])
  print(en2)
}

#linha 171
for(i in 1:length(lep)){
  lep[i] = max(lep[i], y[length(y)])
}

# linha 174
for(i in 1:length(lep)){
  lep[i] = yp[i] - lep[i]
}

  
# linha 177
for(i in 1:length(uep)){
  uep[i] = max(uep[i], y[length(y)])
}

# 181
for(i in 1:length(uep)){
  uep[i] = uep[i] - yp[i]
}

# 184
Nvect = length(x[which(y>100)]) - 5 # pq -5 ?
tvect = x[y>100]

# 186
if(Nvect > 0){
  tvect = tvect[6:length(tvect)]
}

Kvect = array(dim = c(Nvect, 3))
avect = array(dim = c(Nvect, 3))

FR <- coef(fitting) #linha 180 # Coeficientes do ajuste

# 195 a 209
for(k in 1:Nvect){
  xx = x[y>100]
  yy = y[y>100]
  x1 = xx[1:(5+k)]
  y1 = yy[1:(5+k)]
  
  if(length(x1) > 16){
    x1 = x1[(length(x1) - 15) : length(x1)]
    y1 = y1[(length(y1) - 15) : length(y1)]
  }
  
  # Criando uma data frame para fazer o fitting
  data_model2 <- data.frame(x1 = x1, y1 = y1, time = seq(0,(length(x1)-1), 1))   
  
  # Fazer vários fittings aqui para gerar vários valores de parâmetros 
  fitting2 <- nls(
    y1 ~ model_ml(time, k, a), 
    data = data_model2,
    start = list(k = x0[1], a = x0[2])
  )
  
  popt1 = array(coef(fitting2))
  Kvect[k, 1] = popt1[1]
  avect[k, 1] = popt1[2]
  cf = confint(fitting2)
  cf = t(cf)
  
  cf[1,1] = max(cf[1,1], y1[length(y1)])
  cf[1,2] = max(cf[1,2], 0)
  Kvect[k, 2] = Kvect[k,1] - cf[1, 1]
  Kvect[k, 3] = cf[2, 1] - Kvect[k, 1] 
  avect[k, 2] = avect[k, 1] - cf[1, 2]
  avect[k, 2] = min(avect[k,2], avect[k, 1])
  avect[k, 3] = cf[2, 2] - avect[k, 1]
}# fim do laço



# 220

if(max(z) > 10){
  nwd = z
  deathrate = 0.01
  i18 = (1/deathrate) * nwd[3 : length(nwd) - 1]
  i19 = (1/deathrate) * nwd[3: length(nwd)]
  estimated = 0.5*(i18+i19)
}else
  estimated = NULL


t = seq(xx[1], 100, 0.1)


#
#================================================#
# Criação das figuras:
##
##=======================================# 
#Figure 1                                #
#========================================#
{library(ggplot2)
library(hrbrthemes)
# Points

plot_pred = ggplot(NULL) +
  geom_point(data = df_general, aes(x = Avec, y = data, color = "blue")) +
  geom_line(data = df_general, aes(x = Avec, y = predictions),
            color = "red",
            linetype = "dashed") +
  geom_errorbar(data = prediction_df,
                aes(x = Avec, ymin = pred_low, ymax = pred_upp,
                    color = "red"),
                width = .1) +
  scale_color_identity(name = "",
                       breaks = c("blue", "red"),
                       labels = c("Number of cases", "Predictions"),
                       guide = "legend") +
  geom_point(data = prediction_df, aes(x = Avec, y = prediction),
             color = "red") +
  theme_ipsum() + 
  ylab("Cumulative confirmed cases") +
  xlab("Time (day)") +
  scale_y_continuous(breaks = seq(0, max(prediction_df$pred_upp, na.rm = TRUE), 
                                  500),
                     sec.axis = sec_axis(trans = ~.*100000/population[id], 
                                         name =expression(paste("Cumulative cases per", 10^{5}, " inhabitants")))
                     ) +
  theme(legend.position = c(0.2,0.7)) +
  scale_x_date(date_breaks = "5 days", date_labels = "%d-%m")+
  theme(axis.text.x = element_text(angle = 45))



  
plot_pred 



# Table  
library(gridExtra)
new.cases = c(prediction_df$prediction[1]-data_frame1$data[length(data_frame1$data)],
              prediction_df$prediction[2] - prediction_df$prediction[1],
              prediction_df$prediction[3] - prediction_df$prediction[2])
table_pred <- data.frame(Day = prediction_df$Avec,
                Prediction = paste(prediction_df$prediction, " (", "+",
                                   new.cases,
                                   ")",
                                   sep = ""),
                Interval = paste("[", prediction_df$pred_low,"-",
                                 prediction_df$pred_upp, "]", sep = ""))
ss <- tableGrob(table_pred, rows = NULL)


# Final plot
final_plot = plot_pred + annotation_custom(ss,
                              xmin = as.numeric(data_frame1$Avec[7]),
                              xmax =  as.numeric(data_frame1$Avec[9]),
                              ymin = max(prediction_df$pred_low)) +
  

final_plot
}

# Saving in jpg
{jpeg(file = "figure1.jpg",
    width = 6, 
    height = 6, units = 'in', res = 300)
final_plot
dev.off()}
#============================================================================#

##=======================================# 
#Figure 2                                #
#========================================#
{
  dateNum = Avec
confirmedCases = y
estimated_plot = c(estimated[19:length(estimated)], rep(NA, 20)) 
data2 = data.frame(dateNum, confirmedCases, estimated_plot)

figure2 <- ggplot(data = data2, aes(x = dateNum)) +
  geom_point(aes(y = confirmedCases, color = "blue")) +
  geom_point(aes(y = estimated_plot, color = "darkgreen"))+
  theme_ipsum() + 
  scale_color_identity(name = "",
                       breaks = c("blue", "darkgreen"),
                       labels = c("Confirmed cases", "Estimated cases"),
                       guide = "legend")+
  theme(legend.position = c(0.8,0.8))+
  ylab("Number of cases") +
  xlab("Time (day)") +
  scale_x_date(date_breaks = "5 days", date_labels = "%d-%m")+
  theme(axis.text.x = element_text(angle = 45))

figure2
}

# Saving in jpg
{jpeg(file = "figure2.jpg",
     width = 6, 
     height = 6, units = 'in', res = 300)
figure2
dev.off()}

##=======================================# 
#Figure 3: predições de a                #
#========================================#
# Criar uma base de dados com a e seus desvios e data
# a data inicial foi aquela em que se iniciou as predições
{avect
df_general$Avec[tvect]

data_avect = as.data.frame(avect)
names(data_avect) = c("a", "alower", "aupper")

data_avect = data_avect %>% 
  mutate(date = df_general$Avec[tvect])

figure3 <- ggplot(data_avect) +
geom_errorbar(aes(x = date, 
                  ymin = a - alower, 
                  ymax = a + aupper), color = "blue", width = .1) +
  geom_point(aes(x = date, y = a), color = "blue") +
  geom_line(aes(x = date, y = a), color = "blue", linetype = "dashed") +
  theme_ipsum() +
  ylab(expression(paste(a, " (", day^{-1}, ")"))) +
  xlab("Time (day)") +
  scale_x_date(date_breaks = "5 days", date_labels = "%d-%m",
               limits = as.Date(c(Avec[1], Avec[length(Avec)])))+
  theme(axis.text.x = element_text(angle = 45)) 
  #scale_y_continuous(limits = c(0, 0.35))
figure3
}       

# Saving in jpg
{jpeg(file = "figure3.jpg",
     width = 6, 
     height = 6, units = 'in', res = 300)
figure3
dev.off()}

##=======================================# 
#Figure 4: Previsões de K                 #
#========================================#
# Criar uma base de dados com a e seus desvios e data
# a data inicial foi aquela em que se iniciou as predições
{Kvect
  df_general$Avec[tvect]
  
  data_Kvect = as.data.frame(Kvect)
  names(data_Kvect) = c("K", "Klower", "Kupper")
  
  data_Kvect = data_Kvect %>% 
    mutate(date = df_general$Avec[tvect])
  
figure4 <-   ggplot(data_Kvect) +
    geom_errorbar(aes(x = date, 
                      ymin = K - Klower, 
                      ymax = K + Kupper), color = "blue", width = .1) +
    geom_point(aes(x = date, y = K), color = "blue") +
    geom_line(aes(x = date, y = K), color = "blue", linetype = "dashed") +
    theme_ipsum() +
    ylab("K (Final number of cases)") +
    xlab("Time (day)") +
  scale_x_date(date_breaks = "5 days", date_labels = "%d-%m",
               limits = as.Date(c(Avec[1], Avec[length(Avec)])))+
  theme(axis.text.x = element_text(angle = 45)) +
  scale_y_log10(breaks = trans_breaks("log10", function(x) 10^x),
                labels = trans_format("log10", math_format(10^.x))) 
figure4
} 
# Saving in jpg
{jpeg(file = "figure4.jpg",
     width = 6, 
     height = 6, units = 'in', res = 300)
figure4
dev.off()}

##=======================================# 
#Figure 5: Incident observed cases       #
#========================================#
# Novos casos
new_cases = NULL
for(i in 2:length(y)-1){
  new_cases[i-1] = y[i] - y[i-1]
}
df_inc1 = as.data.frame(new_cases)
df_inc1$date = Avec[x[3:length(x)]] # Adicionando as datas
df_inc1 = df_inc1 %>% 
  mutate(status = "Confirmed")
# Três dias de predição
new_cases_pred = NULL
new_cases_pred[1] = prediction_df$prediction[1] - y[length(y)]
for(i in 2:dim(prediction_df)[1]){
  new_cases_pred[i] = prediction_df$prediction[i] - prediction_df$prediction[i-1]
}
df_inc2 = as.data.frame(new_cases_pred)
# Adicionando data
df_inc2$date = prediction_df$Avec - 1
names(df_inc2)[1] = "new_cases"
df_inc2 = df_inc2 %>% 
  mutate(status = "Predicted")
# Juntando as duas bases de dados
incidenceDF = rbind(df_inc1, df_inc2)
# Plot
figure5 <- ggplot(incidenceDF, aes(x = date,
                                   y = new_cases, 
                                   fill = status)) +
  geom_bar(stat = "identity",  
           position = position_dodge()) +
  theme_ipsum() +
  scale_fill_manual(values = c("blue", "red")) +
  theme(legend.title = element_blank()) +
  ylab("Incident observed cases") +
  xlab("Time (day)") +
  theme(legend.position = c(0.1,1)) +
  scale_y_continuous(breaks = seq(0, max(incidenceDF$new_cases, na.rm = TRUE), 
                                  50),
                     sec.axis = sec_axis(trans = ~.*100000/population[id], 
                                         name =expression(paste("Cumulative cases per", 10^{5}, " inhabitants")))
  )+
  scale_x_date(date_breaks = "5 days", date_labels = "%d-%m")+
  theme(axis.text.x = element_text(angle = 45))
  
figure5

# Saving in jpg
{jpeg(file = "figure5.jpg",
     width = 6, 
     height = 6, units = 'in', res = 300)
figure5
dev.off()}

##=======================================# 
#Figure 6: Rho                           #
#========================================#
nw = y[2:length(y)] - y[1: length(y) - 1]
id_ = seq(7, length(nw)-1)


rho = (nw[id_ -1] + nw[id_] + nw[id_ + 1])/(nw[id_-6] + nw[id_-5] + nw[id_-4]) 
actual.rho = round(rho[length(rho)],1)

date = Avec[x[id_+1]] # datas

# data frame
{mytitle <- bquote("Actual" ~ rho ==  ~ .(actual.rho))
rho_df = data.frame(date, rho)
figure6 <- ggplot(rho_df, aes(x = date, y = rho)) +
  geom_point(color = "blue") +
  theme_ipsum() +
  scale_y_continuous(name = expression(rho) ,
                     limits = c(0, 12)) + 
  xlab("Time (day) ") +
  scale_x_date(date_breaks = "5 days", date_labels = "%d-%m",
               limits = as.Date(c(Avec[1], Avec[length(Avec)])))+
  theme(axis.text.x = element_text(angle = 45)) +
  ggtitle(mytitle)

figure6}

figure6 = figure6 + geom_hline(yintercept = 1, linetype = "dashed", color = "gray")

# Saving in jpg
{jpeg(file = "figure6.jpg",
     width = 6, 
     height = 6, units = 'in', res = 300)
figure6
dev.off()}

##=======================================# 
#Figure 7: Cumulative observed deaths    #
#========================================#
death_df <- data.frame(Avec, z)
figure7 <- ggplot(death_df) +
  geom_point(aes(x = Avec, y = z), color = "blue") +
  theme_ipsum() +
  xlab("Time (day) ") +
  ylab("Cumulative observed deaths") +
  scale_y_continuous(breaks = seq(0, max(death_df$z, na.rm = TRUE), 
                                  10),
                     sec.axis = sec_axis(trans = ~.*100000/population[id], 
                                         name =expression(paste("Cumulative deaths per", 10^{5}, " inhabitants")))
  ) +
  scale_x_date(date_breaks = "5 days", date_labels = "%d-%m",
               limits = as.Date(c(Avec[1], Avec[length(Avec)])))+
  theme(axis.text.x = element_text(angle = 45))

figure7

# Saving in jpg
{jpeg(file = "figure7.jpg",
     width = 6, 
     height = 6, units = 'in', res = 300)
figure7
dev.off()}

##=======================================# 
#Figure 8: Case fatality rate            #
#========================================#
cfr <- 100*z/y
cfr_df <- data.frame(Avec, cfr)

figure8 <- ggplot(cfr_df) +
  geom_point(aes(x = Avec, y = cfr), color = "blue") +
  theme_ipsum() +
  xlab("Time (day) ") +
  ylab("Cases fatality rate (%)") +
  scale_y_continuous(breaks = seq(0, max(cfr_df$cfr, na.rm = TRUE), 
                                  0.5),
                     sec.axis = sec_axis(trans = ~.*100000/population[id], 
                                         name =expression(paste("Cumulative cases per", 10^{5}, " inhabitants")))
  ) +
  scale_x_date(date_breaks = "5 days", date_labels = "%d-%m",
               limits = as.Date(c(Avec[1], Avec[length(Avec)])))+
  theme(axis.text.x = element_text(angle = 45))

figure8
# Saving in jpg
jpeg(file = "figure8.jpg",
     width = 6, 
     height = 6, units = 'in', res = 300)
figure8
dev.off()