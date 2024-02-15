import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import s3fs
import time
import sys

from ecco_s3_retrieve import *
import time

if __name__ == '__main__':
    if sys.argv[1] == 'dask-parallel':
        from dask.distributed import Client

        client = Client("tcp://127.0.0.1:39333")
        print(client)

        file_list = ecco_podaac_s3_open(ShortName="ECCO_L4_TEMP_SALINITY_LLC0090GRID_MONTHLY_V4R4",\
                                StartDate="2010-01",EndDate="2010-12")

        ds = xr.open_mfdataset(file_list, engine='h5netcdf', \
                       data_vars='minimal',coords='minimal',\
                       compat='override', parallel=True,
                       decode_cf=False,)

        client.close()

    if sys.argv[1] == 'disk':

        ecco_podaac_s3_get(ShortName="ECCO_L4_TEMP_SALINITY_LLC0090GRID_MONTHLY_V4R4",\
                   StartDate="2010-01",EndDate="2010-12",\
                   n_workers=1)

        ds = xr.open_mfdataset("/home/jovyan/Downloads/ECCO_V4r4_PODAAC/ECCO_L4_TEMP_SALINITY_LLC0090GRID_MONTHLY_V4R4/*.nc",\
                       data_vars='minimal',coords='minimal',\
                       compat='override',)
