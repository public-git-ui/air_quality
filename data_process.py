from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np
    
def convert_format_and_clean_up(value): 
    try: 
        return float(value)
    except: 
        return np.nan

def process_sensors_data(df_data):
    df = df_data.copy()
    df['value'] = df["value"].apply(convert_format_and_clean_up)
    
    all_pm_data = []
    df["day_hour"] = df["timestamp"].str.slice(0, 13)
    for parameter in df.parameter.unique()[:5]:
        df_pm = df[df.parameter == parameter].copy()
        location_df = df_pm[["longitude", "latitude", "location_id", "location"]].drop_duplicates()
        location_id_list = list(df_pm.location_id.unique())
        max_time= datetime.strptime(max(df_pm["day_hour"]), '%Y-%m-%d %H')
        min_time = datetime.strptime(min(df_pm["day_hour"]), '%Y-%m-%d %H')
        all_days_datetime = list(pd.date_range(min_time,max_time,freq='h'))
        max_time = max(df_pm["day_hour"])
        all_days_string = [str(d)[:13] for d in all_days_datetime if str(d)[:13]< max_time]
        df_day_hour = pd.DataFrame(all_days_string, columns = ["day_hour"])
        df_day_hour["location_id"] = [location_id_list]*len(df_day_hour)
        df_combined = df_day_hour.explode("location_id").copy()
        df_pm_by_hour = df_pm.groupby(["day_hour", "location_id"])["value"].mean().reset_index()
        grouped = df_pm_by_hour.merge(df_combined, how = "right", on=["day_hour", "location_id"])
        concat_df = []
        filled_dataset = []
        for location in location_id_list: 
            filtered = grouped[grouped.location_id == location].copy()
            filled_dataset = filtered["value"].ffill().bfill()
            rolling = filled_dataset.rolling(window=25, min_periods=1, win_type = "gaussian").mean(std = 3)
            filtered["rolling"] = rolling.values
            filtered["recorded_and_predicted_value"] =  filtered.apply(lambda x: x['value'] if x['value'] > 0 else x['rolling'], axis=1)
            filtered["location_id"] = location
            concat_df.append(filtered)
        imputed_df = pd.concat(concat_df, axis = 0)
        final_df = imputed_df.merge(location_df, on = "location_id")
        final_df["parameter"] = parameter
        all_pm_data.append(final_df)
    data_to_save = pd.concat(all_pm_data, axis = 0).drop(columns = ["rolling"])
    return data_to_save