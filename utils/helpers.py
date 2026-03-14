import numpy as np
import pandas as pd

def detect_dims(data_array):
    dims = data_array.dims
    time_dim = None
    lat_dim = None
    lon_dim = None

    for d in dims:
        dl = d.lower()
        if "time" in dl:
            time_dim = d
        if "lat" in dl:
            lat_dim = d
        if "lon" in dl or "long" in dl:
            lon_dim = d

    return time_dim, lat_dim, lon_dim


def extract_time_info(dataset, time_dim):
    if not time_dim:
        return None, None, None, None

    time_vals = dataset[time_dim].values

    if len(time_vals) == 0:
        return None, None, None, None

    try:
        time_dt = pd.to_datetime(time_vals)
        all_years = time_dt.year.values.astype(int)
        unique_years = sorted(np.unique(all_years).tolist())
        return time_vals, time_dt, all_years, unique_years
    except Exception:
        all_years = np.arange(len(time_vals))
        unique_years = list(all_years)
        return time_vals, None, all_years, unique_years


def safe_stat(arr, mode="mean"):
    flat = np.array(arr).astype(float).flatten()
    flat = flat[~np.isnan(flat)]

    if len(flat) == 0:
        return "N/A"

    if mode == "mean":
        return round(float(np.mean(flat)), 3)
    if mode == "min":
        return round(float(np.min(flat)), 3)
    if mode == "max":
        return round(float(np.max(flat)), 3)
    return "N/A"


def format_value(val):
    if isinstance(val, (int, float, np.integer, np.floating)):
        return f"{val}"
    return str(val)


def get_variable_options(dataset):
    var_options = {}
    for var in dataset.data_vars:
        long_name = dataset[var].attrs.get("long_name", var)
        units = dataset[var].attrs.get("units", "")
        display_name = f"{long_name} ({units})" if units else long_name
        var_options[display_name] = var
    return var_options
