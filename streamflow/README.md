# Scripts for processing streamflow data go here

## Reynolds Creek
The original data are called `reynolds-creek-<basin_id>-hourly-streamflow.dat` The script to process the data is `reynolds_streamflow.py`. The resulting data are daily averaged streamflow values with the name: `<basin_id>_streamflow_qc.txt` and these are meant to be in the format of the USGS daily streamflow data. I removed the header of the original data to `<basin_id>.metadata`.

## TODO:
* Process data for houly, if time permits.
