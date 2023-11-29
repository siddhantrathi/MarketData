"""
Sample Link for 17 March 2023 Data

https://www1.nseindia.com/content/nsccl/fao_participant_oi_17032023.csv

"""

import pandas as pd
import pymongo
from datetime import datetime, timedelta
from bhavcopy import get_prev_timestamps

client = pymongo.MongoClient(
    "mongodb+srv://siddhant:Siddhant123@marketanalysis.gzugfdt.mongodb.net/?retryWrites=true&w=majority")
db = client["market_data"]
col = db["fao_participation_oi"]


def fao_participation_oi(fao_date):

    data = (col.find({"date": fao_date}))
    d = []
    for i in data:
        del i['_id']
        d.append(i)

    date_1 = datetime.today().strftime("%d%m%Y")
    date_2 = fao_date
    start = datetime.strptime(date_1, "%d%m%Y")
    end = datetime.strptime(date_2, "%d%m%Y")
    diff = (start.date() - end.date()).days

    if d != []:
        return [d, 'success']

    elif (((diff < 365) and (diff > -1)) and (end.weekday() < 5)):
        try:
            get_prev_timestamps(1, end.strftime('%d-%b-%Y'))
            # print(pd.read_csv(
            #     f'https://archives.nseindia.com/content/nsccl/fao_participant_oi_{fao_date}.csv'))
            df = pd.read_csv(
                f'https://archives.nseindia.com/content/nsccl/fao_participant_oi_{fao_date}.csv')
            headers = df.iloc[0]
            df = pd.DataFrame(df.values[1:], columns=headers).iloc[:, :-1]
            df.columns = df.columns.str.replace('\t', '')
            list_of_data = df.to_dict('records')
            for j in list_of_data:
                j['date'] = fao_date
                x = col.insert_one(j)
            return fao_participation_oi(fao_date)
        except:
            return [[], 'data not found']
    else:
        return [[], 'data not found']


