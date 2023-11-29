"""
Link For Data: https://www1.nseindia.com/content/historical/DERIVATIVES/2023/MAR/fo29MAR2023bhav.csv.zip

"""

import pandas as pd
import pymongo
from datetime import datetime, timedelta
import json


client = pymongo.MongoClient(
    "mongodb+srv://siddhant:Siddhant123@marketanalysis.gzugfdt.mongodb.net/?retryWrites=true&w=majority")
db = client["market_data"]
col = db['bhavcopy']
index_future_and_option_data_db = db['index_future_and_option_data']


def get_prev_timestamps(no_of_days, starting_date):
    with open('working_days.json') as f:
        working_days = json.load(f)

    x = (working_days[working_days.index(starting_date) -
                      (no_of_days - 1):working_days.index(starting_date) + (1)])
    j = []
    for i in x:
        j.append({"Date": i})

    print(j)

    return j


def get_prev_data(days, date):
    date = date.split('-')
    date = datetime.strptime(
        f'{date[0]}-{date[1].lower()}-{date[2]}', '%d-%b-%Y')

    last_7_days_data = []
    no_of_days_data_fetched = 0
    x = 0
    while no_of_days_data_fetched != days:
        data = index_future_and_option_data_raw(((date - timedelta(days=x)).strftime('%d')) + '-' + (
            (date - timedelta(days=x)).strftime('%b')).upper() + '-' + ((date - timedelta(days=x)).strftime('%Y')), 'FUTIDX')
        if data['response'] == 'not_found':
            if x == 0:
                return ['data_not_found']
            x += 1
            continue

        last_7_days_data.extend(data['data'])
        x += 1
        no_of_days_data_fetched += 1

    return last_7_days_data


def index_future_and_option_data_raw(date, instrument):
    data = {'response': 'not_found', 'data': []}
    for x in col.find({"SYMBOL": "NIFTY", "TIMESTAMP": date, "INSTRUMENT": instrument}):
        del x['_id']
        x['TIMESTAMP'] = x['TIMESTAMP'].split('-')
        x['TIMESTAMP'] = x['TIMESTAMP'][0] + '-' + \
            (x['TIMESTAMP'][1]).capitalize() + '-' + x['TIMESTAMP'][2]
        data['data'].append(x)
        if data['data'] == []:
            data['response'] = 'not_found'
        else:
            data['response'] = 'success'
    return data


