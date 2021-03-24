import pandas as pd
import gspread
import gspread_dataframe as gd

def get_current_ws():
    gc = gspread.oauth()
    ws=gc.open('My Options Journal').worksheet('data')
    return ws

def get_current_df():
    gc = gspread.oauth()
    ws=gc.open('My Options Journal').worksheet('data')
    df=gd.get_as_dataframe(ws).dropna(how='all').dropna(axis=1,how='all')
    return df

# TODO: Change to append new data
def update_worksheet(df):
    ws=get_current_ws()
    ws.clear()
    gd.set_with_dataframe(ws,df)