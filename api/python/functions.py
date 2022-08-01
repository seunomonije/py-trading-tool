import math

"""
    Reads tickers from stdin
"""
def stdinRead():
    
    #initialize return array
    ret = []
    
    #print instructions
    print("Enter ticker symbols. Enter nothing to stop.")
    
    #continuously read input until empty input
    while True:
        ticker = input()
        if ticker == "":
            break
        ret.append(ticker)
        continue
    
    #don't allow them to enter an empty array
    if len(ret) == 0:
        print("You have to enter something. Rerun the program")
        exit()
    #return
    return ret
    
"""
    Truncates a number to a designated number of digits
"""
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper
