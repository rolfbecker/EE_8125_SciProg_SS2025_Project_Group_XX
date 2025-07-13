import pandas as pd
import requests
import io
import pathlib

class DWD_Stations_from_URL:
    def __init__(self, url):
        try:
            res = requests.get(url)
            text_stream = io.StringIO(res.content.decode('cp1252'))
            headers = ["station_id", "date_from", "date_to", "alt", "lat", "lon", "name", "state"]
            df = pd.read_fwf(text_stream, skiprows=2, names=headers, index_col="station_id", parse_dates=["date_from", "date_to"])
            self.created = pd.Timestamp.now()
            self.url = url
            self.df = df
            self.filename = pathlib.Path(url).name
            self.df["is_active"] = (self.created - self.df["date_to"]) <= pd.Timedelta(days=1)
        except Exception as e:
            print(f"An error occurred: {e}")

    def info(self):
        print(f"filename: {self.filename}")
        print(f"url: {self.url}")
        print(f"columns: {[c for c in self.df.columns]}")
        print(f"head(3):\n{self.df.head(3)}")

    def get_ids(self):
        return [idx for idx in self.df.index]

class DWD_SD_10_mins_from_File:
    def __init__(self, pathfilename, tz="UTC"):
        try:
            created = pd.Timestamp.now()
            headers = ["station_id", "meas_date", "qn", "ds_10", "gs_10", "sd_10", "ls_10", "eor"]
            df = pd.read_csv(pathfilename, na_values=[-999, "  -999"], sep=";", names=headers, skiprows=[0],
                             parse_dates=["meas_date"], date_format="%Y%m%d%H%M", index_col="meas_date")
            df.index = df.index.tz_localize(tz)
            self.created = created
            self.url = "file://" + pathlib.Path(pathfilename).name
            self.df = df
            self.filename = pathlib.Path(self.url).name
        except Exception as e:
            print(f"An error occurred: {e}")

    def info(self):
        print(f"created: {self.created}")
        print(f"filename: {self.filename}")
        print(f"url: {self.url}")
        print(f"columns: {[c for c in self.df.columns]}")
        print(f"head(3):\n{self.df.head(3)}")

    def get_ids(self):
        return [idx for idx in self.df.index]
