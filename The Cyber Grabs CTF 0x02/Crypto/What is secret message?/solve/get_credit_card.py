def checkLuhn(cardNo):
     
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False
     
    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')
     
        if (isSecond == True):
            d = d * 2
  
        # We add two digits to handle
        # cases that make two digits after
        # doubling
        nSum += d // 10
        nSum += d % 10
  
        isSecond = not isSecond
     
    if (nSum % 10 == 0):
        return True
    else:
        return False
 
# Driver code   
if __name__=="__main__":
    for i in range(5430000005251849, 5439999995251849, 10000000):
        if i % 53451 == 0 and checkLuhn(str(i)):
            print("Get valid credit card number {}".format(i))

# Get valid credit card number 5434511245251849
# Get valid credit card number 5435045755251849
