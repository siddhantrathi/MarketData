import pandas as pd
import pymongo
from datetime import datetime, timedelta
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
from bhavcopy import get_prev_timestamps


def convert_timestamps_to_datetime(data_list):
    for item in data_list:
        timestamp_str = item.get("TIMESTAMP")
        if timestamp_str:
            try:
                timestamp_obj = datetime.strptime(timestamp_str, "%d-%b-%Y")
                item["Date_obj"] = timestamp_obj
            except ValueError:
                print(f"Error converting timestamp: {timestamp_str}")
    return data_list


def add_data():
    client = pymongo.MongoClient(
        "mongodb+srv://siddhant:Siddhant123@marketanalysis.gzugfdt.mongodb.net/?retryWrites=true&w=majority")
    db = client["market_data"]
    col = db['bhavcopy']
    i = 0
    j = 0
    inserted = False
    date = None
    dt = None
    data_added_till = datetime.strptime(
        open('data_added_till.txt', "r").read(), '%d-%b-%Y')
    print((datetime.today() - data_added_till).days)
    while j < (datetime.today() - data_added_till).days:
        print(j)
        try:
            date = (datetime.today() - timedelta(days=j))

            day = date.strftime('%d')
            month = date.strftime('%b').upper()
            year = date.strftime('%Y')
            get_prev_timestamps(1, date.strftime('%d-%b-%Y'))
            resp = urlopen(
                f"https://archives.nseindia.com//content/historical/DERIVATIVES/{year}/{month}/fo{day}{month}{year}bhav.csv.zip", timeout=3)
            myzip = ZipFile(BytesIO(resp.read()))
            df = pd.read_csv(myzip.open(
                f'fo{day}{month}{year}bhav.csv'))
            df['Date_obj'] = df["TIMESTAMP"]
            col.insert_many(convert_timestamps_to_datetime(
                df.to_dict('records')))
            print('inserted')
            inserted = True
            if i == 0:
                dt = date
            i += 1
        except Exception as e:
            print(e)
            pass
        j += 1
    with open('data_added_till.txt', 'w') as f:
        f.write(dt.strftime('%d-%b-%Y'))

    return "success"
