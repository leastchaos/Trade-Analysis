import pandas as pd
import numpy as np
# Raw Data

def merge_symbol(df):
    df['Ticker'] = df['Symbol'].where(
        df['UnderlyingSymbol'].isnull(), df['UnderlyingSymbol'])
    return df


def get_strategy(df):
    df['Strategy'] = None
    df.loc[df['AssetClass'] == 'STK', 'Strategy'] = 'Stock'

    short_put = ((df['Open/CloseIndicator'] == 'O')
                 & (df['Buy/Sell'] == 'SELL')
                 & (df['Put/Call'] == 'P'))
    short_call = ((df['Open/CloseIndicator'] == 'O')
                  & (df['Buy/Sell'] == 'SELL')
                  & (df['Put/Call'] == 'C'))
    long_put = ((df['Open/CloseIndicator'] == 'O')
                & (df['Buy/Sell'] == 'BUY')
                & (df['Put/Call'] == 'P'))
    long_call = ((df['Open/CloseIndicator'] == 'O')
                 & (df['Buy/Sell'] == 'BUY')
                 & (df['Put/Call'] == 'C'))

    df.loc[short_put, 'Strategy'] = 'Short Put'
    df.loc[short_call,'Strategy']='Short Call'
    df.loc[long_put, 'Strategy'] = 'Long Put'
    df.loc[long_call,'Strategy']='Long Call'

    return df

def drop_stock(df):
    df=df[df.Strategy!='Stock']
    return df

def group_trades(df):
    df['Put/Call']=df['Put/Call'].where(df['AssetClass']=='OPT','S')
    df_grouped=df.groupby(group_columns)
    df['TradeDateImp']=group_trade_date(df_grouped,df)
    df['Quantity']=group_quantity(df_grouped)
    return df

def group_close_price(df):
    df['adjusted_close_volume']=df['Quantity']*df['ClosePrice']
    df['adjusted_close']=df.groupby(group_columns)['adjusted_close_volume'].transform('sum')
    df['adjusted_close']=df['adjusted_close_volume']/df['Quantity']
    
def group_quantity(df_grouped):
    return df_grouped['Quantity'].transform('sum')

def group_trade_date(df_grouped,df):
    tmp_trade_date_max=df_grouped['TradeDate'].transform('max')
    tmp_trade_date_min=df_grouped['TradeDate'].transform('min')
    return tmp_trade_date_max.where(df['Open/CloseIndicator']=='C',tmp_trade_date_min)

def drop_duplicates(df):
    return df.drop_duplicates(group_columns)

def extract_relevant_columns(df,columns=['ClientAccountID','Symbol','Open/CloseIndicator','Ticker','Strategy','Expiry','Strike','Quantity','TradeDate','ClosePrice']):
    return df[columns]

def merge_open_close(df_rel):
    df_close=df_rel.loc[df_rel['Open/CloseIndicator']=='C'].drop(['Open/CloseIndicator','Ticker','Strategy'],axis=1)
    df_open=df_rel.loc[df_rel['Open/CloseIndicator']=='O'].drop(['Open/CloseIndicator',],axis=1)
    df=df_open.merge(df_close,on=['Symbol','Expiry','Strike',],suffixes=('_Open','_Close'),how='left')
    return df

## Analysis
def get_capital_usage(df):
    column='Capital'
    df[column]=None
    df[column]=df[column].where(df.Strategy!='Short Put',(df['Strike']-df['ClosePrice_Open'])*df['Quantity_Open']*-100)
    df[column]=df[column].where(df.Strategy!='Long Put',(df['ClosePrice_Open'])*df['Quantity_Open']*100)
    df[column]=df[column].where(df.Strategy!='Short Call',(df['Strike'])*df['Quantity_Open']*-100)
    df[column]=df[column].where(df.Strategy!='Long Call',(df['ClosePrice_Open'])*df['Quantity_Open']*100)
    df[column]=df[column].where(df.Strategy!='Stock',(df['ClosePrice_Open'])*df['Quantity_Open']*100)
    return df

def get_profit(df):
    column='Profit'
    df[column]=None
    df[column]=df[column].where(df.ClosePrice_Close.isnull(),(df['ClosePrice_Close']-df['ClosePrice_Open'])*df['Quantity_Open']*100)
    return df

def get_trade_status(df):
    column='TradeStatus'
    df[column]=np.where(df['Quantity_Close'].isnull(),'OPEN','CLOSE')
    return df

def get_max_reward(df):
    column='MaxReward'
    df[column]=None
    df[column]=df[column].where(df.Strategy!='Short Put',(df['ClosePrice_Open'])*df['Quantity_Open']*-100)
    df[column]=df[column].where(df.Strategy!='Long Put',(df['Strike']-df['ClosePrice_Open'])*df['Quantity_Open']*100)
    df[column]=df[column].where(df.Strategy!='Short Call',(df['ClosePrice_Open'])*df['Quantity_Open']*-100)
    return df
def get_ROC(df):
    column='ROC'
    df[column]=None
    df[column]=df[column].where(df['Quantity_Close'].isnull(),df['Profit']/df['Capital'])
    return df

def split_date(df_col):
    #df_col=df_col.apply(str)
    df_col=pd.to_datetime(df_col,format='%Y%m%d')
    year = df_col.dt.year
    month = df_col.dt.month
    day = df_col.dt.day
    return year,month,day

def split_df_date(df):
    df['open_year'],df['open_month'],df['open_day']=split_date(df['TradeDate_Open'])
    df['close_year'],df['close_month'],df['close_day']=split_date(df['TradeDate_Close'])
    return df

def get_days_in_trade(df):
    df['DaysInTrade']=df['TradeDate_Close']-df['TradeDate_Open']+1
    return df

def get_profit_per_day(df):
    df['ProfitPerDay']=df['Profit']/df['DaysInTrade']
    return df

def sort_by_status(df):
    return df.sort_values(by=['TradeStatus'])


def convert_csv_to_report(path):
    df=pd.read_csv(path)
    df=merge_symbol(df)
    df=get_strategy(df)
    df=drop_stock(df)
    df=group_trades(df)
    df=drop_duplicates(df)
    df=extract_relevant_columns(df)
    df=merge_open_close(df)
    df=get_capital_usage(df)
    df=get_trade_status(df)
    df=get_profit(df)
    df=get_max_reward(df)
    df=get_ROC(df)
    df=split_df_date(df)
    df=get_days_in_trade(df)
    df=get_profit_per_day(df)
    df=sort_by_status(df)
    return df

group_columns=['Symbol','Open/CloseIndicator','Buy/Sell','Put/Call']
if __name__=="__main__":
    path=r'data\Trades2.csv'
    df=convert_csv_to_report(path)
    print(df)
    