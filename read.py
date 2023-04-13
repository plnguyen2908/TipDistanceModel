import pandas as pd
import sys
# import pyarrow

file = sys.argv[1]

file1 = pd.read_parquet(file)
file_out = file[:-8] + '.csv'
print(file_out)
file1.to_csv(file_out, index=False, sep=',')
