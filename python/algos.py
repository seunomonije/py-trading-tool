import imports as pkg
import functions as fn

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#    swingRSIHelper(ticker, displayGraph, data)
#        helper function to consolidate buyAlertRSI and twoDayRSItester
#        mainly created for download optimization
def swingRSIHelper(ticker, displayGraph, data):

    if (buyAlertRSI(ticker, data) == True):
        swingRSItester(ticker, displayGraph, data)
        return ticker
    else:
        print(f"{bcolors.FAIL}%s -- swingRSI fail{bcolors.ENDC}" % (ticker))
        return 1


#     buyAlertRSI(ticker, data)
#       signals if the given ticker is on buy alert for this day
def buyAlertRSI(ticker, data):

    #take out the closing price for each day
    closeArr = data['Close'].to_numpy()
    
    #talib calculations
    rsiArr = pkg.talib.RSI(closeArr, timeperiod = 10)
    
    #see if the graphs are close but EMA is over
    if ((rsiArr[-1] < 25) and (rsiArr[-1] < rsiArr[-2] < rsiArr[-3])):
        val = rsiArr[-1]
        print(f"{bcolors.OKGREEN}%s -- swingRSI PASS{bcolors.ENDC}" % (ticker))
        print("More info:\n")
        print("\nval = %s\n" % val)
        return True
    
        
#swingRSItester(ticker, displayGraph, data)
#    prints the two day winning percentage of a given stock using RSI analysis with a 10 day time period

def swingRSItester(ticker,displayGraph, data):
    
    #taking out the closing price for each day
    closeArr = data['Close'].to_numpy()

    #uses talib to calculate the SMA and EMA
    rsiArr = pkg.talib.RSI(closeArr, timeperiod = 10)
    
    
    #initialize the wins and losses for this period
    periodWins = 0
    periodLosses = 0
    
    #for each RSI value
    it = iter(range(len(rsiArr)))
    for i in it:
            
        #error prevention
        if (i-1 < 0 or i-2 < 0):
            continue
                
        #if the rsi is approaching a global min
        if ((rsiArr[i] < 25) and (rsiArr[i] < rsiArr[i-1] < rsiArr[i-2])):
            #print("RSI30 is approaching a global minimum at x = %d, suggest buy" % i)
            
            ##initialize the counters
            winners = 0
            losers = 0
            
            ##evaluate stock price at checkpoints 1, 3, 7, 13, 21
            at = iter(range(1,6))
            for a in at:
            
                #1, 3, 7, 13, 21
                const = 1+(a*(a-1))
                        
                #prevent looking too far ahead
                if (i+const >= len(rsiArr)):
                    break
                            
                #if the potential purchase price is less than the price at this index
                if (closeArr[i] < closeArr[i+const]):
                    
                    #it's a winner
                    print("%d day winner at x = %d" % (const, i))
                    
                    #add to the counter
                    winners+=1
                    
                #otherwise
                else:
                    
                    #it's a loser
                    print("%d day loser at x = %d" % (const, i))
                    
                    #add to the counter
                    losers+=1
                    
                #continue
                continue
                
            #if this checkpoint is a winner
            if winners > 0:
                
                #add to the total wins this period
                periodWins+=1
                
                #print the number of days that it won
                print("%s won on %s/%s days." % (ticker, winners, (winners+losers)))
                
            #otherwise if this checkpoint has no wins
            elif winners == 0:
            
                #count it as a loss
                periodLosses+=1
                
                #print it out the number of days that it won
                print("%s won on %s/%s days." % (ticker, winners, (winners+losers)))
        
    #if there are any period wins
    if periodWins > 0:
        
        #calculate the win rate
        rate = fn.truncate(periodWins/(periodWins+periodLosses), 4)
        
        #print out the overall winrate
        print("%s would have won at least one day in %s/%s past periods for a checkpoint win rate of %s" % (ticker, periodWins, periodWins+periodLosses, rate))
    else:
        print("There were no wins or no data in any past periods for %s" % ticker)

    #if displayGraph is toggled
    if displayGraph == 1:
        
        #tell the graph to keep the days in integer format
        xi = list(range(len(closeArr)))
        pkg.plt.xticks(xi, xi)
        
        #plot the closing prices
        pkg.plt.plot(closeArr, 'o-', label = "Close" )
        
        #plot the EMA
        pkg.plt.plot(rsiArr, 'o-', label = "RSI")

        #display a legend
        pkg.plt.legend()
        
        #display the graph
        pkg.plt.show()
    

#    threeDayEMAHelper(ticker, displayGraph, data)
#        helper function to consolidate buyAlertEMA and threeDayEMAbacktester
#        mainly created for download optimization

def threeDayEMAHelper(ticker, displayGraph, data):
    
    if (buyAlertEMA(ticker, data) == True):
        threeDayEMAbacktester(ticker, displayGraph, data)
        return ticker
    else:
        print(f"{bcolors.FAIL}%s -- threeDayEMA fail{bcolors.ENDC}" % (ticker))
        return 1


