# TipDistanceModel

## Dataset

Link :https://d37ci6vzurychx.cloudfront.net/trip-data/[file]. For example: https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-01.parquet where 2022 is the year and 01 is the month.

We will use the following dataset:

- Precovid: 2017,2018 from jan to dec (24 files)
- Incovid: 2019,2020 from jan to dec (24 files)
- Postcovid: 2021,2022 from jan to dec (24 files)

## Read Data

To read the parquet and conver it to csv, please look at the read.py file. Before reading it, please do:

- pip install pandas
- pip install pyarrow

To run the file:
- open the terminal of the folder that contains your dataset
- run python read.py <dataset> if you are on window
- run python3 read.py <dataset> if you are on mac
