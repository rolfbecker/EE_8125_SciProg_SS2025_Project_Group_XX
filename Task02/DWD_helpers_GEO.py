# WINDOWS Anaconda Problem with PROJ_LIB (projection library)! 
# Correct wrong environment variable value (e.g. occurring when using OSGeo4W installer)

PROJ_LIB_PROBLEM = True
print(f"In DWD_helpers_GEO.py: {PROJ_LIB_PROBLEM=}")
print(f"Should be set to true if you encounter problems with the projection library pyproj.")

if PROJ_LIB_PROBLEM:
    import os
    proj_lib = os.environ['proj_lib']
    print(f"OLD {proj_lib=}")
    #-> C:\OSGeo4W64\share\proj (wrong!)
    
    conda_prefix = os.environ['conda_prefix']
    print(f"{conda_prefix=}")
    os.environ['proj_lib'] = conda_prefix + r"\Library\share\proj"
    proj_lib = os.environ['proj_lib']
    print(f"NEW {proj_lib=}")
    # print(f"New env var value: \nPROJ_LIB={proj_lib:s}")
    #-> C:\Users\me\Anaconda3\envs\geo\Library\share\proj (correct!)
    # Now pyproj should work
    import pyproj
    print(f"{pyproj.datadir.get_data_dir()=}") 


import pandas as pd
import requests
import io
import pathlib
import geopandas as gpd
#import pyproj
from shapely.geometry import Point

class DWD_Stations_gdf_from_URL:

    def __init__(self, url, UTM = False):

        try:
            created = pd.Timestamp.now()
            res = requests.get(url)
            text_stream = io.StringIO(res.content.decode('cp1252'))
            headers=["station_id", "date_from", "date_to", "alt", "lat", "lon",  "name", "state"]
            df = pd.read_fwf(text_stream, skiprows=2, names=headers, index_col = 0, parse_dates=["date_from","date_to"])
            df["is_active"] = ((created - df["date_to"]) <= pd.Timedelta(days=1))

            gdf = gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df.lon, df.lat),crs="EPSG:4326",)

            # reproject if neccessary
            if UTM:
                self.crs = "EPSG:25832"
                gdf = gdf.to_crs(self.crs)
            else:
                self.crs = "EPSG:4326"

            self.created = created
            self.gdf = gdf
            self.url = url
            self.filename = pathlib.Path(url).name 

        except Exception as e:
            print(f"An error occurred: {e}")
#            raise
            
    def info(self):
        print(f"created: {self.created}")
        print(f"filename: {self.filename}")
        print(f"url: {self.url}")
        print(f"columns: {[c for c in self.gdf.columns]}")
        print(f"crs: {self.crs}")
        print(f"head(3):\n{self.gdf.head(3)}")

    def get_ids(self):
        return [idx for idx in self.df.index]
