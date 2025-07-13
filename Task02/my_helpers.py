import pandas as pd
import numpy as np

def matnos_to_doy(matno1, matno2=99999, seed=0, year=2023):
    '''
    Creates a pseudo random day of year (doy) from one or two matriculation numbers.
    Input:  matno1: matriculation number,  10000 <= matno1 <= 99999
            matno2: second matriculation number,  10000 <= matno2 <= 99999
            seed:   integer number modulating the output, if the resulting date for seed=0 is not wanted.
            year:   integer number representing the year. It is tested if it is a leap year.
    Output: integer number, 1 <= doy <= 365 (1 <= doy <= 366 for a leap year)
    '''
    if not (10000 <= matno1 <= 99999):
        raise ValueError("Matriculation number 1 must be a 5-digit integer.")
    if not (10000 <= matno2 <= 99999):
        raise ValueError("Matriculation number 2 must be a 5-digit integer.")

    number = np.int64(matno1) * np.int64(matno2) * np.int64(year) + np.int64(seed)
   
    random_value = xorshift64(number) # The pseudo random sequence generator

    if pd.Period(year).is_leap_year:   
        day_of_year = random_value % 366 + 1
    else:
        day_of_year = random_value % 365 + 1

    return day_of_year
    

def xorshift64(state):
    x = state
    x ^= x << 13
    x ^= x >> 7
    x ^= x << 17
    return x


def doy_to_date(doy, year):
    # Start from the first day of the given year
    date = pd.Timestamp(year, 1, 1) + pd.Timedelta(days = doy-1)
    return date


def matnos_to_date_full_year(matno1, matno2=99999, seed=0, year=2023):
    '''
    Creates a pseudo random date (timestamp) from one or two matriculation numbers for the given year.
    Input:  matno1: matriculation number,  10000 <= matno1 <= 99999
            matno2: second matriculation number,  10000 <= matno2 <= 99999
            seed:   integer number modulating the output, if the resulting date for seed=0 is not wanted.
            year:   integer number representing the year
    Output: pandas timestamp of a pseudo random day in the given year
    '''
    if not (10000 <= matno1 <= 99999):
        raise ValueError("Matriculation number 1 must be a 5-digit integer.")
    if not (10000 <= matno2 <= 99999):
        raise ValueError("Matriculation number 2 must be a 5-digit integer.")

    doy = matnos_to_doy(matno1, matno2, seed, year)
    return doy_to_date(doy, year)


def matnos_to_date(matno1, matno2=99999, seed=0, date_from="2022-01-01", date_to="2022-12-31", tz="CET"):
    '''
    Creates a pseudo random date (timestamp) between two date limits from one or two matriculation numbers 
    Input:  matno1:    integer, matriculation number,  10000 <= matno1 <= 99999
            matno2:    integer, second matriculation number,  10000 <= matno2 <= 99999
            seed:      integer, modulating the random generator, if the resulting date for seed=0 is not wanted.
            date_from: date string, lower limit of the date range the random output date is chosen from
            date_to:   date string, upper limit of the date range the random output date is chosen from
            tz:        time zone
    Output: pandas timestamp with time zone of a pseudo random day in the given date range
    '''
    if not (10000 <= matno1 <= 99999):
        raise ValueError("Matriculation number 1 must be a 5-digit integer.")
    if not (10000 <= matno2 <= 99999):
        raise ValueError("Matriculation number 2 must be a 5-digit integer.")

    
    # The random generator
    year = pd.Timestamp(date_from).year
    number = np.int64(matno1) * np.int64(matno2) * np.int64(year) + np.int64(seed)
    random_value = xorshift64(number) # The pseudo random sequence generator
    
    #print(f"{number:d}")
    
    # Limit the random value to the number of days in the date range    
    N = (pd.Timestamp(date_to) - pd.Timestamp(date_from)).days
    n = random_value % (N+1) 

    # Convert to date, add time zone
    final_date = pd.Timestamp(date_from) + n*pd.Timedelta("1 day")
    final_date = final_date.tz_localize(tz)
    
    return final_date, n


def ts_to_ms_since_1970(ts):
    return (ts - pd.Timestamp("1970-01-01").tz_localize(ts.tz)) // pd.Timedelta('1ms')


def gen_HSRW_weather_station_grafana_URL(start_date, end_date):
    start_date_ux = ts_to_ms_since_1970(start_date)
    end_date_ux = ts_to_ms_since_1970(end_date)

    HSRW_grafana_URL = \
        "https://weather.eolab.de/grafana/public-dashboards/" \
        + "66f207ccd80c47d385996f80d5341708" \
        + "?orgId=1&" \
        + f"from={start_date_ux}&to={end_date_ux}"
    
    return HSRW_grafana_URL
    