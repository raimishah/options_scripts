import numpy as np
import pandas as pd
from yahoo_fin import options 
from datetime import datetime
import argparse




def get_dates_to_sell(ticker, strike, option_type):
    strike = float(strike)

    dates = options.get_expiration_dates(ticker)

    bids = []
    asks = []
    marks = []
    days_till_exps = []
    dates_to_sell = []

    date_price_dict = dict()

    print('Getting ' + option_type + ' data...')
    for date in dates:
        chain = options.get_options_chain(ticker, date)
        df = chain[option_type]
        row_idx = df.loc[df['Strike'] == strike]
        if row_idx.empty:
            continue

        bid = float(row_idx['Bid'])
        ask = float(row_idx['Ask'])
        mark = (bid + ask) / 2
        date_price_dict[date] = [bid, ask, mark]

        dates_to_sell.append(date)
        date = datetime.strptime(date, '%B %d, %Y')
        days_till_exp = (date - datetime.now()).days
        
        bids.append(bid)
        asks.append(ask)
        marks.append(mark)
        days_till_exps.append(days_till_exp)


    bids = np.array(bids)
    asks = np.array(asks)
    marks = np.array(marks)
    dates_to_sell = np.array(dates_to_sell)

    print('Done getting data, sorting to maximize premium / days...')

    #maximize the ratios of premium vs days
    bid_ratios = bids / days_till_exps
    ask_ratios = asks / days_till_exps
    mark_ratios = marks / days_till_exps

    bid_sorted_idxs = np.argsort(bid_ratios)[::-1]
    ask_sorted_idxs = np.argsort(ask_ratios)[::-1]
    mark_sorted_idxs = np.argsort(mark_ratios)[::-1]

    bid_ratios = bid_ratios[bid_sorted_idxs]
    dates_to_sell_bid = dates_to_sell[bid_sorted_idxs]

    ask_ratios = ask_ratios[ask_sorted_idxs]
    dates_to_sell_ask = dates_to_sell[ask_sorted_idxs]

    mark_ratios = mark_ratios[mark_sorted_idxs]
    dates_to_sell_mark = dates_to_sell[mark_sorted_idxs]
 
    print('Using Bid price point \n')
    for i, best_date in enumerate(dates_to_sell_bid):
        print(best_date + ' -- Bid = ' +str(date_price_dict[best_date][0]) + ', Ask = ' + str(date_price_dict[best_date][1]) + '    Ratio = ' + str(np.round(bid_ratios[i],5)))
    print('\n\n')

    print('Using Ask price point \n')
    for i, best_date in enumerate(dates_to_sell_ask):
        print(best_date + ' -- Bid = ' +str(date_price_dict[best_date][0]) + ', Ask = ' + str(date_price_dict[best_date][1]) + '    Ratio = ' + str(np.round(ask_ratios[i],5)))
    print('\n\n')

    print('Using Mark price point \n')
    for i, best_date in enumerate(dates_to_sell_mark):
        print(best_date + ' -- Bid = ' +str(date_price_dict[best_date][0]) + ', Ask = ' + str(date_price_dict[best_date][1]) + '    Ratio = ' + str(np.round(mark_ratios[i],5)))
    print('\n\n')



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('ticker')
    parser.add_argument('strike')
    parser.add_argument('option_type')
    
    try:
        args = parser.parse_args()
    except:
        print('Use: >>> python options.py "ticker" "strike" "c/p"')
        print('Use: >>> python options.py TSLA 500 p')
        quit()

    if 'c' in args.option_type:
        option_type = 'calls'
    elif 'p' in args.option_type:
        option_type = 'puts'
    else:
        print('Use: >>> python options.py "ticker" "strike" "c/p"')
        print('Use: >>> python options.py TSLA 500 p')
        quit()
    
    get_dates_to_sell(args.ticker, args.strike, option_type)






if __name__ == '__main__':
    main()
