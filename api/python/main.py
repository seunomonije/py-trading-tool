import sys
#import imports as pkg
import yfinance as yf

from .functions import stdinRead
from .algos import threeDayEMAHelper, swingRSIHelper


def get_data_from_ticker_list(ticker_list):
    winner_list = []
    data_list = []
    tickers_to_delete = []

    for i in range(len(ticker_list)):     
        data = None
        current_ticker = ticker_list[i]

        # First, let's get the data
        try: 
            #download the data for each ticker
            data = yf.download(current_ticker, period = "1y", interval = "1d")
        except:
            print('There was an error downloading ticker: ', current_ticker)
            tickers_to_delete.append(current_ticker)
            continue

        try:
            #run all my algorithms
            three_day_ema_ticker, three_day_ema_data, outcome = threeDayEMAHelper(current_ticker, 0, data)
            if (outcome == 'WIN'):
                winner_list.append((three_day_ema_ticker, '3EMA'))

            # data_list.append((three_day_ema_ticker))
                
            swingRSI = swingRSIHelper(current_ticker, 0, data)
            if (swingRSI != 1):
                winner_list.append((swingRSI, 'SWNG'))
        except Exception as error:
            print('There was an error running algorithms with ticker: ' + current_ticker )
            print(error)
            tickers_to_delete.append(current_ticker)
            continue
            
    print("Get these stocks out of here")
    print(tickers_to_delete)

    print("These are the winning stocks:")
    print(winner_list)
    print("\n")

    print(data_list)

    return winner_list, data_list


def main():
    ticker_list = []
    #if cmd-line arguments/Users/seunomonije/Desktop/Trading/py-trading-tool/python/main.py
    if (len(sys.argv) > 1):

        #copy the cmd-line arguments
        ticker_list = sys.argv
        
        #pop the filename
        ticker_list.pop(0)
    else:
        ticker_list = stdinRead()

    return get_data_from_ticker_list(ticker_list)
    
 

if __name__ == '__main__':
    main()