def processed_fao_participation_oi(fao_date):
    fao_data = fao_participation_oi(fao_date)
    x = 1
    previous_fao_data = []
    while True:
        # print((datetime.strptime(fao_date, "%d%m%Y") -
        #       timedelta(days=x)).strftime("%d%m%Y"))
        previous_fao_data = fao_participation_oi(
            (datetime.strptime(fao_date, "%d%m%Y") - timedelta(days=x)).strftime("%d%m%Y"))
        if previous_fao_data[1] == 'success':
            print('in')
            break
        x += 1

    future_position = {'Client': 0, 'DII': 0, 'FII': 0, 'Pro': 0, 'TOTAL': 0}
    future_long_short_ratio = {'Client': 0,
                               'DII': 0, 'FII': 0, 'Pro': 0, 'TOTAL': 0}
    future_long_oi = {'Client': 0, 'DII': 0, 'FII': 0, 'Pro': 0, 'TOTAL': 0}
    future_short_oi = {'Client': 0, 'DII': 0, 'FII': 0, 'Pro': 0, 'TOTAL': 0}
    call_long_oi = {'Client': 0, 'DII': 0, 'FII': 0, 'Pro': 0, 'TOTAL': 0}
    call_short_oi = {'Client': 0, 'DII': 0, 'FII': 0, 'Pro': 0, 'TOTAL': 0}
    put_short_oi = {'Client': 0, 'DII': 0, 'FII': 0, 'Pro': 0, 'TOTAL': 0}
    put_long_oi = {'Client': 0, 'DII': 0, 'FII': 0, 'Pro': 0, 'TOTAL': 0}

    for i in fao_data[0]:
        future_position[i['Client Type']] = int(
            i['Future Index Long']) - int(i['Future Index Short'])
        future_long_short_ratio[i['Client Type']] = str(round(int(
            i['Future Index Long'])/(int(i['Future Index Long']) + int(i['Future Index Short'])) * 100)) + '%'
        future_long_oi[i['Client Type']] = int(i['Future Index Long'])
        future_short_oi[i['Client Type']] = int(i['Future Index Short'])
        call_long_oi[i['Client Type']] = int(i['Option Index Call Long'])
        call_short_oi[i['Client Type']] = int(i['Option Index Call Short'])
        put_long_oi[i['Client Type']] = int(i['Option Index Put Long'])
        put_short_oi[i['Client Type']] = int(i['Option Index Put Short'])

    for j in previous_fao_data[0]:
        future_long_oi[j['Client Type']] = (
            int(j['Future Index Long']) - future_long_oi[j['Client Type']])
        future_long_oi[j['Client Type']] *= -1

        future_short_oi[j['Client Type']] = (
            int(j['Future Index Short']) - future_short_oi[j['Client Type']])
        future_short_oi[j['Client Type']] *= -1

        call_long_oi[j['Client Type']] = (
            int(j['Option Index Call Long']) - call_long_oi[j['Client Type']])
        call_long_oi[j['Client Type']] *= -1

        call_short_oi[j['Client Type']] = (
            int(j['Option Index Call Short']) - call_short_oi[j['Client Type']])
        call_short_oi[j['Client Type']] *= -1

        put_long_oi[j['Client Type']] = (
            int(j['Option Index Put Long']) - put_long_oi[j['Client Type']])
        put_long_oi[j['Client Type']] *= -1

        put_short_oi[j['Client Type']] = (
            int(j['Option Index Put Short']) - put_short_oi[j['Client Type']])
        put_short_oi[j['Client Type']] *= -1

    final_data = [
        {
            'Client Type': 'Client',
            'Future Position': future_position['Client'],
            'Future Long OI': future_long_oi['Client'],
            'Future Short OI': future_short_oi['Client'],
            'Call Long OI': call_long_oi['Client'],
            'Call Short OI': call_short_oi['Client'],
            'Put Long OI': put_long_oi['Client'],
            'Put Short OI': put_short_oi['Client'],
            'Future Long Short Ratio': future_long_short_ratio['Client']
        },
        {
            'Client Type': 'DII',
            'Future Position': future_position['DII'],
            'Future Long OI': future_long_oi['DII'],
            'Future Short OI': future_short_oi['DII'],
            'Call Long OI': call_long_oi['DII'],
            'Call Short OI': call_short_oi['DII'],
            'Put Long OI': put_long_oi['DII'],
            'Put Short OI': put_short_oi['DII'],
            'Future Long Short Ratio': future_long_short_ratio['DII']
        },
        {
            'Client Type': 'FII',
            'Future Position': future_position['FII'],
            'Future Long OI': future_long_oi['FII'],
            'Future Short OI': future_short_oi['FII'],
            'Call Long OI': call_long_oi['FII'],
            'Call Short OI': call_short_oi['FII'],
            'Put Long OI': put_long_oi['FII'],
            'Put Short OI': put_short_oi['FII'],
            'Future Long Short Ratio': future_long_short_ratio['FII']
        },
        {
            'Client Type': 'Pro',
            'Future Position': future_position['Pro'],
            'Future Long OI': future_long_oi['Pro'],
            'Future Short OI': future_short_oi['Pro'],
            'Call Long OI': call_long_oi['Pro'],
            'Call Short OI': call_short_oi['Pro'],
            'Put Long OI': put_long_oi['Pro'],
            'Put Short OI': put_short_oi['Pro'],
            'Future Long Short Ratio': future_long_short_ratio['Pro']
        },
        {
            'Client Type': 'TOTAL',
            'Future Position': future_position['TOTAL'],
            'Future Long OI': future_long_oi['TOTAL'],
            'Future Short OI': future_short_oi['TOTAL'],
            'Call Long OI': call_long_oi['TOTAL'],
            'Call Short OI': call_short_oi['TOTAL'],
            'Put Long OI': put_long_oi['TOTAL'],
            'Put Short OI': put_short_oi['TOTAL'],
            'Future Long Short Ratio': future_long_short_ratio['TOTAL']
        },
    ]
    return [final_data, 'success']


# print(fao_participation_oi('31032023'))

# for i in range(365):
# 	# current dateTime
# 	today = datetime.today() - timedelta(days=i)
# 	# convert to date String
# 	date = today.strftime("%d%m%Y")

# 	try:
# 		fao_participation_oi(date)
# 	except:
# 		pass

# 	i += 1
