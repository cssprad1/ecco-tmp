import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import s3fs
import time
import sys

from ecco_s3_retrieve import *
import time
import multiprocessing

if __name__ == '__main__':
    print(f'CPU: {multiprocessing.cpu_count()}')
    sd = '2000-01'
    ed = '2010-12'
    engine = 'h5netcdf'
    print(f'Start: {sd}\nEnd: {ed}')
    print(f'Engine: {engine}')
    if sys.argv[1] == 'dask-parallel':
        from dask.distributed import Client

        client = Client()
        print(client)
        st = time.time()

        file_list = ecco_podaac_s3_open(ShortName="ECCO_L4_TEMP_SALINITY_LLC0090GRID_MONTHLY_V4R4",\
                                StartDate=sd,EndDate=ed)

        ds = xr.open_mfdataset(file_list, engine=engine, \
                       data_vars='minimal',coords='minimal',\
                       compat='override', parallel=True,
                       decode_cf=False,)

        et = time.time()
        print(f'[dask] {et-st}')
        client.close()

    if sys.argv[1] == 'disk':
        st = time.time()

        ecco_podaac_s3_get(ShortName="ECCO_L4_TEMP_SALINITY_LLC0090GRID_MONTHLY_V4R4",\
                   StartDate=sd,EndDate=ed,\
                   n_workers=1, download_root_dir='/tmp')

        ds = xr.open_mfdataset("/tmp/ECCO_L4_TEMP_SALINITY_LLC0090GRID_MONTHLY_V4R4/*.nc",\
                       data_vars='minimal',coords='minimal',\
                       compat='override', decode_cf=False, engine=engine)
        et = time.time()
        print(f'[disk] {et-st}')
