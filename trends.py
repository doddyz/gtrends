# Se focaliser sur trends over time line graphs pour liste de mots clés a surveiller
# Next is gspread integration for autovisualizations in Sheets & then DF 
# Forms in Colab for interactive kwd input if possible

# !pip install pytrends

import pandas as pd
import numpy as np
import seaborn as sns
from pytrends.request import TrendReq
# from google.colab import files

# pytrends.build_payload(KWD_LIST, timeframe='today 5-y')
# pytrends.interest_over_time()
# pytrends.related_queries()


TIMEFRAMES = ['all', 'today 5-y', 'today 12-m', 'today 3-m', 'today 1-m', 'today 7-d', 'today 1-d', 'today 1-H', 'today 4-H']

COUNTRIES = {'AU': 'Australia',
  'AT': 'Austria',
  'BE': 'Belgium',
  'CA': 'Canada',
  'CZ': 'Czechia',
  'DK': 'Denmark',
  'FI': 'Finland',
  'FR': 'France',
  'DE': 'Germany',
  'HK': 'Hong Kong',
  'HU': 'Hungary',
  'IE': 'Ireland',
  'IT': 'Italy',
  'JP': 'Japan',
  'NL': 'Netherlands',
  'NZ': 'New Zealand',
  'NO': 'Norway',
  'PL': 'Poland',
  'PT': 'Portugal',
  'SG': 'Singapore',
  'ZA': 'South Africa',
  'ES': 'Spain',
  'SE': 'Sweden',
  'CH': 'Switzerland',
  'TW': 'Taiwan',
  'UK': 'United Kingdom',
  'US': 'United States'}

KWD_LIST = ['pfizer', 'astrazeneca', 'moderna']
DEFAULT_TIMEFRAME = 'today 12-m'

# KWD_LIST = ['touch tool', 'multi tool']

# Refine tz param value to uk local value, see live params in web trends tool 
pytrends = TrendReq(hl='en-US', tz=360)

def interest_over_time(kwd_list, geo_code='US', timeframe=DEFAULT_TIMEFRAME, gprop='', export=0):
    # Empty geo param to get a list of countries with interest
    pytrends.build_payload(kwd_list, geo=geo_code, timeframe=timeframe, gprop=gprop)
    df = pytrends.interest_over_time()
    if (export == 0):
        return df
    else:
        plot_title = ', '.join(kwd_list) + ' interest over time'
        return df.plot(subplots=False, sharex=False, title=plot_title)


#geoCode will be infered here from file data columns language name
# This func explicitely exports as csv requested related queries as not easy to visualise different languages dfs (not a priority actually)
def related_queries(kwds_csv_file, timeframe=DEFAULT_TIMEFRAME, query_type='top'):

    df = pd.read_csv(kwds_csv_file)
    
    list_of_dfs = []

    for col in df.columns:
        # Check if required to convert this to a list
        kwd_list = list(df[col].values)
        n = len(kwd_list)
        geo_location = 'US' if col.upper() == 'EN' else col.upper()
        
        pytrends.build_payload(kwd_list, cat=0, timeframe=timeframe, geo=geo_location, gprop='')
        for i in range(0, n):
            if query_type == 'mix':
                df1 = pytrends.related_queries()[kwd_list[i]]['top']
                df2 = pytrends.related_queries()[kwd_list[i]]['rising']
                q1, q2 = df1['query'], df2['query']
                v1, v2 = df1['value'], df2['value']
                t1, t2 = pd.Series(np.full_like(q1, 'top')), pd.Series(np.full_like(q2, 'rising'))
                col1 = pd.concat([q1, q2], ignore_index=True)
                col2 = pd.concat([v1, v2], ignore_index=True)
                col3 = pd.concat([t1, t2], ignore_index=True)
                df = pd.DataFrame({'query': col1, 'value': col2, 'query_type': col3})

            else:
                df = pytrends.related_queries()[kwd_list[i]][query_type]

            list_of_dfs.append(df)
        
        for i in range(0, n):
            export_filename = 'related_queries_' + kwd_list[i] + '_' + query_type + '_' + col + '.csv'
            list_of_dfs[i].to_csv(export_filename, index=False)
            files.download(export_filename)


    
