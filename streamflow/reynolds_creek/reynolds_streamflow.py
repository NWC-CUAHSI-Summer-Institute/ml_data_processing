import numpy as np
import pandas as pd
import glob
import numbers

# Get all the file paths for the data
reynolds_files = glob.glob('*.dat')

# The hourly data in Martin's paper uses these headers
hourly_headers = ['date','QObs(mm/h)','QObs count','qualifiers','utcoffset(h)','(iv-camels)/camels','QObs_CAMELS(mm/h)']

# Set a time period to cut down on file size, mostly for the hourly data
start_date = pd.to_datetime('1/1/1980')
end_date = pd.to_datetime('1/1/2019')

# Loop through the data files and save them in the USGS format
for q_file in reynolds_files:

    print(q_file)

    # The 036 gauge has a different format from the rest, so we treat it as a seperate case
    if q_file == "reynolds-creek-036-hourly-streamflow.dat":

        # Open the file as a pandas dataframe, this will be imortant for getting the daily averages
        with open(q_file, "r") as f:
            df = pd.read_csv(f, delim_whitespace=True, index_col=None)
        
        # Remove the index, since the index (days) has duplicates (24, one for each hour in the day)
        df = df.reset_index()
        
        # Remove the first and last value of the dataframe, because there is some funky formatting
        df = df.iloc[1:-1,:]
        
        # Fill in some additional columns. Make sure all the values are numeric.
        df['Hour'] = [int(df.datetime[i].split(':')[0]) for i in df.index.values]
        df['qcms'] = [float(df.loc[i,'qcms']) for i in df.index.values]
        df['Year'] = [int(df.loc[i,'Year']) for i in df.index.values]
        df['datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour']])
        df['date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
        
        # Now set the index to datetime, so we can get the averages easily
        df = df.set_index('datetime')
        
        # Cut the dataframe to the start and end dates
        df = df.loc[start_date:end_date,:]
        
        #####################################################################
        ############    GET THE MEAN DAILY VALUE    #########################
        df_daily = df.resample('D').mean()          #########################
        ############    GET THE MEAN DAILY VALUE    #########################
        #####################################################################
        
        # The gauge id is part of the file name, so add it to the "full" id
        df_daily['basin_id'] = 'RC13172'+q_file.split('-')[2]
        
        # This probably isn't neccessary, but the USGS streamflow values have a quality flag. This is a fake flag.
        df_daily['flag'] = 'si'
        
        # Convert the data from cubic meter per second to cubic feet per second
        df_daily['qcfs'] = df_daily['qcms'] * 35.3147
        
        # Extract just the columns we need, and make sure the dates are integers, just in case.
        df_daily = df_daily[['basin_id', 'Year', 'Month', 'Day', 'qcfs', 'flag']] 
        df_daily['Year'] = [int(df_daily.loc[i,'Year']) for i in df_daily.index.values]
        df_daily['Month'] = [int(df_daily.loc[i,'Month']) for i in df_daily.index.values]
        df_daily['Day'] = [int(df_daily.loc[i,'Day']) for i in df_daily.index.values]
        
        # Write the data out to a csv file
        df_daily.to_csv('{}_streamflow_qc.txt'.format(df_daily.basin_id[1], sep="\s"))

    else:

        # Open the file as a pandas dataframe, this will be imortant for getting the daily averages
        with open(q_file, "r") as f:
            df = pd.read_csv(f, index_col=None)
        
        # Remove the index, since the index (days) has duplicates (24, one for each hour in the day)
        df = df.reset_index()
        
        # Remove the first and last value of the dataframe, because there is some funky formatting
        df = df.iloc[1:-1,:]
        
        # Fill in some additional columns. Make sure all the values are numeric.
        df['qcms'] = [float(df.loc[i,'qcms']) for i in df.index.values]
        df['Year'] = [pd.to_datetime(df.loc[i,'datetime']).year for i in df.index.values]
        df['Month'] = [pd.to_datetime(df.loc[i,'datetime']).month for i in df.index.values]
        df['Day'] = [pd.to_datetime(df.loc[i,'datetime']).day for i in df.index.values]
        df['Hour'] = [pd.to_datetime(df.loc[i,'datetime']).hour for i in df.index.values]
        df['datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour']])
        df['date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
        
        # Now set the index to datetime, so we can get the averages easily
        df = df.set_index('datetime')
        
        # Cut the dataframe to the start and end dates
        df = df.loc[start_date:end_date,:]
        
        #####################################################################
        ############    GET THE MEAN DAILY VALUE    #########################
        df_daily = df.resample('D').mean()          #########################
        ############    GET THE MEAN DAILY VALUE    #########################
        #####################################################################
        
        # The gauge id is part of the file name, so add it to the "full" id
        df_daily['basin_id'] = 'RC13172'+q_file.split('-')[2]
        
        # This probably isn't neccessary, but the USGS streamflow values have a quality flag. This is a fake flag.
        df_daily['flag'] = 'si'
        
        # Convert the data from cubic meter per second to cubic feet per second
        df_daily['qcfs'] = df_daily['qcms'] * 35.3147
        
        # Fill in some additional columns. Make sure all the values are numeric.
        df_daily = df_daily[['basin_id', 'Year', 'Month', 'Day', 'qcfs', 'flag']] 
        df_daily['Year'] = [int(df_daily.loc[i,'Year']) for i in df_daily.index.values]
        df_daily['Month'] = [int(df_daily.loc[i,'Month']) for i in df_daily.index.values]
        df_daily['Day'] = [int(df_daily.loc[i,'Day']) for i in df_daily.index.values]
        
        # Write the data out to a csv file
        df_daily.to_csv('{}_streamflow_qc.txt'.format(df_daily.basin_id[1], sep="\s"))
