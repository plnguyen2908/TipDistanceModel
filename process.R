library(tidyverse)

args = commandArgs(trailingOnly=TRUE)

file = paste("yellow_tripdata_",args[1],"-",args[2],".csv", sep="")
# print(file)
# data = read.csv("yellow_tripdata_2019-01.csv")
data = read.csv(file)

print(data)


data1 = data %>% 
  filter(trip_distance >= 0 & trip_distance <=20 & tip_amount <= 10 & tip_amount >= 0 & fare_amount >= 0 & fare_amount <= 100) %>%
  drop_na(passenger_count) %>% 
  select(
    passenger_count,
    trip_distance,
    tip_amount,
    fare_amount,
    extra, 
    tpep_pickup_datetime,
  ) %>% 
  mutate(
    year = substring(tpep_pickup_datetime,1,4)
  ) %>% 
  select(-tpep_pickup_datetime)
