from src.data import convert_csv_to_report
from src.sheet import update_data_worksheet,update_review_worksheet

if __name__=="__main__":
    path=r'data\Trades2.csv'
    df=convert_csv_to_report(path)
    update_data_worksheet(df)
    update_review_worksheet(df)
    print('complete')