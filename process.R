rm(list=ls())

library(tidyverse)

args = commandArgs(trailingOnly=TRUE)

file = paste("yellow_tripdata_",args[1],"-",args[2],".csv", sep="")
# print(file)
# data = read.csv("yellow_tripdata_2019-01.csv")
data = read.csv(file)

# print(head(data))


data1 = data %>% 
  select(
    passenger_count,
    trip_distance,
    tip_amount,
    fare_amount,
    extra, 
  ) %>% 
  drop_na() %>%
  filter(trip_distance >= 0 & trip_distance <=20 & tip_amount <= 10 & tip_amount >= 0 & fare_amount >= 0 & fare_amount <= 100) %>%
  filter(passenger_count <= 6 & extra >= 0 & extra <= 5) %>%
  mutate(
    period = case_when(
      args[1] == "2017" | args[1] == "2018" ~ 0,
      args[1] == "2019" | args[1] == "2020" ~ 1,
      args[1] == "2020" | args[1] == "2021" ~ 2
    )
  ) 
# print(paste(substring(file, 1, nchar(file) - 4), "_new", ".csv", sep = ""))
write.csv(data1, file = paste(substring(file, 1, nchar(file) - 4), ".csv", sep = ""))
