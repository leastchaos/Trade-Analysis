from src.data import convert_csv_to_report
from src.sheet import update_data_worksheet, update_review_worksheet

if __name__ == "__main__":
    path = r'data\Trades3 (15).csv'
    df = convert_csv_to_report(path)

    spreadsheet='My Options Journal'
    update_data_worksheet(df,spreadsheet,'data')
    update_review_worksheet(df,spreadsheet,'review')
    print('complete')