def index_future_and_option_data(date):
    date_latest = date
    date_latest = date_latest.split('-')
    date_latest = date_latest[0] + '-' + \
        (date_latest[1]).capitalize() + '-' + date_latest[2]

    data_added_till = datetime.strptime(
        open('data_added_till.txt', "r").read(), '%d-%b-%Y')
    if (datetime.strptime(date_latest, '%d-%b-%Y') > data_added_till):
        return ['data_not_found']

    try:
        a = get_prev_timestamps(7, date_latest)
    except:
        return ['data_not_found']

    x = get_prev_data(1, date)
    if x[0] == 'data_not_found':
        return x

    a.reverse()

    df = pd.DataFrame.from_dict(x)
    df['EXPIRY_DT'] = pd.to_datetime(df['EXPIRY_DT'], format='%d-%b-%Y')
    nearest_expiry = df.sort_values(by='EXPIRY_DT')[
        'EXPIRY_DT'].iloc[0]
    # df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], format='%d-%b-%Y')

    # timestamps =((df.TIMESTAMP.unique()[0]).astype('datetime64[s]').item()).strftime()
    timestamps = pd.DataFrame.from_dict(a)
    timestamps['Date'] = (pd.to_datetime(
        timestamps['Date'], format='%d-%b-%Y'))
    timestamps = timestamps['Date'].unique()
    # print(nearest_expiry)

    final_data = []
    for i in timestamps:

        print(i)

        c = (index_future_and_option_data_db.find(
            {"Date": (i.astype('datetime64[s]').item()).strftime('%d-%b-%Y').upper()}))
        d = []
        for i in c:
            del i['_id']
            d.append(i)

        if d != []:
            final_data.append(d[0])
            continue
        df = pd.DataFrame.from_dict(index_future_and_option_data_raw(
            (i.astype('datetime64[s]').item()).strftime('%d-%b-%Y').upper(), 'FUTIDX')['data'])

        df['EXPIRY_DT'] = pd.to_datetime(df['EXPIRY_DT'], format='%d-%b-%Y')

        nearest_expiry_df = (df.loc[df['EXPIRY_DT'] == nearest_expiry])
        current_exp_fut_value = (nearest_expiry_df['CLOSE'].iloc[0]).item()

        avg_fut_value = round(
            ((nearest_expiry_df['OPEN'].iloc[0] + nearest_expiry_df['HIGH'].iloc[0] + nearest_expiry_df['LOW'].iloc[0])/3), 3).item()

        prev_5_days_data = get_prev_data(5,  (i.astype('datetime64[s]').item()).strftime(
            '%d-%b-%Y'))

        prev_5_days_df = (pd.DataFrame.from_dict(
            prev_5_days_data))
        prev_5_days_df['EXPIRY_DT'] = (pd.to_datetime(
            prev_5_days_df['EXPIRY_DT'], format='%d-%b-%Y'))
        prev_5_days_df['TIMESTAMP'] = (pd.to_datetime(
            prev_5_days_df['TIMESTAMP'], format='%d-%b-%Y'))
        prev_5_days_df = prev_5_days_df.loc[prev_5_days_df['EXPIRY_DT']
                                            == nearest_expiry]
        five_day_avg = round(((prev_5_days_df['OPEN'].sum(
        ) + prev_5_days_df['HIGH'].sum() + prev_5_days_df['LOW'].sum())/15
        ), 3).item()

        prev_3_days_df = prev_5_days_df.sort_values(
            by='TIMESTAMP', ascending=False).iloc[:3]
        prev_3_days_df = prev_3_days_df.loc[prev_3_days_df['EXPIRY_DT']
                                            == nearest_expiry]
        three_day_avg = round(((prev_3_days_df['OPEN'].sum(
        ) + prev_3_days_df['HIGH'].sum() + prev_3_days_df['LOW'].sum())/9), 3).item()

        oi_fut = (df['OPEN_INT']).sum().item()
        prev_one_day_df = (pd.DataFrame.from_dict(prev_5_days_data))
        prev_one_day_df['TIMESTAMP'] = (pd.to_datetime(
            prev_one_day_df['TIMESTAMP'], format='%d-%b-%Y'))
        prev_one_day_df = prev_one_day_df.sort_values(
            by='TIMESTAMP', ascending=False).iloc[3:6]

        percent_change = str(round(
            (((prev_3_days_df['CLOSE'].iloc[0] - prev_3_days_df['CLOSE'].iloc[1]) / prev_3_days_df['CLOSE'].iloc[1]) * 100), 3)) + '%'
        change_in_oi_fut = (
            oi_fut - (prev_one_day_df['OPEN_INT'].sum())).item()

        option_df = pd.DataFrame.from_dict(index_future_and_option_data_raw(
            i.astype('datetime64[s]').item().strftime('%d-%b-%Y').upper(), 'OPTIDX')['data'])
        option_df['EXPIRY_DT'] = pd.to_datetime(
            option_df['EXPIRY_DT'], format='%d-%b-%Y')

        put_call_ratio_nearest_total = round(option_df.loc[option_df['OPTION_TYP'] == 'PE']['OPEN_INT'].sum(
        )/option_df.loc[option_df['OPTION_TYP'] == 'CE']['OPEN_INT'].sum(), 3)

        option_df = option_df.loc[option_df['EXPIRY_DT'] == nearest_expiry]

        put_call_ratio_nearest_monthly_exp = round(option_df.loc[option_df['OPTION_TYP'] == 'PE']['OPEN_INT'].sum(
        )/option_df.loc[option_df['OPTION_TYP'] == 'CE']['OPEN_INT'].sum(), 3)
        final_data.append({'Date': (i.astype('datetime64[s]').item()).strftime(
            '%d-%b-%Y').upper(), 'Current Exp Future Value': current_exp_fut_value,  'Percent Change': percent_change, 'Avg Fut Value': avg_fut_value, '3 Day Avg': three_day_avg, '5 Day Avg': five_day_avg, 'OI Fut': oi_fut, 'Change in OI Fut': change_in_oi_fut, "PCR Total": put_call_ratio_nearest_total, "PCR Nearest Monthly Exp": put_call_ratio_nearest_monthly_exp})

        x = index_future_and_option_data_db.insert_one({'Date': (i.astype('datetime64[s]').item()).strftime(
            '%d-%b-%Y').upper(), 'Current Exp Future Value': current_exp_fut_value, 'Percent Change': percent_change, 'Avg Fut Value': avg_fut_value, '3 Day Avg': three_day_avg, '5 Day Avg': five_day_avg, 'OI Fut': oi_fut, 'Change in OI Fut': change_in_oi_fut, "PCR Total": put_call_ratio_nearest_total, "PCR Nearest Monthly Exp": put_call_ratio_nearest_monthly_exp})

    return (final_data)


