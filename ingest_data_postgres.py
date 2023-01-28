import pandas as pd

from sqlalchemy import create_engine
from time import time

df = pd.read_csv('yellow_tripdata_2021-01.csv.gz')



### Put data in Postgres


#"tpep_pickup_datetime", "tpep_dropoff_datetime" are time variable but it have been recognized in Text. We need to change datatype to datetime
 
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

print(pd.io.sql.get_schema(df, name='yellow_taxi_data'))

#Connect to Postgres


## creat_engine(':// User name:password@localhost:port/database name')
engine = create_engine('postgresql://postgres:jongbok@localhost:5432/dataeng')
engine.connect()
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


df_iter = pd.read_csv('yellow_tripdata_2021-01.csv.gz', iterator=True, chunksize=100000)
df = next(df_iter)

df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

df.to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

while True: 

        try:
            t_start = time()
            
            df = next(df_iter)

            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

            df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

            t_end = time()

            print('inserted another chunk, took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break



