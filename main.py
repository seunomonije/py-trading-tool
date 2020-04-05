import imports as pkg
import functions as fn

ticker = "FB"
tickerArr = ["FB", "AAPL", "TSLA", "TWTR", "SNAP", "BAC"]

for i in range(len(tickerArr)):
    fn.threeDayPercentage(tickerArr[i], 0)

print("Let's see if this works!")