def related_queries_us(kwd_list, timeframe=DEFAULT_TIMEFRAME, geoCode='US', query_type='top', export=0):
    n = len(kwd_list)
    list_of_dfs = []
    pytrends.build_payload(kwd_list, cat=0, timeframe=timeframe, geo=geoCode, gprop='')
    for i in range(0, n):
        if query_type == 'mix':
            df1 = pytrends.related_queries()[kwd_list[i]]['top']
            df2 = pytrends.related_queries()[kwd_list[i]]['rising']
            q1, q2 = df1['query'], df2['query']
            v1, v2 = df1['value'], df2['value']
            t1, t2 = pd.Series(np.full_like(q1, 'top')), pd.Series(np.full_like(q2, 'rising'))
            col1 = pd.concat([q1, q2], ignore_index=True)
            col2 = pd.concat([v1, v2], ignore_index=True)
            col3 = pd.concat([t1, t2], ignore_index=True)
            df = pd.DataFrame({'query': col1, 'value': col2, 'query_type': col3})

        else:
            df = pytrends.related_queries()[kwd_list[i]][query_type]
        list_of_dfs.append(df)
        
    if export == 0:
        return list_of_dfs[0] if n == 1 else list_of_dfs 
    else:
        for i in range(0, n):
            export_filename = 'related_queries_' + kwd_list[i] + '_' + query_type + '.csv'
            list_of_dfs[i].to_csv(export_filename, index=False)
            files.download(export_filename)
            

# Will be used to get US (for en lang) & any geo location related queries (for non en langs)
def related_queries_simple(geoCode='US', timeframe=DEFAULT_TIMEFRAME, query_type='top', export=0):
    pytrends.build_payload(kwd_list, cat=0, timeframe=timeframe, geo=geoCode, gprop='')
    export_filename = 'related_queries_' + query_type + '.csv'
    if query_type == 'mix':
        df1 = pytrends.related_queries()[kwd_list[0]]['top']
        df2 = pytrends.related_queries()[kwd_list[0]]['rising']
        q1, q2 = df1['query'], df2['query']
        v1, v2 = df1['value'], df2['value']
        t1, t2 = pd.Series(np.full_like(q1, 'top')), pd.Series(np.full_like(q2, 'rising'))
        col1 = pd.concat([q1, q2], ignore_index=True)
        col2 = pd.concat([v1, v2], ignore_index=True)
        col3 = pd.concat([t1, t2], ignore_index=True)
        df = pd.DataFrame({'query': col1, 'value': col2, 'query_type': col3})

    else:
        df = pytrends.related_queries()[kwd_list[0]][query_type]
    if export == 0:
        return df
    else:
        df.to_csv(export_filename, index=False)


# Remove zero low country data, sort country data by descending interest
def interest_by_country(kwd_list, geoCode='US', timeframe=DEFAULT_TIMEFRAME, export=0):
    # Empty geo param to get a list of countries with interest
    pytrends.build_payload(kwd_list, cat=0, timeframe=timeframe, geo=geoCode, gprop='')
    export_filename = 'interest_by_country' + '.csv'
    df = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=True)
    # Create a Tmp column to map geoCodes to target/marketed country names only
    df['Tmp'] = df['geoCode'].map(COUNTRIES)
    # Remove non targeted countries from dataframe
    df.dropna(inplace=True)
    # Remove Tmp colummn before export
    df.drop('Tmp', axis=1, inplace=True)
    # Finally sort dataframe by descending search interest
    df.sort_values(by=kwd_list[0], ascending=False, inplace=True) 
    if export == 0:
        return df
    else:
        df.to_csv(export_filename)
        files.download(export_filename)
                                          

# Utilities

def get_key_from_value(dico, value):
    for k in dico.keys():
        if dico[k] == value:
            return k

#Debug Code
# df = pd.read_csv('translation-for-trends.csv')
# for col in df.columns:
#         # Check if required to convert this to a list
#     kwd_list = list(df[col].values) 
#     print(col.upper(), kwd_list)
