#!/bin/bash

# untar your Python installation. Make sure you are using the right version!
tar -xzf python39.tar.gz
# (optional) if you have a set of packages (created in Part 1), untar them also
tar -xzf PythonPackages.tar.gz

# make sure the script will use your Python installation, 
# and the working directory as its home location
export PATH=$PWD/python/bin:$PATH
export PYTHONPATH=$PWD/packages
export HOME=$PWD

tar -xzf R413.tar.gz
tar -xzf packages_FITSio_tidyverse.tar.gz

export PATH=$PWD/R/bin:$PATH
export RHOME=$PWD/R
export R_LIBS=$PWD/packages


while read year month; do
    echo "$year $month";
    wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_${year}-${month}.parquet;
    python3 read.py yellow_tripdata_${year}-${month}.parquet;
    Rscript process.R $year $month;
    rm -f yellow_tripdata_${year}-${month}.parquet;
done < $1

echo "\"\",\"passenger_count\",\"trip_distance\",\"tip_amount\",\"fare_amount\",\"extra\",\"year\"" > merge.csv

tail -n +2 -q yellow_tripdata_*.csv >> merge.csv

rm -f yellow_tripdata_*.csv

head -n 1 merge.csv > train.csv

head -n 1 merge.csv > test.csv

tail -n +2 merge.csv | shuf > shuff.csv

rm -f merge.csv

lines=$(cat shuff.csv | wc -l)

trainLine=$(($lines * 7))
trainLine=$(($trainLine / 10))
testLine=$(($lines - $trainLine))

head -n $trainLine shuff.csv >> train.csv

tail -n $testLine shuff.csv >> test.csv

rm -f merge.csv

rm -f shuff.csv

Rscript regression.R train.csv test.csv

mv train.csv_result "train.csv_result_in_$2"

head -n 100000 train.csv > train_in.csv

rm -f train.csv
rm -f test.csv
