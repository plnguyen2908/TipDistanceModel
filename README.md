# TipDistanceModel

## TL;DR

You can download all the files and run ./submit.sh. The polynomial regression result will be in files: train.csv_result_pre_0, train.csv_result_in_0, train.csv_result_post_0. The decision tree will be in the job's output file.

## Dataset

Link :https://d37ci6vzurychx.cloudfront.net/trip-data/[file]. For example: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet where 2022 is the year and 01 is the month.

We will use the following dataset:

- Precovid: 2017,2018 from jan to dec (24 files)
- Incovid: 2019,2020 from jan to dec (24 files)
- Postcovid: 2021,2022 from jan to dec (24 files)

## Read Data

To read the parquet and convert it to csv, please look at the read.py file. Before reading it, please do:

- pip install pandas
- pip install pyarrow

To run the file:
- open the terminal of the folder that contains your dataset
- run python read.py [dataset in parquet form] if you are on window
- run python3 read.py [dataset in parquet form] if you are on mac

For example: python read.py https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet

## Modelling data

To trim the data, run Rscript process.R \<year\> <month from 01 to 12>. 

In the dataset, we only consder data that has trip distance in range [0, 20] miles, tip amount in range [0,10] dollar, and fare amount in range [0, 100] dollar.

For example: Rscript process.R 2019 01 will return yellow_tripdata_2022-01_new.csv with trimmed data
