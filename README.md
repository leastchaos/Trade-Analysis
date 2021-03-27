# Trade-Analysis Purpose
Copy CSV from Interactive Broker into Google Sheets

# Initial Setup
## Requirements
gspread
gspread_dataframe
numpy
pandas
## Interactive Broker
1. Login to Client Portal on interactive Brokers
2. Go to Reports -> Flex Queries
3. Name: Trades
4. Under Section-> Tick Executions ->Click Select All -> Click Save
5. Under Delivery Configuration
  Accounts: Add your account
  Models: Optional
  Format: CSV
  Include header and trailer records?: No
  Include column headers?: Yes
  Include section code and line descriptor? No
  Period: Last 365 days
6. General Configuration
  Date Format: yyyyMMdd
  Time Format: HHmmss
  Date/Time Seperator: ;(semi-colon)
  Profit and Loss: Default
  Include Canceled Trades?: No
  Include Currency Rates? No
  Include Audit Trial Fields? Yes
  Display Account Alias in Place of Account ID?: Yes/No
  Breakout by Day?: No
7. Click Continue -> Save Changes
## Google Sheet
This program uses gspread.
1. Perform the authentication following the instruction in this link: https://gspread.readthedocs.io/en/latest/oauth2.html
2. Create a google spreadsheet in your folder for this program.
3. In the google spreadsheet, create 2 worksheet named 'data' and 'review'

# Usage
1. Login to Interactive Brokers-> Report -> Flex Queries -> Run the flex query 
2. Run the Flex Query again once you the Batch Flex Queries is completed.
3. Copy the CSV file generated into /data
4. Run main.py

