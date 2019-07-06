#analisi csv

setwd("C:/Users/Luca/Documents/Università/Magistrale/Modelli Probabilistici Per le Decisioni/Modelli-Probabilistici")

season = read.csv("./test_filtrato.csv", header= T) 

str(nrow(season))

str(length(which(season$Overall == "1")))
str(length(which(season$Overall == "2")))
str(length(which(season$Overall == "3")))
str(length(which(season$Overall == "4")))
str(length(which(season$Overall == "5")))