#    buyAlertEMA(ticker)
#        signals if the given ticker is on buy alert for this day

def buyAlertEMA(ticker, data):
    
    #download the data
    #data = pkg.yf.download(ticker, period = "1y", interval = "1d")
    
    #take out the closing price for each day
    closeArr = data['Close'].to_numpy()
    
    #talib calculations
    emaArr = pkg.talib.EMA(closeArr, timeperiod = 20)
    
    #see if the graphs are close but EMA is over
    if (emaArr[-1]/closeArr[-1] < 1.01) and (emaArr[-1]/closeArr[-1] > 1) and (closeArr[-1] > closeArr[-2]):
        val = emaArr[-1]/closeArr[-1]
        print(f"{bcolors.OKGREEN}%s -- threeDayEMA PASS{bcolors.ENDC}" % (ticker))
        print("More info:\n")
        print("\nval = %s\n" % val)
        return True
        
    

#   threeDayEMAbacktester(ticker, displayGraph)
#       prints the three day winning percentage for the given stock, my first and probably most simple algorithm
#           PARAMETERS:
#               ticker -> the ticker name
#               displayGraph -> if 1, displays graph

def threeDayEMAbacktester(ticker, displayGraph, data):
    
    #downloading stock data with yfinance
    #data = pkg.yf.download(ticker, period = "1y")

    #taking out the closing price for each day
    closeArr = data['Close'].to_numpy()

    #uses talib to calculate the SMA and EMA
    smaArr = pkg.talib.SMA(closeArr, timeperiod = 10)
    emaArr = pkg.talib.EMA(closeArr, timeperiod = 20)
    
    ##initialize the counters
    winners = 0
    losers = 0
    streak = 0
    highestStreak = 0
    
    #for each EMA value
    it = iter(range(len(emaArr)))
    for i in it:
        
        #if the closing price approaches the EMA
        if (emaArr[i]/closeArr[i] < 1.01) and (emaArr[i]/closeArr[i] > 1) and (closeArr[i] > closeArr[i-1]):

                #first make sure you're not at the end of the data set
                if (i+3 >= len(closeArr)):
                    break
                    
                if (i+1 >= len(closeArr)):
                    break
                
                #if I make money one day after the crossing point
                if (closeArr[i] < closeArr[i+1]):
                    
                    print("Uptrend predicted at x = %d, one day winner" % i)
                    
                    #i'm selling the stock
                    winners+=1
                    
                    #add to the streak
                    streak +=1
                    
                    #fastforward to the next day, python is so extra in C this would be just i+=1
                    for j in range(0, 1):
                         i = next(it)
                    
                    #continue
                    continue
                
                #if I don't make money the first day I'm entering the 3 day mode
                else:
        
                    #if the price at the crossing point is less than the price after 3 days
                    if closeArr[i] < closeArr[i+3]:
                        print("Uptrend predicted at x = %d, three day winner" % i)
                        
                        #this is a winner
                        winners+=1
                        
                        #add to the streak
                        streak+=1
                        
                        #fast forward 3 days since that's how long I would've held the stock
                        for j in range(0, 3):
                            i = next(it)
                        
                        #continue to the next day
                        continue
                    
                    #if the price at the crossing line is more than the price after 3 days
                    if closeArr[i] > closeArr[i+3]:
                        print("Uptrend predicted at x = %d, three day loser" % i)
                        
                        #this is a loser get out of my sight
                        losers+=1
                        
                        #set highest streak
                        highestStreak = streak
                        
                        #reset the streak
                        streak = 0
                        
                        #fast forward 3 days since that's how long I would've held the stock
                        for j in range(0, 3):
                            i = next(it)
                        
                        #continue to the next day
                        continue
    
    #if there is a data
    if winners+losers != 0:
    
        #calculate the rate
        rate = fn.truncate(winners/(winners+losers), 4)
        
        #print the winning percentage
        print("\nthreeDayEMA wins for %s with a rate of %s in the past year.\n" % (ticker, rate))
        
#        #print the current winning streak and highest win streak
#        if (highestStreak == 0):
#            if (streak > 0):
#                print("threeDayEMA is currently on a %s win streak for %s\n" % (streak, ticker))
#            else:
#                print("threeDayEMA has either never won or never lost for %s.\n" % (ticker))
#        else:
#            print("threeDayEMA is currently on a %s win streak for %s\n" % (streak, ticker))
#            print("Year to date, threeDayEMA's highest win streak is %s" % (highestStreak))
            

    
    #if displayGraph is toggled
    if displayGraph == 1:
        
        #tell the graph to keep the days in integer format
        xi = list(range(len(closeArr)))
        pkg.plt.xticks(xi, xi)
        
        #plot the closing prices
        pkg.plt.plot(closeArr, 'o-', label = "Close" )
        
        #plot the EMA
        pkg.plt.plot(emaArr, 'o-', label = "EMA")
        
        #plot the SMA
        pkg.plt.plot(smaArr, 'o-', label = "SMA")
        
        #display a legend
        pkg.plt.legend()
        
        #display the graph
        pkg.plt.show()