def top_5_strikes(date, option_type, expiry=""):

    data_added_till = datetime.strptime(
        open('data_added_till.txt', "r").read(), '%d-%b-%Y')
    if (datetime.strptime(date, '%d-%b-%Y') > data_added_till):
        return ['data_not_found']

    try:
        get_prev_timestamps(1, date)
    except:
        return ['data_not_found']
    prev_5_dates = get_prev_timestamps(5, date)
    df_data = []
    if expiry == "":

        for k, i in enumerate(prev_5_dates):
            for x in (col.find({"SYMBOL": 'NIFTY', "TIMESTAMP": i['Date'].upper(), "OPTION_TYP": option_type})):
                del x['_id']
                y = x['TIMESTAMP'].split('-')
                x["TIMESTAMP"] = y[0] + '-' + y[1].capitalize() + '-' + y[2]
                df_data.append(x)
            if (k == 0) and (df_data == []):
                return ['data_not_found']
    else:
        for a, i in enumerate(prev_5_dates):
            for x in (col.find({"SYMBOL": 'NIFTY', "TIMESTAMP": i['Date'].upper(), "OPTION_TYP": option_type, "EXPIRY_DT": expiry})):
                del x['_id']
                y = x['TIMESTAMP'].split('-')
                x["TIMESTAMP"] = y[0] + '-' + y[1].capitalize() + '-' + y[2]
                df_data.append(x)
            if (a == 0) and (df_data == []):
                return ['data_not_found']

    df = pd.DataFrame.from_dict(df_data)
    if expiry == "":
        df = df.loc[df['EXPIRY_DT'] != date]
    # print(df_data)
    df['TIMESTAMP'] = (pd.to_datetime(df['TIMESTAMP'], format='%d-%b-%Y'))
    df = df.sort_values(by='TIMESTAMP', ascending=False)

    top_5_strikes_df = (df.loc[df['TIMESTAMP'] == (
        datetime.strptime(date, '%d-%b-%Y')).strftime('%Y-%m-%d')]).sort_values(by='OPEN_INT', ascending=False).head().reset_index()

    top_5_strikes_df['Avg Price'] = round((
        top_5_strikes_df['OPEN'] + top_5_strikes_df['HIGH'] + top_5_strikes_df['LOW'])/3, 3)
    five_day_avg = []
    three_day_avg = []

    for index, row in top_5_strikes_df.iterrows():

        x = (df.loc[(df['STRIKE_PR'] == row['STRIKE_PR'])
                    & (df['EXPIRY_DT'] == row['EXPIRY_DT'])])

        x['Avg Price'] = (x['OPEN'] + x['HIGH'] + x['LOW'])/3

        five_day_avg.append(round(x['Avg Price'].sum()/5, 3))
        three_day_avg.append(round(x.head(3)['Avg Price'].sum()/3, 3))

    top_5_strikes_df = top_5_strikes_df.assign(five_day_avg=five_day_avg)
    top_5_strikes_df = top_5_strikes_df.assign(three_day_avg=three_day_avg)

    final_df = top_5_strikes_df.filter(
        ['EXPIRY_DT', 'OPTION_TYP', 'STRIKE_PR', 'OPEN_INT', 'CHG_IN_OI', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'Avg Price', 'five_day_avg', 'three_day_avg'])

    final_df.rename(columns={'five_day_avg': 'Five Day Avg',
                    'three_day_avg': 'Three Day Avg'}, inplace=True)

    return final_df.to_dict('records')


# print(index_future_and_option_data('06-APR-2023'))
# print(top_5_strikes('06-Apr-2023', 'CE'))
# print(get_prev_timestamps(1, '07-Apr-2023'))
