##############################################################
# This sctipt extracts NLDAS forcings for a catchment using  #
# the shape file (or geojson file) of the catchment boundary #
# Define number of cores to do in parallel (line 25)				 #
# by: Hossein Lotfi. Email: agri.meteo@gmail.com						 #
# ############################################################

library(raster)
library(sf)
library(doParallel)
library(dplyr)
library(exactextractr)

# Extract the NLDAS for each year. NLDAS data for each year are stored at 2001, 2002, etc. folders
Year = "2001"
setwd('data/NLDAS')

## Read boundary shape file for Walnut Gulch and Reynolds Creek catchments.
shp_wg = read_sf('data/shp/WG_all_merged.geojson') %>% 
			st_cast('POLYGON')
shp_rc = read_sf('data/shp/RC_all_merged.geojson') %>% 
			st_cast('POLYGON')

## Define number of cores to do paraless
registerDoParallel(cores = 10)

## NLDAS variables name
col_names = c('TMP', # 1) Temperature [C]
							'SPFH', # 2) Specific humidity [kg/kg]
							'PRES', # 3) Pressure [Pa] 
							'UGRD', # 4) u-component of wind [m/s]
							'VGRD', # 5) v-component of wind [m/s]
							'DLWRF', # 6) Downward longwave radiation flux [W/m^2]
							'CONVAPCP', # 7) Cloud Mixing Ratio [kg/m^2]
							'CAPE', # 8) Convective available potential energy [J/kg]
							'PEVAP', # 9) Potential evaporation [kg/m^2]
							'APCP', # 10) Total precipitation [kg/m^2] = mm
							'DSWRF') # 11) Downward shortwave radiation flux [W/m^2]

## List all NLDAS GRIB file in the current directory 
nldas_files =  list.files(path = Year, pattern = '*.grb', full.names = TRUE)
WG_RC_df = foreach(f = nldas_files, .combine = rbind)%dopar%{
							nldas = raster::stack(f)
							names(nldas) = col_names
							df_wg = exact_extract(x = nldas, y = shp_wg, fun=c('mean'))
							df_rc = exact_extract(x = nldas, y = shp_rc, fun=c('mean'))
							res_wg = cbind.data.frame(
												ID = basename(shp_wg$path),
												Year = substr(f, 24, 27),
												Mnth = substr(f, 28, 29),
												Day = substr(f, 30, 31), 
												Hr = substr(f, 33, 34),
												df_wg
								)
							res_rc = cbind.data.frame(
								ID = basename(shp_rc$path),
								Year = substr(f, 24, 27),
								Mnth = substr(f, 28, 29),
								Day = substr(f, 30, 31), 
								Hr = substr(f, 33, 34),
								df_rc
							)
						rbind.data.frame(res_wg, res_rc)
}

data_dir = "data/shp"
saveRDS(WG_RC_df, paste0(data_dir, 'NLDAS_WG_RC_', Year, '.rds'))


stopImplicitCluster()


