# options scripts for so called traders

#1
  best_date_single.py:
    Used for calculating the best return for selling options given a strike. Gives best return for bid/ask/mark. Example below.
    
    raimi> python best_date_single.py TSLA 500 p

#2
  best_date_strangle.py:
    Used for calculating the best return for selling strangles given two strikes. Gives best return for bid/ask/mark. Example below.
    
    raimi> python best_date_strangle.py TSLA 800 1200
