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

echo "Hello from exList"

while read year month; do
    # echo "$year $month";
    wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_${year}-${month}.parquet;
    python3 read.py yellow_tripdata_${year}-${month}.parquet;
    Rscript process.R $year $month;
    rm -f yellow_tripdata_${year}-${month}.parquet;
done < $1

python3 train.py

rm -f *.csv
