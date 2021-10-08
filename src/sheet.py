import gspread
import gspread_dataframe as gd

def get_current_ws(spreadsheet,worksheet):
    gc = gspread.oauth()
    ws=gc.open(spreadsheet).worksheet(worksheet)
    return ws

# TODO: Change to append new data
def update_data_worksheet(df,spreadsheet='My Options Journal',worksheet='data'):
    ws=get_current_ws(spreadsheet,worksheet)
    df2=gd.get_as_dataframe(ws).dropna(how='all').dropna(axis=1,how='all')
    new_df=df2.append(df).drop_duplicates(subset=['Symbol','Strategy','TradeDate_Open','ClosePrice_Open','Quantity_Open'],keep='last')
    ws.clear()
    gd.set_with_dataframe(ws,new_df,allow_formulas=True)
    

def update_review_worksheet(df,spreadsheet='My Options Journal',worksheet='Review'):
    ws=get_current_ws(spreadsheet,worksheet)
    df2=gd.get_as_dataframe(ws).dropna(how='all').dropna(axis=1,how='all')
    append_df=df[~df.Symbol.isin(df2.Symbol)][['Symbol','Expiry','Strike','Strategy','TradeStatus','Profit']].drop_duplicates(subset=['Symbol','Strategy'])
    new_df=df2.append(append_df)
    gd.set_with_dataframe(ws,new_df)